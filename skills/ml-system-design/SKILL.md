# ML System Design

Design the ML part of a system. The method is as important as the architecture:
**choose the algorithm by the available data, do real feature engineering,
choose the model by the shape of the output, and separate training from serving.** A
deepened version — the 15 runs showed that the ML branch was the one with the lowest
coverage (the gap was feature engineering and the algorithm survey, not architecture).

## When To Use
- The system has a prediction/recommendation/ranking/classification component.

## When Not To Use
- There is no learning; a deterministic rule/heuristic solves it. (Do not force ML.)

## Preconditions
- Intent + requirements; knowing which product action becomes the **label**, and what data exists.

## Order Of Operations
1. **Survey of algorithms by available data** (this is a *variation* — use `enumerate-variations`):
   - no interactions yet → **content-based** (item features);
   - many item↔item interactions → **item-collaborative** (item-item similarity table; watch out for the O(items²) cost);
   - more user data than item data → **user-collaborative**;
   - large scale → **two-stage** (cheap candidate generation → expensive ranking).
   Name the alternatives and choose by a criterion (available data, scale).
2. **Label from the product action** (click, follow, purchase = label); and how to **obtain labelled data** (interaction logs, implicit labels).
3. **Feature engineering** (where the gap lives):
   - **reduce dimensionality** (PCA/SVD/autoencoder; discard noisy components) — do not throw raw high-dimensional features at the model;
   - **text**: TF-IDF/embeddings, remove stop words — do not use one column per word;
   - **normalize/pre-process** the inputs (scale, format);
   - **one model per class/tag** for multi-label when it makes sense.
4. **Model by the shape of the output**: graded probability → regression (logistic/linear); binary → classifier. **Baseline-first**: start simple (regression/random forest) before GBM/neural network; the complex one only if the simple one fails.
5. **Metric by the cost of the error**: choose by the domain's FP vs FN; handle **class imbalance** (down-sample/weights).
6. **Similarity/recall**: ANN for candidate generation; watch out for distance in high dimensions (cosine, not Minkowski, which blows up).
7. **Where the computation lives**: feature engineering and training **offline in the warehouse/lake** (Spark/Trino), via CDC from the OLTP — never a full scan on the serving store; **persist the model** in a model store and serve it from there (train/serve parity: the same features in training and in serving).
8. **cold-start / explore-exploit**: handle them, or scope them out explicitly.

## Test Checklist
- [ ] The algorithm families were enumerated and the choice justified by the available data.
- [ ] The label comes from a product action; the origin of the labelled data is stated.
- [ ] There is real feature engineering (dimensionality reduction / text encoding / normalization), not raw features.
- [ ] Model chosen by the shape of the output; there is a baseline before the complex model.
- [ ] The metric matches the cost of error; class imbalance handled.
- [ ] Training/feature engineering offline (warehouse via CDC); model persisted and served from a store; train/serve parity.
- [ ] cold-start/explore-exploit handled or scoped out.

## Anti-Patterns
- Raw high-dimensional features (one column per word) with no reduction.
- **Clustering as dimensionality reduction** (it produces non-overlapping sets, encodes into a single column).
- **DBSCAN/agglomerative in high dimensions** (they do not scale/work) — prefer methods that handle high dimensions.
- **Decision tree for ranking** (regression is better for a rankable probability).
- Overfit: a model that is too sophisticated (NN/exotic SVM) with little data.
- Minkowski distance in high dimensions (overflow collapses the distances).
- Analytical query/ETL on the serving OLTP; model only in the session (not persisted); train/serve skew.

## Provenance
ML appears in 46/82; the deepening (feature engineering, survey, metric, baseline) comes from the
ML videos (Visual Search, Recommendation Engine, PYMK, Ad Click, Video Rec) and closes the
gap measured in the 15 runs. Backs gates G-TWO-STAGE-RANK, G-MODEL-PERSIST, G-COLD-START, **G-ML-FEATURE-ENG**.
