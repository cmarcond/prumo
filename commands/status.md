# /prumo.status — Reconciliar estado

Use após editar uma resposta em `./questions.md` (raiz) ou retomar trabalho.

> **Caminhos:** os resultados (`questions.md`, `intent.json`, `requirements.json`,
> `design/`, `evaluation/`, `ratchet.json`) ficam na **raiz**; o framework é lido de
> `.prumo/`. Convenção completa em `/prumo.init`.

1. Releia `./questions.md`, `./intent.json`, `./requirements.json` e a última versão
   em `./design/` (tudo na raiz).
2. Se uma Problem Gate mudou: marque os artefatos afetados (intent/requirements/
   design) e proponha a reconciliação (ex.: mudou a razão read:write → re-rodar o
   gargalo e os gates de capacidade/amplificação).
3. Reporte: em que fase está (init / design vN / evaluate), gates pendentes, e a
   próxima ação (`/prumo.init`, `/prumo.design` ou `/prumo.evaluate`).
4. Nunca reescreva decisões do dono sem confirmar; o agente executa design, não
   redefine o problema.
