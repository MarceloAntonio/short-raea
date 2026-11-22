# Nicho: NOME

Copie para `references/nichos/<nicho>.md` (nome sem acento, com hífen). Confira cada fonte antes de pôr na lista: `curl -s -o /dev/null -w '%{http_code}' URL` tem que dar 200, e o feed tem que ter itens. Fonte que exige login (TikTok, Instagram, Reddit) não entra em "Fontes para o script": ela quebra sem aviso.

Conferido em: DD/MM/AAAA.

## Fontes para o script
<!-- Lidas pelo scripts/pautas.py. Uma por linha: - tipo | nome | endereço
     Tipos: rss, rss-busca (com {termo}), trends, hn, kev, sugestao, sugestao-yt, youtube.
     Placeholders: {termo} {janela} {geo} {hl} {gl} {ceid}. Em hn/sugestao/youtube, "{termo}" ou lista fixa "a, b". -->
- trends | Google Trends | https://trends.google.com/trending/rss?geo={geo}
- rss-busca | Google Notícias | https://news.google.com/rss/search?q={termo}+when:{janela}&hl={hl}&gl={gl}&ceid={ceid}
- sugestao | Autocompletar Google | {termo}
- sugestao-yt | Autocompletar YouTube | {termo}
- youtube | YouTube mais vistos | {termo}

## Termos de busca
<!-- Os 3 primeiros são os padrão da coleta. Escreva como o público digita, não como a marca fala. -->
- termo 1

## Notícias em português
## Notícias em inglês
## Comunidades
<!-- subreddits, fóruns, grupos; o que não dá para o script ler, você confere com WebFetch ou o usuário cola -->
## Perfis e canais de referência
<!-- para ver o ângulo que todo mundo já usou, não para copiar -->
## Calendário fixo
<!-- eventos, datas e lançamentos que voltam todo ano; mês e o que costuma render -->
## O que evitar
<!-- assuntos sensíveis do nicho, marcas de terceiros, imagem que não pode usar -->
