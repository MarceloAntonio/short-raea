#!/usr/bin/env bash
# Copia os agentes do debate (agents/*.md) para ~/.claude/agents/, para chamá-los direto pelo nome.
# A skill não precisa disso: ela lê agents/ da própria pasta. Pergunta antes de sobrescrever.
# uso: scripts/instalar-agentes.sh
set -eu

origem="$(cd "$(dirname "$0")/.." && pwd)/agents"
destino="${CLAUDE_AGENTS_DIR:-$HOME/.claude/agents}"
mkdir -p "$destino"

for f in "$origem"/*.md; do
  nome=$(basename "$f")
  alvo="$destino/$nome"
  if [ -e "$alvo" ]; then
    if cmp -s "$f" "$alvo"; then echo "igual     $nome"; continue; fi
    printf 'já existe %s e é diferente. Sobrescrever? [s/N] ' "$alvo"
    { read -r resp </dev/tty; } 2>/dev/null || { resp=n; echo; }  # sem terminal: não sobrescreve
    case "$resp" in s|S|sim) ;; *) echo "mantido   $nome"; continue ;; esac
  fi
  cp "$f" "$alvo"
  echo "copiado   $nome"
done
