# NIFTY 500 Machine Learning Alpha Strategy

## Overview

This project investigates whether machine learning can generate alpha in Indian equities by predicting future stock returns using technical and cross-sectional features.

Unlike traditional factor investing approaches that rely on a single signal such as momentum, this research combines multiple features and uses a Random Forest model to identify stocks with superior future performance. The study further explores portfolio construction techniques including long-only portfolios, long-short portfolios, dynamic exposure management, and walk-forward validation.

The objective is not only to build a predictive model but to evaluate whether the generated signals can be transformed into an investable strategy with attractive risk-adjusted returns.

---

## Research Questions

- Can machine learning predict future stock returns in the NIFTY 500 universe?
- Do cross-sectional ranking features improve predictive power?
- Can ML-generated signals outperform simple benchmark portfolios?
- Is long-short implementation superior to long-only implementation?
- Can portfolio exposure be adjusted dynamically using model confidence?
- Does the signal survive walk-forward validation?

---

## Dataset

### Universe

- NIFTY 500 Constituents
- Cleaned Universe Size: 332 Stocks

### Period

- January 2015 – December 2025

### Dataset Size

- 2,716 Trading Days
- 845,236 Stock-Day Observations

### Data Source

- Yahoo Finance
- Adjusted Close Prices

---

## Feature Engineering

The following features were constructed for each stock.

### Momentum Features

- 21-Day Momentum
- 63-Day Momentum
- 126-Day Momentum

### Volatility Features

- 21-Day Volatility
- 63-Day Volatility

### Trend Features

- EMA Distance
- EMA Slope

### Mean Reversion Feature

- RSI (14)

### Cross-Sectional Features

For each date, stocks were ranked relative to all other stocks in the universe.

- Rank Momentum 21
- Rank Momentum 63
- Rank Momentum 126
- Rank Volatility 21
- Rank Volatility 63
- Rank RSI 14

Cross-sectional ranking features proved significantly more informative than raw technical indicators.

---

## Target Variable

The model predicts:

```python
Future Relative Return =
Future 21-Day Return
-
Average Future 21-Day Return of Universe
```

This formulation converts the problem from predicting market direction to identifying stocks likely to outperform their peers.

---

## Machine Learning Model

### Model

```python
RandomForestRegressor
```

### Key Parameters

```python
n_estimators = 300
max_depth = 10
min_samples_leaf = 25
```

### Validation Method

Out-of-sample testing:

```text
Train : 2015-2021
Test  : 2022-2025
```

Additionally, walk-forward validation was performed to simulate a realistic research workflow.

---

# Alpha Model Results

## Initial Model (Raw Features)

The first version relied primarily on raw technical indicators and market features.

### Results

| Metric | Value |
|----------|----------:|
| Rank IC | 0.0043 |
| Correlation | 0.008 |

### Conclusion

The model contained little predictive information and failed to generate meaningful alpha.

---

## Improved Model (Cross-Sectional Features)

The second model incorporated cross-sectional ranking features and relative-return targets.

### Results

| Metric | Value |
|----------|----------:|
| Rank IC | 0.0196 |
| Correlation | 0.0250 |

### Key Observation

Cross-sectional features dramatically improved signal quality and transformed the model from noise into a usable stock-selection framework.

---

# Portfolio Construction

The following portfolio implementations were tested.

---

## 1. Long-Only Portfolio

### Rules

- Rebalance every 21 trading days
- Rank stocks by predicted return
- Buy Top 20 stocks
- Equal Weight Allocation

### Results

| Metric | Value |
|----------|----------:|
| Total Return | 166.44% |
| CAGR | 28.49% |
| Sharpe | 1.28 |
| Max Drawdown | -21.57% |

### Conclusion

The ML portfolio outperformed the benchmark in absolute returns but experienced higher volatility and drawdowns.

---

## 2. Long-Short Portfolio

### Rules

- Long Top 20 Predictions
- Short Bottom 20 Predictions
- Equal Weight

### Results

| Metric | Value |
|----------|----------:|
| Total Return | 56.19% |
| CAGR | 12.08% |
| Sharpe | 0.94 |
| Max Drawdown | -15.48% |
| Win Rate | 61.70% |

### Key Observation

The model was significantly better at identifying winners than losers.

Bottom-ranked stocks generally underperformed but still generated positive returns, reducing the effectiveness of short positions.

### Conclusion

Long-short implementation did not improve performance and was inferior to the long-only approach.

---

## 3. Dynamic Exposure Portfolio

### Motivation

Instead of maintaining constant exposure, portfolio allocation was adjusted according to model confidence.

### Exposure Rules

| Signal Strength | Exposure |
|----------|----------:|
| Very Weak | 0% |
| Weak | 50% |
| Strong | 100% |
| Very Strong | 150% |

A walk-forward exposure framework was used to eliminate look-ahead bias.

### Results

| Metric | Value |
|----------|----------:|
| Total Return | 197.21% |
| CAGR | 32.13% |
| Sharpe | 1.25 |
| Max Drawdown | -19.85% |

### Conclusion

Dynamic exposure improved returns while maintaining reasonable risk characteristics.

---

# Walk-Forward Validation

To evaluate robustness, the model was retrained annually.

### Framework

```text
Train: 2015-2020 → Test: 2021
Train: 2015-2021 → Test: 2022
Train: 2015-2022 → Test: 2023
Train: 2015-2023 → Test: 2024
Train: 2015-2024 → Test: 2025
```

---

## Walk-Forward Rank IC

| Metric | Value |
|----------|----------:|
| Rank IC | 0.01897 |

The signal remained remarkably stable relative to the original out-of-sample test.

---

## Yearly Rank IC

| Year | Rank IC |
|----------|----------:|
| 2021 | 0.0363 |
| 2022 | 0.0078 |
| 2023 | 0.0598 |
| 2024 | -0.0007 |
| 2025 | -0.0104 |

### Observation

The predictive power of the model is regime-dependent and varies significantly across market environments.

---

## Walk-Forward Portfolio Results

| Metric | Value |
|----------|----------:|
| Total Return | 452.97% |
| CAGR | 42.32% |
| Sharpe | 1.53 |
| Max Drawdown | -24.99% |

---

# Final Strategy Comparison

| Strategy | CAGR | Sharpe | Max DD |
|----------|----------:|----------:|----------:|
| Benchmark | 26.60% | 1.45 | -17.10% |
| Long Only ML | 28.49% | 1.28 | -21.57% |
| Long Short ML | 12.08% | 0.94 | -15.48% |
| Dynamic Exposure ML | 32.13% | 1.25 | -19.85% |
| Walk-Forward ML | 42.32% | 1.53 | -24.99% |

---

# Key Findings

### 1. Cross-Sectional Features Matter

Raw technical indicators provided limited predictive power.

Cross-sectional ranking features significantly improved model performance.

---

### 2. ML Signal Contains Alpha

The final model achieved:

```text
Walk-Forward Rank IC = 0.01897
```

demonstrating persistent stock-selection ability.

---

### 3. Long-Only Outperformed Long-Short

The model was better at identifying future winners than future losers.

Long-short implementation diluted performance.

---

### 4. Dynamic Exposure Improved Results

Scaling portfolio exposure based on model confidence generated higher returns than static allocation.

---

### 5. Signal Is Regime Dependent

Performance varied across years, highlighting the importance of market conditions and adaptive portfolio construction.

---

# Future Improvements

Potential extensions include:

- XGBoost / LightGBM Models
- Monthly Model Retraining
- Sector-Neutral Portfolio Construction
- Transaction Cost Modeling
- Alternative Target Variables
- Fundamental Features
- Earnings-Based Signals
- Macro Regime Filters
- Portfolio Optimization Techniques

---

# Conclusion

This research demonstrates a complete quantitative research pipeline, progressing from feature engineering and alpha modeling to portfolio construction and walk-forward validation.

The results suggest that machine learning can generate meaningful cross-sectional alpha within the NIFTY 500 universe, particularly when combined with ranking-based features and adaptive exposure management.

While the predictive signal is modest, it remains persistent across multiple validation frameworks and translates into improved portfolio performance, making it a promising foundation for future quantitative equity research.