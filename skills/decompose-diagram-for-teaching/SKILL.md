# Decompose The Diagram For Teaching

Um único diagrama com todos os componentes é ilegível e não ensina. Quebre o
design em uma **sequência de figuras** que vai do alto nível ao detalhe, mais
fluxos (sequência) e cenários — cada figura legível por si, cada uma com texto
que a lê para o leitor.

## When To Use
- Fase `/prumo.publish`: transformar o `design/v_final` num documento pedagógico.
- Sempre que um `design.json` tem mais de ~8–10 componentes (um diagrama só vira
  emaranhado).

## When Not To Use
- Design trivial (≤ ~6 nós, 1 fluxo): uma figura de contexto + uma de containers
  já bastam; não invente zooms vazios.

## Preconditions
- `design/v_final/design.json` (componentes + arestas anotadas) e
  `requirements.json` (números, invariantes), `critique.md` (decisões/alternativas).
- Os eixos de variação do problema (do `/prumo.design`, skill `enumerate-variations`)
  — eles definem quais zooms e cenários valem a pena.

## Order Of Operations
1. **Mapeie o design nos níveis C4.** Contexto (atores + o sistema como caixa
   preta) → Containers (os grandes blocos: services, stores, broker, cdn) →
   Components (zoom dentro de um subsistema). `type` do componente vira o macro
   C4: `service→Container`, `datastore→ContainerDb`, `broker→ContainerQueue`,
   `cache/cdn→Container` com rótulo.
2. **Corte por eixo de variação, não arbitrariamente.** Cada zoom (component) é um
   subsistema coeso — tipicamente os mesmos eixos que o design separou
   (ingestão×serventia, escrita×leitura, quente×frio). Um zoom por eixo relevante.
3. **Teto de legibilidade: ~10 caixas por figura.** Se um nível passa disso,
   promova um subconjunto a um zoom próprio. A figura de containers mostra o
   esqueleto; os detalhes moram nos zooms.
4. **Fluxos viram diagramas de sequência.** Um por caminho principal (ex.: upload,
   watch). A sequência é onde se vê a **ordem** e a **assincronia** (ack antes do
   fan-out; persist antes de visível) — coisas que o diagrama de blocos esconde.
5. **Cenários viram figuras próprias.** Falha parcial, pico/viral (cold-start),
   concorrência (deleção durante leitura): um recorte por cenário, mostrando só os
   componentes que ele exercita.
6. **Cada figura ganha prosa.** Abaixo de cada figura, leia-a para o leitor: o que
   olhar, por que aquele bloco existe, qual pressão ele alivia. Figura sem texto
   não ensina.

## Test Checklist
- [ ] Existe uma figura de contexto (alto nível) antes de qualquer detalhe.
- [ ] Nenhuma figura passa de ~10 caixas; as densas viraram zooms.
- [ ] Cada eixo de variação do problema tem seu zoom (ou foi colapsado com motivo).
- [ ] Cada caminho principal tem um diagrama de sequência mostrando ordem/assincronia.
- [ ] Cada cenário de falha/pico/concorrência tem sua figura.
- [ ] Toda figura é seguida de prosa que a explica (não fica órfã).

## Anti-Patterns
- **Diagrama-emaranhado**: um único quadro com tudo, ilegível, "tecnicamente completo".
- **Zoom vazio**: quebrar por quebrar, gerando figuras que não acrescentam.
- **Figura órfã**: imagem sem texto que a leia — bonita e muda.
- **Sequência ausente**: só blocos, nunca a ordem temporal — esconde a assincronia
  e a ordenação, que são metade do design.
- **Estourar a página**: figura grande demais para o papel; resolve-se decompondo,
  não encolhendo a fonte até ilegível.

## Provenance
Feature `/prumo.publish`: o `design.json` é a fonte de verdade, mas um humano
aprende a solução por uma progressão de vistas (C4: contexto→container→component)
+ fluxos + cenários, cada vista legível e narrada. Espelha o princípio "o artefato
é a verdade; a narração é contexto" aplicado à comunicação da solução.
