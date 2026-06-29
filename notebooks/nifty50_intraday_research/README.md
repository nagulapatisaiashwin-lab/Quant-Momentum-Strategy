# NIFTY 50 Intraday Research Project (2015–2025)

## Overview

This project investigates whether NIFTY 50 minute-level data contains persistent intraday trading opportunities that can be converted into systematic trading strategies.

Rather than optimizing a single strategy, the objective was to study how information propagates through financial markets and determine which intraday effects remain robust across different market environments.

The research followed a quantitative workflow:

Hypothesis
    ↓
Backtest
    ↓
Remove Bias
    ↓
Validate Across Regimes
    ↓
Accept or Reject
```

The project evolved from strategy development into a broader study of:

- Intraday Momentum
- Volatility Regimes
- Market Structure
- Signal Persistence
- Market Efficiency
- Strategy Decay

---

# Dataset

| Item | Value |
|--------|--------|
| Instrument | NIFTY 50 Index |
| Frequency | 1 Minute |
| Period | 2015–2025 |

Available Fields:

- Open
- High
- Low
- Close
- Volume

---

# Data Cleaning

To ensure consistency across all experiments:

- Restricted data to regular NSE trading hours (09:15–15:29)
- Removed special trading sessions (e.g. Muhurat Trading)
- Removed duplicate timestamps
- Verified data integrity after cleaning

Robustness checks showed that the major findings remained materially unchanged after data cleaning.

## Limitation

The volume column contained only zeros.

As a result, volume-based research could not be performed:

- VWAP
- Volume Profile
- OBV
- Order Flow Models
- Volume Breakout Strategies

The project therefore focused exclusively on:

- Price
- Returns
- Volatility
- Market Structure

---

# Research Roadmap

The project was conducted through a sequence of focused research studies.

| Notebook | Topic |
|-----------|-----------|
| 01 | Data Preparation & Exploration |
| 02 | Opening Range Research |
| 03 | Morning Momentum Research |
| 04 | Gap Analysis |
| 05 | Volatility Regime Analysis |
| 06 | Time-of-Day Analysis |
| 07 | Intraday Momentum Chain |
| 08 | Compression + Momentum Study |
| 09 | Volatility-Adjusted Momentum |
| 10 | Strategy Validation |
| 11 | Z-Score Event Study |
| 12 | Signal Decay Analysis |

Each hypothesis was independently evaluated and classified as accepted, partially accepted, or rejected.

---

# Research Outcomes

## Accepted

🟢 Opening Range Compression

🟢 Morning Momentum

🟢 Volatility Regime Effects

🟢 Volatility-Adjusted Momentum

🟢 Signal Persistence

🟢 Long/Short Asymmetry

🟢 Overnight Persistence

🟢 Time-of-Day Effects

---

## Partially Accepted

🟡 Afternoon Momentum

🟡 Momentum Propagation

🟡 Z-Score Event Effects

---

## Rejected

🔴 EMA Trend Following

🔴 Basic Opening Range Breakout

🔴 Gap-Based Signals

🔴 Compression + Momentum Combination

---

# Key Findings

## 1. Morning Momentum Exists

### Research Question

Do morning returns predict afternoon returns?

### Finding

Strong morning moves tended to continue into the afternoon.

Weak Morning Move
→ Weak Afternoon Move

Strong Morning Move
→ Strong Afternoon Move

### Verdict

🟢 Accepted

Morning price action contains predictive information about same-day returns.

---

## 2. Signal Strength Matters

Stronger signals produced substantially better results.

| Threshold | Trades | Profit Factor |
|-----------|---------:|---------:|
| 0.25% | 1333 | 1.17 |
| 0.50% | 583 | 1.29 |
| 0.75% | 233 | 1.53 |
| 1.00% | 89 | 1.63 |

### Interpretation

Higher thresholds improve signal quality but reduce trade frequency.

The strongest signals contain the most information.

### Verdict

🟢 Accepted

---

## 3. Volatility Regime Matters

### Research Question

Does volatility influence momentum performance?

### Results

| Regime | Profit Factor | Avg Trade |
|---------|---------:|---------:|
| Low Volatility | 1.07 | 0.016% |
| Medium Volatility | 1.50 | 0.116% |
| High Volatility | 1.63 | 0.206% |

### Key Insight

The problem was not that high volatility was exceptional.

The problem was that low volatility significantly weakened momentum.

### Verdict

🟢 Accepted

Volatility is an important market filter.

---

## 4. Volatility Adjustment Improves Momentum

### Motivation

A 0.75% move does not carry the same information in different volatility environments.

Instead of:

```text
Signal = Return
```

Use:


Signal = Return / Volatility


### Finding

Volatility-adjusted momentum produced cleaner relationships with future returns.

### Verdict

🟢 Accepted

Risk-adjusted signals outperform raw signals.

---

## 5. Long Signals Dominate Short Signals

### Results

| Side | Trades | Avg Return | Win Rate |
|--------|--------:|--------:|--------:|
| Long | 55 | 0.363% | 67.3% |
| Short | 114 | -0.130% | 40.4% |

### Interpretation

Most profitability originated from long trades.

This behaviour is consistent with the long-term upward drift of equity indices.

### Verdict

🟢 Accepted

The momentum effect is materially stronger on the long side.

---

## 6. Signal Persistence

### Research Question

How long does the signal remain effective?

| Exit Time | Avg Return | Win Rate | Profit Factor |
|------------|------------:|------------:|------------:|
| 11:30 | 0.036% | 55.0% | 1.55 |
| 12:00 | 0.047% | 55.6% | 1.47 |
| 13:00 | 0.086% | 54.4% | 1.63 |
| 14:00 | 0.135% | 58.6% | 1.84 |
| 15:15 | 0.206% | 62.1% | 2.10 |

### Key Finding

Predictive strength increased throughout the trading day.

The signal did not decay.

Instead, information appeared to diffuse gradually through the market.

### Verdict

🟢 Accepted

---

## 7. Overnight Persistence

### Research Question

Does the signal survive beyond the close?

| Exit | Avg Return | Win Rate | Profit Factor |
|--------|--------:|--------:|--------:|
| Same-Day Close | 0.363% | 67.3% | 3.18 |
| Next-Day Open | 0.569% | 72.7% | 5.55 |
| Next-Day Close | 0.290% | 62.3% | 1.99 |

### Key Finding

The strongest performance occurred between:

```text
11:00 Day T
        ↓
09:15 Day T+1
```

The signal survives overnight but weakens during the following trading session.

### Verdict

🟢 Accepted

---

# Best Strategy Discovered

## Volatility-Adjusted Morning Momentum

### Signal


Signal = Morning Return / 20-Day Volatility

![Volatility Adjusted Momentum Strategy](results/strategy_equity_curve.png)

### Entry

At 11:00

- Long if Signal > 1.0
- Short if Signal < -1.0

### Exit

15:15 Close

### Transaction Cost

0.05%

### Performance

| Metric | Value |
|----------|----------:|
| Trades | 169 |
| Total Return | 40.64% |
| CAGR | 3.34% |
| Sharpe | 0.96 |
| Profit Factor | 2.10 |
| Win Rate | 62.13% |
| Max Drawdown | -4.12% |

Sharpe ratio is annualized using the average number of trades per year.

This was the strongest intraday strategy discovered during the research process.

---

# Strategy Decay & Market Efficiency

The strongest finding of the entire project was not a trading strategy.

It was the gradual deterioration of the underlying relationship between morning and afternoon returns.

## Morning vs Afternoon Correlation

| Period | Correlation |
|----------|----------:|
| 2015–2019 | 0.165 |
| 2020–2022 | 0.128 |
| 2023–2025 | 0.059 |

## Interpretation

The decline occurred despite:

- Volatility Filtering
- Volatility Normalization
- Threshold Optimization

This suggests that the predictive relationship itself weakened over time.

The strategy did not fail because of implementation.

The strategy weakened because the predictive relationship between morning and afternoon returns deteriorated over time.

---

# Market Regime Assessment

## 2015–2019

Characteristics:

- Strong Momentum
- Strong Continuation
- High Signal Quality

Assessment:

Momentum-based intraday trading worked extremely well.

---

## 2020–2022

Characteristics:

- High Volatility
- Strong Momentum
- Excellent Signal Quality

Assessment:

The momentum edge remained robust despite elevated market volatility.

---

## 2023–2025

Characteristics:

- Flat Performance
- Sharpe ≈ 0
- Profit Factor ≈ 1

Assessment:

The momentum edge appears to have been largely arbitraged away.

---

# Rejected Ideas

The following concepts failed to demonstrate robust performance:

### EMA Trend Following

🔴 Rejected

Simple moving-average alignment did not produce a reliable intraday edge.

### Opening Range Breakout

🔴 Rejected

Raw breakouts contained little predictive information.

### Gap-Based Signals

🔴 Rejected

Overnight gap size alone was not a useful forecasting variable.

### Compression + Momentum

🔴 Rejected

Combining two individually promising ideas reduced overall performance.

---

# Limitations

- Research was conducted exclusively on the NIFTY 50 index.
- Transaction costs were simplified.
- Slippage was not explicitly modeled.
- Volume-based studies were not possible due to missing volume information.
- Findings may not generalize to all market environments.

---


## Possible Causes of Strategy Decay

The decline in predictive power after 2023 cannot be explained solely by parameter selection or implementation choices.

Several structural explanations are plausible:

- Increased market efficiency
- Faster information dissemination
- Greater adoption of quantitative trading
- Strategy crowding
- Reduced volatility relative to the 2020–2022 period
- Growth in institutional participation

Each of these factors could accelerate the incorporation of information into prices, reducing the persistence of intraday momentum effects.

While the exact cause cannot be identified from this dataset alone, the evidence suggests that the market became progressively more efficient over time.

# Related Project

A follow-up project investigates:

```text
Intraday Volatility Forecasting
```

using the same NIFTY 50 minute-level dataset.

Unlike return forecasting, volatility forecasting remained robust across all market regimes and exhibited significantly greater stability after 2023.

---

# Key Takeaway

This project began as a search for profitable intraday trading strategies.

Several statistically significant effects were identified:

- Morning Momentum
- Volatility Regimes
- Signal Persistence
- Volatility-Adjusted Momentum

The strongest strategy discovered was Volatility-Adjusted Morning Momentum.

However, the most important finding was not the strategy itself.

The most important finding was that the underlying relationship between morning and afternoon returns weakened substantially after 2023.

This highlights an important lesson in quantitative research:

> Finding an edge is not enough. Understanding how and why an edge decays is equally important.

The project ultimately evolved from strategy development into a study of information propagation, market efficiency, and strategy decay in financial markets.