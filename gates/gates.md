# Design Gates — biblioteca genérica (catraca-SD, v0)

Gates de raciocínio de design, derivados dos anti-padrões em `patterns.md` e generalizados.
São **agnósticos de problema** (não contêm a resposta de nenhum vídeo). Cada gate: o
princípio, a condição de **RED**, a skill que ele força, e a camada (DET = checável sobre
o grafo/aritmética; ADV = verificador adversarial por sub-agente).

Uso: rodar contra `(requirements.json, design.json)` de uma versão; cada RED vira item de
refino para a próxima versão (v1→v2→…). Verde em todos = pode parar.

| id | princípio | RED quando | skill | camada |
|---|---|---|---|---|
| G-REQ-COMPLETENESS *(roda na fase requirements, antes do design)* | os requisitos cobrem a superfície implícita do problema (entidades, ações, relacionamentos, edge-cases, invariantes) e cada NFR vem da forma do workload | falta funcional/relacionamento/invariante que o domínio claramente implica, ou NFR sem amarração ao workload, ou requisitos são eco do enunciado sem derivação | elicit-requirements-from-intent | ADV |
| G-AMPLIFICATION | ao materializar uma propriedade por fan-out (1 write por entidade afetada), calcule o write TPS pós-amplificação e re-teste a razão read:write | há fan-out/materialização e o write TPS pós-amplificação **não foi calculado**, ou foi e a razão virou write-heavy sem troca de engine | find-the-binding-constraint | DET+ADV |
| G-CAPACITY | traduza o gargalo limitante em nº concreto de máquinas/partições; capacidade do design ≥ exigida | falta a conta gargalo→máquinas, ou a soma de capacidade < QPS/throughput exigido | find-the-binding-constraint | DET |
| G-NO-REINVENT | escolhido um processador especializado (stream/engine), não reintroduza store+merge que duplica o que ele já faz | há um stream/engine especializado **e** um contador/merge redundante sem justificativa | iterate-naive-to-optimal | ADV |
| G-FREETEXT | só adicione índice invertido/search-engine se a query é mesmo full-text | há search-engine para query que é equality/term/range | choose-datastore-by-access-pattern | DET+ADV |
| G-IDEMPOTENT | chamada externa com efeito colateral deve ser precedida de persist de idempotency key | aresta para `external` com side-effect sem persist antes | design-for-partial-failure | DET |
| G-UNIQUENESS | unicidade/exactly-once exige store linearizável, não eventual | requisito de unicidade cujo write-path termina em store `consistency=eventual` | design-for-partial-failure | DET |
| G-ORDERING | ordene passos para a ação irreversível ser a última / falha menos-pior | passo irreversível (cobrar, despachar) antes da dependência que o justifica | design-for-partial-failure | ADV |
| G-HOTPART | partition key não pode ser skewed; hotspot read-heavy → replicas, não resharding | `partition_key` skewed, ou hotspot read-heavy resolvido com hash+scatter-gather | partition-keys-and-hot-partitions | DET |
| G-PAYLOAD | blobs grandes via object store + URL, nunca pelos app servers | aresta `payload=large` com destino `service` (≠ object_store), ou blob inline no metadata DB | keep-large-payloads-out-of-path | DET |
| G-ASYNC | persista+ack imediato, propague/replique async; nada de fan-out síncrono antes do ack | ack depende de fan-out/replicação completar | decouple-with-async-propagation | DET+ADV |
| G-LEVER | não pague por garantia que o requisito não exige (consistência forte, índice live, contagem exata) | design paga por garantia mais forte que o requisito tolera (ex.: índice live com staleness OK) | exploit-tolerated-weakness | ADV |
| G-NAIVE-FIRST | há ≥1 alternativa naive descartada com a falha nomeada antes da escolhida | design final sem nenhuma alternativa considerada/rejeitada com motivo | iterate-naive-to-optimal | ADV |
| G-OLTP-OLAP | leitura analítica / full-scan / group-by não roda no store operacional; dados analíticos/treino saem via CDC para um warehouse/lake | há query analítica/ETL/batch contra o store de serventia (OLTP), ou um único store servindo OLTP+OLAP | separate-operational-from-analytical | DET+ADV |
| G-TWO-STAGE-RANK | quando há ranking/recomendação sobre muitos candidatos, gere candidatos baratos antes do ranking caro (evite O(N) em runtime) | ranking pairwise/pontual em runtime contra todo o conjunto, sem etapa barata de candidate-generation | ml-system-design | ADV |
| G-MODEL-PERSIST | um modelo treinado é persistido num model store e servido de lá; nunca vive só na sessão nem é deployado direto na máquina de serventia | modelo mantido em sessão/efêmero, ou deployado direto sem store, ou I/O do modelo não declarado | ml-system-design | DET+ADV |
| G-PERSIST-BEFORE-VISIBLE | persista de forma durável antes de tornar um efeito visível a terceiros (broadcast/fan-out/200 OK) | broadcast/publish/ack a outros usuários antes do dado estar durável no store (crash entre passos perde/expõe dado) | persist-before-external-visibility | DET+ADV |
| G-DELTA-NOT-STATE | em escala, propague mudanças (deltas) e não estado constante; e mande id+refetch em vez do payload pelo broker | broadcast de estado/heartbeat constante a grupo grande, ou payload grande trafegando pelo broker em vez de id | model-invariants-in-data | DET+ADV |
| G-INVARIANT-IN-DATA | invariantes do domínio são garantidos pelo modelo de dados (dinheiro não é float; contagens não-negativas; timestamp em vez de boolean para detectar staleness) | dinheiro como float; contador que pode ir a negativo sem guarda; boolean onde um timestamp é necessário | model-invariants-in-data | DET |
| G-NO-CLIENT-TRUST | enforcement de segurança/correção é server-side; o cliente não decide nem filtra o que é sensível | rate-limit/autorização/filtragem de dado sensível no browser; id/shard/timestamp escolhido pelo cliente (spoofável, DDoS) | enforce-on-the-server | DET+ADV |
| G-APPEND-ONLY | onde há auditoria/reconstrução de estado ou store LSM, preferir append-only/event-sourcing a update/delete in-place | update/delete in-place num store LSM (tombstones); estado que precisa ser reconstruível sem trilha de eventos | append-only-event-sourcing | ADV |
| G-NO-DUAL-WRITES | não escrever em dois stores no caminho de criação; sincronizar o segundo via CDC | dual-write síncrono a dois stores antes de responder (falha parcial) | separate-operational-from-analytical | DET |
| G-COLD-START | (ML/recsys) trate cold-start e explore/exploit, ou escope-os fora explicitamente | recsys/ranking sem nenhuma menção a cold-start; usar o domínio como cop-out p/ ignorá-lo | ml-system-design | ADV |
| G-NO-OVERENGINEER-REALTIME | não adicionar real-time/stateful (WebSocket/SSE) quando o acesso é intermitente | conexão persistente/stateful onde o usuário não observa continuamente (polling/reload serve) | classify-workload-first | ADV |
| G-CACHE-POPULAR-NOT-ALL | cachear/CDN só o subconjunto quente (via batch de popularidade); não empurrar tudo | tentar pôr todo o dataset no CDN/cache em vez do popular | exploit-tolerated-weakness | ADV |
| G-MATERIALIZE-TECH | todo componente nomeia uma tecnologia concreta justificada pela forma do acesso (princípio→materialização) | componente deixado como abstração genérica ("log durável"/"object store") sem tech nomeada, ou tech sem amarração ao padrão de acesso | materialize-tech-choices | DET+ADV |
| G-ENUMERATE-VARIATIONS | nomear os eixos de variação do problema e desenhar as variações distintas (ou justificar colapsar) | um único design onde o problema tem 2+ regimes (forte×eventual, fixo×dinâmico, contínuo×intermitente) sem os eixos expostos | enumerate-variations | ADV |
| G-ML-FEATURE-ENG | (ML) survey de algoritmo por dado disponível; feature-engineering real (redução de dimensionalidade, encoding de texto, normalização); modelo pela forma da saída com baseline-first; treino offline no warehouse | features cruas de alta dimensão sem redução; pular o survey de algoritmo; treino/feature-eng no OLTP de serventia; sem baseline antes do complexo | ml-system-design | ADV |
| G-DOC-LEGIBLE *(roda na fase publish)* | as figuras vão do alto nível ao detalhe e cada uma é legível por si: existe uma vista de contexto, nenhuma figura passa de ~10 caixas, e há diagrama de sequência para cada fluxo principal | falta a vista de contexto; alguma figura é um emaranhado (>~10 caixas) em vez de virar zoom; ou não há nenhuma sequência mostrando ordem/assincronia | decompose-diagram-for-teaching | DET+ADV |
| G-DOC-PEDAGOGIC *(roda na fase publish)* | o documento explica em linguagem simples os NFR de capacidade/demanda (nomeando o binder e a conta), e cada decisão de design vem com a alternativa naive rejeitada; toda figura é seguida de prosa que a lê | NFR de capacidade só como números crus sem explicação; binder não nomeado; decisão sem alternativa rejeitada; figura órfã (sem texto) | decompose-diagram-for-teaching | ADV |

> Princípio do catraca: um gate só conta como instalado depois de **visto reprovar** uma
> violação provocada. Validação por mutação: injete o anti-padrão no design (trocar store
> forte por eventual, partition key skewed, remover o persist de idempotência) e confirme
> que o gate correspondente fica RED.
