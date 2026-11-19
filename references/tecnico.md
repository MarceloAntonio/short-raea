# Referência técnica

## Índice
1. Chaves
2. Voz (ElevenLabs)
3. Sons e música (Freesound)
4. raea: estrutura e armadilhas
5. Verificação
6. Entrega
7. Windows
8. Vários idiomas
9. Bugs de composição que já custaram um render

## 1. Chaves

Ficam em `~/api/` (pasta 700, arquivos 600), no formato `NOME=valor`:
- `~/api/elevenlabs.env` → `ELEVENLABS_API_KEY`
- `~/api/freesound.env` → `FREESOUND_API_KEY`

Leia o valor para uma variável (`K=$(grep '^ELEVENLABS_API_KEY=' ~/api/elevenlabs.env | cut -d= -f2-)`) e mande só no cabeçalho do próprio serviço. Nunca rode `cat`, `sed` ou `echo` nesses arquivos: a saída aparece no terminal e a chave vaza (já aconteceu uma vez e a chave precisou ser trocada). Os scripts do projeto modelo já leem desses caminhos.

Se a chave não estiver em `~/api/`, **pergunte onde está**. Não varra o disco atrás de `.env` (o modo automático do Claude Code bloqueia isso, e com razão). Em outra máquina ela veio em `~/.raea/elevenlabs.env` com o nome `ELEVENLABS_KEY`: o script de voz deve aceitar os dois nomes (`ELEVENLABS_API_KEY` e `ELEVENLABS_KEY`) e os dois lugares. Para confirmar que a linha existe sem mostrar o valor: `grep -c '^ELEVENLABS_KEY=.' ARQUIVO`.

## 2. Voz (ElevenLabs)

- `POST https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/with-timestamps?output_format=mp3_44100_128`
- Cabeçalho `xi-api-key`. Corpo: `{"text": ..., "model_id": "eleven_multilingual_v2", "language_code": "pt", "voice_settings": {"stability": 0.5, "similarity_boost": 0.75, "speed": 1.15}}`
- Voz padrão: **Liam** `TX3LPaxmHKxFdv7VOQHJ` (americana falando português; avise que pode ter sotaque). A chave não tem permissão de listar vozes: para outra voz, peça o ID.
- A resposta traz `audio_base64` e `alignment` (tempo por caractere). Agrupe em palavras com `~/projetos/terceirizar-ti/scripts/palavras.ts`. O `scripts/gerar-audio.ts` desse projeto faz tudo por passo (só refaz o que mudou), grava `public/audio/narracao.json` e falha se passar de `duracaoMaxSeg`.
- Duração do passo = fim da última palavra + 0,2 s. O MP3 tem silêncio no fim e, somado em 8 passos, estoura os 60 s.
- Alternativa grátis: edge-tts (`pt-BR-AntonioNeural`, `+18%`), com `meta.voz.provedor: "edge"`.
- **Nome de marca pronunciado errado** ("Graal" saiu "girl" com o Liam): troque a palavra **só no texto enviado à voz**, com `meta.voz.pronuncia: {"Graal": "Graál"}` no roteiro (em inglês, `"Grah-ahl"`). A legenda e as deixas continuam com a grafia real: depois do alinhamento, troque cada palavra falada pela escrita na mesma posição (a troca é uma palavra por uma, então o número de palavras bate; se não bater, avise). Inclua o texto enviado à voz na assinatura do passo, para só aquele passo ser refeito. Você não ouve o áudio: peça ao usuário para conferir a pronúncia, e não diga que está corrigido antes disso.
- **Prévia sem gastar créditos**: um modo `--previa` no script de voz que grava áudio mudo (`ffmpeg -f lavfi -i anullsrc`) e tempos estimados por palavra (0,12 s + 0,045 s por letra, mais pausa na pontuação). Serve para ver as cenas e conferir as deixas antes da voz real. A estimativa sai cerca de 30% mais longa que o Liam a 1,15.
- Fala mais longa estoura os 60 s rápido: na rodada de ajustes, a fala do custo foi de 10,7 s para 16,8 s e o vídeo foi para 63 s. Avise a duração nova junto com o texto, antes de gerar.

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
- **Nomeie toda `<mesh>`** com forma e cor (`name={`box${JSON.stringify(args)}${cor}`}`). O raea guarda a geometria pelo caminho na árvore; quando algo entra ou sai, uma peça herda a geometria de outra e aparecem "lajes gigantes" nas cores dos personagens. Peça transparente (vidro) leva a opacidade no nome também, e sem sombra (`castShadow={false}`), senão o vidro projeta uma sombra sólida.
- **Vidro deixa o cenário maior sem tapar a ação**: para o escritório ter "cara de empresa grande", uma divisória de vidro (opacidade 0,16) com um salão cheio atrás funcionou melhor que paredes. A câmera alta vê o fundo pelo vidro, e os planos fechados continuam limpos.
- **Personagens low-poly parecem todos calvos** com uma tampinha só na cabeça. Dê penteados variados (curto, liso até a nuca, longo até os ombros, rabo de cavalo, coque, cacheado, calvo com faixa grisalha) e cores variadas. O rosto olha para -z, então o cabelo comprido fica em +z, o lado que a câmera vê. O protagonista fica com um cabelo fixo e fácil de reconhecer.
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
3. Render: `raea render compositions/X.tsx -o out/X-vN.mp4` (cerca de 140 ms por quadro no Linux, uns 4 min para 53 s; no Windows com GPU pequena, 3 vezes isso, seção 7). Rode em segundo plano, um vídeo por comando.
4. Meça: `ffprobe` (duração ≤ 60 s) e `ffmpeg -i out/X-vN.mp4 -af ebur128=peak=true -f null -` (cerca de -14 LUFS, pico ≤ -1 dBTP). Para cada efeito, meça o trecho com `-ss T -t D` e compare com a voz logo antes. No zsh, `set -- $var` não separa palavras; rode laços desse tipo com `bash -c`.

## 6. Entrega

O raea no Linux grava o áudio em Opus; o WhatsApp e o Instagram recusam ("arquivo não compatível"). Gere a cópia de entrega:

```
ffmpeg -i out/X-vN.mp4 -c:v libx264 -profile:v high -level 4.1 -pix_fmt yuv420p -crf 18 -preset slow -c:a aac -b:a 192k -ar 48000 -movflags +faststart out/X-whatsapp.mp4
```

Fica com uns 18 MB para 53 s, contra 65 MB do original. Entregue os dois: o original para reeditar e o `-whatsapp` para postar.

Capa, legenda e hashtags: `references/publicacao.md`.

## 7. Windows

- Instalação no PowerShell: `irm https://raea.io/install.ps1 | iex` (o `install` em `sh` recusa o Git Bash). Leia o script antes de rodar. Ele põe `~\.raea\bin` no PATH só para terminais novos: no terminal já aberto, `export PATH="$HOME/.raea/bin:$PATH"`. Rode `raea doctor --fix` em seguida, para a skill `raea` ficar na versão do binário.
- **"three is not defined" antes do primeiro quadro**: o `node_modules` veio sem os links do topo (projeto criado em outra máquina). Rode `raea install` no projeto e depois `touch` na composição: o raea guarda a recusa enquanto o arquivo não muda e repete "the file is unchanged since raea last refused it".
- **Render lento**: com uma GPU de 1,8 GB, foram 420 a 490 ms por quadro (no Linux, 140 ms), cerca de 16 min para 63 s. Os primeiros minutos não imprimem nada; o vídeo só começa a ser gravado quando aparece a linha do `[OpenH264]`.
- **Pouca memória**: o Claude Code mata comandos em segundo plano quando a RAM acaba, e um laço que renderizava três idiomas em sequência morreu no primeiro. Confira a RAM livre antes (`Get-CimInstance Win32_OperatingSystem`) e renderize **um vídeo por comando**. Se o comando for morto, não reinicie sozinho: avise e pergunte.
- O áudio também sai em Opus no Windows; a cópia AAC da seção 6 vale aqui.
- `ffmpeg -pattern_type glob` não existe no build do Windows: monte a lista de entradas com `$(for f in pasta/*.png; do echo -i $f; done)` e use `hstack`/`vstack`, ou `-i frame-%05d.png` com `tile=`.

## 8. Vários idiomas

- **O roteiro em português é a fonte da cena** (câmera, lugares, cores, tempos fixos). Um script (`ferramentas/idiomas.py`) gera `roteiro.es.json` e `roteiro.en.json` a partir dele, trocando só os textos: falas, rótulos, overlays, CTA e as **palavras das deixas**. Assim, ajustar uma cena no português vale para os três depois de rodar o script.
- Cada deixa precisa ser uma palavra **dita naquele idioma**. "caiu" vira "cayó" e "crashed"; "agora" vira "ahora" e "what".
- **A primeira ocorrência vence**: se a palavra aparece duas vezes na fala ("é **só** contratar... de uma pessoa **só**"), a deixa cai na primeira. Prenda em outra palavra (`{"palavra": "pessoa", "depoisSeg": 0.25}`).
- Antes de renderizar, rode uma checagem que procura cada deixa na `narracao.json` do idioma e lista as que faltam. Nos três idiomas ela rodou antes de cada render, e nenhum render saiu com deixa perdida.
- Narração por idioma em `compositions/media/audio/{es,en}/`, uma composição por idioma (`NOME-es.tsx`, `NOME-en.tsx`) que só troca o roteiro e a narração importados.
- Durações medidas com o Liam a 1,15, mesmo texto: PT 60 s de voz, ES 63 s, EN 59 s. O espanhol fica uns 5% mais longo.
- Termos que não existem fora do Brasil: 13º vira "aguinaldo" (América Latina) e "bonuses" (inglês); LGPD vira "protección de datos" e "data privacy". O relógio de 24 h vira "11:47 PM" no texto em inglês.
- Textos traduzidos ficam mais longos. Confira os quadros de cada idioma: "casi 2×" ao lado de uma barra quebrou em duas linhas no espanhol.

## 9. Bugs de composição que já custaram um render

- **Dois componentes com o mesmo nome no mesmo arquivo**: uma `function Seta` para a seta do roteiro e outra `function Seta` para o ícone do botão do CTA. A segunda declaração vence em silêncio, e as setas "cadê ele?" e "o conhecimento foi junto" não apareciam desde a primeira versão do vídeo; no lugar delas ficava só um "→" no canto. Procure nomes repetidos em cada arquivo (no bash, com `shopt -s globstar`): `for f in components/**/*.tsx; do grep -oE "^(export )?function [A-Za-z0-9_]+" "$f" | sed 's/^export //' | sort | uniq -d | sed "s|^|$f: |"; done`. Nada impresso = nenhum nome repetido.
- **Emoji da mesma cor do fundo**: o ❓ da Noto é vermelho e sumiu dentro de uma pílula vermelha. Em fundo colorido, use texto ("?") em vez do emoji.
- **Texto ao lado de uma barra que cresce**: calcule a largura da barra máxima mais o texto mais longo de todos os idiomas, e ponha `whiteSpace: "nowrap"` no texto.
- **Mudar o cenário sem quebrar a história**: as cenas dependem da posição de algumas peças (a mesa do protagonista, a porta por onde ele sai, a parede do relógio, o servidor que dá alarme). Ao trocar o layout, mantenha essas âncoras nos mesmos lugares (desloque o layout novo inteiro, se for preciso) e atualize no roteiro só as que mudarem de lugar. Depois confira um quadro de cada cena que usa uma âncora.
- **Faces no mesmo plano piscam (z-fighting)**: no vídeo do vazamento, o cliente viu portas, vitrines e batentes "piscando". Eram peças encostadas com faces coincidentes (vitrine e porta da loja na mesma profundidade e sobrepostas; porta, batente e vão da fachada com a mesma borda). Deixe 1 a 2 cm de folga ou sobreposição clara entre peças que se tocam, e confira de perto (recorte o quadro) toda porta, janela e placa. Vale dentro da mesma peça: os dentes da chave tinham a mesma espessura da haste e piscavam onde se encostavam; peça encaixada em outra fica um pouco mais fina.
- **Objeto que gira não pode encostar na parede**: a cópia da chave continuava girando pendurada no quadro e metade entrava na parede. Quando o objeto pousa, pare a rotação.
- **Cabelo com furos**: esfera achatada de det 1 sobre a cabeça deixa vértices da cabeça aparecendo. Use det 2 e raio um pouco maior que a cabeça.
- **Peças iguais acesas e apagadas**: ponha o emissive no nome da malha, senão as duas dividem o material.

