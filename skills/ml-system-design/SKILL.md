# ML System Design

Projetar a parte de ML de um sistema. O método é tão importante quanto a arquitetura:
**escolher o algoritmo pelo dado disponível, fazer feature-engineering de verdade,
escolher o modelo pela forma da saída, e separar treino de serventia.** Versão
aprofundada — os 15 runs mostraram que o ramo ML era o de menor cobertura (o gap era
feature-engineering e survey de algoritmo, não arquitetura).

## When To Use
- O sistema tem um componente de predição/recomendação/ranking/classificação.

## When Not To Use
- Não há aprendizado; uma regra/heurística determinística resolve. (Não force ML.)

## Preconditions
- Intent + requirements; saber qual ação do produto vira o **label**, e que dados existem.

## Order Of Operations
1. **Survey de algoritmo por dado disponível** (é uma *variação* — use `enumerate-variations`):
   - sem interações ainda → **content-based** (features do item);
   - muitas interações item↔item → **item-collaborative** (tabela de similaridade item-item; cuidado com o custo O(itens²));
   - mais dado de usuário que de item → **user-collaborative**;
   - escala grande → **two-stage** (candidate generation barato → ranking caro).
   Nomeie as alternativas e escolha por critério (dado disponível, escala).
2. **Label a partir da ação do produto** (clique, follow, compra = label); e como **obter dados rotulados** (logs de interação, rótulos implícitos).
3. **Feature engineering** (onde o gap mora):
   - **reduzir dimensionalidade** (PCA/SVD/autoencoder; descartar componentes ruidosos) — não jogue features cruas de alta dimensão no modelo;
   - **texto**: TF-IDF/embeddings, remover stop words — não use uma coluna por palavra;
   - **normalizar/pré-processar** entradas (escala, formato);
   - **um modelo por classe/tag** para multi-label quando fizer sentido.
4. **Modelo pela forma da saída**: probabilidade graduada → regressão (logística/linear); binário → classificador. **Baseline-first**: comece simples (regressão/random forest) antes de GBM/rede neural; o complexo só se o simples falhar.
5. **Métrica pelo custo do erro**: escolha por FP vs FN do domínio; trate **class imbalance** (down-sample/weights).
6. **Similaridade/recall**: ANN para candidate generation; cuidado com distância em alta dimensão (cosine, não Minkowski que estoura).
7. **Onde a computação vive**: feature-engineering e treino **offline no warehouse/lake** (Spark/Trino), via CDC do OLTP — nunca full-scan no store de serventia; **persistir o modelo** num model store e servir de lá (train/serve parity: mesmas features no treino e na serventia).
8. **cold-start / explore-exploit**: trate, ou escope fora explicitamente.

## Test Checklist
- [ ] As famílias de algoritmo foram enumeradas e a escolha justificada pelo dado disponível.
- [ ] O label vem de uma ação do produto; a origem dos dados rotulados está dita.
- [ ] Há feature-engineering real (redução de dimensionalidade / encoding de texto / normalização), não features cruas.
- [ ] Modelo escolhido pela forma da saída; há um baseline antes do complexo.
- [ ] Métrica casa com o custo de erro; class imbalance tratado.
- [ ] Treino/feature-eng offline (warehouse via CDC); modelo persistido e servido de um store; train/serve parity.
- [ ] cold-start/explore-exploit tratado ou escopado fora.

## Anti-Patterns
- Features cruas de alta dimensão (uma coluna por palavra) sem redução.
- **Clustering como redução de dimensionalidade** (gera conjuntos não-sobrepostos, encoda numa coluna só).
- **DBSCAN/aglomerativo em alta dimensão** (não escalam/funcionam) — preferir métodos que lidam com alta dim.
- **Decision tree para ranking** (regressão é melhor para probabilidade rankeável).
- Overfit: modelo sofisticado demais (NN/SVM exótico) com pouco dado.
- Distância Minkowski em alta dimensão (overflow colapsa as distâncias).
- Query analítica/ETL no OLTP de serventia; modelo só na sessão (não persistido); train/serve skew.

## Provenance
ML aparece em 46/82; o aprofundamento (feature-eng, survey, métrica, baseline) vem dos
vídeos ML (Visual Search, Recommendation Engine, PYMK, Ad Click, Video Rec) e fecha o
gap medido nos 15 runs. Backs gates G-TWO-STAGE-RANK, G-MODEL-PERSIST, G-COLD-START, **G-ML-FEATURE-ENG**.
