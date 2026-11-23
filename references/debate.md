# Debate do roteiro entre agentes

Leia na fase 3, no modo crítica, no modo debate rápido e na fase 5 (rolador de feed com o render). Um roteirista sozinho não vê os próprios pontos cegos; quatro revisores cegos uns aos outros, e um juiz com ordem de desempate fixa, pegam o que uma revisão só deixaria passar. O custo é de tokens: o debate pode ser pulado se o usuário pedir "sem debate".

## Índice
1. Os agentes
2. Como disparar um agente
3. Fluxo na fase 3
4. Modo crítica e debate rápido
5. Rolador de feed na fase 5
6. Pasta do debate
7. O que mostrar ao usuário

## 1. Os agentes

Cada um é um arquivo em `agents/`, com o papel, o que recebe, o que é proibido e o formato exato da saída.

| Agente | Arquivo | Recebe | Modelo |
|---|---|---|---|
| roteirista | `agents/roteirista.md` | brief, conceito, fatos, marca; depois, roteiro anterior + veredito | sonnet |
| crítico | `agents/critico.md` | roteiro, brief, fatos | sonnet |
| defensor | `agents/defensor.md` | roteiro, brief, fatos | sonnet |
| rolador-de-feed | `agents/rolador-de-feed.md` | **só** os primeiros 3 s: quadro 0 (descrição ou imagem), texto na tela, fala do gancho marcada "com som" | haiku |
| especialista-chato | `agents/especialista-chato.md` | roteiro, brief, fatos | sonnet |
| juiz | `agents/juiz.md` | roteiro, brief, fatos + as 4 saídas | opus |
| diretor-de-arte-original (fase 2, antes do debate) | `agents/diretor-de-arte-original.md` | os 5 conceitos com a estética de cada um, as últimas 5 linhas do histórico e o caminho de `references/esteticas.md` | sonnet |

Regras de todos:
- Quem recebe o roteiro recebe também a **lista de fatos**, e é proibido de acrescentar número, selo ou promessa fora dela.
- Nenhum agente lê `~/api/*.env` nem escreve arquivos. Eles devolvem texto; **você** salva na pasta do debate (seção 6).
- O rolador-de-feed **nunca** recebe brief, tema, marca nem o resto do roteiro. Se ele souber do que é o vídeo, o teste do desconhecido no feed deixa de valer.

## 2. Como disparar um agente

Use a ferramenta `Agent` com `subagent_type: "general-purpose"` e o `model` do frontmatter. O `prompt` é o arquivo do agente **sem o frontmatter**, seguido das entradas:

```
<conteúdo de agents/critico.md, a partir de "# Crítico">

---
## Entradas desta rodada (v1)
### Brief
...
### Fatos aprovados (nada fora desta lista)
...
### Roteiro v1
...
```

Assim os agentes vão junto com a skill para qualquer máquina. Quem preferir chamá-los direto pelo nome roda `scripts/instalar-agentes.sh`, que os copia para `~/.claude/agents/`.

Para os revisores rodarem em paralelo, dispare os quatro **na mesma resposta**, cada um num `Agent` próprio. Não passe a saída de um para outro: os revisores são cegos de propósito, para não se influenciarem.

## 3. Fluxo na fase 3

Antes, crie a pasta do debate (seção 6) e salve nela o brief e os fatos (`brief.md`).

1. **Roteirista** escreve a v1 → salve `roteiro-v1.md`. Rode `scripts/lint-texto.py` na fala; o que ele apontar entra como ponto para o juiz.
2. **Crítico, defensor, rolador-de-feed e especialista-chato** em paralelo, na mesma resposta → `critica-v1.md`, `defesa-v1.md`, `feed-v1.md`, `especialista-v1.md`.
3. **Juiz** com o roteiro, o brief, os fatos e as 4 saídas → `veredito-v1.md`.
4. Se o juiz pedir outra rodada: o **roteirista** recebe a v1 e o veredito e escreve a v2 (só o que foi mandado mudar) → repita os passos 2 a 4 com o sufixo `-v2`. O rolador-de-feed só entra na rodada nova **se o gancho mudou** (fala, texto na tela ou quadro 0); se não mudou, o juiz recebe o `feed` da rodada anterior.
5. **No máximo 2 rodadas** no vídeo completo. Se depois disso ainda houver MUDA de gravidade alta ou o juiz listar pontos "em aberto", eles vão para o usuário decidir, sem uma terceira rodada.

Depois do debate, a fase 3 segue: mostre ao usuário (seção 7) e **espere aprovação** antes do `roteiro.json`. A decisão final é sempre do usuário, não do juiz.

## 4. Modo crítica e debate rápido

- **Modo crítica** (o usuário traz o roteiro): sem roteirista. Rode os 4 revisores e o juiz sobre o roteiro dele, uma rodada, e entregue o veredito com as reescritas pontuais. Se faltar brief ou fatos, pergunte só o essencial (marca, objetivo, o que pode ser afirmado); sem fatos, o especialista e o crítico tratam todo número como "conferir".
- **Debate rápido** ("debate rápido", "roda o debate nisso"): uma rodada só, sem perguntar nada. Use o que já está na conversa como brief e fatos; o que faltar fica como "em aberto" no veredito.

## 5. Rolador de feed na fase 5

Depois do render, antes de entregar, tire os quadros do MP4 e rode o rolador-de-feed de novo, sem som:

```
mkdir -p out/feed
ffmpeg -v error -y -i out/X-vN.mp4 -vf "select=eq(n\,0)" -frames:v 1 out/feed/q0.png
for t in 0.5 1 1.5 3; do ffmpeg -v error -y -ss $t -i out/X-vN.mp4 -frames:v 1 out/feed/q$t.png; done
```

Passe só os caminhos das 5 imagens e a fala do gancho marcada "com som" (nada de brief nem tema). Salve como `feed-render.md` na pasta do debate. Se der **PASSO sem som**, avise o usuário antes de entregar e sugira o que mudar no começo (quadro 0, texto na tela), com base no que o rolador disse que entendeu.

## 6. Pasta do debate

Dentro do projeto do raea: `debate/<AAAA-MM-DD>-<tema-curto>/` (ex.: `debate/2026-11-21-vazamento-email/`).

```
brief.md            brief e fatos usados
roteiro-v1.md       critica-v1.md   defesa-v1.md   feed-v1.md   especialista-v1.md   veredito-v1.md
roteiro-v2.md       critica-v2.md   ...                                               veredito-v2.md
roteiro-final.md    a versão aprovada pelo usuário
feed-render.md      o rolador de feed com os quadros do MP4 (fase 5)
```

Salve a saída de cada agente como veio, sem editar: o objetivo é o usuário poder ver depois por que algo saiu.

## 7. O que mostrar ao usuário

1. O **roteiro final** (fala, imagem e texto na tela por passo, duração estimada).
2. O **PARO/PASSO** do rolador-de-feed (sem som e com som) e a pergunta que ficou.
3. A tabela do veredito final:

   | Ponto | Quem levantou | FICA/SAI/MUDA | Motivo |
   |---|---|---|---|

4. As **notas** (gancho, escalada, virada, envio, verdade) e os pontos em aberto.
5. O caminho da pasta do debate.

Depois, espere a aprovação. Se o usuário discordar de uma decisão do juiz, vale o usuário.
