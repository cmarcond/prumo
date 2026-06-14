# Enumerate Variations

Muitos problemas têm **regimes distintos** que pedem arquiteturas distintas (ex.:
deadline fixo vs deslizante; consistência forte vs eventual; regime read-heavy vs
write-heavy). O mestre quase sempre **enumera as variações** e desenha as relevantes,
em vez de cravar uma só. Esta skill traz esse reflexo; fecha a lacuna nº2 dos 15 runs
("fez um design, não enumerou as variações").

## When To Use
- No início do design, para nomear os eixos de variação do problema.
- Sempre que o problema tem 2+ regimes que mudam a arquitetura.

## When Not To Use
- Problema genuinamente de regime único (registre que checou e não há variação).

## Preconditions
- Intent + requirements (os eixos saem dos requisitos: consistência, deadline, escala, padrão de acesso).

## Order Of Operations
1. Nomeie os **eixos de variação** do problema (consistência forte×eventual, fixo×dinâmico, exato×aproximado, contínuo×intermitente).
2. Para cada eixo relevante, **desenhe a variação distinta** (ou justifique colapsar numa só por que as outras não mudam a arquitetura).
3. Registre a progressão naive→escolhido com a **falha nomeada** da alternativa rejeitada (complementa G-NAIVE-FIRST).
4. Deixe explícito qual variação é o caminho principal e por quê.

## Test Checklist
- [ ] Os eixos de variação do problema estão nomeados.
- [ ] Cada eixo com impacto arquitetural tem sua variação desenhada ou um motivo registrado para colapsar.
- [ ] Há ≥1 alternativa rejeitada com a falha nomeada.

## Anti-Patterns
- Cravar uma arquitetura sem expor os eixos de variação.
- Apresentar um único design onde o problema claramente tem 2+ regimes (ex.: tempo-real só quando há watchers contínuos).

## Provenance
Derivada dos 15 runs: partials/misses concentravam-se em "construiu um design, o mestre
explorou variações". Backs gate **G-ENUMERATE-VARIATIONS** (complementa G-NAIVE-FIRST).
