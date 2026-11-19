# Publicação: capa, legenda e hashtags

Leia na fase 5, depois da entrega do vídeo. Um perfil pequeno depende mais da capa e da legenda do que um perfil grande, porque quase ninguém chega pelo perfil: chega pela busca e pelo feed de quem não segue.

## Índice
1. O que o Instagram mede
2. Legenda
3. Hashtags
4. Capa
5. Outros recursos para perfil pequeno
6. Ler os insights e o que já aprendemos

## 1. O que o Instagram mede

Pesquisado em 18/11/2026. As fontes são blogs de marketing que citam o Adam Mosseri (chefe do Instagram); confira de novo se passou muito tempo.

- Os três sinais mais citados para Reels: **tempo assistido**, **envios por mensagem por alcance** e **curtidas por alcance**. O envio por mensagem é o que mais leva o vídeo a quem não segue o perfil.
- Desde dezembro de 2025, o Instagram aceita **no máximo 5 hashtags** por post ou Reel (antes eram 30), na legenda ou nos comentários. Elas servem para classificar o assunto, não para dar alcance.
- A busca lê a **primeira linha da legenda**, o campo de nome do perfil, o texto na tela e a fala. Palavra-chave na primeira linha vale mais que hashtag.

## 2. Legenda

1. **Primeira linha**: a pergunta ou o termo que o cliente procuraria, com a palavra-chave do serviço ("Terceirizar o suporte de TI vale a pena para a sua empresa?"). É a única linha visível antes do "mais".
2. **Corpo**: o gancho do vídeo e o argumento em 2 ou 3 frases, só com os fatos aprovados na fase 1. Nada que o vídeo não diga.
3. **Chamada**: **a mesma do fechamento do vídeo**, com as mesmas palavras ("Fale com a Graal Solutions: link na bio").
4. **Hashtags**: na última linha.

**Não invente uma chamada que o vídeo não faz.** Numa versão, a legenda dizia "Comente TI que a gente te chama no WhatsApp" e "Manda pra quem é dono de empresa". O usuário recusou as duas: o vídeo não pede comentário, "a gente te chama" promete um atendimento que ninguém combinou, e nem todo perfil tem WhatsApp. Se quiser testar "comente PALAVRA" ou um pedido de envio, isso precisa estar no roteiro do vídeo, e a resposta automática (ManyChat ou parecido) precisa existir antes de postar.

"Link na bio" serve para qualquer destino (WhatsApp, site, formulário). Confira se o link da bio leva mesmo a um contato.

## 3. Hashtags

- Exatamente 5, uma linha só, no fim da legenda.
- Misture: o nome do serviço como o cliente procura (#suportedeti), o tema exato (#terceirizacaodeti), quem é o público em palavras de nicho (#tiparaempresas) e o assunto de um fato do vídeo (#segurancadainformacao, se o vídeo mostra a certificação). Use a cidade quando a marca atende numa região só.
- Evite as gigantes (#reels, #tecnologia, #empreendedorismo): o vídeo some em minutos. O guia da Later sugere hashtags de 50 mil a 1 milhão de publicações.
- **Pergunte antes de usar hashtag de público.** O usuário vetou #pequenasempresas para a Graal; o público "pequena empresa" estava no brief, mas não é como a marca quer ser vista.
- Você não vê a contagem de publicações de fora do app. Diga isso e peça para o usuário conferir cada hashtag na busca do Instagram antes de postar.

## 4. Capa

A capa é feita em HTML e fotografada com o Chrome sem janela. Fica em `out/capa/` (HTML editável e o fundo) e a imagem final vai para `out/` ao lado do vídeo.

1. **Fundo**: a própria cena 3D do vídeo, **sem legendas nem overlays**. Faça uma composição que monta só a `<Cena />` dentro do `<Canvas3D layered>`, com o contexto do filme, e congela num quadro com `<Freeze frame={N}>`. Renderize 3 quadros do gancho e escolha o que conta o problema sozinho (no da Graal: luz vermelha, telas apagadas, cadeira do técnico vazia).
2. **HTML de 1080 × 1920**: `@font-face` com os `.woff2` de `compositions/media/fonts/`, as cores da marca, o logo real de `compositions/media/brand/`, e um degradê escuro em cima e embaixo para o texto ler sobre a cena.
3. **Recorte da grade**: o perfil mostra a capa em 3:4. Tudo o que importa fica entre y = 240 e y = 1680. Confira com `ffmpeg -i capa.png -vf "crop=1080:1440:0:240" grade.png`.
4. **Texto**: o gancho do vídeo como título (o "E agora?" em dourado), um selo curto do problema ("SISTEMA FORA DO AR"), a plaquinha da cena, uma frase do argumento e, embaixo, o logo e um fato forte (o selo ISO). Junte as palavras que não podem separar com `white-space: nowrap` (o "E" ficou sozinho numa linha e o "agora?" na outra).
5. **Foto**:
   ```
   chrome --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=1 --allow-file-access-from-files --virtual-time-budget=3000 --window-size=1080,1920 --screenshot=CAMINHO\capa.png file:///CAMINHO/capa.html
   ```
   No Windows, o Chrome fica em `C:\Program Files\Google\Chrome\Application\chrome.exe`; passe caminhos do Windows (`cygpath -w`) no `--screenshot`. Confira o tamanho com `ffprobe` (1080 × 1920) e olhe a imagem.
6. Diga ao usuário onde fica: no app, "Editar capa" → "Adicionar da galeria".

## 5. Outros recursos para perfil pequeno

- **Reel de teste (Trial Reels)**: mostra o Reel só para quem não segue, por até 72 h, e depois você decide se publica para todos. As fontes divergem sobre o mínimo de seguidores (200 ou 1.000); peça para o usuário ver se a opção aparece ao postar.
- **Post em parceria (Collab)**: o Reel aparece também no perfil do parceiro ou cliente convidado.
- **Campo de nome do perfil** com o serviço ("Suporte de TI para empresas"): é ali que a busca procura, não só na bio.
- **Texto na capa e na tela** com as palavras que o cliente buscaria.

## 6. Ler os insights e o que já aprendemos

Peça ao usuário os prints de "Insights do reel" (visão geral, gráfico de retenção, "o que afeta suas visualizações") 24 a 48 h depois de postar. Cruze a curva de retenção com o início de cada passo (some `duracao` de `narracao.json` + `pausaEntrePassosSeg` por passo) para saber **qual trecho** perdeu gente, e leia cada taxa como resposta a uma pergunta: o vídeo deu motivo para essa ação?

### Caso Graal, terceirizar suporte de TI (v7, 63 s, perfil com 31 seguidores, 19 h)

| Métrica | Valor | Leitura |
|---|---|---|
| Visualizações / contas | 1.923 / 1.648 | 90 % da aba Reels (não seguidores). Pico entre 5 e 9 h depois de postar |
| Reels pulados | 35,5 % | Gancho bom: 65 % passaram dos 3 s |
| Tempo médio | 24 s (38 %) | Vídeo longo para o que entrega |
| Curtidas | 6,1 % | Alta: dor reconhecível, visual 3D agrada |
| Salvamentos | 0,7 % | Nada útil para guardar |
| Envios | 0,5 % | Nenhum momento "manda pro chefe" |
| Comentários | 0,1 % | O vídeo não pergunta nada |
| Seguidores ganhos | 1 | Termina como anúncio, sem promessa de mais |

Retenção por trecho: gancho 100 → 68 %; **custo (16,8 s de lista falada) 68 → 48 %, a maior perda**; três problemas seguidos 48 → 37 %; virada com a marca aos 39 s, vista por ~37 %; CTA de 6 s parado, 25 → 5 %.

### Regras que saíram daí

1. **30 a 40 s.** Nenhum passo com mais de 8 s de fala. Problemas parecidos viram um passo só.
2. **Marca e solução antes dos 20 s.** Quem não vê a marca não tem o que seguir.
3. **Comentário: pergunta no vídeo, com resposta de um toque.** Narrada e escrita na tela, perto do fim ("Quando a TI cai aí, quem resolve? 1, 2 ou 3?"). Fixe um comentário com a mesma pergunta assim que postar. Continua valendo a regra da seção 2: a legenda só repete o que o vídeo pede.
4. **Envio: um momento de identificação.** Uma cena ou frase que a pessoa reconhece da própria empresa ("o sobrinho que entende de computador"), com humor. Tom institucional não é enviado.
5. **Salvamento: algo para consultar depois.** Um quadro de 2 a 3 s com checklist, conta ou número.
6. **Seguir: promessa de continuação.** Série com nome e número ("TI sem enrolação #1") e um final que anuncia o próximo. Venda ("fala com a gente, link na bio") fica para a legenda e para poucos vídeos.
7. **CTA de 2 a 3 s**, emendando no loop. Tela final parada é deslize.
8. **Capa escolhida na hora de postar.** Sem isso, o Instagram pega um quadro qualquer (aqui, a tela do CTA) e a grade parece anúncio.
