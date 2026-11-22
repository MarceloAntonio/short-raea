// Gera a narração de cada passo do roteiro.json e grava narracao.json com a duração de cada áudio e o
// tempo de cada palavra (usado pelas legendas e pelas deixas). Só refaz os passos cujo texto ou voz mudou.
//
// uso: node scripts/gerar-audio.ts PASTA_DO_PROJETO [--roteiro roteiro.en.json] [--tudo] [--previa]
//   --previa  áudio mudo e tempos estimados (0,12 s + 0,045 s por letra, mais pausa na pontuação), sem gastar
//             créditos: serve para ver as cenas e conferir as deixas. Sai cerca de 30 % mais longo que o Liam a 1,15.
//
// Tudo o que é da marca ou do vídeo vem do roteiro.json, não deste arquivo:
//   meta.voz.provedor     "elevenlabs" ou "edge" (edge-tts, grátis; precisa de `pip install edge-tts`)
//   meta.voz.elevenlabs   { id, modelo, velocidade, estabilidade }
//   meta.voz.edge         { nome, velocidade }  ex.: { "nome": "pt-BR-AntonioNeural", "velocidade": "+18%" }
//   meta.voz.idioma       "pt" (padrão), "es", "en"...
//   meta.voz.pronuncia    { "Graal": "Graál" }  troca a palavra só no texto enviado à voz; legenda e deixas
//                         continuam com a grafia real (troca de uma palavra por uma)
//   meta.pastaAudio       onde gravar, relativo ao projeto (padrão "public/audio"; no raea, "compositions/media/audio")
//   meta.duracaoMaxSeg, meta.pausaEntrePassosSeg, passo.duracaoFixaSeg
//
// Chave: arquivo de ELEVENLABS_KEY_FILE, ~/api/elevenlabs.env ou ~/.raea/elevenlabs.env, com a linha
// ELEVENLABS_API_KEY=... ou ELEVENLABS_KEY=... A chave nunca é impressa.
import { execFileSync } from "node:child_process";
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { homedir } from "node:os";
import { join, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { palavrasDeCaracteres, type Palavra } from "./palavras.ts";

type Passo = { id: string; narracao: string | null; duracaoFixaSeg?: number };
type Voz = {
  provedor: "elevenlabs" | "edge";
  idioma?: string;
  pronuncia?: Record<string, string>;
  elevenlabs?: { id: string; modelo: string; velocidade: number; estabilidade: number };
  edge?: { nome: string; velocidade: string };
};
type Roteiro = {
  meta: { voz: Voz; duracaoMaxSeg: number; pausaEntrePassosSeg: number; pastaAudio?: string };
  gancho: Passo;
  passos: Passo[];
};
type Narracao = Record<string, { arquivo: string; duracao: number; palavras: Palavra[]; assinatura: string }>;

const args = process.argv.slice(2);
const opcao = (nome: string) => { const i = args.indexOf(nome); return i >= 0 ? args.splice(i, 2)[1] : undefined; };
const arqRoteiro = opcao("--roteiro") ?? "roteiro.json";
const tudo = args.includes("--tudo");
const previa = args.includes("--previa");
const raiz = resolve(args.find((a) => !a.startsWith("--")) ?? ".");

const roteiro: Roteiro = JSON.parse(readFileSync(join(raiz, arqRoteiro), "utf8"));
const voz = roteiro.meta.voz;
const pastaRel = roteiro.meta.pastaAudio ?? "public/audio";
const pasta = join(raiz, pastaRel);
const manifesto = join(pasta, "narracao.json");
mkdirSync(pasta, { recursive: true });
const anterior: Narracao = existsSync(manifesto) ? JSON.parse(readFileSync(manifesto, "utf8")) : {};

function paraVoz(texto: string): string {
  let t = texto;
  for (const [escrito, falado] of Object.entries(voz.pronuncia ?? {}))
    t = t.replace(new RegExp(`(?<![\\p{L}\\p{N}])${escrito}(?![\\p{L}\\p{N}])`, "gu"), falado);
  return t;
}

/** Depois do alinhamento, volta cada palavra falada para a grafia do roteiro (mesma posição). */
function grafiaReal(faladas: Palavra[], texto: string): Palavra[] {
  if (!voz.pronuncia) return faladas;
  const chars = [...texto];
  const escritas = palavrasDeCaracteres(chars, chars.map(() => 0), chars.map(() => 0));
  if (escritas.length !== faladas.length) {
    console.warn(`  aviso: ${faladas.length} palavras faladas e ${escritas.length} escritas; legenda fica com a grafia falada`);
    return faladas;
  }
  return faladas.map((p, i) => ({ ...p, texto: escritas[i].texto }));
}

function edge(texto: string, mp3: string): Palavra[] {
  const v = voz.edge!;
  const venv = join(raiz, ".venv/bin/python");
  const python = process.env.PYTHON ?? (existsSync(venv) ? venv : "python3");
  const tts = fileURLToPath(new URL("./tts.py", import.meta.url));
  return JSON.parse(execFileSync(python, [tts, texto, v.nome, v.velocidade, mp3], { encoding: "utf8" }));
}

function chaveElevenLabs(): string {
  const lugares = [process.env.ELEVENLABS_KEY_FILE, join(homedir(), "api/elevenlabs.env"), join(homedir(), ".raea/elevenlabs.env")];
  for (const arq of lugares) {
    if (!arq || !existsSync(arq)) continue;
    const m = readFileSync(arq, "utf8").match(/^ELEVENLABS_(?:API_)?KEY=(.+)$/m);
    if (m) return m[1].trim();
  }
  throw new Error("chave da ElevenLabs não encontrada em ~/api/elevenlabs.env nem em ~/.raea/elevenlabs.env: pergunte ao usuário onde está");
}

async function elevenlabs(texto: string, mp3: string): Promise<Palavra[]> {
  const v = voz.elevenlabs!;
  const res = await fetch(`https://api.elevenlabs.io/v1/text-to-speech/${v.id}/with-timestamps?output_format=mp3_44100_128`, {
    method: "POST",
    headers: { "xi-api-key": chaveElevenLabs(), "Content-Type": "application/json" },
    body: JSON.stringify({
      text: texto,
      model_id: v.modelo,
      language_code: voz.idioma ?? "pt",
      voice_settings: { stability: v.estabilidade, similarity_boost: 0.75, speed: v.velocidade },
    }),
  });
  if (!res.ok) throw new Error(`ElevenLabs ${res.status}: ${(await res.text()).slice(0, 300)}`);
  const d = await res.json();
  writeFileSync(mp3, Buffer.from(d.audio_base64, "base64"));
  const a = d.alignment;
  return palavrasDeCaracteres(a.characters, a.character_start_times_seconds, a.character_end_times_seconds);
}

function estimar(texto: string, mp3: string): Palavra[] {
  const palavras: Palavra[] = [];
  let t = 0;
  for (const bruta of texto.split(/\s+/).filter(Boolean)) {
    const letras = bruta.replace(/[^\p{L}\p{N}]/gu, "").length;
    if (!letras) continue;
    const fim = t + 0.12 + 0.045 * letras;
    palavras.push({ texto: bruta.replace(/^[^\p{L}\p{N}]+|[^\p{L}\p{N}]+$/gu, ""), inicio: t, fim });
    t = fim + (/[.!?…]$/.test(bruta) ? 0.35 : /[,;:]$/.test(bruta) ? 0.15 : 0.03);
  }
  execFileSync("ffmpeg", ["-v", "error", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono", "-t", (t + 0.2).toFixed(2), "-b:a", "64k", mp3]);
  return palavras;
}

const config = voz.provedor === "elevenlabs" ? voz.elevenlabs : voz.edge;
const saida: Narracao = {};
for (const passo of [roteiro.gancho, ...roteiro.passos]) {
  if (!passo.narracao) continue;
  const falado = paraVoz(passo.narracao);
  // o texto falado entra na assinatura: mudar uma pronúncia refaz só os passos que a usam
  const assinatura = `${previa ? "previa|" : ""}${voz.provedor}|${voz.idioma ?? "pt"}|${JSON.stringify(config)}|${passo.narracao}|${falado}`;
  const mp3 = join(pasta, `${passo.id}.mp3`);
  const velho = anterior[passo.id];
  if (!tudo && velho?.assinatura === assinatura && existsSync(mp3)) {
    saida[passo.id] = velho;
    continue;
  }
  const faladas = previa ? estimar(falado, mp3) : voz.provedor === "elevenlabs" ? await elevenlabs(falado, mp3) : edge(falado, mp3);
  const palavras = grafiaReal(faladas, passo.narracao);
  const arquivo = Number(execFileSync("ffprobe", ["-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", mp3], { encoding: "utf8" }));
  // os TTS deixam silêncio no fim: o passo acaba 0,2 s depois da última palavra
  const duracao = Math.min(arquivo, palavras.at(-1)!.fim + 0.2);
  saida[passo.id] = { arquivo: `${pastaRel.split("/").pop()}/${passo.id}.mp3`, duracao, palavras, assinatura };
  console.log(`${passo.id.padEnd(14)} ${duracao.toFixed(2)}s  ${palavras.length} palavras`);
}

writeFileSync(manifesto, JSON.stringify(saida, null, 2));
const pausas = roteiro.meta.pausaEntrePassosSeg * roteiro.passos.length;
const fixos = roteiro.passos.reduce((s, p) => s + (p.duracaoFixaSeg ?? 0), 0);
const total = Object.values(saida).reduce((s, n) => s + n.duracao, 0) + pausas + fixos;
console.log(`total ≈ ${total.toFixed(1)}s (máx ${roteiro.meta.duracaoMaxSeg}s)`);
if (total > roteiro.meta.duracaoMaxSeg) {
  console.error("passou do limite: enxugue a narração ou suba a velocidade da voz em meta.voz");
  process.exit(1);
}
