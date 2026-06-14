# /prumo.evaluate — Rubrica + auditoria de contexto limpo + ratchet

Avalia o design final de um problema. Pré-condição: `/prumo.design` convergiu
(gates verdes). Saídas (na **raiz do projeto**): `evaluation/<slug>.md` +
`ratchet.json` atualizado.

> **Caminhos:** `evaluation/` e `ratchet.json` vão na **raiz**; o framework
> (`gates/`, `skills/`, `templates/`) é lido de `.prumo/`. Convenção completa em
> `/prumo.init`. Exceção deliberada: promover um gate/skill (Passo 4) **edita** o
> framework em `.prumo/gates/gates.md` ou `.prumo/skills/` — é mudança do *método*,
> que deve voltar para o repo do Prumo, não um resultado do problema.

## Dois modos
- **Benchmark** (existe ground truth do mestre): compare `design/v_final` contra
  o `requirements.json` + `design.json` de referência, nas dimensões abaixo. É o
  **meta-gate** — mede se intent + skills + gates reproduzem o mestre.
- **Standalone** (sem ground truth): pontue só pelos gates (quantos verdes,
  quantos exigiram quantas iterações) + a auditoria limpa. Não há "match", mas há
  "passou nos gates e sobreviveu à refutação".

## Passo 1 — Rubrica (com evidência por linha)
Dimensões (0..1), conforme `templates/schemas/scores.schema.json`:
- `requirements_coverage` — funcionais + não-funcionais cobertos.
- `estimation_fidelity` — números na ordem de grandeza certa / raciocínio correto.
- `design_match` — casamento semântico de componentes/arestas/decisões (benchmark)
  **ou** cobertura dos gates aplicáveis (standalone).
- `criteria_coverage` — as heurísticas de método aparecem (gargalo achado, naive
  rejeitada nomeada, tolerância usada como alavanca…).
- `baseline_gap` — onde o design diverge da baseline neutra do arquiteto (o
  movimento não-óbvio). Sem evidência, 0.

## Passo 2 — Auditoria de contexto limpo
Delegue a um subagente **sem acesso a quem gerou o design** (e, no benchmark, que
não viu o ground truth ao desenhar): re-execute os gates DET (refaça as contas),
e **mute o design** (injete um anti-padrão) para confirmar que o gate pega. Ele
reporta achados; você acata (ajusta score) ou refuta com justificativa. Registre
mutações aplicadas × sobreviventes.

## Passo 3 — Ratchet
Compare cada score com `ratchet.json` (chave = slug do problema). Maior → sobe o
piso. Menor que `piso - buffer` → regressão:
- `warn` ⇒ alerta na rubrica;
- `block` ⇒ HALT, reporte ao usuário;
- `repair` ⇒ volte ao `/prumo.design` com os REDs/diferenças como itens de refino
  (nova versão), reavalie uma vez; recuperou ⇒ segue, senão ⇒ HALT.
Guarde a progressão de versões (v1→vN) e o piso por dimensão.

## Passo 4 — Encerramento
Resuma: verdict, scores por dimensão, gates que exigiram iteração, e (se
benchmark) as divergências do mestre — cada divergência é candidata a **novo
gate** (`.prumo/gates/gates.md`) ou nova skill (`.prumo/skills/`). Lacuna vira
conhecimento incorporado. Promover é mudança **do método** (volta para o repo do
Prumo), distinta dos resultados na raiz; faça-a deliberadamente, não em silêncio.
