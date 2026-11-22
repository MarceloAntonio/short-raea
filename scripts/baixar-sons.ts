// Busca no Freesound os efeitos e as músicas do vídeo (só CC0: uso comercial sem crédito obrigatório),
// baixa a prévia HQ (MP3 ~128 kbps; o original exige OAuth), trata com ffmpeg e grava os créditos.
//
// uso: node scripts/baixar-sons.ts PASTA_DO_PROJETO              (todos)
//      node scripts/baixar-sons.ts PASTA_DO_PROJETO ding pop     (só esses)
//
// A lista de sons fica no roteiro.json do projeto, em "sons" (o id fixa o som escolhido; as buscas
// ficam como alternativa e para achar outro):
//   "sons": [
//     { "arquivo": "sfx/pop.mp3", "id": 245645, "buscas": ["pop", "bubble pop"], "dur": [0.05, 0.8], "corte": 0.4 },
//     { "arquivo": "music/tensa.mp3", "buscas": ["suspense music loop"], "dur": [25, 240], "corte": 45, "musica": true }
//   ]
// meta.pastaMidia: onde gravar, relativo ao projeto (padrão "public"; no raea, "compositions/media").
// Chave: FREESOUND_API_KEY no arquivo de FREESOUND_KEY_FILE ou em ~/api/freesound.env. Nunca é impressa.
import { homedir, tmpdir } from "node:os";
import { execFileSync, spawnSync } from "node:child_process";
import { existsSync, mkdirSync, readFileSync, renameSync, writeFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";

const args = process.argv.slice(2);
const raiz = resolve(args.shift() ?? ".");
const roteiro = JSON.parse(readFileSync(join(raiz, "roteiro.json"), "utf8"));
const midia = join(raiz, roteiro.meta?.pastaMidia ?? "public");
const chave = readFileSync(process.env.FREESOUND_KEY_FILE ?? join(homedir(), "api/freesound.env"), "utf8").match(/^FREESOUND_API_KEY=(.+)$/m)?.[1].trim();
if (!chave) throw new Error("falta FREESOUND_API_KEY em ~/api/freesound.env: pergunte ao usuário onde está");

type Pedido = { arquivo: string; id?: number; buscas: string[]; dur: [number, number]; corte: number; musica?: boolean };
const PEDIDOS: Pedido[] = roteiro.sons ?? [];
if (!PEDIDOS.length) throw new Error('roteiro.json sem "sons": liste os efeitos e as músicas (ver o cabeçalho deste script)');

type Som = { id: number; name: string; username: string; duration: number; avg_rating: number; num_ratings: number; num_downloads: number; license: string; url: string; previews: Record<string, string> };

async function buscar(q: string, [a, b]: [number, number]): Promise<Som[]> {
  const u = new URL("https://freesound.org/apiv2/search/");
  u.search = new URLSearchParams({
    query: q,
    filter: `license:"Creative Commons 0" duration:[${a} TO ${b}]`,
    fields: CAMPOS,
    sort: "downloads_desc",
    page_size: "15",
  }).toString();
  const res = await fetch(u, { headers: { Authorization: `Token ${chave}` } });
  if (!res.ok) throw new Error(`Freesound ${res.status}: ${(await res.text()).slice(0, 200)}`);
  return (await res.json()).results;
}

/** Pico em dBFS (o volumedetect do ffmpeg escreve no stderr). */
function pico(arquivo: string): number {
  const err = spawnSync("ffmpeg", ["-i", arquivo, "-af", "volumedetect", "-f", "null", "-"], { encoding: "utf8" }).stderr;
  const m = /max_volume: (-?[\d.]+) dB/.exec(err);
  if (!m) throw new Error(`sem max_volume para ${arquivo}`);
  return Number(m[1]);
}

// nota pesa, mas um som muito baixado e pouco avaliado também conta
const CAMPOS = "id,name,username,duration,avg_rating,num_ratings,num_downloads,license,url,previews";
async function porId(id: number): Promise<Som> {
  const res = await fetch(`https://freesound.org/apiv2/sounds/${id}/?fields=${CAMPOS}`, { headers: { Authorization: `Token ${chave}` } });
  if (!res.ok) throw new Error(`Freesound ${res.status} no som ${id}`);
  const som: Som = await res.json();
  if (som.license !== "http://creativecommons.org/publicdomain/zero/1.0/" && !/zero/i.test(som.license)) throw new Error(`som ${id} não é CC0: ${som.license}`);
  return som;
}

const pontos = (s: Som) => (s.num_ratings >= 3 ? s.avg_rating : 3.5) * Math.log10(10 + s.num_downloads);

const so = args;
const creditos: string[] = [];
const credFile = join(midia, "sfx/CREDITOS.md");
const anteriores = existsSync(credFile) ? readFileSync(credFile, "utf8").split("\n").filter((l) => l.startsWith("| `")) : [];

for (const p of PEDIDOS) {
  const nome = p.arquivo.split("/").pop()!.replace(".mp3", "");
  if (so.length && !so.includes(nome)) {
    const velho = anteriores.find((l) => l.includes(`\`${p.arquivo}\``));
    if (velho) creditos.push(velho);
    continue;
  }
  let melhor: Som | undefined = p.id ? await porId(p.id) : undefined;
  if (!melhor) for (const q of p.buscas) {
    const r = (await buscar(q, p.dur)).sort((x, y) => pontos(y) - pontos(x));
    if (r[0] && (!melhor || pontos(r[0]) > pontos(melhor))) melhor = r[0];
  }
  if (!melhor) { console.error(`✗ ${p.arquivo}: nada CC0 encontrado`); continue; }

  const bruto = join(tmpdir(), `freesound-${melhor.id}.mp3`);
  const mp3 = await fetch(melhor.previews["preview-hq-mp3"], { headers: { Authorization: `Token ${chave}` } });
  writeFileSync(bruto, Buffer.from(await mp3.arrayBuffer()));

  const destino = join(midia, p.arquivo);
  mkdirSync(dirname(destino), { recursive: true });
  const fadeIni = Math.max(0, Math.min(p.corte, melhor.duration) - 0.15);
  // efeitos: tira o silêncio do começo, corta, fade curto, pico em -2 dB.
  // músicas: corta, fade de entrada (sem fade de saída: a Trilha faz o crossfade), nível em -16 LUFS (a Trilha ainda baixa 20 dB sob a voz).
  const filtro = p.musica
    ? `atrim=0:${p.corte},afade=t=in:d=1.5,loudnorm=I=-16:TP=-1.5:LRA=11`
    : `silenceremove=start_periods=1:start_threshold=-50dB,atrim=0:${p.corte},afade=t=out:st=${fadeIni}:d=0.15`;
  execFileSync("ffmpeg", ["-v", "error", "-y", "-i", bruto, "-af", filtro, "-ar", "44100", "-ac", "2", "-b:a", "192k", destino]);
  if (!p.musica) {
    const ganho = -2 - pico(destino);
    execFileSync("ffmpeg", ["-v", "error", "-y", "-i", destino, "-af", `volume=${ganho.toFixed(1)}dB`, "-b:a", "192k", destino + ".tmp.mp3"]);
    renameSync(destino + ".tmp.mp3", destino);
  }
  const dur = Number(execFileSync("ffprobe", ["-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", destino], { encoding: "utf8" }));
  creditos.push(`| \`${p.arquivo}\` | [${melhor.name}](${melhor.url}) | ${melhor.username} | CC0 | ${melhor.avg_rating.toFixed(1)} (${melhor.num_ratings}) | ${melhor.num_downloads} |`);
  console.log(`✓ ${p.arquivo.padEnd(16)} ${dur.toFixed(1)}s  ${melhor.name.slice(0, 40)} — ${melhor.username}`);
}

mkdirSync(dirname(credFile), { recursive: true });
writeFileSync(credFile, [
  "# Créditos dos sons",
  "",
  "Baixados do Freesound por `baixar-sons.ts` (prévia HQ, tratada com ffmpeg). Todos CC0: uso comercial",
  "permitido sem crédito obrigatório; a lista fica para referência. Para trocar um som, mude o id ou as",
  "buscas em `sons` no roteiro.json e rode o script com o NOME do som, ou substitua o arquivo mantendo o nome.",
  "",
  "| Arquivo | Som | Autor | Licença | Nota (votos) | Downloads |",
  "|---|---|---|---|---|---|",
  ...creditos,
  "",
].join("\n"));
