---
name: short-raea
description: Cria Shorts verticais (Reels, TikTok, YouTube Shorts) chamativos, feitos para reter e ganhar views, renderizados com o raea em 3D, com narração ElevenLabs, sons e músicas do Freesound, legendas por palavra e CTA no padrão da marca. Pergunta o tema primeiro, propõe 5 conceitos fora do óbvio e nunca repete o formato do vídeo anterior (histórico em ~/.claude/skills/short-raea/historico/HISTORICO-SHORTS.md). Use sempre que o usuário pedir um short, reels, vídeo vertical, vídeo pro Insta ou TikTok, vídeo "pra viralizar" ou "pegar view", vídeo explicativo de marca ou serviço, ou digitar /short-raea, mesmo que não cite o raea.
---

# Short chamativo com raea

Você vai fazer um vídeo vertical 1080x1920 que prende a atenção nos primeiros segundos e não se parece com o vídeo anterior. O que separa um short que viraliza de um genérico é a ideia, não a técnica; por isso a maior parte deste processo é decidir **o que** fazer antes de abrir o raea. Responda em português.

Detalhes técnicos (chaves, endpoints, armadilhas do raea, Windows, vários idiomas, comandos de verificação e entrega) estão em `references/tecnico.md`; leia antes da fase 4. Ideias de formato e a lista de clichês estão em `references/conceitos.md`; leia na fase 2. Capa, legenda e hashtags estão em `references/publicacao.md`, e o jeito de escrever a legenda (tom brasileiro, estrutura, checklist) em `references/legenda.md`; leia os dois na fase 5.

## Fase 1. Perguntar

Faça um **grill me** com a ferramenta `AskUserQuestion`, nunca com uma lista de perguntas no chat. Sem estas respostas, qualquer conceito é chute.

- Mande no máximo 4 perguntas por chamada, cada uma com 2 a 4 opções concretas tiradas do que você já sabe (argumentos, histórico, workspace). Marque a melhor opção com "(Recomendado)" e coloque-a em primeiro. O "Outro" já vem pronto e serve para respostas livres (@, site, comando de instalação).
- Faça quantas rodadas forem precisas. Use cada resposta para afinar a rodada seguinte, insista quando a resposta for vaga e só avance para a fase 2 quando os 7 itens estiverem respondidos.
- Não pergunte o que os argumentos ou o workspace já respondem; diga em uma linha o que foi deduzido.

1. **Tema**: sobre o que é o vídeo?
2. **Marca**: de quem é? Site (para cores e fontes) e onde estão os logos.
3. **Objetivo**: o que a pessoa deve fazer no fim? (seguir, comentar, enviar, salvar, chamar no WhatsApp). Escolha **uma** ação principal e construa o vídeo para ela: perfil pequeno precisa primeiro de seguidor e comentário, não de venda.
4. **Público**: quem assiste? (dono de empresa leigo, dev, estudante...)
5. **Fatos**: quais números, selos e promessas posso afirmar? O que não estiver nessa lista não entra: um dado inventado num vídeo de marca vira problema real para o cliente.
6. **Duração**: o padrão é 30 a 40 s, nunca mais de 60 s. O vídeo da Graal de 63 s teve tempo médio de 24 s: só 1 em cada 3 pessoas chegou à virada (`references/publicacao.md`, seção 6).
7. **CTA**: o texto exato do fechamento (@, site, WhatsApp, "link na bio").

Se a marca já tem projeto num workspace do raea (`~/Documentos/raea/`), leia o `brief.ts` e o `AGENTS.md` dele e pergunte só o que faltar.

## Fase 2. Conceito, sem repetir o anterior

1. Leia `~/.claude/skills/short-raea/historico/HISTORICO-SHORTS.md` (crie com o cabeçalho de tabela se não existir). O vídeo novo precisa diferir do último em pelo menos 4 das 7 colunas: conceito, formato, câmera, gancho, final, paleta e trilha. Quem segue a mesma página vê o mesmo vídeo com outro texto e passa direto.
2. Leia `references/conceitos.md` e gere **5 conceitos**, cada um com um motor diferente (invente motores novos também). Para cada um: o gancho do primeiro 1,5 s, a imagem central, a virada e o final.
3. Dê nota de 1 a 5 a cada conceito em **surpresa** (já vi isso mil vezes?), **clareza** (um leigo entende sem som?) e **aderência ao tema**. Recomende um em duas linhas e **espere o usuário escolher**.

## Fase 3. Roteiro

1. Escreva a narração por passo: fala curta, português do Brasil coloquial, sem cara de anúncio. Mire em **80 a 110 palavras no total** (30 a 40 s). Nenhum passo passa de 8 s de fala: lista falada ("salário, encargos, férias, décimo terceiro…") é onde a retenção mais cai; troque a lista por uma frase de impacto e deixe a imagem mostrar o resto. Calcule o tempo (com o Liam a 1,15, são cerca de 3 palavras por segundo: 70 palavras dão uns 26 s e 120 dão uns 42 s, sem contar as pausas; medido em 17/11/2026). **Espere aprovação.**
2. Monte um `roteiro.json` que controla o vídeo inteiro: passos, narração, elementos, câmera, overlays, efeitos sonoros e CTA. Prenda cada acontecimento a uma **palavra da fala** (`{ "palavra": "cair" }`), não a segundos: assim, quando a voz muda, tudo continua no lugar.
3. Modelo de **estrutura** (não de conteúdo): `~/projetos/terceirizar-ti` (`roteiro.json`, `src/linhaDoTempo.ts`, `src/animacoes/`, `scripts/gerar-audio.ts`, `scripts/baixar-sons.ts`) e o porte para o raea em `~/Documentos/raea/graal/projects/terceirizar-ti` (no Windows, `~/projetos/graal/projects/terceirizar-ti`, que também tem `ferramentas/narrar.py` e `ferramentas/idiomas.py`). Copie o encanamento (linha do tempo, deixas por palavra, legendas, `emo()`, fontes); invente as cenas do zero.
4. Se o vídeo vai sair em mais de um idioma, escreva o roteiro já sabendo disso: deixas em palavras que existem nos outros idiomas e nenhuma palavra repetida na mesma fala (`references/tecnico.md`, seção 8).

## Fase 4. Produzir no raea

Siga a skill `raea` para workspace, projeto, `raea context .`, `brief.ts` e `plan.org`, e diga "Working in WORKSPACE / PROJECT". Depois, com `references/tecnico.md` aberto:

1. **Voz**: ElevenLabs (Liam) → MP3 por passo e `narracao.json` com o tempo de cada palavra.
2. **Sons e música**: Freesound CC0, escolhidos pela descrição e não pelo primeiro resultado, com os créditos anotados.
3. **Cena, overlays, legendas e CTA**, contornando as limitações do raea listadas na referência.
4. **CTA no padrão do site da marca**: leia o CSS do site (cores, fontes, raio, botões, espaçamento) e copie essa linguagem. Um fechamento genérico (logo brilhando, botão pílula com emoji) parece template e desvaloriza a marca.

## Fase 5. Verificar e entregar

Faça a verificação da referência: check rápido, folha de quadros-chave (olhe as imagens), render completo, medição de duração e loudness, volume de cada efeito contra a voz, e a cópia em AAC para WhatsApp e Instagram (o raea grava Opus, que eles recusam). Só diga que está pronto mostrando os números medidos.

Depois:
- Ofereça a **capa** (HTML com a cena 3D do vídeo de fundo, salva em `out/` ao lado do vídeo) e a **legenda com até 5 hashtags**, seguindo `references/legenda.md` e `references/publicacao.md`. A chamada da legenda é a mesma do fim do vídeo, nunca uma nova.
- Lembre o usuário de **escolher a capa** ao postar (o Reel da Graal saiu com a tela final do CTA de miniatura, e a grade ficou com cara de anúncio) e de **fixar um comentário** com a pergunta do vídeo.
- Peça os prints dos insights depois de 24 a 48 h e analise com a seção 6 de `references/publicacao.md`; registre o resultado no histórico.
- Acrescente a linha do vídeo ao `HISTORICO-SHORTS.md`; é ela que garante que o próximo será diferente.
- Apague renders intermediários e testes; ficam o original final e a cópia de entrega.
- Registre armadilhas novas na seção `## Regressões` do `AGENTS.md` do projeto.

## Fase 6. Rodadas de ajuste do cliente

O cliente quase sempre volta com uma lista ("mais peso no custo", "mostrar a certificação", "escritório com cara de empresa maior", "versão em inglês"). Para cada rodada:

1. **Planeje antes de mexer**: cada pedido vira uma tarefa no `plan.org`, com as suas palavras, e a resposta de cada um é uma mudança concreta (fala nova, overlay novo, peça nova). Fatos que entram no vídeo continuam vindo só da lista da fase 1; a certificação da Graal já estava confirmada no `roteiro.json` (`fatos`), por isso pôde ir para a fala.
2. **Mudança de visual grande (layout, cenário, personagem): mostre opções em imagem antes de refazer o vídeo.** Faça uma composição de prévia que desenha uma proposta por quadro (`--at 0,1,2,3,4`), com o título de cada uma, e entregue as imagens soltas e uma lado a lado. Use as peças do próprio vídeo, para a escolhida entrar sem retrabalho. Quando o usuário pedir variações de uma delas, faça outra rodada de 5 a partir dela.
3. **Mantenha as âncoras da história** ao trocar o cenário (`references/tecnico.md`, seção 9) e confira um quadro de cada cena que depende delas.
4. **Mexa só no que foi pedido.** "Só o layout" quer dizer roteiro, vozes e tempos intactos. Um defeito antigo que você encontrar no caminho (setas que não apareciam) pode ser corrigido junto, mas diga isso.
5. **Um render por vez** e um arquivo novo por versão (`-v6`, `-v7`); a versão anterior fica para comparar.
6. Feche cada rodada dizendo o que mudou, o que você conferiu nos quadros e o que só o usuário pode conferir (a pronúncia, por exemplo).

## Regras que valem o tempo todo

- **Engajamento (aprendido com os insights da Graal, 19/11/2026)**: o vídeo precisa **pedir** a ação que quer, dentro do vídeo e não só na legenda. Cada ação tem um gatilho próprio: comentário = pergunta com resposta de uma palavra ou número; envio = um momento "isso é a gente" que a pessoa manda para o chefe ou o sócio; salvamento = algo útil para guardar (checklist, conta, número); seguir = promessa de continuação (série, "parte 2"). A marca e a solução aparecem antes dos 20 s. O CTA final dura no máximo 2 a 3 s e emenda no loop. Detalhes em `references/publicacao.md`, seção 6.
- **Retenção**: conflito no primeiro 1,5 s; alguma mudança a cada 2 a 4 s; uma metáfora visual central que volta; a virada transforma a mesma imagem do problema; o último quadro encaixa no primeiro para o replay parecer contínuo.
- **Verdade**: só os fatos da fase 1; na dúvida, suavize ou pergunte. Em afirmação técnica (segurança, TI), pense no caso em que a pessoa já está protegida: "com a senha vazada, ele faz login" só vale para quem não tem verificação em duas etapas; o chefe do cliente apontou isso e a fala virou "sem verificação em duas etapas, ele faz login; com ela, ele usa seus dados pra te enganar". Um especialista que assiste comenta a lacuna; cubra os dois casos na fala. Logos só dos arquivos reais. Nada de imagem ou vídeo gerado por IA.
- **Segredos**: chaves só em `~/api/`, lidas para uma variável e enviadas só no cabeçalho do próprio serviço. Nunca imprima o conteúdo desses arquivos. Se a chave estiver em outro lugar, pergunte onde; não procure arquivos de chave pelo disco.
- **Você não ouve o áudio**: pronúncia, sotaque e mixagem fina são do usuário. Meça o que dá para medir (loudness, duração) e peça para ele ouvir o resto.
- **Versões**: cada render novo vira um arquivo novo (`-v2`, `-v3`), para dar para comparar e voltar.
