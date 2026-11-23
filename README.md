# short-raea

Skill do Claude Code que faz Shorts verticais (Reels, TikTok, YouTube Shorts) renderizados em 3D com o
[raea](https://raea.io), com narração, sons CC0 do Freesound, legendas por palavra e CTA no padrão da marca.

O fluxo: perguntas em rodadas (grill me) → 5 conceitos com 5 estéticas diferentes, sem repetir o visual dos 3 últimos vídeos e passados por um diretor de arte → roteiro debatido por agentes
(roteirista, quatro revisores cegos e um juiz) com deixas presas às palavras da fala → produção no raea → verificação medida (duração, loudness, efeitos contra a voz, orçamento de zoom e pop) → cópia AAC
para WhatsApp e Instagram.

## Instalar

```sh
git clone git@github.com:MarceloAntonio/short-raea.git ~/.claude/skills/short-raea
```

Depois, no Claude Code: `/short-raea` com o tema do vídeo.

## Requisitos

- raea instalado (`curl -fsSL https://raea.io/install | sh`; no Windows, `irm https://raea.io/install.ps1 | iex` no
  PowerShell) e a skill `raea`.
- Chaves em `~/api/elevenlabs.env` (`ELEVENLABS_API_KEY=`) e `~/api/freesound.env` (`FREESOUND_API_KEY=`), pasta 700 e
  arquivos 600. Nunca dentro deste repositório.
- ffmpeg, ImageMagick (`magick`), Node 22.18+ (roda os `.ts` de `scripts/` direto) e Python 3. Para a capa, Google Chrome
  (usado sem janela).

## Arquivos

- `SKILL.md`: o processo, fase a fase.
- `references/conceitos.md`: motores de conceito e clichês proibidos.
- `references/esteticas.md`: catálogo de estéticas (papercraft, CRT, blueprint, noir, raio-X...) com cena, paleta, tipografia,
  câmera, trilha, para que tema serve e o que é difícil no raea.
- `references/movimento.md`: o que conta como mudança na tela (informação nova, não zoom nem pop), orçamento de ênfase,
  vocabulário de movimentos, câmera, movimento de cada estética e a lista do que é "pipoca".
- `references/roteiro.md`: gancho em 3 camadas, as 3 falhas, estruturas de envio e modo crítica.
- `references/pautas.md`: o modo Pautas (pesquisa do que está em alta num nicho, com fonte e data).
- `references/nichos/`: fontes, termos, calendário e o que evitar por nicho (tecnologia, segurança digital, criação de
  sites, futebol); `_modelo.md` para criar outro.
- `references/debate.md`: o debate do roteiro (rodadas, como disparar os agentes, pasta `debate/` no projeto).
- `agents/`: os 6 agentes do debate (roteirista, crítico, defensor, rolador-de-feed, especialista-chato, juiz), o
  diretor-de-arte-original da fase 2 e os 2 das pautas (caçador de pautas, cético de pauta). A skill
  os passa à ferramenta `Agent`; para chamá-los direto pelo nome, rode `scripts/instalar-agentes.sh` (copia para
  `~/.claude/agents/` e pergunta antes de sobrescrever).
- `references/tecnico.md`: voz, sons, armadilhas do raea, verificação, entrega, Windows e vários idiomas.
- `references/publicacao.md`: capa em HTML, legenda e hashtags para Reels.
- `references/legenda.md`: tom brasileiro, estrutura e checklist da legenda.
- `references/plataformas.md`: diferenças entre Reels, TikTok e YouTube Shorts (zonas seguras, duração, título, áudio).
- `scripts/`: coleta de pautas (`pautas.py`, só biblioteca padrão do Python), voz (`gerar-audio.ts`), sons (`baixar-sons.ts`), `emo.tsx`, `estilo.ts`, verificação (`verificar.sh`),
  contagem de zooms, pops e tremidas contra o orçamento (`contar-enfases.py`) e lint de texto (`lint-texto.py`). Sem dados de marca: tudo vem do `roteiro.json` do projeto.
- `marcas/_modelo.md`: modelo do perfil de marca. Os perfis reais (`marcas/<marca>.md`) ficam só no disco (`.gitignore`).
- `pautas/`: coletas e `HISTORICO-PAUTAS.md`, só no disco (`.gitignore`).
- `historico/HISTORICO-SHORTS.exemplo.md`: formato do histórico (com as colunas Estética e Formas recorrentes). O real (`HISTORICO-SHORTS.md`) fica só no disco.
- `evals/evals.json`: cenários de teste da skill e do debate.
