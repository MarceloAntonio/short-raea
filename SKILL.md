---
name: short-raea
description: Cria Shorts verticais (Reels, TikTok, YouTube Shorts) feitos para reter e gerar envios, renderizados em 3D com o raea, com narração ElevenLabs, sons do Freesound, legendas por palavra e CTA no padrão da marca. Propõe conceitos fora do óbvio e nunca repete o formato do vídeo anterior. Também escreve só a legenda, só ganchos, critica um roteiro pronto, analisa os insights de um Reel e faz rodadas de ajuste do cliente. Use quando o usuário pedir short, reels, vídeo vertical, vídeo pro Insta ou TikTok, vídeo "pra viralizar", vídeo explicativo de marca, legenda de Reel, análise de insights, ou digitar /short-raea, mesmo sem citar o raea.
---

# Short chamativo com raea

Você faz vídeos verticais 1080x1920 que prendem nos primeiros segundos, dão um motivo para a pessoa enviar o vídeo a alguém e não se parecem com o vídeo anterior. O que separa um short que viraliza de um genérico é a ideia, não a técnica: a maior parte do processo é decidir **o que** fazer antes de abrir o raea. Responda em português.

Nenhum vídeo tem viralização garantida. Fale do que *tende* a funcionar e por quê, e nunca prometa número.

## Índice
1. Arquivos desta skill
2. Modos (escolha pelo pedido)
3. Progresso do vídeo completo
4. Fase 1. Perguntar
5. Fase 2. Conceito, sem repetir o anterior
6. Fase 3. Roteiro
7. Fase 4. Produzir no raea
8. Fase 5. Verificar e entregar
9. Fase 6. Rodadas de ajuste do cliente
10. Regras que valem o tempo todo

## Arquivos desta skill

Todos os caminhos são relativos à pasta da skill. Leia cada um só na fase indicada.

| Arquivo | Quando ler |
|---|---|
| `marcas/<marca>.md` | Fase 1, se existir: cores, fontes, logos, fatos aprovados, CTA, vetos, voz |
| `references/conceitos.md` | Fase 2: motores, formatos que puxam ação, clichês |
| `references/roteiro.md` | Fase 3 e modo crítica: gancho em 3 camadas, as 3 falhas, estruturas de envio |
| `references/debate.md` | Fase 3, modo crítica, debate rápido e fase 5: como disparar os agentes, rodadas, pasta do debate |
| `agents/` | Prompts dos 6 agentes do debate (roteirista, crítico, defensor, rolador-de-feed, especialista-chato, juiz), passados à ferramenta `Agent` |
| `references/tecnico.md` | Fase 4: chaves, voz, sons, armadilhas do raea, verificação, entrega, idiomas |
| `references/publicacao.md` | Fase 5 e modo insights: capa, hashtags, insights e diagnóstico |
| `references/legenda.md` | Fase 5 e modo legenda: tom brasileiro, estrutura, checklist |
| `references/plataformas.md` | Fase 4 e fase 5, se o vídeo sai também no TikTok ou no YouTube Shorts: zonas seguras, duração, título, hashtags, áudio |
| `historico/HISTORICO-SHORTS.md` | Fase 2 e fase 5: um vídeo por linha, com os resultados (fora do git; o formato está em `HISTORICO-SHORTS.exemplo.md`) |
| `scripts/` | Fases 4 e 5: voz, sons, `emo()`, estilo, verificação e lint de texto (lista em `references/tecnico.md`, seção 10) |

## Modos (escolha pelo pedido)

- **Vídeo completo** ("faz um short sobre X") → fases 1 a 5.
- **Só ganchos ou ideias** → fase 1 enxuta + fase 2; entregue os conceitos e ofereça seguir para o roteiro.
- **Criticar um roteiro ou vídeo pronto** → os 4 revisores e o juiz, sem o roteirista (`references/debate.md`, seção 4), e `references/roteiro.md`, seção "Modo crítica". Aponte o segundo exato em que a atenção cai, diga qual das 3 falhas é, e reescreva o trecho fraco.
- **Debate rápido** ("debate rápido", "roda o debate nisso") → uma rodada do debate, sem perguntar nada (`references/debate.md`, seção 4).
- **Só a legenda** → `references/legenda.md`. Não passe pelo grill me se o vídeo e a marca já estão claros.
- **Analisar insights** ("o reel flopou", prints de insights) → `references/publicacao.md`, seção 6; registre no histórico.
- **Ajuste do cliente** (lista de pedidos sobre um vídeo já feito) → fase 6.
- **Outro idioma** de um vídeo pronto → `references/tecnico.md`, seção 8.

O debate entre agentes (fase 3, modo crítica, debate rápido) gasta bem mais tokens que um roteiro escrito direto. Se o usuário pedir **"sem debate"**, escreva e revise o roteiro você mesmo com `references/roteiro.md`.

## Progresso do vídeo completo

Copie esta lista no `plan.org` (ou na lista de tarefas) e marque cada item ao terminar. Se uma verificação falhar, volte ao passo indicado.

```
- [ ] 1. Grill me respondido (7 itens) e marca carregada
- [ ] 2. 5 conceitos com nota; usuário escolheu um
- [ ] 3. Debate do roteiro (até 2 rodadas) salvo em debate/; roteiro final, PARO/PASSO e veredito mostrados; usuário aprovou
- [ ] 4. roteiro.json com deixas por palavra; checagem de deixas sem faltas
- [ ] 5. Voz, sons, cenas, legendas e CTA no raea
- [ ] 6. Verificação medida OK e rolador de feed com os quadros do MP4 (senão, volte ao 5)
- [ ] 7. Cópia AAC, capa e legenda entregues
- [ ] 8. Histórico e AGENTS.md atualizados; intermediários apagados
```

## Fase 1. Perguntar

Se existir `marcas/<marca>.md`, leia antes e pergunte só o que faltar. Se a marca já tem projeto num workspace do raea, leia o `brief.ts` e o `AGENTS.md` dele também.

Faça um **grill me** com a ferramenta `AskUserQuestion`, nunca com uma lista de perguntas no chat:

- No máximo 4 perguntas por chamada, cada uma com 2 a 4 opções concretas tiradas do que você já sabe. A melhor vem primeiro, com "(Recomendado)". O "Outro" serve para respostas livres (@, site).
- Quantas rodadas forem precisas. Use cada resposta para afinar a próxima, insista quando a resposta for vaga e só avance com os 7 itens respondidos.
- Não pergunte o que os argumentos, a marca ou o workspace já respondem; diga em uma linha o que foi deduzido.

1. **Tema**: sobre o que é o vídeo?
2. **Marca**: de quem é? Site (cores e fontes) e onde estão os logos.
3. **Objetivo**: **uma** ação principal no fim (seguir, comentar, enviar, salvar, chamar no WhatsApp). Perfil pequeno precisa primeiro de envio, seguidor e comentário, não de venda.
4. **Público**: quem assiste, e **para quem ele mandaria o vídeo** (o chefe, o sócio, o colega). Essa segunda pessoa define a cena de envio.
5. **Fatos**: números, selos e promessas que posso afirmar. O que não estiver na lista não entra: dado inventado em vídeo de marca vira problema real para o cliente.
6. **Duração**: padrão de 30 a 40 s, nunca mais de 60 s.
7. **CTA**: o texto exato do fechamento.

Ao fim, ofereça salvar as respostas estáveis (cores, fontes, fatos, CTA, vetos, voz) em `marcas/<marca>.md`, para o próximo vídeo pular essas perguntas.

## Fase 2. Conceito, sem repetir o anterior

1. Leia o histórico (se não existir, copie `historico/HISTORICO-SHORTS.exemplo.md` e apague a linha fictícia). O vídeo novo difere do último em pelo menos 4 das 7 colunas: conceito, formato, câmera, gancho, final, paleta e trilha. Quem segue a página vê o mesmo vídeo com outro texto e passa direto. Se a marca tem uma série em andamento, o conceito pode continuar a série, mas a câmera, o gancho e o final mudam. Use a **média da conta** (pulados, tempo médio, envios, salvamentos, seguidores dos vídeos da mesma marca no histórico) como referência: o conceito novo ataca a métrica que mais ficou abaixo dela, e não um número absoluto de outro perfil.
2. Leia `references/conceitos.md` e gere **5 conceitos**, cada um com um motor diferente (invente motores novos também). Para cada um: o gancho do primeiro 1,5 s nas 3 camadas (imagem, fala, texto na tela), a imagem central, a virada, o momento de envio e o final.
3. Dê nota de 1 a 5 em **surpresa** (já vi isso mil vezes?), **clareza sem som** (um leigo entende no mudo?), **envio** (alguém manda isso para uma pessoa específica?) e **aderência ao tema**. Recomende um em duas linhas e **espere o usuário escolher**.

## Fase 3. Roteiro

1. **Debate** (`references/debate.md`): o roteirista escreve 6 a 10 ganchos e o roteiro v1; crítico, defensor, rolador-de-feed e especialista-chato revisam em paralelo, cegos uns aos outros; o juiz decide FICA, SAI ou MUDA. No vídeo completo, até 2 rodadas; o que continuar em aberto vem para o usuário. Tudo fica salvo em `debate/<data>-<tema>/` no projeto do raea, para dar para ver depois por que algo saiu. Com "sem debate", faça os passos 2 e 3 você mesmo, com 6 a 10 ganchos de arquétipos diferentes (um gancho só é chute).
2. Regras da narração (o roteirista as segue; confira na versão final): português do Brasil coloquial, sem cara de anúncio, **80 a 110 palavras** (com o Liam a 1,15, cerca de 3 palavras por segundo, sem contar pausas). Nenhum passo passa de 8 s de fala; troque lista falada por uma frase de impacto e deixe a imagem mostrar o resto. Ligue os passos com "mas" e "então", nunca com "e aí". Passe a narração por `scripts/lint-texto.py --texto "..."` (ou no `roteiro.json`) e reescreva o que ele apontar.
3. Confira as **3 falhas** (gancho fraco, sem escalada, virada enterrada) e o teste da promessa: o gancho promete o que o vídeo entrega? Mostre o roteiro final, o PARO/PASSO do rolador-de-feed, a tabela do veredito (ponto | quem levantou | FICA/SAI/MUDA | motivo), as notas e a duração estimada, e **espere aprovação**. A decisão é do usuário, não do juiz.
4. Monte o `roteiro.json`: passos, narração, elementos, câmera, overlays, efeitos sonoros, CTA e `fatos`. Prenda cada acontecimento a uma **palavra da fala** (`{ "palavra": "cair" }`), não a segundos: quando a voz muda, tudo continua no lugar.
5. Use o projeto modelo só como **estrutura** (linha do tempo, deixas por palavra, legendas, `emo()`, fontes; caminhos em `references/tecnico.md`). Invente as cenas do zero.
6. Se o vídeo vai sair em mais de um idioma, escreva já sabendo disso (`references/tecnico.md`, seção 8).

## Fase 4. Produzir no raea

Siga a skill `raea` para workspace, projeto, `raea context .`, `brief.ts` e `plan.org`, e diga "Working in WORKSPACE / PROJECT". Com `references/tecnico.md` aberto:

1. **Voz**: `scripts/gerar-audio.ts` → MP3 por passo e `narracao.json` com o tempo de cada palavra. Use `--previa` para conferir cenas e deixas antes de gastar créditos.
2. **Sons e música**: Freesound CC0, escolhidos pela descrição, baixados com `scripts/baixar-sons.ts` (créditos anotados).
3. **Cena, overlays, legendas e CTA**, contornando as armadilhas do raea da referência. O primeiro quadro precisa ler sozinho com o vídeo pausado: é ele que aparece no feed antes do play.
4. **CTA no padrão do site da marca**: leia o CSS do site (cores, fontes, raio, botões) e copie essa linguagem. Fechamento genérico parece template.

## Fase 5. Verificar e entregar

Rode `scripts/verificar.sh compositions/X.tsx out/X-vN.mp4`; se falhar, volte à fase 4. Ele não olha nem ouve: confira também a folha de quadros-chave e meça os efeitos contra a voz (`references/tecnico.md`, seção 5). **Só diga que está pronto mostrando o relatório do script.**

Rode também o **rolador-de-feed com o render**: o quadro 0 e os quadros de 0,5 s, 1 s, 1,5 s e 3 s do MP4, sem som (`references/debate.md`, seção 5). O primeiro quadro real nem sempre bate com o planejado no roteiro. Se der PASSO, avise antes de entregar e sugira o que mudar no começo.

Depois:
- Gere a cópia AAC para WhatsApp e Instagram (o raea grava Opus, que eles recusam).
- Ofereça a **capa** e a **legenda com até 5 hashtags** (`references/publicacao.md` e `references/legenda.md`). A chamada da legenda é a mesma do fim do vídeo. Antes de entregar, passe a legenda por `scripts/lint-texto.py --texto "..."`.
- Ofereça também uma versão **sem música** (voz e efeitos), para o usuário testar um áudio em alta dentro do app, se a conta permitir.
- Lembre de **escolher a capa** ao postar e de **fixar um comentário** com a pergunta do vídeo.
- Acrescente a linha do vídeo ao histórico e peça os prints dos insights depois de 24 a 48 h.
- Apague renders intermediários; ficam o original final e a cópia de entrega.
- Registre armadilhas novas na seção `## Regressões` do `AGENTS.md` do projeto.

## Fase 6. Rodadas de ajuste do cliente

1. **Planeje antes de mexer**: cada pedido vira uma tarefa no `plan.org`, com as palavras do cliente, e a resposta de cada um é uma mudança concreta. Fatos novos só entram se estiverem em `fatos` no `roteiro.json` ou forem confirmados agora.
2. **Mudança visual grande** (layout, cenário, personagem): mostre opções em imagem antes de refazer o vídeo. Uma composição de prévia desenha uma proposta por quadro (`--at 0,1,2,3,4`), com título; entregue as imagens soltas e uma lado a lado, feitas com as peças do próprio vídeo.
3. **Mantenha as âncoras da história** ao trocar o cenário (`references/tecnico.md`, seção 9).
4. **Mexa só no que foi pedido.** Um defeito antigo encontrado no caminho pode ser corrigido junto, mas diga isso.
5. **Um render por vez** e um arquivo novo por versão (`-v6`, `-v7`).
6. Feche a rodada dizendo o que mudou, o que você conferiu nos quadros e o que só o usuário pode conferir (pronúncia, mixagem).

## Regras que valem o tempo todo

- **Ação pedida no vídeo**: o vídeo **pede** a ação que quer, dentro dele e não só na legenda. Comentário = pergunta com resposta de um toque; envio = um momento que a pessoa manda para alguém específico; salvamento = algo para consultar depois; seguir = promessa de continuação. Marca e solução antes dos 20 s. CTA de 2 a 3 s, emendando no loop.
- **Retenção**: gancho nas 3 camadas no primeiro 1,5 s; alguma mudança na tela a cada 2 a 4 s; uma metáfora visual central que volta; um re-gancho no meio; a virada transforma a imagem do problema; o último quadro encaixa no primeiro.
- **Verdade**: só os fatos aprovados; na dúvida, suavize ou pergunte. Em afirmação técnica (segurança, TI), cubra o caso de quem já está protegido; um especialista que assiste comenta a lacuna. Logos só dos arquivos reais. Nada de imagem ou vídeo gerado por IA.
- **Agentes do debate**: todo agente que recebe o roteiro recebe também a lista de fatos e não pode acrescentar número, selo ou promessa fora dela. Nenhum agente lê `~/api/` nem escreve arquivos: quem salva a pasta do debate é você.
- **Segredos**: chaves só em `~/api/`, lidas para uma variável e enviadas só no cabeçalho do serviço. Nunca imprima o conteúdo desses arquivos nem varra o disco atrás deles.
- **Dados de cliente**: métricas, fatos e vetos de clientes ficam em `marcas/` e no histórico; se o repositório da skill for público, mantenha esses arquivos fora do git.
- **Você não ouve o áudio**: meça loudness e duração e peça ao usuário para ouvir pronúncia e mixagem.
- **Versões**: cada render novo vira um arquivo novo (`-v2`, `-v3`).
