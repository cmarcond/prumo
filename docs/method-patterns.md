# Method Patterns — biblioteca final (corpus completo: 82 vídeos)

Proveniência = nº de vídeos do corpus (de 82) cujas heurísticas/anti-padrões/decisões
exibem o pattern (bucketing por palavra-chave sobre as `video-observation.json`; é um
piso, não exato). Patterns de **técnica** viram skill + gate; os de **estilo** ficam
registrados (informam fidelidade, não viram gate).

## Tier 1 — quase universais (>50/82)
| pattern | /82 | essência | skill / gate |
|---|---|---|---|
| async-propagate | **78** | persista+ack imediato, propague async; decoupar via broker; push-vs-pull explícito; nada de fan-out síncrono antes do ack | `decouple-with-async-propagation`, `persist-before-external-visibility` / G-ASYNC, G-PERSIST-BEFORE-VISIBLE |
| datastore-by-access | **72** | escolher DB/índice pela razão read:write e forma da query; a tecnologia mais simples que serve (B-tree/Dynamo read-heavy; LSM/Cassandra write-heavy) | `choose-datastore-by-access-pattern` / G-INLINE, G-FREETEXT |
| staleness-lever | **63** | explorar o que o problema tolera (staleness/aproximação) como movimento-chave: batch, precompute, TTL | `exploit-tolerated-weakness` / G-LEVER |

## Tier 2 — fortes (40–46/82)
| pattern | /82 | essência | skill / gate |
|---|---|---|---|
| partition/hot-partition | **46** | partition key sem skew; evitar scatter-gather; hotspot read-heavy → replicas | `partition-keys-and-hot-partitions` / G-HOTPART |
| ml-method | **46** | método ML: abordagem a partir do requisito, two-stage (candidate→rank), persistir o modelo, train/serve parity, label vem da ação, normalizar features, métrica por custo de erro, baseline antes de complexidade | `ml-system-design` / G-TWO-STAGE-RANK, G-MODEL-PERSIST, G-TRAIN-SERVE-PARITY, **G-BASELINE-FIRST**, **G-COLD-START** |
| oltp-olap | **41** | tirar leitura analítica/treino do store operacional; analítico via CDC→warehouse; sem dual-writes | `separate-operational-from-analytical` / G-OLTP-OLAP, **G-NO-DUAL-WRITES** |
| idempotency/partial-failure | **41** | enumerar falhas parciais; persistir a chave antes da chamada; ordem com falha menos-pior; escada let-it-fail→retry idempotente→2PC→consenso | `design-for-partial-failure` / G-IDEMPOTENT, G-UNIQUENESS, G-ORDERING |

## Tier 3 — recorrentes (30–36/82)
| pattern | /82 | essência | skill / gate |
|---|---|---|---|
| payload-off-path | **36** | blobs via object store/URL, nunca pelos app servers | `keep-large-payloads-out-of-path` / G-PAYLOAD |
| naive-first | **34** | naive → expõe a falha → refina; enumerar por eixos de variação e ranquear | `iterate-naive-to-optimal` / G-NO-REINVENT, G-NAIVE-FIRST |
| workload-classify | **34** | classificar o workload (read/write/total-ordering) primeiro; o fork escolhe a arquitetura | **`classify-workload-first`** (nova) |
| binding-constraint | **33** | calcular candidatos a gargalo e projetar para o dominante; traduzir em nº de máquinas | `find-the-binding-constraint` / G-AMPLIFICATION, G-CAPACITY |
| scope-blackbox | **31** | sub-problema → black box nomeada; não rolar o próprio consenso/crypto; construir o núcleo antes de colapsar em managed | `scope-defer-and-blackbox` / G-SCOPE |

## Tier 4 — presentes (13–22/82)
| pattern | /82 | essência | skill / gate |
|---|---|---|---|
| client-trust | **22** | enforcement de segurança/correção é server-side; nunca filtrar dado sensível / escolher id/shard no browser | **`enforce-on-the-server`** (nova) / **G-NO-CLIENT-TRUST** |
| hot-key (≠ hot-partition) | **17** | distinguir hot partition (→ consistent hashing) de hot key (→ CDN/cache/contador shardado) | `partition-keys-and-hot-partitions` (refinar) |
| invariant-data | **15** | invariantes no modelo (dinheiro exato, contagens guardadas, timestamp vs boolean); deltas, não estado | `model-invariants-in-data` / G-INVARIANT-IN-DATA, G-DELTA-NOT-STATE |
| entry-exit-diagram | **14** | começar o diagrama pelos pontos de entrada/saída e traduzir requisitos em caixas | **`diagram-from-dataflow`** (nova, processo) |
| append-only | **13** | preferir append-only/event-sourcing; evitar update/delete in-place; reconstruir estado por eventos; fugir de tombstones | **`append-only-event-sourcing`** (nova) / **G-APPEND-ONLY** |

## Gates surfados pela avaliação (lacunas que todos os braços perderam)
- **G-NO-OVERENGINEER-REALTIME** — não adicionar real-time/stateful (WebSocket) quando o acesso é intermitente (use polling/reload).
- **G-CACHE-POPULAR-NOT-ALL** — cachear/CDN só o subconjunto popular (via batch de popularidade); não empurrar tudo pro CDN.

## ESTILO (registrado, não vira gate)
| pattern | /82 | nota |
|---|---|---|
| cite-sources | 39 | ancora em DDIA/Alex Xu/Grokking/experiência de produção — tell de credibilidade |
| number-pedagogy | 10 | ajusta números "to keep it interesting" — relevante p/ fidelidade, não é método a reproduzir |

## Leitura
O método dele é dominado por **3 reflexos** (decoupar async, casar store ao acesso,
explorar staleness) + um núcleo de ~9 patterns, com um ramo **ML forte** (46/82) e uma
cauda de patterns de nicho mas reais. Convergiu cedo (~30 vídeos); os 82 deram a
proveniência e a cauda (client-trust, append-only, hot-key, invariantes).
