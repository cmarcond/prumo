# Prumo — framework agêntico de System Design

O **prumo** é o fio que verifica se algo está alinhado contra uma referência
verdadeira. Aqui a referência é o que o sistema precisa atender; os **gates**
verificam se o design está "no prumo".

Irmão do [`catraca`](../catraca) (spec-driven TDD) — mesma filosofia (artefatos
de texto que guiam um agente; o agente executa), aplicada a system design.
Destilado de um corpus real de entrevistas de system design; ver
`docs/method-patterns.md` e `docs/catraca-study.md`.

## Ideia em uma frase
Em vez de o agente cuspir um design zero-shot (que tende à "baseline neutra"),
ele projeta por **versões** (v1 → v2 → …), com **gates de raciocínio de design**
reprovando entre as versões até ficar verde — o mesmo red → green → refactor do
catraca, só que sobre o design. Uma **catraca** (ratchet) trava o melhor resultado.

## As peças
| Peça | Arquivo | Papel |
|---|---|---|
| Constituição | `MANIFESTO.md` | princípios que não se negociam |
| Problem Gates | `gates/questions.md` | o que o **dono** decide (escopo, escala, garantias, custo) |
| Design Gates | `gates/gates.md` | o que **reprova** um design (lints DET + verificadores ADV) |
| Skills | `skills/` + `index.yaml` | o **como** projetar bem (cada skill conserta o gate que ela respalda) |
| Comandos | `commands/` | `init` → `design` → `evaluate` → `status` |
| Memória | `templates/ratchet.json` | piso de qualidade que só sobe |
| Schemas | `templates/schemas/` | formato de requirements / design / scores |

## Layout no projeto — framework × resultados
O instalador cria `.prumo/` no projeto alvo. Vale a separação:

- **`.prumo/` = framework/método** (MANIFESTO, `gates/`, `skills/`, `templates/`,
  `commands/`, `docs/`). Compartilhado entre projetos; só muda **deliberadamente**
  ao promover um novo gate/skill — e essa mudança é do *método*, que volta para
  este repo (`prumo`), não um subproduto de um problema.
- **Raiz do projeto = resultados** do problema, gravados pelos comandos:
  `questions.md` (Problem Gates respondidos), `intent.json`, `requirements.json`,
  `requirements-critique.md`, `design/v1..vN/` + `design/v_final`, `evaluation/`,
  `ratchet.json`.

```
projeto/
├── questions.md            # respostas dos Problem Gates (resultado)
├── intent.json             # resultado
├── requirements.json       # resultado
├── requirements-critique.md
├── design/ v1.. v_final/   # resultado
├── evaluation/             # resultado
├── ratchet.json            # resultado (piso de qualidade)
└── .prumo/                 # FRAMEWORK (método): gates, skills, templates, …
```

O template `.prumo/gates/questions.md` fica **em branco**; o `init` o lê e grava as
respostas em `./questions.md`. Citações a `gates/…`, `skills/…`, `templates/…` nos
comandos referem-se a `.prumo/…` para **leitura**.

## Fluxo
1. `/prumo.init` — Problem Gates (o agente **sugere**, o dono confirma) → `intent.json`
   **fino** (problema + escopo do dono + contexto qualitativo; sem lista derivada).
2. `/prumo.requirements` — **expande** o intent fino em requisitos ricos (funcionais
   implícitos, relacionamentos, invariantes, NFR derivados do workload, números), com
   o gate de completude `G-REQ-COMPLETENESS`. Derivar bem é skill, não insumo.
3. `/prumo.design` — loop versionado: v1 → gate critique (red) → refina (green) →
   simplifica (refactor) → mutação (prova os gates).
4. `/prumo.evaluate` — rubrica + auditoria de contexto limpo + ratchet. Em modo
   benchmark, compara contra o ground truth do mestre (o meta-gate).

> O benchmark alimenta o agente **só com o intent fino** (ou um prompt genérico) —
> nunca com os requisitos prontos. Derivar os requisitos é parte do que se mede.

## Instalação
```
python3 install.py /caminho/do/projeto-alvo
```
Idempotente; cria `.prumo/` no alvo + atalhos `/prumo.*` em `.claude/commands/prumo/`.

## Estado
v0 — destilado de um piloto de 10 vídeos. Reprodução cega de held-out (intent +
skills + gates) sobe de ~0.63 (zero-shot) para ~0.75 (versionado com gates). Os
gates DET ainda dependem de anotações no `design.json`; o loop-until-green hoje é
roteiro de comando, não runner automatizado. Próximos: automatizar o loop,
engrossar gates/skills com o corpus completo (82 vídeos), triangular a avaliação.
