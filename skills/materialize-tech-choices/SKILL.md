# Materialize Tech Choices

Depois que a estrutura do design (componentes + arestas) está verde, **materialize**:
nomeie a tecnologia concreta de cada componente e justifique pela forma do acesso.
O manifesto separa princípio (o que o componente faz) de materialização (a tech que o
realiza) — esta skill é o passo de materialização, e fecha a lacuna nº1 medida nos 15
runs (33% das nuances ficaram "princípio certo, tech não nomeada").

## When To Use
- Sempre, ao finalizar o design — cada componente precisa de uma tech nomeada.
- Quando uma escolha de tech não é óbvia (citar 1 alternativa e por que perdeu).

## When Not To Use
- Num spike descartável. Numa fase de estrutura ainda instável (materialize depois que a topologia parar de mudar).

## Preconditions
- `design.json` com componentes/arestas e a forma do workload (read:write, consistência, payload) conhecida.

## Order Of Operations
1. Para cada componente, escreva `tech_choices[{component, choice, rationale}]`: a tech concreta + uma linha amarrando à característica de acesso (ex.: "write-heavy + scans → Cassandra/LSM"; "read-heavy point lookup → DynamoDB/B-tree"; "stream de eventos → Kafka").
2. Onde a escolha é não-óbvia, registre `alternatives_considered` e o motivo da rejeição.
3. Não deixe nenhum componente como abstração genérica ("um log durável", "um object store") sem tech nomeada.
4. Roll-from-scratch vs managed: decida explicitamente (evite lock-in onde o nível do problema pede o de baixo).

## Test Checklist
- [ ] Todo componente de `design.json` tem uma `tech_choice` nomeada.
- [ ] Cada escolha cita a característica de acesso que a justifica (não é catálogo).
- [ ] Escolhas não-óbvias têm ≥1 alternativa considerada com motivo.

## Anti-Patterns
- Componentes como abstrações genéricas sem tech nomeada.
- Nomear tech sem amarrar ao padrão de acesso.
- Lock-in de vendor onde rolar-do-zero é o esperado (ou o inverso).

## Provenance
Derivada da análise dos 15 runs: a maior fatia das nuances perdidas era partial por
falta de materialização concreta de tecnologia. Backs gate **G-MATERIALIZE-TECH**.
