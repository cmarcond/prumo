# Problem Gates — perguntas iniciais (decisões do dono)

> Registro vivo das decisões do **problema**. O usuário pode ser **genérico**: o
> agente **sugere** cada resposta a partir de uma leitura do problema (init,
> Passo 0.5) e o usuário só confirma/ajusta. Gate é proposta-para-confirmar, não
> pergunta aberta — ninguém precisa chegar sabendo escala ou consistência.
> Coluna "Resposta" recebe a resposta final; "Origem" registra de onde veio
> (`proposto` = sugestão confirmada · `usuário` = ele mudou · `prompt` = já
> fixara no prompt · `[assumed]` = modo automático). Estas decisões NÃO são de
> design — são o que o dono fixa, e contra o que os Design Gates (`gates.md`)
> verificam o design. Saída: `intent.json` (sem solução) + esqueleto de
> `requirements.json`.

## Gate A — Problema e escopo
| # | Pergunta | Resposta (proposta→confirmada) | Origem |
|---|---|---|---|
| P1 | Que sistema vamos projetar, em termos de problema (não de solução)? Quem usa e o que consegue fazer? | | |
| P2 | O que está **dentro** do escopo (capacidades) e o que está **fora** (variantes que NÃO trataremos)? | | |

## Gate B — Escala e forma do workload
| # | Pergunta | Resposta (proposta→confirmada) | Origem |
|---|---|---|---|
| P3 | Ordem de grandeza: usuários/itens, e a razão **leitura:escrita**? (read-heavy? write-heavy? balanceado?) | | |
| P4 | Há fan-out / amplificação de escrita (um evento gera N escritas)? Picos/sazonalidade? | | |

## Gate C — Garantias (o que o problema exige e o que tolera)
| # | Pergunta | Resposta (proposta→confirmada) | Origem |
|---|---|---|---|
| P5 | Prioridade **consistência × disponibilidade** no caminho crítico? Há requisito de unicidade / exactly-once? | | |
| P6 | Quanta **staleness** é tolerada nas leituras? Contagem aproximada é aceitável onde? | | |
| P7 | Alvos de **latência** (SLA, P99) e de **durabilidade** (pode perder dado? qual)? | | |

## Gate D — Restrições e custo
| # | Pergunta | Resposta (proposta→confirmada) | Origem |
|---|---|---|---|
| P8 | Restrições de custo/infra, multi-região, compliance, ou tecnologias mandatórias/proibidas? | | |

## Gate E — Rigor e ratchet
| # | Pergunta | Resposta (proposta→confirmada) | Origem |
|---|---|---|---|
| P9 | Avaliação rígida, pedagógica ou pragmática? | | |
| P10 | Em regressão de score, o ratchet alerta (`warn`), bloqueia (`block`) ou repara (`repair`)? | | |

## Defaults do perfil canônico (modo automático)
Escopo mínimo explícito · razão read:write declarada (se desconhecida, assumir
read-heavy e marcar) · disponibilidade > consistência salvo requisito de
unicidade · staleness tolerada quando não dito o contrário · P99 como alvo ·
sem multi-região salvo pedido · avaliação pedagógica · ratchet em `repair`.

> Regra de ferro: **método nunca é pergunta; problema nunca é default sem marca.**
> O que o usuário fixa explicitamente vira origem "prompt", não `[assumed]`.
