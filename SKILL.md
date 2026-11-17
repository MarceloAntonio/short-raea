---
name: short-raea
description: Cria Shorts verticais (Reels, TikTok, YouTube Shorts) chamativos, feitos para reter e ganhar views, renderizados com o raea em 3D, com narração ElevenLabs, sons e músicas do Freesound, legendas por palavra e CTA no padrão da marca. Pergunta o tema primeiro, propõe 5 conceitos fora do óbvio e nunca repete o formato do vídeo anterior (histórico em ~/.claude/skills/short-raea/historico/HISTORICO-SHORTS.md). Use sempre que o usuário pedir um short, reels, vídeo vertical, vídeo pro Insta ou TikTok, vídeo "pra viralizar" ou "pegar view", vídeo explicativo de marca ou serviço, ou digitar /short-raea, mesmo que não cite o raea.
---

# Short chamativo com raea

Você vai fazer um vídeo vertical 1080x1920 que prende a atenção nos primeiros segundos e não se parece com o vídeo anterior. O que separa um short que viraliza de um genérico é a ideia, não a técnica; por isso a maior parte deste processo é decidir **o que** fazer antes de abrir o raea. Responda em português.

Detalhes técnicos (chaves, endpoints, armadilhas do raea, comandos de verificação e entrega) estão em `references/tecnico.md`; leia antes da fase 4. Ideias de formato e a lista de clichês estão em `references/conceitos.md`; leia na fase 2.

## Fase 1. Perguntar

Faça um **grill me** com a ferramenta `AskUserQuestion`, nunca com uma lista de perguntas no chat. Sem estas respostas, qualquer conceito é chute.

- Mande no máximo 4 perguntas por chamada, cada uma com 2 a 4 opções concretas tiradas do que você já sabe (argumentos, histórico, workspace). Marque a melhor opção com "(Recomendado)" e coloque-a em primeiro. O "Outro" já vem pronto e serve para respostas livres (@, site, comando de instalação).
- Faça quantas rodadas forem precisas. Use cada resposta para afinar a rodada seguinte, insista quando a resposta for vaga e só avance para a fase 2 quando os 7 itens estiverem respondidos.
- Não pergunte o que os argumentos ou o workspace já respondem; diga em uma linha o que foi deduzido.

1. **Tema**: sobre o que é o vídeo?
2. **Marca**: de quem é? Site (para cores e fontes) e onde estão os logos.
3. **Objetivo**: o que a pessoa deve fazer ou pensar no fim? (seguir, chamar no WhatsApp, comentar, salvar)
4. **Público**: quem assiste? (dono de empresa leigo, dev, estudante...)
5. **Fatos**: quais números, selos e promessas posso afirmar? O que não estiver nessa lista não entra: um dado inventado num vídeo de marca vira problema real para o cliente.
6. **Duração**: o padrão é 30 a 55 s, nunca mais de 60 s.
7. **CTA**: o texto exato do fechamento (@, site, WhatsApp, "link na bio").

Se a marca já tem projeto num workspace do raea (`~/Documentos/raea/`), leia o `brief.ts` e o `AGENTS.md` dele e pergunte só o que faltar.

## Fase 2. Conceito, sem repetir o anterior

1. Leia `~/.claude/skills/short-raea/historico/HISTORICO-SHORTS.md` (crie com o cabeçalho de tabela se não existir). O vídeo novo precisa diferir do último em pelo menos 4 das 7 colunas: conceito, formato, câmera, gancho, final, paleta e trilha. Quem segue a mesma página vê o mesmo vídeo com outro texto e passa direto.
2. Leia `references/conceitos.md` e gere **5 conceitos**, cada um com um motor diferente (invente motores novos também). Para cada um: o gancho do primeiro 1,5 s, a imagem central, a virada e o final.
3. Dê nota de 1 a 5 a cada conceito em **surpresa** (já vi isso mil vezes?), **clareza** (um leigo entende sem som?) e **aderência ao tema**. Recomende um em duas linhas e **espere o usuário escolher**.

## Fase 3. Roteiro

1. Escreva a narração por passo: fala curta, português do Brasil coloquial, sem cara de anúncio. Calcule o tempo (com o Liam a 1,15, são cerca de 3 palavras por segundo: 70 palavras dão uns 26 s e 120 dão uns 42 s, sem contar as pausas; medido em 17/11/2026). **Espere aprovação.**
2. Monte um `roteiro.json` que controla o vídeo inteiro: passos, narração, elementos, câmera, overlays, efeitos sonoros e CTA. Prenda cada acontecimento a uma **palavra da fala** (`{ "palavra": "cair" }`), não a segundos: assim, quando a voz muda, tudo continua no lugar.
3. Modelo de **estrutura** (não de conteúdo): `~/projetos/terceirizar-ti` (`roteiro.json`, `src/linhaDoTempo.ts`, `src/animacoes/`, `scripts/gerar-audio.ts`, `scripts/baixar-sons.ts`) e o porte para o raea em `~/Documentos/raea/graal/projects/terceirizar-ti`. Copie o encanamento (linha do tempo, deixas por palavra, legendas, `emo()`, fontes); invente as cenas do zero.

## Fase 4. Produzir no raea

Siga a skill `raea` para workspace, projeto, `raea context .`, `brief.ts` e `plan.org`, e diga "Working in WORKSPACE / PROJECT". Depois, com `references/tecnico.md` aberto:

1. **Voz**: ElevenLabs (Liam) → MP3 por passo e `narracao.json` com o tempo de cada palavra.
2. **Sons e música**: Freesound CC0, escolhidos pela descrição e não pelo primeiro resultado, com os créditos anotados.
3. **Cena, overlays, legendas e CTA**, contornando as limitações do raea listadas na referência.
4. **CTA no padrão do site da marca**: leia o CSS do site (cores, fontes, raio, botões, espaçamento) e copie essa linguagem. Um fechamento genérico (logo brilhando, botão pílula com emoji) parece template e desvaloriza a marca.

## Fase 5. Verificar e entregar

Faça a verificação da referência: check rápido, folha de quadros-chave (olhe as imagens), render completo, medição de duração e loudness, volume de cada efeito contra a voz, e a cópia em AAC para WhatsApp e Instagram (o raea grava Opus, que eles recusam). Só diga que está pronto mostrando os números medidos.

Depois:
- Acrescente a linha do vídeo ao `HISTORICO-SHORTS.md`; é ela que garante que o próximo será diferente.
- Apague renders intermediários e testes; ficam o original final e a cópia de entrega.
- Registre armadilhas novas na seção `## Regressões` do `AGENTS.md` do projeto.

## Regras que valem o tempo todo

- **Retenção**: conflito no primeiro 1,5 s; alguma mudança a cada 2 a 4 s; uma metáfora visual central que volta; a virada transforma a mesma imagem do problema; o último quadro encaixa no primeiro para o replay parecer contínuo.
- **Verdade**: só os fatos da fase 1; na dúvida, suavize ou pergunte. Logos só dos arquivos reais. Nada de imagem ou vídeo gerado por IA.
- **Segredos**: chaves só em `~/api/`, lidas para uma variável e enviadas só no cabeçalho do próprio serviço. Nunca imprima o conteúdo desses arquivos.
- **Versões**: cada render novo vira um arquivo novo (`-v2`, `-v3`), para dar para comparar e voltar.
