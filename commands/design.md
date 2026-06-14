# /prumo.design — Loop de design versionado (red → green → refactor)

O coração do Prumo. Produz o design por **versões**, com os Design Gates
reprovando entre elas, até verde. Pré-condição: `intent.json` (do `/prumo.init`) +
`requirements.json` rico e completo (do **`/prumo.requirements`**, já passado pelo
gate G-REQ-COMPLETENESS). Saídas: `design/v1..vN/{requirements.json,design.json,design.mmd,critique.md}`
e `design/v_final` simbólico para a melhor versão.

## Princípio
Nunca produza o design final de uma vez (zero-shot tende à "baseline neutra" e
perde o movimento que distingue um bom design). Itere naive → ótimo, como manda a
skill `iterate-naive-to-optimal`.

## Passo 0 — Eixos de variação (skill `enumerate-variations`)
Antes de desenhar, nomeie os **eixos de variação** do problema (consistência
forte×eventual, deadline fixo×dinâmico, exato×aproximado, acesso contínuo×intermitente,
regime read-heavy×write-heavy). Para cada eixo com impacto arquitetural, decida:
desenhar a variação distinta, ou colapsar com justificativa. Gate `G-ENUMERATE-VARIATIONS`.

## Passo 1 — v1 (primeira versão)
Aplicando as skills (`skills/index.yaml`), produza:
- `requirements.json` completo — **faça o back-of-the-envelope** (skill
  `find-the-binding-constraint`): estime os candidatos a gargalo e nomeie o que
  limita. Não pule a conta.
- `design.json` (componentes + arestas, conforme `templates/schemas/design.schema.json`)
  e `design.mmd` (Mermaid a partir dos nós/arestas).

## Passo 2 — Gate critique (red)
Rode TODOS os gates de `gates/gates.md` contra a versão atual:
- **DET** (lints sobre o grafo + aritmética): compute concretamente
  (amplificação pós-fan-out, soma de capacidade vs demanda, partition key skewed,
  idempotência antes de chamada externa, blob fora do app server…). Verifique
  sobre `design.json` (anote `consistency`/`partition_key`/`payload`/`idempotent`
  nos elementos para tornar o lint mecânico).
- **ADV** (verificadores adversariais): para cada requisito não-funcional, um
  sub-agente tenta **refutar** que o design o atende (acha a carga/falha/sequência
  que quebra). RED se a maioria refuta.
Grave `critique.md` (gate | verdict RED/AMBER/GREEN | issue | fix + skill).

## Passo 3 — vN+1 (green)
Se houver RED: refine a versão endereçando **cada** RED, aplicando a skill que
faz o conserto (a coluna "skill" do gate / `backs_gates` no index). É permitido
mudar a arquitetura quando um gate exige (dropar store redundante, re-keyar log,
trocar engine pela forma do workload). Re-rode o Passo 2.

## Passo 4 — Convergência e refactor
Pare quando todos os gates ficarem GREEN (ou após K iterações sem novo RED).
Então **refactor**: simplifique (menos componentes) mantendo tudo verde.

## Passo 4b — Materialização de tech (skill `materialize-tech-choices`)
Com a estrutura estável, **nomeie a tecnologia concreta de cada componente**
justificada pela forma do acesso (write-heavy+scans→LSM/Cassandra; point-lookup
read-heavy→DynamoDB/B-tree; stream→Kafka; etc.), em `tech_choices`. Nenhum componente
pode ficar como abstração genérica. Escolhas não-óbvias citam 1 alternativa rejeitada.
Gate `G-MATERIALIZE-TECH`. Marque então a versão como `v_final`.

## Passo 5 — Mutação (provar os gates)
Para os gates críticos do problema, injete o anti-padrão no `design.json`
(trocar store forte por eventual; partition key skewed; remover o persist de
idempotência) e confirme que o gate correspondente fica RED. Gate que não pega a
mutação não está instalado — registre.

## Saída
Anuncie `/prumo.evaluate` (rubrica + ratchet). Em modo automático, siga direto.
