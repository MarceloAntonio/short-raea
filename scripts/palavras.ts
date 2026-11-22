// Agrupa os tempos por caractere do ElevenLabs em palavras (o formato das legendas e das deixas).
// `node scripts/palavras.ts` roda a checagem abaixo.
export type Palavra = { texto: string; inicio: number; fim: number };

export function palavrasDeCaracteres(chars: string[], ini: number[], fim: number[]): Palavra[] {
  const out: Palavra[] = [];
  let atual: Palavra | null = null;
  chars.forEach((c, i) => {
    if (/\s/.test(c)) { if (atual) out.push(atual); atual = null; return; }
    const letra = /[\p{L}\p{N}]/u.test(c);
    if (!atual) atual = { texto: "", inicio: -1, fim: -1 };
    atual.texto += c;
    if (letra) { if (atual.inicio < 0) atual.inicio = ini[i]; atual.fim = fim[i]; }
  });
  if (atual) out.push(atual);
  // pontuação solta ("…", "—") não é palavra; pontuação colada sai do texto
  return out
    .filter((w) => w.inicio >= 0)
    .map((w) => ({ ...w, texto: w.texto.replace(/^[^\p{L}\p{N}]+|[^\p{L}\p{N}]+$/gu, "") }));
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const texto = "Oi, e-mail… LGPD! — ok";
  const chars = [...texto];
  const t = chars.map((_, i) => i * 0.1);
  const p = palavrasDeCaracteres(chars, t, t.map((x) => x + 0.05));
  const esperado = ["Oi", "e-mail", "LGPD", "ok"];
  console.assert(JSON.stringify(p.map((w) => w.texto)) === JSON.stringify(esperado), "textos", p);
  console.assert(p[0].inicio === 0 && Math.abs(p[0].fim - 0.15) < 1e-9, "Oi: tempo sem a vírgula", p[0]);
  console.assert(Math.abs(p[1].fim - (texto.indexOf("l…") * 0.1 + 0.05)) < 1e-9, "e-mail termina no l, não nas reticências", p[1]);
  console.log(p.length === 4 ? "✓ palavras ok" : "✗ palavras");
}
