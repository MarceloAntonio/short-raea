# Referência técnica

## Índice
1. Chaves
2. Voz (ElevenLabs)
3. Sons e música (Freesound)
4. raea: estrutura e armadilhas
5. Verificação
6. Entrega

## 1. Chaves

Ficam em `~/api/` (pasta 700, arquivos 600), no formato `NOME=valor`:
- `~/api/elevenlabs.env` → `ELEVENLABS_API_KEY`
- `~/api/freesound.env` → `FREESOUND_API_KEY`

Leia o valor para uma variável (`K=$(grep '^ELEVENLABS_API_KEY=' ~/api/elevenlabs.env | cut -d= -f2-)`) e mande só no cabeçalho do próprio serviço. Nunca rode `cat`, `sed` ou `echo` nesses arquivos: a saída aparece no terminal e a chave vaza (já aconteceu uma vez e a chave precisou ser trocada). Os scripts do projeto modelo já leem desses caminhos.

## 2. Voz (ElevenLabs)

- `POST https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/with-timestamps?output_format=mp3_44100_128`
- Cabeçalho `xi-api-key`. Corpo: `{"text": ..., "model_id": "eleven_multilingual_v2", "language_code": "pt", "voice_settings": {"stability": 0.5, "similarity_boost": 0.75, "speed": 1.15}}`
- Voz padrão: **Liam** `TX3LPaxmHKxFdv7VOQHJ` (americana falando português; avise que pode ter sotaque). A chave não tem permissão de listar vozes: para outra voz, peça o ID.
- A resposta traz `audio_base64` e `alignment` (tempo por caractere). Agrupe em palavras com `~/projetos/terceirizar-ti/scripts/palavras.ts`. O `scripts/gerar-audio.ts` desse projeto faz tudo por passo (só refaz o que mudou), grava `public/audio/narracao.json` e falha se passar de `duracaoMaxSeg`.
- Duração do passo = fim da última palavra + 0,2 s. O MP3 tem silêncio no fim e, somado em 8 passos, estoura os 60 s.
- Alternativa grátis: edge-tts (`pt-BR-AntonioNeural`, `+18%`), com `meta.voz.provedor: "edge"`.

## 3. Sons e música (Freesound, CC0)

- Busca: `https://freesound.org/apiv2/search/?query=...&filter=license:"Creative Commons 0"&fields=id,name,username,license,duration,avg_rating,num_downloads,description,previews` com `Authorization: Token $K`. Baixe `previews["preview-hq-mp3"]`. Para um ID fixo: `/apiv2/sounds/{id}/`.
- `~/projetos/terceirizar-ti/scripts/baixar-sons.ts` é a base: lista de pedidos com ID fixo; nos efeitos corta silêncio, faz fade e normaliza o pico em -2 dB; na música corta, faz fade-in e loudnorm -16; grava `CREDITOS.md`.
- Leia nome e descrição antes de escolher. Já vieram "alarme" que era bip de cinto de avião e "suspense" que era trilha de RPG. Depois de escolher, fixe o ID.
- Música: uma faixa por fase (tensa no problema, leve depois da virada), crossfade de cerca de 1,2 s, uns -20 dB sob a voz. Faixa curta com fade-out no meio do vídeo soa como erro: corte 40 a 45 s sem fade-out e faça loop. Alternativa: compor com Tone.js no raea (`raea guide music`, `raea sounds`).
- Volume dos efeitos: comece em 0,1 a 0,3. Agudos (alarme, bip, brilho) soam bem mais altos do que o pico indica. Meça o trecho com `ebur128` contra a voz logo antes; se passar mais de 1 LU, abaixe.

## 4. raea: estrutura e armadilhas

- Workspaces em `~/Documentos/raea/` (`git config --global raea.root`). Projeto: `raea project new NOME`; composições em `compositions/`, código em `components/`, renders em `out/`.
- **Mídia em `compositions/media/`**: o `staticFile("x")` procura ao lado da composição, não em `assets/`.
- **3D com React Three Fiber**: `raea add three@0.187.0 @react-three/fiber@9.8.2 @react-three/drei@10.7.9`, cena dentro de `<R3F shadows camera={{fov, near, far}}>`, e o `<R3F>` dentro de `<Canvas3D layered>`. Sem o layered, o gradiente da página não aparece atrás do 3D. Contexto do React: repasse o Provider dentro do `<R3F>`.
- **Nomeie toda `<mesh>`** com forma e cor (`name={`box${JSON.stringify(args)}${cor}`}`). O raea guarda a geometria pelo caminho na árvore; quando algo entra ou sai, uma peça herda a geometria de outra e aparecem "lajes gigantes" nas cores dos personagens.
- **`<Line>` do drei quebra o render** ("BufferMesh: attribute instanceStart"). Use `tubeGeometry` com `CatmullRomCurve3`.
- **Emoji**: o raea não desenha fonte de emoji colorida. Use PNGs da Noto (`npm pack emoji-datasource-google`, `img/google/64/CODIGO.png`) e uma `emo(texto)` que troca cada emoji por `<Img>`, e o ✓ por um SVG. Pronta em `~/Documentos/raea/graal/projects/terceirizar-ti/components/emo.tsx`.
- **Contorno de texto**: `-webkit-text-stroke` e `paint-order` são ignorados. Use um anel de 16 `textShadow` (`estilo.ts` do mesmo projeto).
- **Fontes**: `npm pack @fontsource/NOME`, copie os `.woff2` para `compositions/media/fonts/` e declare `@font-face` com `src: url(${staticFile(...)})`. Sempre defina `fontFamily`; o padrão do raea é serifado.
- **API compatível com Remotion**: `interpolate`, `spring`, `Easing`, `Sequence`, `Audio` (`volume` como número ou função do quadro), `Img`, `staticFile`, `useCurrentFrame`. Ponha `<Mix lufs={-14} />` na composição.
- **Duração** calculada no módulo: importe `narracao.json` e passe `durationInFrames` ao `<Composition>`.
- **Zonas seguras (1080x1920)**: texto fora do topo (220 px), da base (420 px), da direita (140 px) e da esquerda (60 px). Legenda entre 65% e 75% da altura, com 60 px ou mais.

## 5. Verificação

1. `raea check --quick compositions/X.tsx` após cada mudança. Avisos de leitura "0.0 s" vêm de olhar só 3 quadros e podem ser ignorados.
2. Quadros-chave (meio e fim de cada passo): `raea render compositions/X.tsx --at A,B,C -o out/quadros/`, depois `magick montage out/quadros/*.png -resize 360x -tile 6x -geometry +6+6 -background '#222' out/folha.png`, e abra a folha. Quadros soltos com saltos grandes podem sair com o 3D errado; na dúvida, tire o mesmo quadro do MP4 final: `ffmpeg -i out/X.mp4 -vf "select=eq(n\,N)" -vframes 1 q.png`.
3. Render: `raea render compositions/X.tsx -o out/X-vN.mp4` (cerca de 140 ms por quadro; uns 4 min para 53 s). Rode em segundo plano.
4. Meça: `ffprobe` (duração ≤ 60 s) e `ffmpeg -i out/X-vN.mp4 -af ebur128=peak=true -f null -` (cerca de -14 LUFS, pico ≤ -1 dBTP). Para cada efeito, meça o trecho com `-ss T -t D` e compare com a voz logo antes. No zsh, `set -- $var` não separa palavras; rode laços desse tipo com `bash -c`.

## 6. Entrega

O raea no Linux grava o áudio em Opus; o WhatsApp e o Instagram recusam ("arquivo não compatível"). Gere a cópia de entrega:

```
ffmpeg -i out/X-vN.mp4 -c:v libx264 -profile:v high -level 4.1 -pix_fmt yuv420p -crf 18 -preset slow -c:a aac -b:a 192k -ar 48000 -movflags +faststart out/X-whatsapp.mp4
```

Fica com uns 18 MB para 53 s, contra 65 MB do original. Entregue os dois: o original para reeditar e o `-whatsapp` para postar.
