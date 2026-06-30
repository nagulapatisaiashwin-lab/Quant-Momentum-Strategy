# NIFTY500 Factor Investing Research

A quantitative research project exploring factor investing, momentum strategies, factor timing, dynamic capital allocation, and portfolio construction in the Indian equity market.

---

## Project Overview

This project follows a complete quantitative research workflow:

Data Collection
    ↓
Factor Discovery
    ↓
IC Analysis
    ↓
Portfolio Construction
    ↓
Portfolio Optimization
    ↓
Transaction Cost Analysis
    ↓
Market Regime Analysis
    ↓
Volatility Regime Analysis
    ↓
Factor Timing
    ↓
Dynamic Allocation


Universe: **NIFTY500**

Period: **2015–2025**

Frequency: **Daily**

---

# Key Research Finding

The strongest result was not the momentum factor itself.

A **Factor Strength** signal was developed:


Factor Strength
=
Mean(Top 20 Momentum Scores)
-
Mean(Bottom 20 Momentum Scores)
```

This signal was used to dynamically adjust portfolio exposure.

The research shows that capital allocation based on factor conditions can materially improve performance without materially increasing average portfolio leverage.

---

# Strategy Evolution

## Baseline Strategy

- Factor: Momentum126
- Portfolio: Top 20 Stocks
- Equal Weight
- Rebalance Every 42 Trading Days
- Transaction Cost: 0.10%

Result:

| Metric | Value |
|----------|----------:|
| CAGR | 40.39% |
| Sharpe | 1.38 |
| Max Drawdown | -28.45% |

---

# Dynamic Allocation Variants

Instead of a single "best" model, multiple allocation profiles were evaluated.

| Strategy | Exposure Range | CAGR | Sharpe | MaxDD |
|----------|----------|----------:|----------:|----------:|
| Baseline | 1.00x | 40.39% | 1.38 | -28.45% |
| Conservative | 0.75x → 1.25x | 43.19% | 1.38 | -30.33% |
| Balanced | 0.50x → 1.50x | 45.82% | 1.36 | -32.35% |
| Aggressive | 0.00x → 2.00x | 50.55% | 1.29 | -36.76% |

### Interpretation

**Conservative**

- Highest Sharpe Ratio
- Smallest increase in drawdown
- Most stable implementation

**Balanced**

- Strong CAGR improvement
- Moderate drawdown increase
- Best risk-return compromise

**Aggressive**

- Highest CAGR
- Highest Profit Factor
- Largest drawdown
- Suitable for growth-oriented investors

---

## Allocation Variant Comparison

[Allocation Variants](results/plots/08_allocation_variants.png)

This figure illustrates how progressively wider exposure ranges improve CAGR while increasing portfolio volatility and drawdown.

---

# Dynamic Exposure Profiles

![Exposure Profiles](results/plots/08_exposure_profiles.png)

Exposure is determined by Factor Strength and varies through time according to market conditions.

Average exposure remained close to 1x across all tested variants.

---

# Exposure vs Factor Strength

![Exposure vs Factor Strength](results/plots/08_exposure_vs_factor_strength.png)

Exposure increases monotonically with Factor Strength.

This confirms that capital allocation responds systematically to factor conditions.

---

# Momentum Strategy vs Benchmark

![Strategy vs Benchmark](results/plots/03_strategy_vs_benchmark.png)

Baseline Momentum126 strategy before dynamic allocation.

---

# Factor Discovery

Multiple candidate factors were constructed and evaluated.

## Factors Tested

- Momentum63
- Momentum126
- Relative Strength
- Trend Strength
- Breakout
- Volatility
- Volume Trend

### Mean IC Results

| Factor | Mean IC |
|----------|----------:|
| Momentum126 | 0.0427 |
| TrendStrength | 0.0358 |
| Momentum63 | 0.0258 |
| RelativeStrength | 0.0258 |
| Breakout | 0.0239 |
| Volatility | -0.0019 |
| VolumeTrend | -0.0049 |

### Key Finding

Momentum126 emerged as the strongest and most consistent factor.

---

# Portfolio Construction

Portfolio Rules:

- Rank stocks using Momentum126
- Select Top 20 Stocks
- Equal Weight Allocation
- 42-Day Rebalancing

### Portfolio Size Analysis

| Portfolio Size | Top-Bottom Spread |
|----------|----------:|
| Top 5 | 2.26% |
| Top 10 | 4.43% |
| Top 20 | 4.42% |
| Top 30 | 3.94% |
| Top 50 | 3.13% |

### Key Finding

Top 20 provided the best balance between return and diversification.


# Rebalance Frequency Analysis

Rebalancing frequencies tested:

- 21 Days
- 42 Days
- 63 Days
- 126 Days

| Frequency | CAGR | Sharpe |
|----------|----------:|----------:|
| 21D | 40.10% | 1.40 |
| 42D | 40.79% | 1.39 |
| 63D | 37.21% | 1.17 |
| 126D | 36.01% | 1.14 |

### Key Finding

42-Day Rebalancing delivered the strongest overall performance.

---

# Transaction Cost Analysis

Transaction costs tested:

- 0.05%
- 0.10%
- 0.25%
- 0.50%

Average Portfolio Turnover:


54.4%
```

### Key Finding

The strategy remained robust under realistic transaction cost assumptions.

---

# Market Regime Analysis

Momentum performance was analyzed across:

- Bull Markets
- Bear Markets

### Key Finding

Momentum remained effective in both environments.

Restricting trading to bull markets reduced performance.

---

# Volatility Regime Analysis

Market volatility was classified into:

- Low Volatility
- Medium Volatility
- High Volatility

### Key Finding

High-volatility periods exhibited stronger momentum returns.

However, filtering trades using volatility regimes reduced overall performance.

---

# Factor Timing Research

This notebook contains the primary contribution of the project.

### Research Question

Can factor strength predict future momentum performance?

### Findings

- Positive correlation between Factor Strength and future returns
- Stronger factor environments generated higher future momentum profits
- Dynamic allocation improved portfolio performance

### Conclusion

Factor Strength contains useful predictive information and can be used as a dynamic capital allocation signal.

---

# Market Extremes Research

Market Stretch was defined as:

```text
Market Stretch
=
Market Index / MA252 - 1
```

### Findings

- Correlation: -0.1587
- Oversold markets generated stronger future returns
- Evidence of mean reversion observed

However, incorporating Market Stretch into the allocation framework did not improve momentum performance.

---

# Combined Allocation Model

Combined:

- Factor Strength Timing
- Market Stretch Timing

### Result

The combined model underperformed pure Factor Strength Allocation.

Final allocation framework therefore uses Factor Strength only.

---

# Repository Structure

```text
nifty500_strategy/

├── data/
│
├── notebooks/
│   ├── 01_DATA_COLLECTION.ipynb
│   ├── 02_FACTOR_ZOO.ipynb
│   ├── 03_PORTFOLIO_CONSTRUCTION.ipynb
│   ├── 04_REBALANCE_FREQUENCY_ANALYSIS.ipynb
│   ├── 05_TRANSACTION_COSTS_AND_TURNOVER.ipynb
│   ├── 06_MARKET_REGIME_ANALYSIS.ipynb
│   ├── 07_VOLATILITY_REGIME_ANALYSIS.ipynb
│   ├── [MAIN]_08_FACTOR_TIMING_RESEARCH.ipynb
│   ├── 09_MARKET_EXTREMES_RESEARCH.ipynb
│   └── 10_COMBINED_ALLOCATION_MODEL.ipynb
│
├── results/
│   ├── plots/
│   └── tables/
│
└── README.md
```

---


## Disclaimer

This project is intended for educational and research purposes only and does not constitute investment advice.