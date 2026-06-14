# Manifesto do Prumo — Princípios Constitucionais

> O **prumo** é o fio que verifica se algo está alinhado contra uma referência
> verdadeira. Aqui a referência é o que o sistema **precisa** atender; os gates
> verificam se o design está "no prumo". Estes princípios valem para **todo**
> projeto que usa o Prumo — não são perguntados, não dependem do prompt, não se
> negociam por design. O que os Problem Gates (perguntas iniciais) calibram é o
> **problema** (escopo, escala, prioridades), nunca a vigência dos princípios.
>
> Método agnóstico de domínio e tecnologia: a tecnologia é exemplo descartável;
> o princípio é o que se mantém. Destilado de um corpus de system design real
> (ver `docs/method-patterns.md`) e do meta-método em `CORE_IDEA.md`.

## Princípios

1. **Todo design passa pelos gates; um gate só conta depois de visto reprovar.**
   O design é verificado contra os gates de raciocínio (`gates/gates.md`). Um
   gate só está instalado depois de reprovar uma violação provocada (mutação:
   injete o anti-padrão e veja o gate ficar RED). Configurar não é instalar.
2. **Ache a restrição limitante antes de desenhar, e desenhe para ela.**
   Bandwidth, CPU, storage, throughput, fan-out: calcule os candidatos e projete
   para o que de fato limita. Número não calculado é decisão não tomada.
3. **Requisito é intenção; skill é método; gate é o piso.** O requisito diz o
   QUE o sistema faz e tolera; a skill diz COMO se projeta bem; o gate reprova o
   que viola. Não misture — intenção que cita componente está vazando solução.
4. **Itere do naive ao ótimo.** Todo design nomeia ao menos uma alternativa
   rejeitada com a falha que a derruba. Red (gate reprova) → Green (refina até
   passar) → Refactor (simplifica sob verde). Versões: v1, v2, … até verde.
5. **O artefato é a verdade; a narração é contexto.** O diagrama e os números
   mandam sobre a fala quando divergem.
6. **Não pague por garantia que o requisito não exige.** Consistência forte,
   índice live, contagem exata: se o problema tolera menos, a tolerância é
   alavanca de design, não dívida.
7. **Falha parcial e idempotência primeiro** em todo caminho com efeito
   colateral ou estado: persista a chave antes da chamada retriável; ordene para
   a ação irreversível ser a última; a falha menos-pior ganha.
8. **A catraca só sobe.** O melhor score já medido vira piso (`ratchet.json`);
   regressão é evento explícito (alerta, bloqueio ou reparo), nunca decadência
   silenciosa.
9. **Gates automáticos, não disciplina.** Toda verificação possível roda como
   gate que reprova — determinística onde dá (lints sobre o grafo + aritmética),
   adversarial (sub-agentes que tentam refutar um requisito) onde não dá.
10. **O dono decide o problema; o framework decide o design.** Escopo, escala,
    prioridade consistência×disponibilidade, SLA e orçamento são **Problem
    Gates** do usuário, registrados com origem. O resto o agente executa pelos
    Design Gates até o próximo Problem Gate.

## As camadas (espelham o CORE_IDEA)

| Camada | Artefato | Pergunta |
|---|---|---|
| Constituição | `MANIFESTO.md` | O que nunca se negocia? |
| Conhecimento | `skills/` | Como se projeta cada coisa bem? |
| Decisão | `gates/questions.md` | O que é escolha do dono? (Problem Gates) |
| Verificação | `gates/gates.md` | O que reprova um design? (Design Gates) |
| Execução | `commands/design.md` | Qual a próxima versão verificável? (v1→vN) |
| Medição | `commands/evaluate.md` | Foi feito do jeito certo? (rubrica + auditoria limpa) |
| Memória | `ratchet.json` | O que já foi conquistado? (piso de qualidade) |
