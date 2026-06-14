# /prumo.reverse — Engenharia reversa: projeto existente → seed (problema + Problem Gates)

Entrada auxiliar do fluxo. Em vez de partir de um prompt, parte de **código pronto**
e reconstrói o *seed* que, dado ao `/prumo.init`, regeneraria o design deste sistema.
Pré-condição: `.prumo/` instalado + o **path de um projeto-alvo**. Saída (na **raiz do
projeto** de resultados): o seed pronto para colar no `/prumo.init` — opcionalmente
`questions.md` (Problem Gates respondidos) e `intent.json` fino, para encurtar o init.

> **Caminhos:** o framework (`gates/`, `skills/`, `templates/`) é lido de `.prumo/`;
> os resultados vão na **raiz**. Convenção completa em `/prumo.init`.

> Regra de altitude: o prumo projeta o projeto no eixo **system design** — escala,
> componentes, garantias. A história de *features/craft/TDD* NÃO é dele (é da catraca).
> Se o projeto-alvo é CRUD sem desafio de escala, o seed sai magro — e tudo bem.

## Passo 0 — Modo e alvo
- Receba o **path do projeto-alvo**. Modo guiado (default) ou automático.
- Releia `manifesto.md` e `gates/gates.md`: o design que você vai inverter precisa ser
  defensável pelos mesmos gates, então é por eles que você lê o código.

## Passo 1 — Leitura de arquiteto reversa (mapear a solução materializada)
Leia, nesta ordem, o que revela o **design já tomado**: README; infra/deploy
(`docker-compose*`, `k8s/*.yaml`, `*.tf`, Helm, Procfile); escolha de datastores,
caches, filas, balanceadores; configs de réplica/escala/particionamento; métricas,
SLAs, alertas, dashboards. Identifique **componentes + arestas reais** — isto é o
`design.json` já materializado no projeto (não o escreva ainda; é insumo da inversão).

## Passo 2 — Inverter para os Problem Gates (sugerir a partir da evidência)
Leia as perguntas do **template** `.prumo/gates/questions.md` (em branco — NÃO o edite)
e, para cada gate (A→E / P1–P10), **infira** a resposta a partir da evidência no
código, citando o arquivo/trecho que a sustenta. Exemplos do raciocínio reverso:
- réplica 3x no datastore → durabilidade alta (P7); cache no caminho quente +
  read-replicas → read-heavy e SLA de latência apertado (P3, P7); fila/broker →
  fan-out assíncrono e picos (P4); índice de unicidade/transação → unicidade exigida
  (P5). Marque o que não dá pra inferir como `[assumed AAAA-MM-DD]`. Grave em
  `./questions.md` (raiz). Em guiado, apresente as inferências e peça confirmação.

## Passo 3 — Destilar o `intent.json` fino (sem solução)
A partir do Gate A, escreva o intent: `problem`, `goal`, `scope_in[]`/`scope_out[]`,
`context_assumptions[]` qualitativas. Duas barreiras, agora invertidas:
- **intenção/solução**: NENHUM componente/tecnologia/padrão do Passo 1 entra no
  enunciado (Redis/Kafka/sharding pertencem a P8 "tech mandatória" ou ao design, não
  ao problema);
- **intenção/derivação**: não enumere a lista funcional nem números — isso é
  `/prumo.requirements`.
Rode uma **revisão adversarial de contexto limpo** (no Claude Code, um subagente Task)
que caça vazamento de solução no enunciado — se achar tecnologia no `problem`, mova
para P8 e reescreva. Schema: `templates/schemas/intent.schema.json`.

## Passo 4 — Emitir o seed
Monte um bloco **`SEED PARA /prumo.init`** = enunciado (Passo 3) + Problem Gates
respondidos com evidência (Passo 2) + um `leak-check` confirmando que o enunciado não
cita tecnologia. Esse bloco é o **prompt extraído**. Em automático, grave também
`intent.json` e `questions.md` para o init seguir direto.

## Passo 5 — Validação por round-trip (recomendado)
Rode o seed por `/prumo.requirements` → `/prumo.design` e **compare** o `design.json`
gerado com os componentes/arestas reais do Passo 1. Cada divergência é uma **lacuna no
seed** (uma garantia ou número que o problema não capturou) — endereça e re-emita.
Convergência = o seed reconstrói o projeto.
