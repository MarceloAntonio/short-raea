#!/usr/bin/env bash
# Verificação medida antes de dizer que o vídeo está pronto (fase 5 do SKILL.md).
# uso: scripts/verificar.sh compositions/X.tsx out/X-vN.mp4
#
# Roda, em ordem: raea check --quick, deixas do roteiro × narração, nomes de componente repetidos, orçamento de ênfase,
# duração (≤ 60 s), loudness (cerca de -14 LUFS, pico ≤ -1 dBTP), trechos de mais de 3 s sem mudança
# na tela e quadro 0 vazio ou escuro. Sai com 1 se algo falhar.
#
# O projeto é a pasta acima de compositions/. Para outro idioma ou caminho, troque por variável:
#   ROTEIRO=roteiro.en.json NARRACAO=compositions/media/audio/en/narracao.json scripts/verificar.sh ...
# Funciona no bash do Linux e no Git Bash do Windows (sem globstar nem -pattern_type glob).
set -u

if [ $# -ne 2 ]; then echo "uso: $0 COMPOSICAO.tsx VIDEO.mp4" >&2; exit 2; fi
COMP=$1
VIDEO=$2
PROJ=$(cd "$(dirname "$COMP")/.." && pwd)
ROTEIRO=${ROTEIRO:-$PROJ/roteiro.json}
case "$ROTEIRO" in /*|[A-Za-z]:*) ;; *) [ -f "$ROTEIRO" ] || ROTEIRO=$PROJ/$ROTEIRO ;; esac

MAX_SEG=${MAX_SEG:-60}
LUFS_ALVO=${LUFS_ALVO:--14}
LUFS_TOL=${LUFS_TOL:-1.5}
PICO_MAX=${PICO_MAX:--1}
PARADA_SEG=${PARADA_SEG:-3}

falhas=0
ok()    { printf 'OK     %-18s %s\n' "$1" "$2"; }
falha() { printf 'FALHA  %-18s %s\n' "$1" "$2"; falhas=$((falhas + 1)); }

for cmd in raea node ffmpeg ffprobe awk; do
  command -v "$cmd" >/dev/null || { echo "falta o comando $cmd no PATH" >&2; exit 2; }
done
[ -f "$COMP" ] || { echo "composição não encontrada: $COMP" >&2; exit 2; }
[ -f "$VIDEO" ] || { echo "vídeo não encontrado: $VIDEO" >&2; exit 2; }

# 1. raea check --quick
if saida=$(raea check "$COMP" --quick 2>&1); then
  ok "raea check" "sem erros"
else
  falha "raea check" "$(printf '%s' "$saida" | tail -n 5 | tr '\n' ' ')"
fi

# 2. Deixas: cada {"palavra": ...} de um passo precisa estar na fala desse passo, na narracao.json
if [ ! -f "$ROTEIRO" ]; then
  falha "deixas" "roteiro não encontrado: $ROTEIRO"
else
  saida=$(ROTEIRO="$ROTEIRO" PROJ="$PROJ" NARRACAO="${NARRACAO:-}" node -e '
    const fs = require("fs"), path = require("path");
    const r = JSON.parse(fs.readFileSync(process.env.ROTEIRO, "utf8"));
    const candidatos = [process.env.NARRACAO, r.meta && r.meta.pastaAudio && path.join(r.meta.pastaAudio, "narracao.json"),
      "compositions/media/audio/narracao.json", "public/audio/narracao.json"].filter(Boolean);
    const arq = candidatos.map((c) => path.isAbsolute(c) ? c : path.join(process.env.PROJ, c)).find((c) => fs.existsSync(c));
    if (!arq) { console.log("narracao.json não encontrada (" + candidatos.join(", ") + ")"); process.exit(1); }
    const n = JSON.parse(fs.readFileSync(arq, "utf8"));
    const norm = (s) => String(s).toLowerCase().replace(/^[^\p{L}\p{N}]+|[^\p{L}\p{N}]+$/gu, "");
    const deixas = (o, acc = []) => {
      if (Array.isArray(o)) o.forEach((x) => deixas(x, acc));
      else if (o && typeof o === "object") for (const [k, v] of Object.entries(o)) k === "palavra" && typeof v === "string" ? acc.push(v) : deixas(v, acc);
      return acc;
    };
    const faltas = []; let total = 0;
    for (const p of [r.gancho, ...(r.passos || [])].filter(Boolean)) {
      const ditas = new Set(((n[p.id] || {}).palavras || []).map((w) => norm(w.texto)));
      for (const d of deixas(p)) { total++; if (!ditas.has(norm(d))) faltas.push(p.id + ": \"" + d + "\""); }
    }
    console.log(faltas.length ? faltas.length + " de " + total + " faltando: " + faltas.join(", ") : total + " deixas encontradas");
    process.exit(faltas.length ? 1 : 0);
  ' 2>&1) && ok "deixas" "$saida" || falha "deixas" "$saida"
fi

# 3. Dois componentes com o mesmo nome no mesmo arquivo (a segunda declaração vence em silêncio)
repetidos=$(find "$PROJ/components" "$PROJ/compositions" -name '*.tsx' -not -path '*/node_modules/*' -not -path '*/media/*' 2>/dev/null |
  while IFS= read -r f; do
    grep -oE '^(export )?(default )?function [A-Za-z0-9_]+' "$f" | sed -E 's/^(export )?(default )?//' | sort | uniq -d | sed "s|^|${f#"$PROJ"/}: |"
  done)
[ -z "$repetidos" ] && ok "nomes repetidos" "nenhum" || falha "nomes repetidos" "$(printf '%s' "$repetidos" | tr '\n' ';')"

# 3b. Orçamento de ênfase: zoom, pop, tremida e pulso do roteiro e escala animada no código (references/movimento.md)
PY=$(command -v python3 || command -v python)
if [ -z "$PY" ]; then
  falha "ênfases" "falta python3 no PATH"
elif saida=$("$PY" "$(dirname "$0")/contar-enfases.py" "$ROTEIRO" "$PROJ/components" 2>&1); then
  ok "ênfases" "$(printf '%s\n' "$saida" | head -n 1)"
else
  printf '%s\n' "$saida" | sed -n '/^código/,/^REPROVADO/p' | grep -v '^REPROVADO' >&2
  falha "ênfases" "$(printf '%s\n' "$saida" | grep '^REPROVADO' | cut -c1-400) → troque o excesso por informação nova"
fi

# 4. Duração
dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$VIDEO" | tr -d '\r')
dur=$(awk -v d="$dur" 'BEGIN { printf "%.1f", d }')
if awk -v d="$dur" -v m="$MAX_SEG" 'BEGIN { exit !(d > 0 && d <= m) }'; then
  ok "duração" "${dur}s (máx ${MAX_SEG}s)"
else
  falha "duração" "${dur}s (máx ${MAX_SEG}s)"
fi

# 5. Loudness integrado e pico verdadeiro (resumo do ebur128 no fim do stderr)
resumo=$(ffmpeg -nostats -hide_banner -i "$VIDEO" -af ebur128=peak=true -f null - 2>&1 | tr -d '\r' | sed -n '/Summary:/,$p')
lufs=$(printf '%s\n' "$resumo" | awk '/^ *I:/ { print $2; exit }')
pico=$(printf '%s\n' "$resumo" | awk '/^ *Peak:/ { print $2; exit }')
if [ -z "$lufs" ] || [ -z "$pico" ]; then
  falha "loudness" "não consegui ler o ebur128 (o vídeo tem áudio?)"
elif awk -v l="$lufs" -v a="$LUFS_ALVO" -v t="$LUFS_TOL" -v p="$pico" -v pm="$PICO_MAX" \
      'BEGIN { d = l - a; if (d < 0) d = -d; exit !(d <= t && p <= pm) }'; then
  ok "loudness" "${lufs} LUFS, pico ${pico} dBTP"
else
  falha "loudness" "${lufs} LUFS (alvo ${LUFS_ALVO} ±${LUFS_TOL}), pico ${pico} dBTP (máx ${PICO_MAX})"
fi

# 6. Tela parada: intervalos de mais de PARADA_SEG s entre duas mudanças de imagem
paradas=$(ffmpeg -hide_banner -i "$VIDEO" -vf "select='gt(scene,0.02)',showinfo" -an -f null - 2>&1 |
  tr -d '\r' | grep -o 'pts_time:[0-9.]*' | cut -d: -f2 |
  awk -v fim="$dur" -v lim="$PARADA_SEG" '
    BEGIN { ant = 0 }
    { if ($1 - ant > lim) printf "%.1f-%.1fs ", ant, $1; ant = $1 }
    END { if (fim - ant > lim) printf "%.1f-%.1fs ", ant, fim }')
[ -z "$paradas" ] && ok "tela parada" "nenhum trecho > ${PARADA_SEG}s" ||
  falha "tela parada" "$paradas→ acrescente informação nova (elemento que entra, faixa de texto, cena ou luz que muda), nunca zoom ou pulso"

# 7. Quadro 0: vira a miniatura antes do play; não pode ser escuro nem uma cor só
stats=$(ffmpeg -hide_banner -i "$VIDEO" -vf "select='eq(n,0)',signalstats,metadata=print" -frames:v 1 -an -f null - 2>&1 | tr -d '\r')
yavg=$(printf '%s\n' "$stats" | grep -o 'lavfi.signalstats.YAVG=[0-9.]*' | head -n1 | cut -d= -f2)
ylow=$(printf '%s\n' "$stats" | grep -o 'lavfi.signalstats.YLOW=[0-9.]*' | head -n1 | cut -d= -f2)
yhigh=$(printf '%s\n' "$stats" | grep -o 'lavfi.signalstats.YHIGH=[0-9.]*' | head -n1 | cut -d= -f2)
if [ -z "$yavg" ]; then
  falha "quadro 0" "não consegui medir"
elif awk -v m="$yavg" -v lo="$ylow" -v hi="$yhigh" 'BEGIN { exit !(m >= 25 && hi - lo >= 20) }'; then
  ok "quadro 0" "brilho médio ${yavg}, faixa ${ylow}-${yhigh}"
else
  falha "quadro 0" "escuro ou vazio: brilho médio ${yavg} (mín 25), faixa ${ylow}-${yhigh} (mín 20)"
fi

echo
if [ "$falhas" -gt 0 ]; then echo "$falhas item(ns) com FALHA: volte à fase 4."; exit 1; fi
echo "Tudo OK. Olhe também a folha de quadros-chave e ouça a mixagem (pronúncia e efeitos contra a voz)."
