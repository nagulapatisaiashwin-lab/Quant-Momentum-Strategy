# Intraday Volatility Forecasting in NIFTY 50

## Overview

This project investigates whether future intraday volatility can be predicted using information available at the current minute.

Unlike traditional intraday trading research that attempts to predict returns, this study focuses on forecasting realized volatility over future horizons using minute-level NIFTY 50 data.

The research explores:

- Volatility clustering
- Intraday seasonality
- Forecast horizon selection
- Market regime stability
- Feature importance analysis
- Machine learning-based volatility forecasting

Dataset:

- NIFTY 50 Minute Data
- Period: 2015 – 2025
- Frequency: 1 Minute

---

# Executive Summary

## Research Question

Can current market conditions predict realized volatility over the next 15 minutes?

## Answer

Yes.

A Random Forest model achieved:

| Metric | Value |
|----------|----------:|
| R² | 0.288 |
| Correlation | 0.596 |
| MAE | 0.000106 |

Future volatility exhibits meaningful predictability through:

- Intraday seasonality
- Volatility clustering
- Recent price range expansion

---

# Methodology

## Target Variable

Future realized volatility:

Future Volatility (15 Minutes)

= Std Dev of Returns

from t+1 to t+15

## Features

### Volatility Features

- 5-Minute Volatility
- 10-Minute Volatility
- 20-Minute Volatility

### Range Features

- 5-Minute Price Range

### Time Features

- Minute of Day

### Return Features

- 5-Minute Return
- 10-Minute Return

---

# Feature Correlation Analysis

Correlation with Future 15-Minute Volatility:

| Feature | Correlation |
|----------|----------:|
| Range (5m) | 0.345 |
| Volatility (20m) | 0.343 |
| Volatility (10m) | 0.315 |
| Volatility (5m) | 0.283 |
| Return (10m) | -0.025 |
| Return (5m) | -0.022 |
| Volatility Ratio | -0.017 |

## Key Finding

Returns contain almost no predictive power.

Volatility and recent trading range are the primary drivers of future volatility.

---

# Volatility Clustering Study

Current volatility was divided into quintiles.

## Results

| Volatility Bucket | Future 15m Volatility |
|----------|----------:|
| Very Low | 0.000205 |
| Low | 0.000261 |
| Medium | 0.000308 |
| High | 0.000370 |
| Very High | 0.000559 |

## Key Finding

Future volatility rises monotonically with current volatility.

The highest volatility regime experiences approximately **2.73x** the future volatility of the lowest volatility regime.

This confirms the existence of volatility clustering.

---

# Time-of-Day Analysis

Correlation:

**0.140**

Future volatility by time bucket:

| Period | Future Volatility |
|----------|----------:|
| Open | 0.000362 |
| Morning | 0.000264 |
| Midday | 0.000260 |
| Afternoon | 0.000305 |
| Close | 0.000511 |

## Key Finding

Volatility follows a clear U-shaped intraday profile:

**High → Low → High**

Volatility is highest near market open and close.

---

# Forecast Horizon Study

Multiple forecast horizons were evaluated.

| Horizon | R² | Correlation |
|----------|----------:|----------:|
| 5 Minutes | 0.089 | 0.516 |
| 10 Minutes | 0.227 | 0.572 |
| 15 Minutes | 0.288 | 0.595 |
| 30 Minutes | 0.253 | 0.574 |
| 60 Minutes | 0.272 | 0.576 |

## Key Finding

The 15-minute horizon produced the strongest forecasting performance.

This suggests volatility clustering is strongest over short-to-medium intraday timescales.

---

# Market Regime Analysis

Forecasting performance across different market regimes:

| Period | R² | Correlation |
|----------|----------:|----------:|
| 2015–2019 | 0.283 | 0.603 |
| 2020–2022 | 0.483 | 0.710 |
| 2023–2025 | 0.339 | 0.588 |

## Key Finding

Volatility forecasting remained effective across all market regimes.

The strongest performance occurred during 2020–2022, a period characterized by elevated market volatility.

---

# Feature Importance Analysis

## 2023–2025

| Feature | Importance |
|----------|----------:|
| Minute of Day | 0.449 |
| Volatility (20m) | 0.262 |
| Range (5m) | 0.181 |
| Volatility (10m) | 0.061 |
| Volatility (5m) | 0.048 |

## Key Finding

The model relies primarily on:

1. Intraday seasonality
2. Volatility clustering
3. Recent range expansion

Longer-term volatility measures consistently outperform shorter-term volatility measures.

---

# Comparison with Return Prediction

This project complements the earlier Intraday Momentum Research.

## Return Prediction

Predict Afternoon Returns from Morning Returns

Finding:

**Predictability weakened significantly after 2023.**

## Volatility Prediction

Predict Future Volatility from Current Market Conditions

Finding:

**Predictability remained stable across all market regimes.**

## Conclusion

Return predictability appears fragile and regime-dependent.

Volatility predictability appears structural and persistent.

---

# Project Outputs

## Plots


plots/
├── horizon_study.png
├── volatility_regime_performance.png
└── feature_importance_by_regime.png

## Results
results/
├── volatility_clustering.csv
├── horizon_study.csv
├── volatility_regime_performance.csv
└── feature_importance_by_regime.csv

## Findings


Finding 1

Future intraday volatility is predictable.

Finding 2

Volatility clustering is a persistent market characteristic.

Finding 3

The optimal forecasting horizon is approximately 15 minutes.

Finding 4

Intraday seasonality is the strongest predictor of future volatility.

Finding 5

Volatility forecasting remains robust across different market regimes.

Finding 6

Volatility predictability is considerably more stable than return predictability.
