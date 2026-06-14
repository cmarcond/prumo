# /prumo.init — Problem Gates → intent + requirements skeleton

Roteiro de inicialização. Pré-condição: `.prumo/` instalado. Saídas (na **raiz do
projeto**): `questions.md` preenchido, `intent.json`, `requirements.json` (esqueleto).

> **Convenção de caminhos — framework × resultados.** `.prumo/` guarda o
> **framework/método** (MANIFESTO, `gates/`, `skills/`, `templates/`, `docs/`),
> compartilhado entre projetos: só muda **deliberadamente**, quando se promove um
> novo gate/skill (mudança do *método*, que volta para o repo do Prumo) — nunca como
> subproduto de um problema. Os **resultados** deste problema vão na **raiz do
> projeto**: `questions.md`, `intent.json`, `requirements.json`,
> `requirements-critique.md`, `design/`, `evaluation/`, `ratchet.json`. As respostas
> dos Problem Gates são anotadas em `./questions.md` (raiz), **não** no template
> `.prumo/gates/questions.md` (que fica em branco). Citações a `gates/…`, `skills/…`,
> `templates/…` para **ler** referem-se a `.prumo/…`.

## Passo 0 — Modo e constituição
- Modo guiado (default) ou automático (se o usuário pedir).
- Releia `manifesto.md` (princípios já valem — não pergunte se "quer achar o
  gargalo": isso é constituição) e `gates/gates.md` (os Design Gates que vão
  reger o design).

## Passo 0.5 — Leitura do problema (para poder SUGERIR)
Antes de perguntar qualquer coisa, faça uma leitura rápida de arquiteto sobre o
problema (mesmo que o prompt seja genérico, ex.: "projete um social graph"):
qual o padrão de uso provável, o que domina (leitura? escrita? fan-out?), que
garantias o domínio realmente exige, ordem de grandeza plausível. Essa leitura é
a base das **propostas** dos gates — o usuário não precisa chegar sabendo escala
nem consistência.

## Passo 1 — Problem Gates (A→E): sugerir, não interrogar
O usuário pode ser **genérico**. Leia as perguntas do **template**
`.prumo/gates/questions.md` (em branco — NÃO o edite) e grave as respostas em
`./questions.md` na **raiz**. Para CADA gate, o agente **propõe** uma resposta
derivada do Passo 0.5, com uma linha de justificativa, e pede só confirmação —
nunca deixa a pergunta aberta para o usuário preencher do zero. Regras:
- **Guiado**: um gate por vez. Apresente a proposta ("Sugiro read-heavy ~100:1
  porque buscas/visualizações ≫ novas conexões; ok?"). O usuário confirma, ajusta
  ou pede alternativas. Grave com origem `proposto` (confirmado) ou `usuário`
  (se ele mudou) ou `prompt` (se ele já fixara no prompt).
- **Automático**: grave a própria proposta como resposta, marcada
  `[assumed AAAA-MM-DD]`, e siga.
- O que o usuário fixou no prompt é proposta a confirmar (origem `prompt`), não
  pergunta. O que ele NÃO fixou, você propõe — não pergunta em aberto.

## Passo 2 — `intent.json` (a semente, **fino**, sem solução)
A partir do Gate A: `problem`, `goal`, `scope_in[]` / `scope_out[]` **de alto nível
(o que o DONO decide incluir/excluir)**, `context_assumptions[]` (qualitativas).
**Mantenha fino**: o intent NÃO traz a lista funcional detalhada, nem invariantes,
nem números — isso é **derivação**, e nasce na fase `/prumo.requirements` (pôr aqui
vaza o trabalho que será testado). Duas barreiras:
- **intenção/solução**: o intent não cita componente/tecnologia/padrão;
- **intenção/derivação**: o intent não enumera requisitos derivados (relacionamentos,
  edge-cases, invariantes, métricas) — só o escopo que o dono fixa.
Rode uma revisão adversarial (contexto limpo) que caça vazamento de solução **e** de
derivação antes de aceitar. Schema: `templates/schemas/intent.schema.json`.

## Passo 3 — Encerramento
- Confirme consistência (problema × escopo do dono × respostas dos gates).
- Próxima fase: **`/prumo.requirements`** (expande o intent fino em requisitos ricos,
  com o gate de completude), e só então `/prumo.design`.
