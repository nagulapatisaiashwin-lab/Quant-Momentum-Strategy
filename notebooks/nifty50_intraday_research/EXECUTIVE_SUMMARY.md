# NIFTY Intraday Research Project (2015–2025)

## Executive Summary

This project investigates whether NIFTY 1-minute data contains exploitable intraday trading opportunities.

Research was conducted on over 10 years of minute-level market data using a systematic quantitative workflow:

Hypothesis → Backtest → Validation → Regime Analysis → Conclusion

---

# Dataset

| Item | Value |
|--------|--------|
| Instrument | NIFTY Index |
| Frequency | 1 Minute |
| Period | 2015–2025 |

Data was cleaned to include only regular NSE trading hours (09:15–15:29).

---

# Main Research Findings

## Morning Momentum Exists

Morning returns contain predictive information about afternoon returns.

| Morning Return Bucket | Avg Afternoon Return |
|----------------------|---------------------:|
| < -1% | -0.18% |
| -1% to -0.5% | -0.09% |
| -0.5% to 0% | -0.04% |
| 0% to 0.5% | 0.01% |
| 0.5% to 1% | 0.12% |
| > 1% | 0.45% |

Stronger morning moves consistently lead to stronger afternoon moves.

---

## Volatility Matters

Momentum performs substantially better in higher-volatility environments.

| Regime | Profit Factor |
|---------|---------:|
| Low Volatility | 1.07 |
| Medium Volatility | 1.50 |
| High Volatility | 1.63 |

Low-volatility environments suppress momentum.

---

## Signal Persistence

The information contained in morning momentum signals persists throughout the trading day.

| Exit Time | Profit Factor |
|------------|------------:|
| 11:30 | 1.55 |
| 12:00 | 1.47 |
| 13:00 | 1.63 |
| 14:00 | 1.84 |
| 15:15 | 2.10 |

The strongest same-day edge occurs near the close.

---

## Long Signals Are Stronger

| Side | Profit Factor |
|--------|--------:|
| Long | 3.18 |
| Short | 1.66 |

Most profitability originates from long signals.

---

# Best Strategy

## Volatility-Adjusted Morning Momentum

### Signal

Signal = Morning Return / 20-Day Volatility

### Entry

11:00 AM

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
| Total Return | 29.27% |
| CAGR | 2.51% |
| Sharpe | 0.73 |
| Profit Factor | 1.75 |
| Win Rate | 57.4% |
| Max Drawdown | -4.80% |
| Average Trade | 0.16% |

---

# Regime Performance

| Period | Sharpe | Profit Factor |
|---------|---------:|---------:|
| 2015–2019 | 1.02 | 2.20 |
| 2020–2022 | 0.88 | 2.16 |
| 2023–2025 | 0.00 | 1.00 |

Performance deteriorated significantly after 2023.

---

# Most Important Discovery

The strategy weakened because the underlying predictive relationship weakened.

### Morning vs Afternoon Correlation

| Period | Correlation |
|----------|----------:|
| 2015–2019 | 0.165 |
| 2020–2022 | 0.128 |
| 2023–2025 | 0.059 |

Correlation declined by approximately 64% over the sample period.

The result remained unchanged after data-cleaning and robustness checks.

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

# Key Takeaway

The project confirmed the existence of a genuine intraday momentum effect in NIFTY data, particularly between 2015 and 2022.

However, the most important finding was not the strategy itself.

The most important finding was that the predictive relationship between morning and afternoon returns weakened substantially after 2023.

This project ultimately evolved from strategy development into a study of how market efficiency changes over time.