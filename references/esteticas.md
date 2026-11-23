# Catálogo de estéticas visuais

Serve para escolher a cara de cada Short novo do canal de TI (Linux, DevOps, redes, segurança, incidentes famosos). Os últimos ~20 vídeos saíram com o mesmo visual: formas abstratas com brilho. Este catálogo existe para quebrar isso. Cada entrada diz como a cena fica, o que cabe no raea (Canvas3D, Mesh3d, Text3D, luzes, Bloom, Fog, PBR, glTF, `ToonMaterial`, `Look`, `DepthOfField`, `Outline`, HTML/CSS por cima, shaders) e o que dá trabalho.

## Regra de uso

1. Leia o histórico anti-repetição e anote a estética dos 3 últimos vídeos.
2. A estética do vídeo novo não pode ter aparecido nesses 3.
3. No máximo 1 forma recorrente dos 3 últimos pode voltar (por exemplo, o mesmo cubo ou o mesmo círculo com bolinhas).
4. O visual "limpo/abstrato" (formas geométricas, partículas, prédios brilhando) é a entrada 1, **Abstrato com brilho (seguro)**. Só entra marcada como (seguro) e com o público para o qual funciona, descrito na própria entrada.
5. Registre a estética escolhida no histórico junto com o vídeo.
6. Cada estética tem os próprios movimentos: como os elementos entram, como a cena troca e o que a câmera faz estão em `movimento.md`, seção 5, com os mesmos números deste catálogo. Use esses movimentos em vez de zoom e pop; é isso que faz dois vídeos com o mesmo tema não parecerem iguais.

Regras do projeto valem para todas: sem imagem ou vídeo gerado por IA, fontes locais (baixar o arquivo da fonte do Google Fonts e carregar localmente), sons CC0 do Freesound, peças que se sobrepõem de propósito precisam de `allowOverlap`, `Text3D` é centralizado na posição, instâncias têm contagem fixa (esconder com tamanho 0.001), sem `Intl`.

Legenda de risco: seguro = fácil de acertar na primeira renderização; médio = pede 1 ou 2 rodadas de ajuste de luz/material; ousado = exige shader, textura procedural ou muito trabalho de cena.

## Índice

1. [Abstrato com brilho (seguro)](#1-abstrato-com-brilho-seguro)
2. [Papel recortado (papercraft)](#2-papel-recortado-papercraft)
3. [Massinha (claymation)](#3-massinha-claymation)
4. [Miniatura com tilt-shift](#4-miniatura-com-tilt-shift)
5. [Planta técnica azul (blueprint)](#5-planta-técnica-azul-blueprint)
6. [Terminal CRT âmbar](#6-terminal-crt-âmbar)
7. [Pixel art isométrico](#7-pixel-art-isométrico)
8. [Risografia com 2 cores](#8-risografia-com-2-cores)
9. [Quadrinho com balões](#9-quadrinho-com-balões)
10. [Noir em preto e branco com uma cor](#10-noir-em-preto-e-branco-com-uma-cor)
11. [Brinquedo de plástico de montar](#11-brinquedo-de-plástico-de-montar)
12. [Maquete de isopor](#12-maquete-de-isopor)
13. [Tabuleiro de jogo](#13-tabuleiro-de-jogo)
14. [Mapa de cartografia antiga](#14-mapa-de-cartografia-antiga)
15. [Interface de videogame retrô](#15-interface-de-videogame-retrô)
16. [Ficha de laboratório](#16-ficha-de-laboratório)
17. [Embalagem de produto](#17-embalagem-de-produto)
18. [Teatro de bonecos](#18-teatro-de-bonecos)
19. [Sonho surreal](#19-sonho-surreal)
20. [Tipografia gigante que vira cenário](#20-tipografia-gigante-que-vira-cenário)
21. [Raio-X](#21-raio-x)
22. [Aquário](#22-aquário)
23. [Cozinha: o problema como receita](#23-cozinha-o-problema-como-receita)
24. [Diorama low-poly de escritório](#24-diorama-low-poly-de-escritório)
25. [Rua noturna cinematográfica](#25-rua-noturna-cinematográfica)
26. [Bauhaus e construtivismo](#26-bauhaus-e-construtivismo)
27. [Vitral](#27-vitral)
28. [Origami](#28-origami)
29. [Neon de letreiro com chuva](#29-neon-de-letreiro-com-chuva)
30. [Mapa de metrô](#30-mapa-de-metrô)

---

## 1. Abstrato com brilho (seguro)

No histórico aparece como "formas abstratas com brilho".

- **Cena**: fundo escuro quase preto com Bloom. Cubos emissivos, círculos com bolinhas orbitando, prédios ou racks como caixas altas com janelas acesas, partículas flutuando. É o visual que vem se repetindo nos últimos ~20 vídeos; se a cena nova se parece com isso, é esta entrada.
- **Paleta**: #0b0f1a (fundo), #22d3ee (ciano emissivo), #a78bfa (violeta), #f472b6 (rosa), #e5e7eb (texto).
- **Tipografia**: sans geométrica, peso médio a bold, por exemplo Space Grotesk ou Inter.
- **Câmera**: órbita lenta ou dolly para frente, com leve balanço.
- **Trilha**: synth ambiente, pad escuro e pulso eletrônico; whoosh, blips e um sub grave nas viradas.
- **Serve para**: qualquer tema quando falta tempo; funciona melhor para público que já gosta de visual "tech" genérico (iniciantes em redes e cloud) e para conceitos sem objeto físico claro (latência, zero trust).
- **Difícil no raea**: nada técnico. O problema é a repetição e a perda de identidade do canal; usar só como (seguro) e com forma diferente das 3 últimas.
- **Risco**: seguro.

## 2. Papel recortado (papercraft)

- **Cena**: camadas de papel colorido empilhadas com pequena distância em Z, cada uma com sombra suave sobre a de trás; personagens e objetos são recortes planos com borda irregular. Parallax entre camadas quando a câmera anda de lado.
- **Paleta**: #f4ead5 (papel creme), #e76f51 (laranja queimado), #2a9d8f (verde-azulado), #264653 (azul petróleo), #e9c46a (mostarda).
- **Tipografia**: serifada gorda ou slab, por exemplo Fraunces ou Bitter, letras também como recortes com sombra.
- **Câmera**: travelling lateral lento mais leve avanço em Z; sem rotação, para o parallax aparecer.
- **Trilha**: ukulele ou xilofone, percussão leve de dedos; sons de papel rasgando, folheando e tesoura (Freesound).
- **Serve para**: conceitos explicados em camadas (modelo OSI, containers dentro de host, firewall em zonas), histórias curtas de incidente com poucos personagens.
- **Difícil no raea**: papel fino com `Cuboid` de espessura 0.02 e material rugoso sem metal; sombra vem de DirectionalLight com `Shadows`. Borda irregular: usar `Decal` ou `BufferMesh` com contorno ruidoso fixo (seed por índice). Evite luz muito dura, que mostra z-fighting entre camadas; separar camadas por pelo menos 0.05.
- **Risco**: médio.

## 3. Massinha (claymation)

- **Cena**: personagens e objetos feitos de esferas, cápsulas e cilindros arredondados com material fosco, com marcas de dedo simuladas por pequenas variações de escala. Movimento em 12 quadros por segundo (segurar cada pose 2 a 3 quadros) para dar o tremor de stop motion.
- **Paleta**: #d94f3d (vermelho massinha), #f2b134 (amarelo), #3f8f6b (verde), #5a7fb0 (azul), #f1e3c8 (fundo de papelão claro).
- **Tipografia**: arredondada e gorda, por exemplo Fredoka ou Baloo 2, letras como massa com leve irregularidade.
- **Câmera**: quase fixa, pequenos deslocamentos em degraus (também em 12 fps); close nos olhos para emoção.
- **Trilha**: tuba, clarinete, pizzicato, percussão de brinquedo; sons de beliscar, estalo molhado e passos abafados.
- **Serve para**: incidentes com personagem (o estagiário que apagou o banco), humor, erro humano, explicar bug como "criatura".
- **Difícil no raea**: o raea não tem massa deformável; compor com primitivas e variar `scale` por quadro com hash de índice para o tremor. `StandardMaterial` com roughness alto e `AmbientOcclusion` ligada fazem o volume. Sem impressão digital real: pode usar `ToonMaterial` sem contorno para suavizar.
- **Risco**: médio.

## 4. Miniatura com tilt-shift

- **Cena**: cidade ou datacenter visto de cima em ângulo de 35 a 45 graus, prédios e carrinhos como brinquedos, com foco em uma faixa estreita e o resto desfocado. Cores saturadas e luz de fim de tarde.
- **Paleta**: #ffcf6e (luz quente), #ff7a59 (telhados), #5fb3a1 (verde), #4a6fa5 (sombras azuis), #f7f3e8 (ruas claras).
- **Tipografia**: sans humanista legível, por exemplo Nunito ou Poppins, em plaquinhas pequenas na cena.
- **Câmera**: pairando alto com deslocamento lento lateral; rack focus movendo a faixa nítida entre pontos.
- **Trilha**: lo-fi leve, vibrafone e baixo suave; sons de cidade distante, buzina curta e trem pequeno.
- **Serve para**: fluxo de tráfego, balanceamento de carga, rotas de rede, CDN, ataque DDoS visto como multidão de carrinhos.
- **Difícil no raea**: usar `DepthOfField` com `focal_distance` e abertura grande; ele desfoca por profundidade, não por faixa da tela, então incline a câmera para que a faixa nítida coincida com a profundidade. Muitos carrinhos: `Instances` com contagem fixa. Desfoque nas bordas inferior e superior não existe como filtro de tela; contorne com a inclinação.
- **Risco**: médio.

## 5. Planta técnica azul (blueprint)

- **Cena**: fundo azul-cianotipia com grade fina; objetos desenhados só em linhas brancas (arestas), cotas com setas, legendas em caixas, carimbo no canto. As linhas se desenham aos poucos.
- **Paleta**: #0d3b66 (azul fundo), #1b5a99 (grade), #f4f9ff (linha branca), #8ecae6 (linha secundária), #ffd166 (destaque raro).
- **Tipografia**: monoespaçada ou letra de projetista, por exemplo Share Tech Mono ou IBM Plex Mono; títulos em caixa alta com espaçamento.
- **Câmera**: ortográfica frontal ou isométrica, deslocamento lento como mesa de desenho; o detalhe com cota entra por corte (zoom só se for um dos 2 do orçamento).
- **Trilha**: sons de mesa técnica, pulso discreto de sintetizador, clique de régua; efeitos de lápis riscando e papel vegetal.
- **Serve para**: arquitetura de sistemas, topologia de rede, anatomia de um protocolo, diagrama de pipeline, explicação passo a passo.
- **Difícil no raea**: linhas finas em 3D não vêm prontas. Opção 1: renderizar em HTML/SVG por cima com `stroke-dashoffset` animado (mais simples e nítido). Opção 2: `Outline` sobre cubos com material branco. Cotas e setas em SVG. Usar o 2D como base e o 3D só se precisar de giro.
- **Risco**: seguro.

## 6. Terminal CRT âmbar

- **Cena**: monitor CRT antigo com tela abaulada e brilho âmbar em sala escura, texto aparecendo caractere a caractere, linhas de varredura e leve cintilação. Cursor piscando como ritmo.
- **Paleta**: #0a0703 (fundo), #ffb000 (âmbar), #ff7a00 (âmbar quente), #5c3b00 (âmbar apagado), #2b2b2b (carcaça).
- **Tipografia**: monoespaçada de terminal, por exemplo VT323 ou IBM Plex Mono.
- **Câmera**: close fixo na tela; corte para plano aberto do monitor na mesa; tremor mínimo.
- **Trilha**: drone grave de transformador, teclado mecânico, bipes; ventoinha, relê, estática e disquete (Freesound).
- **Serve para**: Linux, shell, logs, sysadmin, invasão e incidentes históricos, qualquer comando mostrado na tela.
- **Difícil no raea**: o texto é HTML/CSS por cima ou `Text3D` na tela; scanlines com gradiente repetido e `Bloom` baixo. Distorção de lente só vale no 3D (`Fisheye`/`LensDistortion` não curvam o HTML). Para a curvatura, desenhe o texto em um plano curvo ou aceite tela plana. Foi uma das estéticas originais do canal; checar o histórico antes de repetir.
- **Risco**: seguro.

## 7. Pixel art isométrico

- **Cena**: salas, servidores e cidades em blocos isométricos com paleta limitada, personagens de poucos pixels, sombras em degrau. Tudo parece pintado em grade.
- **Paleta**: #1a1c2c (contorno escuro), #5d275d (roxo), #b13e53 (vermelho), #38b764 (verde), #73eff7 (ciano claro).
- **Tipografia**: fonte pixel, por exemplo Press Start 2P ou Pixelify Sans.
- **Câmera**: ortográfica isométrica fixa, com deslocamento em passos inteiros de pixel; zoom por corte e não por movimento suave.
- **Trilha**: chiptune com onda quadrada e triangular, arpejos; blips, moeda e passos em 8 bits (Freesound CC0).
- **Serve para**: histórias de incidente com mapa de salas, progressão de ataque em fases, explicação de arquitetura em "andares".
- **Difícil no raea**: câmera ortográfica (`projection` Orthographic) com `Cuboid` e materiais sem brilho; `<Look mode="pixel" pixelSize={4} />` converte o quadro em pixels e com `palette` limitada. Sombras por pixel exigem `AntiAliasing` desligado. Personagens: cubinhos empilhados, não sprites.
- **Risco**: médio.

## 8. Risografia com 2 cores

- **Cena**: imagem em duas tintas (por exemplo rosa e azul) sobre papel off-white; onde se sobrepõem aparece uma terceira cor; grão de meio-tom, leve desalinhamento entre as chapas.
- **Paleta**: #f6f0e4 (papel), #ff4f8b (rosa fluo), #1d4ed8 (azul), #5b2a86 (sobreposição roxa), #222222 (texto raro).
- **Tipografia**: grotesca grossa ou display condensada, por exemplo Archivo Black ou Bebas Neue, em uma só chapa.
- **Câmera**: movimento mínimo; cortes secos e pequenas translações das chapas, como se o papel passasse de novo pela máquina.
- **Trilha**: batida lo-fi com vinil, baixo de bossa ou indie leve; sons de impressora, rolo de papel e carimbo.
- **Serve para**: infográficos de segurança (antes e depois), comparações, estatística de incidentes, glossários rápidos.
- **Difícil no raea**: melhor feito em 2D: duas camadas HTML com `mix-blend-mode: multiply`, cores sólidas e textura de meio-tom via `radial-gradient` repetido, deslocadas 3 a 6 px. Em 3D, usar `<Look mode="paint" palette>` com 3 cores, mas o resultado é mais ilustração do que riso. Evite texto de duas cores (fica ilegível com a sobreposição).
- **Risco**: médio.

## 9. Quadrinho com balões

- **Cena**: quadro dividido em painéis com bordas grossas, retícula (meio-tom) nas sombras, onomatopeias grandes ("BZZT", "404"), balões de fala e legendas em caixas amarelas.
- **Paleta**: #fff8e7 (papel), #111111 (traço), #e63946 (vermelho), #ffd23f (amarelo), #3a86ff (azul).
- **Tipografia**: letra de quadrinho em caixa alta, por exemplo Bangers para ruídos e Comic Neue ou Patrick Hand para balões.
- **Câmera**: painéis que entram em sequência deslizando ou virando; "câmera" é o corte entre painéis; tremor só no impacto principal.
- **Trilha**: orquestra de jazz de desenho ou rock curto; sons de impacto, whoosh, sino e "tum" de página virando.
- **Serve para**: narrativa de incidente com diálogo (suporte x usuário), mitos de segurança, comparação de duas opções em painéis.
- **Difícil no raea**: painéis e balões em HTML/CSS com `clip-path`; cena dentro de cada painel em `Canvas3D` com `<Look mode="cartoon" />` e `ToonMaterial` com contorno. Balão com rabinho: `clip-path: polygon`. Vários Canvas3D ao mesmo tempo pesam; use um só e recorte por máscara.
- **Risco**: médio.

## 10. Noir em preto e branco com uma cor

- **Cena**: contraste alto, luz dura entrando por persianas, névoa baixa, silhueta de detetive/analista; tudo em preto, cinza e branco, com um único elemento colorido (a chave, o log em vermelho, a luz da tela).
- **Paleta**: #000000, #f2f2f2, #6b6b6b, #d00000 (cor única, vermelho), #2a2a2a.
- **Tipografia**: serifada de cartaz antigo ou máquina de escrever, por exemplo Playfair Display ou Special Elite.
- **Câmera**: planos baixos e inclinados (ângulo holandês leve), dolly lento, corte para close em objeto.
- **Trilha**: saxofone com surdina e contrabaixo, chuva; passos, isqueiro, telefone antigo e máquina de escrever.
- **Serve para**: investigação forense, resposta a incidente, malware, vazamento de dados, "quem fez isso".
- **Difícil no raea**: `Grade` com saturação 0 e a cor única via material emissivo ou camada HTML por cima; sombras de persiana com `SpotLight` e uma máscara de caixas finas (ou `WindowLight`). `VolumetricFog` dá os feixes. Sem pós-processo seletivo de cor, então a exceção deve ser um objeto com emissive e `Grade` aplicada só à cena (colocar o elemento colorido em HTML).
- **Risco**: médio.

## 11. Brinquedo de plástico de montar

- **Cena**: mundo feito de blocos de plástico encaixáveis genéricos (tijolos retangulares com pinos cilíndricos, placas base), cores primárias brilhantes, personagens de blocos empilhados; a construção se monta peça por peça.
- **Paleta**: #e4002b (vermelho), #0057b8 (azul), #ffd500 (amarelo), #00a651 (verde), #f2f2f2 (placa base clara).
- **Tipografia**: arredondada e gorda, por exemplo Lilita One ou Baloo 2; letras em relevo de bloco.
- **Câmera**: planos médios com leve órbita; câmera baixa com desfoque de fundo; "stop motion" em passos.
- **Trilha**: marcha divertida com xilofone e baixo; clique de encaixe de plástico, peças caindo na mesa.
- **Serve para**: montagem passo a passo (pipeline CI/CD, deploy, arquitetura de microsserviços, "construir um servidor").
- **Difícil no raea**: usar só `Cuboid` e `Cylinder` genéricos com `StandardMaterial` brilhante (roughness baixo, clearcoat); não copiar proporções ou logos de marcas existentes (sem texto nos pinos). Muitos tijolos: `Instances`. Peças que se tocam precisam de `allowOverlap`. Montagem animada com `spring` por peça.
- **Risco**: médio.

## 12. Maquete de isopor

- **Cena**: edifícios e relevos brancos de isopor com cantos retos, texturas granulares e sombras suaves, sobre mesa de trabalho com cortador e alfinetes; pequenas marcas em caneta.
- **Paleta**: #f5f5f0 (isopor), #d9d9d2 (sombra), #ff5a36 (alfinete/destaque), #2f3e46 (mesa), #cad2c5 (verde pálido).
- **Tipografia**: sans neutra de projeto, por exemplo Work Sans ou DM Sans, em etiquetas coladas.
- **Câmera**: aérea lenta sobre a maquete, descendo para plano baixo entre os prédios; luz lateral fixa.
- **Trilha**: piano minimalista ou cordas suaves; som de corte em isopor, lápis e alfinete batendo.
- **Serve para**: arquitetura de sistemas, planejamento (migração, rede de escritório), segmentação de rede, plano de resposta.
- **Difícil no raea**: material branco fosco com `AmbientOcclusion` ligada e `Shadows`; granulado com textura de ruído ou normal map procedural (se faltar, `Look` com grão leve). Iluminação suave: DirectionalLight com sombra mais `EnvironmentMapLight` fraco. Peças encostadas: `allowOverlap`.
- **Risco**: seguro.

## 13. Tabuleiro de jogo

- **Cena**: tabuleiro de madeira ou papel com casas, peões, dados e cartas; o problema vira um jogo de percurso, com casas de "sorte" e "revés" que representam eventos.
- **Paleta**: #7c4a2d (madeira), #f1e4c3 (papel), #c1121f (vermelho), #1d3557 (azul), #f4a261 (laranja).
- **Tipografia**: serifada de jogo de mesa ou slab, por exemplo Rye ou Alfa Slab One para títulos, Lora para texto.
- **Câmera**: plano zenital inclinando para perspectiva; seguimento do peão; close nos dados.
- **Trilha**: banjo, piano de bar leve, percussão de caixa; dados rolando, peça batendo na madeira e cartas virando.
- **Serve para**: etapas de um ataque (kill chain), fluxo de decisão, escalonamento de incidente, "aprenda jogando".
- **Difícil no raea**: tabuleiro com `Cuboid` e casas em `Plane3d` ou `Decal`; peões como cilindro + esfera. Dado com física: `Physics`/`usePhysics` existem, mas em render é mais seguro animar a queda por keyframes. Texto nas casas com `Text3D` pequeno (checar legibilidade em 1080 de largura).
- **Risco**: médio.

## 14. Mapa de cartografia antiga

- **Cena**: pergaminho envelhecido com costas desenhadas, rosa dos ventos, rotas pontilhadas, monstros marinhos e legendas caligráficas; a rota do dado ou do ataque é traçada como uma viagem.
- **Paleta**: #e8d5a8 (pergaminho), #b08d57 (ocre), #6b4226 (tinta marrom), #3a6b7e (azul mar desbotado), #9b2226 (vermelho carimbo).
- **Tipografia**: caligráfica ou serifada antiga, por exemplo IM Fell English ou Cinzel Decorative.
- **Câmera**: travelling sobre o mapa em ângulo quase zenital, a rota desenhada leva a câmera de ilha em ilha; rolagem lateral.
- **Trilha**: alaúde, flauta e tambor suave; ondas, vento, tinta riscando e pergaminho abrindo.
- **Serve para**: rotas de rede (traceroute), histórico de uma intrusão por países, topologia da internet, cabos submarinos.
- **Difícil no raea**: textura de pergaminho precisa de ruído (gradiente + `Look` com grão; sem imagem gerada por IA). Rotas pontilhadas em SVG com `stroke-dasharray` animado. Monstros: silhuetas simples em SVG. Melhor em 2D com leve inclinação 3D num plano (`ImagePlane`).
- **Risco**: médio.

## 15. Interface de videogame retrô

- **Cena**: tela com moldura de console genérico, barras de vida e de mana, menu de comandos, caixas de diálogo com texto digitando, inventário e "fase" com nome; a situação vira uma batalha ou fase.
- **Paleta**: #0f0f1b (fundo), #00e436 (verde de vida), #ff004d (vermelho de dano), #29adff (azul), #fff1e8 (texto).
- **Tipografia**: fonte pixel, por exemplo Press Start 2P ou VT323.
- **Câmera**: plano fixo de tela de jogo; tremor curto só no dano principal; troca de plano por corte.
- **Trilha**: chiptune de batalha, arpejos rápidos; blips de menu, dano, vitória e "game over" (todos de Freesound CC0, sem copiar melodias conhecidas).
- **Serve para**: ataques e defesas como combate, "boss" de incidente, métricas como barras de vida (disponibilidade, risco).
- **Difícil no raea**: quase tudo em HTML/CSS (barras, menus, caixas com `border` pixelado via `box-shadow`); a "fase" pode ser `Canvas3D` com `<Look mode="pixel">`. Não copiar personagens, interface ou música de jogo existente: inventar elementos próprios.
- **Risco**: seguro.

## 16. Ficha de laboratório

- **Cena**: prancheta ou ficha de exame em papel branco, campos preenchidos à caneta, carimbos de "REPROVADO" ou "POSITIVO", amostras em tubos de ensaio, lupa e gráfico de resultado.
- **Paleta**: #fbfbf8 (papel), #1a4d8f (azul caneta), #c62828 (carimbo), #2e7d32 (aprovado), #8d99ae (linhas da ficha).
- **Tipografia**: sans clínica, por exemplo Source Sans 3, com letra manuscrita para preenchimento (por exemplo Caveat) e carimbo em Special Elite.
- **Câmera**: zenital sobre a mesa, deslocamento de campo para campo; o carimbo desce sobre a ficha.
- **Trilha**: instrumental clínico e quieto, relógio; caneta, carimbo batendo, clip de prancheta e máquina de exame.
- **Serve para**: análise de malware, auditoria, checklist de segurança, teste de vulnerabilidade, resultado de pentest.
- **Difícil no raea**: melhor em 2D com HTML; caneta aparecendo com `clip-path` ou `stroke-dashoffset`. Tubos de ensaio em 3D: `Cylinder` com material de vidro (transmissão) pesa; usar poucos e com `Bloom` desligado.
- **Risco**: seguro.

## 17. Embalagem de produto

- **Cena**: caixa de produto de papelão com ilustração frontal, selo, "novo!", lista de conteúdo e aviso legal; a caixa gira, abre e revela o item (o serviço, a falha).
- **Paleta**: #ffd23f (amarelo vitrine), #ee4266 (vermelho), #3bceac (turquesa), #0b132b (azul escuro), #f6f1e9 (papelão claro).
- **Tipografia**: display de embalagem, por exemplo Anton ou Lilita One; letras miúdas em Roboto Condensed.
- **Câmera**: órbita de produto, plano médio com luz de estúdio; abertura da tampa em close.
- **Trilha**: jingle de comercial, baixo funky; sons de papelão, fita sendo rasgada, plástico e "pop" de abertura.
- **Serve para**: comparar ferramentas, "o que vem na caixa" de um sistema, falsos pacotes e supply chain, sátira de produto ruim.
- **Difícil no raea**: caixa de `Cuboid` com texturas em `Decal` ou `ImagePlane` nas faces; a ilustração é feita por HTML renderizado em textura se o raea permitir, senão em planos separados na frente de cada face. Tampa com articulação por rotação em torno da aresta (pivô em `Transform`).
- **Risco**: médio.

## 18. Teatro de bonecos

- **Cena**: palco com cortinas vermelhas, bastidores de papelão, bonecos de fantoche ou marionete com fios visíveis, cenário em camadas de painéis e luz de refletor.
- **Paleta**: #7b1e2b (cortina), #e9c46a (dourado), #2b2d42 (fundo do palco), #f1faee (luz), #457b9d (cenário azul).
- **Tipografia**: cartaz de teatro, por exemplo Abril Fatface ou Rye; legendas em serifada simples.
- **Câmera**: plano frontal de plateia, fixo; corte para vista dos bastidores; cortina abre e fecha.
- **Trilha**: acordeão ou piano de teatro, marcha curta; cortina deslizando, aplausos, tábua de palco rangendo (Freesound).
- **Serve para**: histórias de incidente em atos, comédia de erros, "dois sistemas conversando", golpes de engenharia social.
- **Difícil no raea**: palco em `Cuboid`s e painéis; fantoche como esferas e cilindros; fios de marionete como cilindros finos. Cortinas com dobras: `Cuboid` repetidos com escala variável e `Instances`. Sombras de refletor com `SpotLight` e `Shadows`.
- **Risco**: médio.

## 19. Sonho surreal

- **Cena**: espaço impossível com objetos em escala errada (porta flutuando sobre o deserto, relógio derretido genérico, escada para o céu), céu em degradê, sombras longas e figuras minúsculas.
- **Paleta**: #ffb4a2 (céu rosa), #6d6875 (roxo cinza), #b5838d (malva), #355070 (azul profundo), #fcd5ce (areia clara).
- **Tipografia**: serifada elegante e leve, por exemplo Cormorant Garamond; letras flutuando no cenário.
- **Câmera**: dolly lento e contínuo, sensação de câmera que flutua; transições por corte para escala maior.
- **Trilha**: pad etéreo, caixinha de música desafinada, reverso; sons de vento, sino distante e respiração.
- **Serve para**: conceitos abstratos (estado de um sistema, dívida técnica, paranoia de segurança), "pesadelo do on-call".
- **Difícil no raea**: céu com `Skybox`/`Atmosphere` e `Fog`; objetos por primitivas com `Torus`, `Cone`. Metáforas dependem de ideia, não de técnica; evitar referências diretas a obras de arte famosas (nada de cópia de pinturas conhecidas). Muita névoa esconde o texto: manter contraste.
- **Risco**: ousado.

## 20. Tipografia gigante que vira cenário

- **Cena**: letras enormes ocupam o quadro; a câmera entra nelas, e as letras viram prédios, túneis ou salas ("ROOT" vira corredor, "404" vira portas). O texto é o cenário.
- **Paleta**: #111111 (fundo), #fafafa (letra), #ff3d00 (laranja), #00b4d8 (ciano), #ffd60a (amarelo).
- **Tipografia**: display grossa e condensada, por exemplo Anton, Bebas Neue ou Archivo Black, em tamanhos enormes.
- **Câmera**: avanço contínuo atravessando as letras; cortes em letras diferentes; rotação lenta.
- **Trilha**: batida seca com baixo grave, cortes rítmicos; hits de impacto, whoosh e relógio.
- **Serve para**: códigos de erro, comandos (`sudo`, `rm -rf`), siglas (DNS, TLS), manchetes de incidente.
- **Difícil no raea**: `Text3D` com `Mesh` extrudado funciona, mas é centralizado na posição (calcular o deslocamento por letra). Entrar dentro de uma letra exige dimensionar com cuidado para evitar clipping da câmera. Letras como vigas: pode usar `Cuboid` em vez de texto. Fontes locais obrigatórias.
- **Risco**: médio.

## 21. Raio-X

- **Cena**: fundo escuro azulado, objetos translúcidos em tons de azul e branco mostrando o interior (ossos, circuitos, chips, cabos), com brilho nas bordas e feixe de varredura.
- **Paleta**: #02121f (fundo), #1c7ed6 (azul), #74c0fc (azul claro), #e7f5ff (branco), #ff6b6b (anomalia).
- **Tipografia**: técnica, por exemplo Orbitron ou Rajdhani, em rótulos finos com linhas de chamada.
- **Câmera**: plano fixo de exame com leve deslocamento lateral; a anomalia é revelada pela varredura (zoom só se for um dos 2 do orçamento); de cima para baixo.
- **Trilha**: sons de máquina de tomografia, bipes baixos, zumbido eletrônico; clique do disparo e respiração de aparelho.
- **Serve para**: "o que há dentro" de um dispositivo, malware escondido, firmware, backdoor em hardware, exame de um pacote de rede.
- **Difícil no raea**: transparência sorteada ordem pode dar erros; usar materiais com `alpha_mode` aditivo e fresnel (emissivo nas bordas, centro escuro), `Bloom` baixo. Vazado de camadas com `Cuboid` finos em fila. Inversão de cor (negativo) via `Grade`.
- **Risco**: médio.

## 22. Aquário

- **Cena**: vidro com água azul-esverdeada, bolhas, plantas, peixes simples nadando em curvas e uma criatura grande ao fundo; luz entrando por cima em feixes.
- **Paleta**: #05445e (água funda), #189ab4 (azul), #75e6da (turquesa), #d4f1f4 (feixe de luz), #ff9f1c (peixe laranja).
- **Tipografia**: sans amigável, por exemplo Quicksand ou Nunito, em letreiro do aquário.
- **Câmera**: deslizando lentamente ao longo do vidro, profundidade de campo rasa; aproximação em um peixe.
- **Trilha**: pad submerso e harpa suave; bolhas, filtro de aquário borbulhando e tom grave de profundidade.
- **Serve para**: ecossistemas (peixes como processos, containers ou usuários), "cardume" de requisições, predador como malware, observabilidade.
- **Difícil no raea**: `Fog` colorida e `VolumetricFog` com `SpotLight` para os feixes; peixes como `Instances` (contagem fixa) animados por seno e fase por índice; bolhas como `Sphere` instanciadas. Vidro do aquário fora do enquadramento para não complicar transmissão. `DepthOfField` aumenta a profundidade.
- **Risco**: médio.

## 23. Cozinha: o problema como receita

- **Cena**: bancada de cozinha vista de cima, tábua, panelas, ingredientes como componentes (um "pacote" é farinha, um "serviço" é panela), receita escrita passo a passo, tempo de forno e erro de receita queimada.
- **Paleta**: #f7f0e3 (bancada clara), #d62828 (tomate), #f77f00 (laranja), #fcbf49 (amarelo), #3a5a40 (verde).
- **Tipografia**: manuscrita de caderno de receitas, por exemplo Caveat para anotações e Merriweather para título.
- **Câmera**: zenital com travelling lateral entre etapas; close em panela e faca; relógio de forno.
- **Trilha**: bossa nova ou jazz leve de cozinha; faca na tábua, óleo chiando, timer e forno abrindo.
- **Serve para**: processos explicados em receita (deploy, backup, hardening "passo a passo"), "o que não fazer" (receita que queima), comparação de abordagens.
- **Difícil no raea**: utensílios por primitivas: panela = `Cylinder` oco com `CrossSection`/`Solid`, ovo = esfera achatada. Chiado e vapor: partículas por `Instances`. Para ficar legível, usar 3 a 4 objetos grandes e a receita em HTML.
- **Risco**: médio.

## 24. Diorama low-poly de escritório

- **Cena**: escritório em caixa cortada (uma sala vista em corte) com mesas, monitores, plantas e pessoas de poucos polígonos, luz suave de janela; ambiente aconchegante. Foi uma das estéticas originais do canal.
- **Paleta**: #f4e3c1 (parede), #c9a27e (madeira), #6c9a8b (verde), #3d5a80 (azul), #ee6c4d (laranja).
- **Tipografia**: sans arredondada leve, por exemplo Nunito ou Poppins, em plaquinhas e post-its.
- **Câmera**: órbita lenta de 20 a 30 graus ao redor da caixa, com aproximação em um detalhe.
- **Trilha**: lo-fi de escritório, teclado e piano elétrico; teclas, mouse, chat e telefone distante.
- **Serve para**: vida de TI (plantão, deploy na sexta, reunião), cultura de equipe, histórias humanas de incidente.
- **Difícil no raea**: montar muitos móveis com primitivas toma tempo; reaproveitar componentes de vídeos antigos do canal. `ToonMaterial` ou materiais foscos e `AmbientOcclusion` dão o acabamento; luz da janela com `DirectionalLight` e `Shadows`.
- **Risco**: médio.

## 25. Rua noturna cinematográfica

- **Cena**: rua molhada à noite com poças refletindo postes, um objeto de destaque (uma chave, um cartão, um servidor na calçada), névoa baixa, janelas acesas ao fundo. Foi uma das estéticas originais do canal.
- **Paleta**: #0a0f1c (noite), #1f3a5f (azul), #f2a65a (lâmpada quente), #e63946 (luz de freio), #bde0fe (reflexo frio).
- **Tipografia**: sans limpa e fina de título de filme, por exemplo Montserrat Light ou Bebas Neue.
- **Câmera**: dolly lento, plano baixo ao nível do chão; rack focus entre objeto e fundo.
- **Trilha**: pad sombrio, piano esparso e batida suave; chuva, passos na poça, carro distante e cano pingando.
- **Serve para**: histórias de incidente com clima de investigação, segurança física, credenciais perdidas, resposta a invasão.
- **Difícil no raea**: reflexo na rua: material com roughness baixo e metallic, sem reflexo de tela por padrão; contornar com `EnvironmentMapLight` e planos emissivos espelhados abaixo do chão. Chuva: `Instances` de cilindros finos com queda por frame. `Fog` e `VolumetricFog` ajudam. Cuidado para não cair no "abstrato com brilho": o cenário precisa ter objetos reconhecíveis.
- **Risco**: médio.

## 26. Bauhaus e construtivismo

- **Cena**: composição de formas geométricas planas (círculo, triângulo, quadrado), diagonais, barras grossas e tipografia inclinada; poucas cores chapadas, sem sombra; blocos que se encaixam como cartaz.
- **Paleta**: #f2e9dc (fundo), #d62828 (vermelho), #1d3557 (azul), #f4c430 (amarelo), #111111 (preto).
- **Tipografia**: geométrica e condensada, por exemplo Josefin Sans, Jost ou Oswald em caixa alta.
- **Câmera**: 2D, deslocamentos em diagonal; cortes secos; rotação de 15 graus em blocos.
- **Trilha**: percussão seca, metais curtos, piano preparado; hits de máquina, batidas de metal e régua.
- **Serve para**: manifestos curtos, regras ("três regras de segurança"), contraste entre dois lados (nuvem x on-premise), conceitos de política.
- **Difícil no raea**: é 2D com HTML/CSS e `clip-path`, fácil de fazer; o desafio é parecer diferente do "abstrato com brilho": sem Bloom, sem fundo escuro, sem gradiente. Formas em chapa e cores fixas.
- **Risco**: seguro.

## 27. Vitral

- **Cena**: painel de vidro colorido com chumbo preto entre os cacos, luz atravessando e projetando cores no chão; a imagem principal é desenhada em peças de vidro, a luz se move durante o vídeo.
- **Paleta**: #1b1b1e (chumbo), #d00000 (vermelho), #0077b6 (azul), #ffba08 (âmbar), #2d6a4f (verde).
- **Tipografia**: gótica ou serifada de manuscrito, por exemplo UnifrakturCook ou Cinzel, em faixa do vitral.
- **Câmera**: frontal com leve pan; luz passando; close em um caco que acende.
- **Trilha**: coral sintético e órgão, sino; reverberação de catedral, passos em pedra.
- **Serve para**: conceitos "sagrados" de TI (chave raiz, certificado, a CA), mitos fundadores (história do Unix), ritual de deploy como sátira.
- **Difícil no raea**: vidro com transmissão é caro; mais simples fazer em 2D: polígonos SVG com preenchimento translúcido e `mix-blend-mode`, luz como gradiente animado por trás. Projeção no chão em 3D com `SpotLight` e `Decal` colorido.
- **Risco**: médio.

## 28. Origami

- **Cena**: figuras de papel dobrado (grou, barco, caixa) sobre mesa clara; dobras aparecendo, facetas com sombra, uma figura que se desdobra para revelar outra.
- **Paleta**: #fefae0 (papel), #bc4749 (vermelho), #386641 (verde), #274c77 (azul), #f2cc8f (areia).
- **Tipografia**: sans minimalista, por exemplo Noto Sans JP ou Zen Kaku Gothic, em linhas pequenas.
- **Câmera**: aérea próxima e lenta; giro leve ao redor da dobra; foco raso.
- **Trilha**: koto ou piano suave, silêncio entre notas; papel dobrando, vinco e vento leve.
- **Serve para**: transformação de dados (encapsulamento, criptografia em camadas), "dobra" de protocolo, empacotar/desempacotar.
- **Difícil no raea**: facetas por `BufferMesh` ou `Plane3d` rotacionados com pivô na aresta; dobras animadas por ângulo. Cada figura precisa ser desenhada com cuidado, então começar com caixa e barco simples. `allowOverlap` para facetas que se encostam.
- **Risco**: ousado.

## 29. Neon de letreiro com chuva

- **Cena**: letreiro de neon em tubos de cor sobre parede de tijolo molhada, chuva diagonal, reflexo rosa e azul no chão, fumaça de bueiro.
- **Paleta**: #090611 (noite), #ff2e97 (rosa neon), #00e5ff (ciano neon), #ffe66d (amarelo), #3a0ca3 (roxo).
- **Tipografia**: letra de neon em script ou tubo, por exemplo Monoton ou Tilt Neon; texto curto.
- **Câmera**: travelling lateral com pequena aproximação; letreiro piscando como ritmo.
- **Trilha**: synthwave lento com baixo, pad; zumbido de neon, chuva, relâmpago distante e estalo elétrico.
- **Serve para**: temas de rede e conexão (ping, online/offline), cultura hacker, apresentações curtas de "ataque em andamento".
- **Difícil no raea**: tubos como `Cylinder`/`Torus` emissivos com `Bloom`; texto em tubo exige desenhar letras com segmentos (ou `Text3D` extrudado emissivo). Chuva em `Instances`. Parente próximo do "abstrato com brilho": só usar se o cenário tiver tijolo, chão molhado e objetos além do letreiro.
- **Risco**: médio.

## 30. Mapa de metrô

- **Cena**: diagrama de linhas coloridas com ângulos de 45 e 90 graus, estações como círculos e traços, trens como pontos que percorrem a linha; o fluxo do dado ou da dependência vira trajeto.
- **Paleta**: #ffffff (fundo), #e63946 (linha vermelha), #1d70b8 (linha azul), #2a9d4f (linha verde), #f4a300 (linha amarela).
- **Tipografia**: sans neutra de sinalização, por exemplo Inter ou Public Sans, em peso médio, rótulos horizontais.
- **Câmera**: 2D com pan seguindo o trem; trem como ponto guia; sem perspectiva.
- **Trilha**: eletrônica leve e rítmica, piano curto; anúncio de estação (sem voz clonada), portas fechando, trilho e freio.
- **Serve para**: roteamento, dependências entre serviços, pipeline com estágios, histórico de versões, "baldeação" entre sistemas.
- **Difícil no raea**: puro 2D (SVG ou HTML) com animação de `stroke-dashoffset` e pontos seguindo o caminho; o 3D não ajuda aqui. Garantir espaço para o texto e linhas separadas por pelo menos 24 px.
- **Risco**: seguro.

---

## Fontes

- https://en.wikipedia.org/wiki/Cutout_animation (traços de animação com recortes: papel, silhueta, articulação por pinos)
- Buscas web de apoio (resultados lidos, páginas não abertas): panorama de estilos de animação, características de cutout, características de risografia (grão, sobreposição, desalinhamento). Não citadas como fonte por não terem sido abertas.
- Recursos do raea conferidos localmente: /home/celo/.claude/skills/raea/SKILL.md, /home/celo/.claude/skills/raea/3d/limits.md, /home/celo/.claude/skills/raea/3d/post.md, /home/celo/.claude/skills/raea/reference/sdk.md
