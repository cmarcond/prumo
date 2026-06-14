# /prumo.requirements — Expandir o intent fino em requisitos ricos (gated)

A fase que faltava. O `init` produz um **intent fino** (problema + escopo do dono
+ contexto qualitativo). Aqui o agente **deriva** os requisitos ricos — e derivar
bem é uma skill sob teste, não um insumo dado. Pré-condição: `intent.json`.
Saída (na **raiz do projeto**): `requirements.json` (rico) + `requirements-critique.md`.

> **Caminhos:** resultados vão na **raiz**; o framework (`gates/`, `skills/`,
> `templates/`) é lido de `.prumo/`. Convenção completa em `/prumo.init`.

> Regra de ouro (anti-vazamento): o `intent.json` NÃO contém a lista funcional
> detalhada nem os números — se contiver, isso é vazamento da derivação. Esta
> fase é onde a lista nasce.

## Passo 1 — Derivar (skill `elicit-requirements-from-intent`)
A partir do intent fino, derive:
- **Funcionais**: percorra entidades, ações, **relacionamentos** e **edge-cases**
  que o domínio implica — inclusive os não-óbvios (ex.: distinguir tipos de
  relação; ciclo de vida/deleção; o que acontece em conflito/duplicata).
- **Invariantes**: unicidade, monotonicidade (upgrade-only), ordenação,
  idempotência — o que o domínio exige que nunca seja violado.
- **Não-funcionais**: derive da **forma do workload** (read:write → consistência/
  latência; fan-out → amplificação; volume → durabilidade) — cada NFR amarrado ao
  porquê.
- **Escala**: faça o back-of-the-envelope (skill `find-the-binding-constraint`):
  números que o dono fixou + os que você estima, com a conta.
Escreva `requirements.json` conforme `templates/schemas/requirements.schema.json`.

## Passo 2 — Gate de completude (`G-REQ-COMPLETENESS`, ADV)
Rode um crítico de contexto limpo que **enumera a superfície implícita** do
problema (entidades/ações/relacionamentos/invariantes/NFR esperados) e checa se os
requisitos cobrem — e marca o que **faltou** como RED. Ele NÃO desenha solução;
só verifica completude e se cada NFR está ancorado no workload. Grave
`requirements-critique.md`.

## Passo 3 — Iterar até verde
Endereça cada RED (derive o que faltou). Re-rode o gate. Pare quando completo.
Não invente requisito que o domínio não pede (over-spec também é achado).

## Saída
Anuncie `/prumo.design`. Em automático, siga direto. O design consome ESTES
requisitos, não o intent.
