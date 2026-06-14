# /prumo.status — Reconciliar estado

Use após editar uma resposta em `gates/questions.md` ou retomar trabalho.

1. Releia `questions.md`, `intent.json`, `requirements.json` e a última versão em
   `design/`.
2. Se uma Problem Gate mudou: marque os artefatos afetados (intent/requirements/
   design) e proponha a reconciliação (ex.: mudou a razão read:write → re-rodar o
   gargalo e os gates de capacidade/amplificação).
3. Reporte: em que fase está (init / design vN / evaluate), gates pendentes, e a
   próxima ação (`/prumo.init`, `/prumo.design` ou `/prumo.evaluate`).
4. Nunca reescreva decisões do dono sem confirmar; o agente executa design, não
   redefine o problema.
