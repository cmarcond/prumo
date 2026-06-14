# Como o Catraca funciona — estudo para o Prumo

Resumo da arquitetura do `catraca` (framework spec-driven de TDD/Clean
Architecture, irmão deste) e o que o Prumo herda, adapta ou substitui.

## O que o catraca é
Uma pilha de artefatos de texto instalada em `.catraca/` no projeto alvo. O
agente hospedeiro executa; o framework **guia com texto**. Instalação por
`install.py` idempotente (cria / pula idêntico / preserva divergente em `.new`).

## Peças
- **`MANIFESTO.md`** — constituição: 11 princípios que valem para todo projeto e
  não são perguntados (TDD red-green-refactor, dependências para dentro, libs por
  adapter, erro na borda, cobertura é gate, gates automáticos não disciplina…).
- **`skills/` + `index.yaml`** — 13 skills, cada uma com When To Use / When Not /
  Preconditions / Order Of Operations / **Test Checklist** (de onde saem os
  critérios de aceitação) / **Anti-Patterns** (o que reprova na rubrica).
- **`templates/questions.md`** — os **User Feedback Gates** (A produto, B
  plataforma, C método, D avaliação, E por-feature). Em modo guiado o agente
  pergunta um gate por vez e grava a resposta; em automático grava defaults com
  `[assumed]`. Calibram o **rigor**, nunca os princípios.
- **`commands/`** — o fluxo: `init` (gates → product/architecture/method),
  `plan` (roadmap + tasks), `implement` (red→green→refactor por comportamento),
  `evaluate` (rubrica + auditoria + ratchet), `status` (reconciliar).
- **Esteira de qualidade (feature 000)** — antes de qualquer feature de produto,
  instala os gates automáticos (lint, type-check, cobertura) como hooks que
  reprovam commit/push. Cada gate **visto reprovar** uma violação provocada.
- **`evaluate` + `ratchet.json`** — rubrica com evidência por linha; **auditoria
  de contexto limpo** (subagente que tenta derrubar scores, re-executando e
  **mutando** o código para ver se algum teste quebra); ratchet em modo
  warn/block/**repair** (anexa tasks R1, R2… e reavalia).

## O chão determinístico do catraca
O "red" do catraca é **executar e falhar**: teste, linter, cobertura, mutação.
Tudo verificável mecanicamente. É isso que o Prumo precisa recriar — e é o ponto
onde system design diverge.

## O que o Prumo herda, adapta, substitui

| Catraca | Prumo (system design) |
|---|---|
| Constituição (`MANIFESTO`) | herdada, reescrita para design (ver `MANIFESTO.md`) |
| Skills com Anti-Patterns | herdadas — 9 skills de método de design |
| User Feedback Gates (questions) | **Problem Gates** (`gates/questions.md`): escopo, escala, consistência×disponibilidade, SLA, orçamento |
| Esteira de gates automáticos (lint/cobertura) | **Design Gates** (`gates/gates.md`): lints sobre o grafo + aritmética (DET) e verificadores adversariais (ADV) |
| red→green→refactor de código | red→green→refactor de **design**: v1→v2→…, gate reprova → refina → simplifica |
| Mutação no código (teste do teste) | Mutação no **design** (injeta anti-padrão, confirma gate RED) — análogo do chaos engineering |
| Auditoria de contexto limpo | idêntica: scorer/critic sem acesso ao ground truth |
| Ratchet por feature | Ratchet por **design** (piso por dimensão de reprodução) |
| `implement` executa tasks de TDD | `design` roda o loop versionado de design |

## A diferença essencial
Código se prova **executando**; design se prova por **inspeção estruturada +
aritmética + refutação adversarial**. Por isso o Prumo apoia o máximo no chão
determinístico que existe (lints sobre `design.json` anotado + contas de
capacidade/amplificação) e usa sub-agentes só para o que não dá para mecanizar.
O **meta-gate** é a reprodução cega contra o ground truth do mestre: se intent +
skills + gates reproduzem o design dele, o conjunto funciona; onde diverge, falta
gate ou skill (a lacuna vira o próximo gate).
