# Pautas: pesquisar o que está em alta num nicho

Leia no modo Pautas e na fase 1, quando o tema ficar vazio. Uma pauta "em alta" sem fonte com data é palpite, e vídeo de marca feito sobre palpite envelhece antes de postar ou espalha coisa errada. Por isso a pesquisa é por fonte, e cada pauta carrega a prova de que é recente.

## Índice
1. Quando entra
2. Perguntas
3. Coleta (script)
4. Complemento na web
5. Caçador, cético e juiz
6. O que entregar
7. Depois da escolha
8. Pasta e histórico de pautas
9. Regras

## 1. Quando entra

- **Modo Pautas**: "me dá ideias", "o que tá em alta em X", "sobre o que eu posto?".
- **Fase 1, tema vazio**: se o item Tema ficar sem resposta ou vier "não sei" ou "me dá ideias", ofereça pelo `AskUserQuestion`:
  - "Pesquisar o que está em alta (Recomendado)"
  - "Temas que não envelhecem (dúvidas frequentes)"
  - "Eu digo o tema"

"Temas que não envelhecem" pula a coleta de notícias: rode o script com `--tipos sugestao,sugestao-yt` (as perguntas que as pessoas fazem sempre) e monte as pautas a partir delas e do calendário fixo do nicho.

## 2. Perguntas

Num só `AskUserQuestion` (máximo 4 perguntas), só o que a marca não responde:
1. **Nicho**: opções tiradas de `marcas/<marca>.md` e do histórico, mais as que têm arquivo em `references/nichos/` (tecnologia, segurança digital, criação de sites, futebol). "Outro" para um nicho novo (crie o arquivo a partir de `references/nichos/_modelo.md`, conferindo cada fonte com `curl`).
2. **Público**: quem assiste e para quem mandaria.
3. **Região**: Brasil (Recomendado), um estado (`BR-SC`), uma cidade ou global.
4. **Janela**: 7 dias (Recomendado), 24 h, 30 dias.

Se a marca tem perfil em `marcas/`, pegue nicho e público de lá e só confirme.

## 3. Coleta (script)

```
python3 scripts/pautas.py --nicho seguranca-digital --janela 7d --regiao BR [--termos "golpe pix,boleto falso"]
```

- Lê as fontes de `references/nichos/<nicho>.md` ("Fontes para o script") e os termos ("Termos de busca", os 3 primeiros por padrão).
- Busca os RSS, o Google Trends, o Google Notícias por termo, a API do Hacker News, o catálogo KEV da CISA, o autocompletar do Google e do YouTube e, se existir `~/api/youtube.env` com `YOUTUBE_API_KEY`, os vídeos mais vistos do termo na janela (sem a chave, segue sem ela; não peça a chave).
- Tira o que está fora da janela e os duplicados, e grava `pautas/<data>-<nicho>/coleta.json`. Cada fonte tem 15 s e uma nova tentativa; se falhar, fica anotada em `fontes` e a coleta segue.
- Mostre ao usuário o resumo que o script imprime (itens por fonte e falhas).

**TikTok e Instagram não entram**: exigem login e quebram. Diga ao usuário que ele pode conferir os áudios e os temas em alta no app e colar aqui. O mesmo para o Reddit, que recusa o script.

## 4. Complemento na web

Depois da coleta, use `WebSearch` e `WebFetch` para o que o script não cobre: a tabela da rodada no futebol, uma notícia citada sem link, a página oficial de um golpe. **No máximo umas 15 buscas por rodada.** Anote o que achou (título, link, data) para passar ao caçador junto com o `coleta.json`.

Se o usuário pedir "mais", faça outra rodada **sem repetir as fontes** da anterior: outros termos, outras buscas, outra janela.

## 5. Caçador, cético e juiz

Mesmo jeito de disparar do debate (`references/debate.md`, seção 2): ferramenta `Agent`, `subagent_type: "general-purpose"`, o arquivo do agente sem o frontmatter e as entradas.

1. **Caçador de pautas** (`agents/cacador-de-pautas.md`): recebe o caminho do `coleta.json`, os achados da web, o brief, o histórico de Shorts e o `pautas/HISTORICO-PAUTAS.md`. Devolve 8 a 12 pautas → salve `pautas.md`.
2. **Cético de pauta** (`agents/cetico-de-pauta.md`): recebe **só as pautas** (sem o raciocínio do caçador), a janela e os dois históricos → `ceticismo.md`.
3. **Juiz** (`agents/juiz.md`, seção "Modo pautas"): recebe as duas saídas e o brief, e ordena por momento, encaixe, envio, 3D sem terceiros e segurança dos fatos → `veredito.md`.

## 6. O que entregar

1. Uma tabela com as **5 melhores**:

   | Pauta | Por que agora | Ângulo | Gancho | Nota | Janela | Link principal |
   |---|---|---|---|---|---|---|

2. **2 temas que não envelhecem** como reserva.
3. As que ficaram de fora por serem sensíveis (tragédia, política), em uma linha cada, com o motivo.
4. O `AskUserQuestion` para escolher (as 3 melhores + "Outra da lista" + o "Outro" livre).

Se a coleta não trouxe nada forte (poucos itens, nenhuma pauta com mais de uma fonte na janela, ou tudo descartado pelo cético), **diga isso** e ofereça os temas que não envelhecem. Não promova notícia fraca a "em alta".

## 7. Depois da escolha

- A pauta escolhida vira o **Tema** da fase 1.
- Os fatos dela entram na lista de **Fatos** como **sugestão**: mostre cada um com fonte e data e peça confirmação (no `AskUserQuestion` ou numa lista para o usuário marcar). Só os confirmados seguem para o roteiro.
- No `roteiro.json`, cada fato guarda a fonte e a data: `{"afirmacao": "...", "status": "confirmado pelo usuário (DD/MM)", "fonte": "link", "data": "AAAA-MM-DD"}`.
- Depois, o fluxo normal: o resto da fase 1 e a fase 2 (conceitos).

## 8. Pasta e histórico de pautas

`pautas/` fica na pasta da skill e fora do git (`.gitignore`).

```
pautas/
  HISTORICO-PAUTAS.md
  2026-11-21-seguranca-digital/
    coleta.json      web.md (achados da web)
    pautas.md        ceticismo.md     veredito.md
    escolha.md       pauta escolhida, fatos confirmados e recusados
```

`pautas/HISTORICO-PAUTAS.md` tem uma linha por rodada:

| Data | Nicho | Pautas oferecidas | Escolhida |
|---|---|---|---|

Antes de oferecer pautas, leia esse arquivo: pauta **recusada ou já feita** no último mês não volta, a menos que tenha fato novo (diga qual).

## 9. Regras

- **Nunca chame algo de "em alta" sem fonte com data** dentro da janela.
- **Tragédia, morte, crime com vítima ou política** não vira pauta de marca. No máximo, avise que o assunto existe e por que ficou de fora.
- **Futebol e marcas de terceiros**: nada de escudo, foto de jogador, imagem de jogo, uniforme de clube nem música de torcida. Represente em 3D genérico (bola, campo, uniforme sem marca, placar) e diga isso na pauta.
- **Golpes e falhas de segurança**: só com fonte oficial ou imprensa confiável, e com a orientação correta de proteção (a cartilha do CERT.br é a base). O especialista-chato revisa de novo na fase 3.
- **Pesquisa leve**: até umas 15 buscas na web por rodada.
- **Segredos**: a chave do YouTube só é lida pelo script, para uma variável; nunca imprima `~/api/youtube.env`.
