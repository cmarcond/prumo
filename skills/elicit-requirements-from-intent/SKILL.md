# Elicit Requirements From a Thin Intent

Derivar uma lista rica de requisitos a partir de um enunciado genérico. O intent
diz o problema e o escopo do dono; os requisitos — funcionais (inclusive os
implícitos), invariantes, não-funcionais e números — são **derivados**, e derivar
é o trabalho. Não copie as palavras do enunciado como se fossem os requisitos.

## When To Use
- Logo após o intent estar fixado e antes de qualquer design.
- Sempre que o enunciado for genérico ("projete um X estilo Y") e a superfície de
  requisitos ainda não existir.

## When Not To Use
- Quando os requisitos já vêm dados e verificados pelo dono (raro; ainda assim
  rode o checklist de completude).
- Para um spike descartável que não vira design mantido.

## Preconditions
- Um `intent.json` fino (problema + escopo in/out do dono + contexto qualitativo).
- A forma do workload pelo menos proposta (read:write, fan-out, volume).

## Order Of Operations
1. **Modele o domínio**: liste entidades, ações sobre elas, e os
   **relacionamentos** entre entidades. Relacionamento é onde moram os requisitos
   esquecidos (ex.: dois tipos de relação que parecem um só; relação direcional).
2. **Caminhe os edge-cases**: criação/atualização/deleção, conflito/duplicata,
   ausência, limites (o maior/menor caso), concorrência. Cada um costuma revelar
   um funcional ou um invariante.
3. **Extraia invariantes**: o que NUNCA pode ser violado? unicidade, monotonicidade
   (upgrade-only), ordenação, exactly-once, conservação. Invariante vira NFR e
   gate depois.
4. **Derive NFR da forma do workload**: read-heavy → latência/leitura e
   consistência tolerável; write/fan-out → amplificação e durabilidade; volume →
   retenção. Cada NFR amarrado ao porquê (workload), não a um catálogo genérico.
5. **Back-of-the-envelope**: número que o dono fixou + estimativa com a conta
   (use `find-the-binding-constraint`).
6. **Revise por completude**: passe o `G-REQ-COMPLETENESS` e feche os buracos.

## Test Checklist
- [ ] Todo relacionamento entre entidades virou ≥1 requisito ou foi descartado com motivo.
- [ ] Os edge-cases (criar/atualizar/deletar/conflito/limite) estão cobertos.
- [ ] Os invariantes do domínio estão explícitos.
- [ ] Cada NFR cita a característica de workload que o motiva.
- [ ] Os números têm conta, não chute; o gargalo provável está nomeado.
- [ ] Nada é cópia literal do enunciado sem expansão.

## Anti-Patterns
- **Eco do enunciado**: repetir as palavras do prompt como "requisitos", sem derivar.
- **Relacionamento esquecido**: tratar dois tipos de relação como um (ex.: seguir ≠ conectar).
- **NFR de catálogo**: listar "alta disponibilidade, baixa latência" sem amarrar ao workload.
- **Invariante implícito**: assumir unicidade/monotonicidade sem declará-la (some no design).
- **Over-spec**: inventar requisito que o domínio não pede só para parecer completo.

## Provenance
Derivada empiricamente: o benchmark clean-room mostrou que, a partir de prompt
genérico, a derivação de requisitos era o elo fraco (relacionamentos e invariantes
implícitos eram perdidos). Corroborada pelo `requirements_method` observado no
build-set (o mestre deriva números com conta e distingue variantes do problema).
