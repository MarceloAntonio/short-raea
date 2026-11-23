# Movimento: informação nova, não pipoca

Este guia diz como as coisas se mexem num Short vertical 1080x1920 feito no raea. Leia na fase 2, ao escolher a estética (a seção 5 diz como cada uma entra, troca de cena e move a câmera), e na fase 4, ao animar (seções 1 a 4, 6 e 7). O problema que ele resolve: em todos os vídeos havia zoom e elementos crescendo o tempo todo para a tela não parecer parada. Isso cansa, esconde a história e não conta como mudança. Mudança é informação nova.

## Índice

1. [A regra](#1-a-regra)
2. [Orçamento de ênfase](#2-orçamento-de-ênfase)
3. [Vocabulário de movimentos](#3-vocabulário-de-movimentos)
4. [Câmera que conta a história](#4-câmera-que-conta-a-história)
5. [Movimento por estética](#5-movimento-por-estética)
6. [Pipoca: o que não vira padrão](#6-pipoca-o-que-não-vira-padrão)
7. [Tela parada sem pipoca](#7-tela-parada-sem-pipoca)

## 1. A regra

"Mudar algo a cada 2 a 4 s" quer dizer que o espectador recebe uma informação que não tinha.

Conta como mudança:
- um elemento novo entra no quadro;
- um personagem faz uma ação (pega, empurra, abre, quebra);
- a cena muda (corte, outro cenário, outro painel);
- a câmera revela outra parte do cenário;
- um texto novo aparece (título, rótulo, linha de terminal);
- a cor ou a luz muda com a história (verde vira vermelho, a sala apaga).

Não conta como mudança:
- zoom ou punch-in;
- escala que cresce ou encolhe;
- pop (spring de 0 para 1) como único movimento;
- pulso, respiração, brilho oscilando;
- tremida de câmera sem impacto na história.

Teste rápido: pause em dois instantes com 3 s de distância. Se a diferença entre eles for só tamanho, é pipoca. Se der para dizer "agora há X que não havia", é mudança.

## 2. Orçamento de ênfase

Por vídeo de 30 a 40 s:

- no máximo 2 punch-ins/zooms de câmera, só no gancho e na virada;
- no máximo 3 elementos com entrada em escala (pop/spring de 0 para 1), só nos momentos-chave (o problema, a virada, o CTA);
- nenhum elemento que já está na tela pulsa, respira ou cresce para chamar atenção;
- tremida de câmera só no impacto principal, uma vez.

O resto entra com movimentos que fazem sentido na cena: deslizar, cair, ser colocado por alguém, abrir, acender, desenhar, revelar por trás de algo, corte seco.

### Como marcar no roteiro.json

Cada passo declara o movimento:

```json
"movimento": {
  "entra": "papel desliza da direita",
  "como": "interpolate em x com easing out",
  "camera": "travelling lateral lento",
  "enfases": [
    {"tipo": "zoom", "enfase": true, "em": {"palavra": "caiu"}, "alvo": "camera"}
  ]
}
```

- `entra`: o que chega no passo e de que jeito (vocabulário da seção 3).
- `como`: a técnica no raea, em uma linha.
- `camera`: o movimento de câmera do passo (seção 4).
- `enfases`: lista de ênfases gastas no passo. Cada item tem `tipo`, `enfase: true`, `em.palavra` (a palavra da narração que dispara) e `alvo` (o elemento ou a câmera).

Tipos aceitos: `zoom`, `pop`, `tremida`, `pulso`.
- `pulso` tem orçamento 0. Não use.
- `zoom` só nos passos gancho e virada.
- `pop` no máximo 3 no vídeo, nos passos do problema, da virada e do CTA.
- `tremida` uma vez, no impacto principal.

Entrada que não é ênfase (deslizar, cair, desenhar) não entra na lista `enfases`, só em `entra` e `como`.

### Conferência

```
scripts/contar-enfases.py roteiro.json components/
```

O script soma as ênfases declaradas no roteiro por tipo, reprova passo sem `movimento`, zoom fora do gancho e da virada e qualquer tipo acima do orçamento. Depois procura no código (`components/**/*.tsx`) escala com valor calculado (`scale(${e})`, `withScale([e, e, e])`, `scale: e`), `fov` ou zoom animado e usos de `pulso()`/`soco()` ou `cameraPorPasso()` com força, e lista arquivo e linha de cada um. Pulso no código reprova; mais de 6 linhas de escala animada (2 + 3 + 1) também. A busca é heurística: confira a lista, e se um item for falso positivo (um helper genérico, uma escala fixa), anote no `AGENTS.md` do projeto. O `verificar.sh` roda o script junto com as outras checagens.

## 3. Vocabulário de movimentos

Escolha pela cena, não pelo hábito. Varie: dois passos seguidos não entram do mesmo jeito.

| Movimento | Quando usar | Como no raea |
|---|---|---|
| Deslizar | peça, painel ou etiqueta que chega de fora do quadro | `interpolate` na posição (x ou y) com `Easing.out` |
| Cair | objeto que despenca ou é largado, erro, peça que encaixa | queda com gravidade (posição quadrática no tempo), pouso com um pequeno rebote só se o objeto for pesado |
| Ser colocado | alguém traz o elemento: mão, personagem, braço | grupo da mão ou do personagem anda até o ponto, solta, e sai; o objeto só aparece ao ser solto |
| Desenhar | linha, rota, diagrama, assinatura | `strokeDashoffset` no SVG ou largura que cresce num `Cuboid` fino |
| Revelar por trás | informação escondida, segredo, causa do problema | o objeto da frente sai do caminho, ou máscara/`clip-path` que abre |
| Acender | algo liga, passa a funcionar, falha | cor ou `emissive` que muda no quadro certo; janela, LED, barra |
| Apagar | queda de serviço, perda, fim | mesma técnica de acender ao contrário, com a luz ambiente caindo junto |
| Corte seco | troca de cena, de painel, de ângulo | troca de componente no quadro da deixa da palavra, sem transição |
| Digitar | comando, log, diálogo, título de terminal | texto que cresce letra a letra (`slice` do texto pelo quadro), cursor fixo |
| Dobrar/desdobrar | origami, caixa, papel, camadas que se fecham | rotação em torno de uma aresta, com o pivô num `group` posicionado na aresta |
| Abrir | porta, tampa, cortina, gaveta | porta ou tampa girando no eixo da dobradiça; cortina deslizando em x |
| Virar página | passo seguinte numa ficha, caderno ou mapa | folha que gira em torno da lombada, com a seguinte já embaixo |
| Encher | nível, fila, barra de carga, tanque | altura de um `Cuboid` ou `Cylinder` que sobe, ancorado pela base |
| Seguir | acompanhar um pacote, trem, peão ou personagem | câmera presa ao objeto com deslocamento fixo, ou o mundo andando para trás dele |
| Deslizar em fila | lista, etapas de pipeline, itens que chegam em ordem | um `interpolate` com atraso fixo por índice, todos na mesma direção |

Regras de uso:
- Todo movimento tem origem e destino. Se o elemento sai do nada, é pop.
- Peso combina com duração: objeto pesado cai rápido e para seco; papel leve desliza devagar.
- Easing de saída (rápido no começo, suave no fim) para entradas; easing de entrada para saídas.
- Rebote e overshoot só quando o objeto de verdade quicaria.

## 4. Câmera que conta a história

A câmera mostra algo. Se ela se mexe, é porque tem algo novo para revelar.

- **Travelling**: a câmera anda de lado ou para frente ao longo do cenário. Cada metro percorrido revela uma peça nova. Bom para fluxos, pipelines, rotas.
- **Órbita lenta**: 15 a 30 graus ao redor do objeto durante o passo inteiro. Revela o lado de trás, onde está o defeito. Bom para objeto único (servidor, caixa, maquete).
- **Plano-sequência que segue um objeto**: a câmera fica presa a um pacote, trem ou personagem e o cenário passa. Substitui vários cortes e vários zooms.
- **Plano parado de 2 a 3 s com ação no quadro**: permitido. Câmera fixa, mas algo entra, cai, acende ou é digitado. A ação precisa ser grande o bastante (seção 7).
- **Corte**: para trocar de lugar ou de escala, corte seco, nunca zoom curto.
- **Quando um zoom do orçamento vale**: no gancho, para entrar no problema; na virada, para mostrar o detalhe que muda tudo. Dois no máximo, e cada um com a palavra que o dispara registrada em `enfases`.
- **Tremida**: uma vez, no impacto principal (o servidor cai, a porta arromba). Curta, de 0,3 a 0,5 s, que decai.

Movimento contínuo e lento vence zoom curto repetido. Se a câmera precisa de energia, aumente a velocidade do travelling, não a quantidade de zooms.

## 5. Movimento por estética

Mesmos números e nomes do catálogo em `esteticas.md`.

### 1. Abstrato com brilho (seguro)

**Entra:** blocos deslizam do escuro e acendem (`emissive` sobe); linhas de luz se desenham entre eles. Nada de pop em cada cubo.
**Troca de cena:** a luz muda de cor com a história (ciano para vermelho) e a câmera chega a outro conjunto de formas.
**Câmera:** órbita lenta ou dolly contínuo para frente, com leve balanço; sem punch-in repetido.

### 2. Papel recortado (papercraft)

**Entra:** recortes deslizam por cima das camadas, dobram de uma aresta ou são colocados por uma mão; a camada da frente sai e revela a de trás.
**Troca de cena:** a folha da frente é puxada para o lado e a seguinte já estava embaixo.
**Câmera:** travelling lateral lento com avanço leve em Z; o parallax entre camadas é o movimento.

### 3. Massinha (claymation)

**Entra:** o personagem é esticado para o quadro ou amassado numa forma; objetos são colocados por uma mão de massinha, em 12 fps.
**Troca de cena:** a massa se desfaz e se refaz no próximo cenário, ou corte seco com o fundo de papelão igual.
**Câmera:** quase fixa, em degraus de 12 fps; close nos olhos só no gancho ou na virada.

### 4. Miniatura com tilt-shift

**Entra:** carrinhos e peças andam pelas ruas vindos da borda; prédios acendem janela por janela.
**Troca de cena:** a câmera paira para outro bairro do mesmo mapa, ou a faixa nítida (foco) muda de ponto.
**Câmera:** voo alto e lento lateral, descendo aos poucos; rack focus em vez de zoom.

### 5. Planta técnica azul (blueprint)

**Entra:** as linhas se desenham (`strokeDashoffset`), cotas crescem a partir de um ponto e legendas aparecem em caixas já posicionadas.
**Troca de cena:** a folha é desenhada por cima ou o desenho é varrido por uma linha de apagar e uma nova planta é traçada.
**Câmera:** mesa de desenho: pan lento lateral; zoom em detalhe só se for um dos 2 do orçamento.

### 6. Terminal CRT âmbar

**Entra:** o texto é digitado letra a letra; blocos novos chegam com uma interferência curta de linha de varredura.
**Troca de cena:** corte seco com estática de 3 a 4 quadros, ou a tela rola para a próxima tela de terminal.
**Câmera:** plano fixo na tela, corte para o plano aberto do monitor; tremor mínimo só no impacto.

### 7. Pixel art isométrico

**Entra:** blocos descem em passos inteiros de pixel e encaixam; personagens andam pela sala em passos discretos.
**Troca de cena:** a câmera pula por corte para outra sala ou outro andar, em passos de pixel.
**Câmera:** isométrica fixa, deslocamento em degraus; zoom só por corte.

### 8. Risografia com 2 cores

**Entra:** cada chapa entra separada: primeiro a rosa, depois a azul, com 3 a 6 px de desalinhamento que se ajusta.
**Troca de cena:** a página passa de novo pela máquina: chapas saem para um lado, as novas entram do outro.
**Câmera:** praticamente nenhuma; cortes secos e pequenas translações das chapas.

### 9. Quadrinho com balões

**Entra:** painéis entram por corte ou deslizando em ordem de leitura; balões aparecem já no lugar, digitados ou revelados por máscara; a onomatopeia só entra com pop no impacto principal.
**Troca de cena:** corte entre painéis, como página de quadrinho; no máximo uma página virando.
**Câmera:** o corte entre painéis é a câmera; tremor só no impacto principal.

### 10. Noir em preto e branco com uma cor

**Entra:** a luz das persianas varre a sala e revela o objeto; o elemento colorido acende devagar, sem pop.
**Troca de cena:** fusão pelo escuro (a luz apaga e acende em outro lugar) ou corte seco para o close.
**Câmera:** dolly baixo e lento com ângulo inclinado; corte para close em objeto em vez de zoom.

### 11. Brinquedo de plástico de montar

**Entra:** as peças caem do alto e encaixam com um pequeno pouso, ou uma mão as coloca uma a uma; a construção cresce por peças e não por escala.
**Troca de cena:** a construção é levada para fora e entra outra na mesma placa base.
**Câmera:** órbita leve em torno da montagem; câmera baixa seguindo a peça que cai.

### 12. Maquete de isopor

**Entra:** blocos de isopor são colocados na maquete por uma mão ou descem e encostam; alfinetes são fincados nos pontos.
**Troca de cena:** a maquete é girada para outra face, ou a câmera passa por cima e desce para outra rua.
**Câmera:** aérea lenta descendo para plano baixo entre os prédios; luz lateral fixa.

### 13. Tabuleiro de jogo

**Entra:** peões andam casa por casa; cartas viram; o dado cai e rola até parar.
**Troca de cena:** a câmera segue o peão até a casa de "revés" e o evento aparece ali; corte para outro trecho do tabuleiro.
**Câmera:** zenital que inclina para perspectiva, seguindo o peão; close no dado só quando cai.

### 14. Mapa de cartografia antiga

**Entra:** a rota se desenha pontilhada (`stroke-dasharray`); ilhas e monstros aparecem ao serem tocados pela rota; a legenda é escrita à pena.
**Troca de cena:** o pergaminho rola para outra região do mapa.
**Câmera:** travelling sobre o mapa quase zenital, rolagem lateral; zoom em ilha só como um dos 2 do orçamento.

### 15. Interface de videogame retrô

**Entra:** caixas de diálogo digitam o texto; barras de vida descem ou enchem; menus abrem por cima.
**Troca de cena:** corte seco para outra tela ("fase 2"), com título da fase digitado.
**Câmera:** plano fixo de tela de jogo; tremor curto só no dano principal.

### 16. Ficha de laboratório

**Entra:** a caneta escreve os campos (`clip-path` ou `strokeDashoffset`); o carimbo cai de cima e bate (um dos 3 pops permitidos, no resultado).
**Troca de cena:** a ficha é virada, ou outra ficha é colocada por cima da mesa.
**Câmera:** zenital sobre a mesa, deslocamento de campo para campo; zoom no carimbo só se for um dos 2 do orçamento.

### 17. Embalagem de produto

**Entra:** a caixa chega girando na mesa; a tampa abre em torno da aresta; o item sobe de dentro; selos são colados.
**Troca de cena:** uma caixa sai, outra entra; ou a caixa abre e a câmera entra no conteúdo por corte.
**Câmera:** órbita de produto em luz de estúdio; a abertura da tampa é filmada de perto sem zoom.

### 18. Teatro de bonecos

**Entra:** bonecos descem presos aos fios; cenários deslizam pelos trilhos; a cortina abre.
**Troca de cena:** a cortina fecha e abre no ato seguinte, ou o painel do cenário é trocado à vista.
**Câmera:** plano frontal de plateia, quase parado; corte para bastidores.

### 19. Sonho surreal

**Entra:** objetos flutuam para o quadro com lentidão e param no lugar; a porta se abre sozinha; letras se soltam do céu.
**Troca de cena:** corte para escala maior (a escada vira a cidade) ou o céu muda de cor com a história.
**Câmera:** dolly lento e contínuo, como flutuando.

### 20. Tipografia gigante que vira cenário

**Entra:** a letra já está lá; a câmera chega a ela. Letras novas são derrubadas ou deslizam como vigas.
**Troca de cena:** a câmera atravessa a letra e sai em outra palavra, ou corte seco de uma palavra para a seguinte.
**Câmera:** avanço contínuo atravessando as letras; é o travelling que faz o trabalho, sem zooms.

### 21. Raio-X

**Entra:** a varredura passa de cima para baixo e revela o interior; a anomalia acende em vermelho; rótulos se desenham com linha de chamada.
**Troca de cena:** nova varredura sobre outro objeto, ou a varredura muda de camada.
**Câmera:** plano fixo de exame com leve deslocamento lateral; zoom na anomalia só na virada.

### 22. Aquário

**Entra:** peixes nadam para o quadro em curvas; bolhas sobem; a criatura grande passa ao fundo.
**Troca de cena:** a câmera desliza pelo vidro para outro trecho do aquário; a luz da superfície muda de cor.
**Câmera:** deslizar lento ao longo do vidro com foco raso; rack focus entre peixes.

### 23. Cozinha: o problema como receita

**Entra:** ingredientes são colocados na bancada por uma mão; a faca corta; a panela é posta no fogo e o vapor sobe.
**Troca de cena:** a câmera corre pela bancada até a próxima etapa; o forno abre e mostra o resultado.
**Câmera:** zenital com travelling lateral entre etapas; close na panela por corte.

### 24. Diorama low-poly de escritório

**Entra:** pessoas entram pela porta e andam até a mesa; monitores acendem; post-its são colados.
**Troca de cena:** a câmera orbita até outro canto da caixa cortada, ou a luz da janela muda do dia para a noite.
**Câmera:** órbita lenta de 20 a 30 graus ao redor da caixa; aproximação em detalhe só como um dos 2 zooms.

### 25. Rua noturna cinematográfica

**Entra:** o objeto de destaque é deixado na calçada por alguém; os faróis varrem a rua; janelas acendem ao fundo.
**Troca de cena:** a luz de um poste apaga e a de outro acende, levando o olhar a outro ponto; corte para o plano de reflexo.
**Câmera:** dolly lento ao nível do chão; rack focus entre objeto e fundo.

### 26. Bauhaus e construtivismo

**Entra:** barras e formas deslizam em diagonal e se encaixam; faixas de texto entram de uma borda; sem escala.
**Troca de cena:** corte seco, com blocos que saem na diagonal e outros que entram.
**Câmera:** 2D com deslocamentos em diagonal; rotação de 15 graus em blocos, no corte.

### 27. Vitral

**Entra:** cada caco de vidro acende em sequência conforme a luz passa; a faixa de texto é revelada por máscara.
**Troca de cena:** a luz muda de lugar e outro painel acende; corte seco para o painel seguinte.
**Câmera:** frontal com leve pan; a luz que passa é o movimento principal.

### 28. Origami

**Entra:** a folha lisa é dobrada passo a passo até virar a figura; facetas giram em torno da aresta.
**Troca de cena:** a figura se desdobra e revela outra por baixo.
**Câmera:** aérea próxima e lenta com giro leve em torno da dobra; foco raso.

### 29. Neon de letreiro com chuva

**Entra:** os tubos acendem um a um, com falha curta de tensão e depois estáveis; a chuva já está caindo.
**Troca de cena:** o letreiro apaga e outro acende (outra cor); relâmpago como corte para outra parede.
**Câmera:** travelling lateral pela parede, passando de letreiro em letreiro.

### 30. Mapa de metrô

**Entra:** as linhas se desenham de estação em estação; estações acendem ao serem alcançadas; o trem percorre o trajeto.
**Troca de cena:** a câmera segue o trem até outra linha (baldeação) ou corte seco para outro trecho do mapa.
**Câmera:** 2D com pan acompanhando o trem; zoom em estação só se for um dos 2 do orçamento.

## 6. Pipoca: o que não vira padrão

| Evitar | No lugar |
|---|---|
| Zoom a cada efeito sonoro | O som acompanha uma ação: algo cai, abre, acende. O efeito marca o evento, a câmera não se mexe. |
| Pop em cada palavra ou ícone | O ícone entra deslizando ou sendo colocado. Pop só nos 3 momentos-chave. |
| Escala "respirando" em loop | Elemento parado fica parado. Se precisa de vida, uma luz que varre ou uma peça pequena que se move de verdade. |
| Pulso no ritmo da música | A música fica no áudio. O visual segue a história, não o beat. Pulso tem orçamento 0. |
| Tremida em toda batida | Uma tremida, no impacto principal. Nas outras batidas, corte seco ou luz que muda. |
| Tudo entrando do mesmo jeito | Varie por tipo: o que é pesado cai, o que é leve desliza, o que é texto digita, o que é luz acende. |
| Bounce e overshoot em tudo | Easing de saída simples. Rebote só em objeto que quicaria de verdade. |
| Punch-in em todo passo | Travelling ou órbita contínua no passo inteiro. Para trocar de ponto, corte. |
| "Soco" de câmera em cada sfx | Deixe a câmera quieta e ponha a ação no quadro (porta que bate, peça que cai). O som se apoia nela. |
| Número ou barra que cresce de escala | Barra que enche pela base (`Encher`); número que muda por troca de dígitos, sem crescer. |

## 7. Tela parada sem pipoca

O `verificar.sh` acusa "tela parada" quando passam mais de 3 s sem quadro com mudança de cena maior que 0,02 (scene do ffmpeg). Animação suave de um objeto pequeno fica abaixo desse limiar. Um personagem pequeno que anda, uma luz que oscila ou um ícone que desliza não bastam.

A correção é acrescentar informação nova e grande o bastante: um elemento novo que entra, uma faixa de texto, a cena que muda, a luz que muda. Nunca um zoom ou um pulso, que além de pipoca também gastam o orçamento.

Jeitos de resolver, do mais barato ao mais caro:

1. **Faixa de texto nova**: uma linha com o dado do passo (número, nome do erro, comando) que entra deslizando de uma borda e ocupa uma faixa larga.
2. **Elemento novo e grande**: uma peça que chega ao quadro (painel, caixa, personagem) e ocupa área relevante.
3. **Mudança de luz**: a cor de fundo ou da iluminação muda com a história (azul para vermelho, sala que apaga). Muda o quadro inteiro.
4. **Corte seco para outro plano**: outro ângulo do mesmo cenário ou outro cenário, no quadro de uma deixa da narração.
5. **Câmera que revela**: travelling que passa a mostrar outra parte do cenário; a área nova entra em quadro.
6. **Troca do conteúdo da tela interna**: o terminal, o painel ou o monitor mostra outra tela (a tela inteira, não uma linha).
7. **Transição de cenário**: a cortina, a folha ou a camada da frente sai e revela a próxima.
8. **Fundo que muda de região**: a faixa de fundo (chão, parede, céu) troca de cor ou textura em bloco, junto com a virada.

Depois de ajustar, rode o `verificar.sh` de novo. Se ainda acusar, o elemento novo era pequeno demais: aumente a área, não a velocidade.
