# Statistical Arbitrage in Indian Equities

## Overview

This project investigates whether statistical arbitrage opportunities exist among NIFTY 50 stocks using correlation, cointegration, stationarity testing, and mean-reversion trading strategies.

Rather than stopping at an apparently profitable backtest, the research progressively removes assumptions and sources of bias to evaluate how robust the strategy remains under increasingly realistic conditions.

The project evolves through seven stages:

1. Correlation Screening
2. Pair Discovery
3. In-Sample Multi-Pair Portfolio
4. Out-of-Sample Validation
5. Parameter Robustness Testing
6. Walk-Forward Backtesting
7. Dynamic Pair Selection

---

## Dataset

- Universe: NIFTY 50 Stocks
- Frequency: Daily Data
- Period: January 2020 – June 2026
- Market: NSE India

---

# Research Methodology

## 02. Pair Discovery

### Objective

Identify statistically valid mean-reverting pairs.

### Tests Used

#### Engle-Granger Cointegration Test

Tests whether two non-stationary price series maintain a stable long-run equilibrium.

#### Augmented Dickey-Fuller Test

Tests whether the spread between two assets is stationary.

### Pair Selection Criteria

```text
Cointegration p-value < 0.05
ADF p-value < 0.05
```

### Assumptions

- Historical cointegration persists
- Stationary spreads continue to mean-revert

### Limitations

- Relationships may break due to changing market regimes
- Cointegration can disappear over time

---

## 03. In-Sample Multi-Pair Portfolio

### Objective

Trade multiple pairs simultaneously.

### Trading Logic

#### Spread Construction

```text
Spread = Stock1 − β × Stock2
```

#### Signal Generation

```text
Z-Score < -2  → Long Spread
Z-Score > 2   → Short Spread
Z-Score = 0   → Exit
```

### Portfolio Construction

- Equal weight active pairs
- Returns averaged across open positions

### Assumptions

- Pair selection uses entire dataset
- Hedge ratio estimated on full dataset
- Spread mean estimated on full dataset
- Spread volatility estimated on full dataset

### Neglected Factors

- Look-ahead bias
- Data snooping bias
- Relationship instability

### Conclusion

Useful for hypothesis generation only.

Not suitable for evaluating real performance.

---

## 04. Out-of-Sample Validation

### Train Period

```text
2020-2023
```

### Test Period

```text
2024-2026
```

Pairs are discovered exclusively using training data and traded on unseen data.

### Results

| Metric | Value |
|----------|----------|
| Total Return | 239.83% |
| CAGR | 65.08% |
| Sharpe Ratio | 2.39 |
| Max Drawdown | -18.47% |

### Improvements

Removed:

- Pair selection leakage
- Major data snooping bias

### Remaining Assumptions

- Hedge ratio estimated on entire test period
- Spread mean estimated on entire test period
- Spread volatility estimated on entire test period

### Remaining Bias

Moderate look-ahead bias.

---

## 05. Parameter Robustness

### Objective

Evaluate sensitivity to entry thresholds.

### Thresholds Tested

```text
1.5
2.0
2.5
```

### Results

| Entry Z | CAGR | Sharpe | Max DD |
|----------|----------|----------|----------|
| 1.5 | 57.81% | 2.25 | -12.14% |
| 2.0 | 65.08% | 2.39 | -18.47% |
| 2.5 | 49.45% | 2.39 | -8.48% |

### Findings

Performance remained positive across multiple thresholds.

This suggests the strategy was not dependent on a single parameter choice.

### Assumptions

Same assumptions as Notebook 04.

---

## 06. Walk-Forward Statistical Arbitrage

### Objective

Remove remaining look-ahead bias.

### Improvements

Instead of using future information:

```text
Static Beta
Static Mean
Static Standard Deviation
```

This version uses:

```text
252-Day Rolling Beta
252-Day Rolling Mean
252-Day Rolling Standard Deviation
```

Signals are generated using only historical information available at the time.

### Results

| Metric | Value |
|----------|----------|
| Total Return | 24.08% |
| CAGR | 9.24% |
| Sharpe Ratio | 0.58 |
| Max Drawdown | -29.02% |

### Key Finding

Performance deteriorated significantly once future information was removed.

### Interpretation

A substantial portion of the apparent edge observed in earlier versions was driven by static parameter estimation and look-ahead effects.

---

## 07. Dynamic Pair Selection

### Objective

Account for changing market relationships.

### Procedure

For each year:

```text
Train 2020-2023 → Trade 2024
Train 2021-2024 → Trade 2025
Train 2022-2025 → Trade 2026
```

Pairs are rediscovered using only historical information before each trading period.

### Results

| Metric | Value |
|----------|----------|
| Total Return | 18.17% |
| CAGR | 7.08% |
| Sharpe Ratio | 0.41 |
| Max Drawdown | -39.83% |

### Key Finding

Dynamic pair selection did not improve performance.

### Interpretation

Pair relationships exhibit significant instability and regime dependence.

---

# Assumptions and Simplifications

The following factors were intentionally ignored throughout the study:

## Transaction Costs

Assumed to be zero.

Ignored:

- Brokerage
- Slippage
- Bid-Ask Spread
- Market Impact

## Short Selling

Assumed unlimited ability to short stocks.

## Liquidity

Assumed all trades can be executed at closing prices.

## Corporate Actions

Assumed data correctly incorporates:

- Stock splits
- Bonus issues
- Dividends

## Execution

Signals generated today are executed on the next trading day.

---

# Key Research Findings

1. Correlation alone is insufficient for pair selection.
2. Cointegration and stationarity provide stronger pair candidates.
3. In-sample results can be highly misleading.
4. Out-of-sample testing is essential.
5. Parameter robustness does not guarantee true robustness.
6. Walk-forward testing significantly reduces apparent performance.
7. Pair relationships decay over time.
8. Realistic statistical arbitrage is substantially more difficult than simple backtests suggest.

---

| Stage             |   CAGR | Sharpe |
| ----------------- | -----: | -----: |
| Out-of-Sample     | 65.08% |   2.39 |
| Walk-Forward      |  9.24% |   0.58 |
| Dynamic Selection |  7.08% |   0.41 |


# Final Conclusion

Initial experiments suggested a highly profitable statistical arbitrage strategy. However, progressively removing assumptions and reducing look-ahead bias resulted in a substantial decline in performance.

The research demonstrates the importance of:

- Out-of-sample testing
- Walk-forward validation
- Robust parameter estimation
- Bias detection
- Regime awareness

While simple mean-reversion strategies appeared attractive under static assumptions, their effectiveness weakened considerably under realistic trading conditions.

The project therefore serves both as a statistical arbitrage study and as an illustration of how rigorous validation can dramatically change conclusions in quantitative finance.

---

# Project Structure

```text
pairs_trading_statistical_arbitrage/

│
├── 01_CORRELATION_SCREENING.ipynb
├── 02_PAIR_DISCOVERY.ipynb
├── 03_IN_SAMPLE_MULTI_PAIR_PORTFOLIO.ipynb
├── 04_ROBUSTNESS_TESTS.ipynb
├── 05_PARAMETER_ROBUSTNESS.ipynb
├── 06_WALK_FORWARD_STAT_ARB.ipynb
├── 07_DYNAMIC_PAIR_SELECTION.ipynb
│
├── selected_pairs_train.csv
├── parameter_robustness.csv
├── walk_forward_results.csv
├── dynamic_selection_results.csv
│
└── nifty50_comp_price_data.csv
```