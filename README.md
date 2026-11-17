# short-raea

Skill do Claude Code que faz Shorts verticais (Reels, TikTok, YouTube Shorts) renderizados em 3D com o
[raea](https://raea.io), com narração, sons CC0 do Freesound, legendas por palavra e CTA no padrão da marca.

O fluxo: perguntas em rodadas (grill me) → 5 conceitos sem repetir o vídeo anterior → roteiro com deixas presas
às palavras da fala → produção no raea → verificação medida (duração, loudness, efeitos contra a voz) → cópia AAC
para WhatsApp e Instagram.

## Instalar

```sh
git clone git@github.com:MarceloAntonio/short-raea.git ~/.claude/skills/short-raea
```

Depois, no Claude Code: `/short-raea` com o tema do vídeo.

## Requisitos

- raea instalado (`curl -fsSL https://raea.io/install | sh`) e a skill `raea`.
- Chaves em `~/api/elevenlabs.env` (`ELEVENLABS_API_KEY=`) e `~/api/freesound.env` (`FREESOUND_API_KEY=`), pasta 700 e
  arquivos 600. Nunca dentro deste repositório.
- ffmpeg, ImageMagick (`magick`) e Node 22+.

## Arquivos

- `SKILL.md`: o processo, fase a fase.
- `references/conceitos.md`: motores de conceito e clichês proibidos.
- `references/tecnico.md`: voz, sons, armadilhas do raea, verificação e entrega.
- `historico/HISTORICO-SHORTS.md`: um vídeo por linha; o próximo precisa diferir do último.
