# Formato "construindo do zero" (Mas → Então)

Leia na fase 2, quando o tema é algo que se monta por partes (pôr um site no ar, montar uma rede, como surgiu o elevador, um servidor seguro), e na fase 3 ao escrever o roteiro. O usuário pediu esse formato pela primeira vez assim: "o entregador subiu 9 andares de escada; então faz um túnel, mas não dá pra subir; então uma caixa de metal, mas não tem o que puxar; então uma corda, mas a caixa bate; então a guia, mas como sabe onde parar? então o computador, e assim você tem um elevador."

## Por que funciona

Cada problema abre uma pergunta pequena ("e agora?") que a peça seguinte fecha. Quem assiste sente que entende o sistema inteiro no fim, porque viu ele nascer peça por peça. É ótimo para salvamento e para envio a quem acha que a coisa é simples.

## Estrutura

1. **Gancho**: a situação crua e o problema que dispara tudo, e já **plante a crença que o CTA vai desmontar** ("e pra ir pro ar não é só arrastar um arquivo"). Texto na tela: a pergunta + quantas peças ("SÓ FUNCIONA NO SEU PC? · 7 PEÇAS PRO AR").
2. **Peças**: cada passo é **"Mas [problema]. Então [peça]."** Uma peça por passo, sempre na ordem em que alguém de verdade montaria. Nunca "e aí".
3. **Final**: a coisa funcionando inteira, de uma vez ("Pronto: seu site tá no ar"), com uma imagem de clímax (os personagens atravessam todas as peças).
4. **CTA**: fecha a crença do gancho (envio: "manda pra quem acha que é só arrastar o arquivo"; salvamento: a cola das peças num cartão).

## Regras

- **Cada "Mas" precisa ser um problema real**, com fato conferido. Nada de problema inventado para ter mais peças.
- **Cubra quem já está protegido**: "Mas se o firewall tá ligado…" em vez de afirmar que está.
- **Peça nova = elemento novo que entra na cena** (desce, é colocado, encaixa), nunca só um rótulo.
- **Texto na tela em duas etiquetas**: o problema numa etiqueta escrita à mão, que é **riscada** no "Então", e a peça numa etiqueta de cor da marca ("PEÇA 4 · NGINX NA FRENTE"). Dá para acompanhar sem som.
- **Duração**: 6 a 8 peças cabem em 45 a 55 s. Esse formato aguenta passar dos 40 s, porque cada peça é um mini gancho; pergunte ou siga o pedido do usuário, e nunca passe de 60 s.
- **Câmera**: um plano por problema e outro pela peça, ligados por um **movimento suave e curto** (12 a 16 quadros, ease in-out), nunca corte seco (o usuário achou o corte seco brusco). O movimento rápido também conta como mudança no `verificar.sh`; um travelling lento não conta.
- **Etiqueta sempre na face que a câmera vê**: uma etiqueta colada atrás de uma peça some, e o plano parece "só um zoom" (aconteceu com o ":3000").

## Exemplo pronto

`~/Documentos/raea/dark/projects/site-no-ar` (maquete de isopor 3D, 7 peças, 48,8 s): `roteiro.json` mostra os passos "Mas/Então" com deixas em "mas" e "entao"; `components/Video.tsx` tem as peças entrando com `desce()`, a câmera com `planos()` e transição suave, e o `Topo` com a etiqueta riscada. Use como estrutura, não como cena: a estética muda a cada vídeo.
