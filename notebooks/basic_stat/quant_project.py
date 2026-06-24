import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# =====================================
# STEP 1 : DOWNLOAD DATA
# =====================================

ticker = "AAPL"

data = yf.download(
    ticker,
    start="2022-01-01",
    end="2025-01-01",
    auto_adjust=True
)

print("\nFirst 5 Rows")
print(data.head())

# =====================================
# STEP 2 : DAILY RETURNS
# =====================================

data["Return"] = data["Close"].pct_change()

# =====================================
# STEP 3 : MOVING AVERAGES
# =====================================

data["SMA20"] = data["Close"].rolling(20).mean()

data["SMA50"] = data["Close"].rolling(50).mean()

# =====================================
# STEP 4 : GENERATE SIGNALS
# =====================================

data["Signal"] = np.where(
    data["SMA20"] > data["SMA50"],
    1,
    0
)

# =====================================
# STEP 5 : STRATEGY RETURNS
# =====================================

data["Strategy_Return"] = (
    data["Return"]
    * data["Signal"].shift(1)
)

# =====================================
# STEP 6 : CUMULATIVE RETURNS
# =====================================


data["Market_Cumulative"] = (
    1 + data["Return"]
).cumprod()

data["Strategy_Cumulative"] = (
    1 + data["Strategy_Return"]
).cumprod()

# =====================================
# STEP 7 : SHARPE RATIO
# =====================================

strategy_returns = data["Strategy_Return"].dropna()

sharpe_ratio = (
    strategy_returns.mean()
    /
    strategy_returns.std()
) * np.sqrt(252)

print("\nSharpe Ratio")
print(round(sharpe_ratio, 3))

# =====================================
# STEP 8 : TOTAL RETURN
# =====================================

market_return = (
    data["Market_Cumulative"].iloc[-1] - 1
) * 100

strategy_return = (
    data["Strategy_Cumulative"].iloc[-1] - 1
) * 100

print("\nMarket Return (%)")
print(round(market_return, 2))

print("\nStrategy Return (%)")
print(round(strategy_return, 2))

# =====================================
# STEP 9 : MAX DRAWDOWN
# =====================================

rolling_max = (
    data["Strategy_Cumulative"]
    .cummax()
)

drawdown = (
    data["Strategy_Cumulative"]
    - rolling_max
) / rolling_max

max_drawdown = drawdown.min() * 100

print("\nMaximum Drawdown (%)")
print(round(max_drawdown, 2))

# =====================================
# STEP 10 : PRICE CHART
# =====================================

plt.figure(figsize=(12,6))

plt.plot(
    data.index,
    data["Close"],
    label="Close Price"
)

plt.plot(
    data.index,
    data["SMA20"],
    label="SMA20"
)

plt.plot(
    data.index,
    data["SMA50"],
    label="SMA50"
)

plt.title(f"{ticker} Price with Moving Averages")
plt.xlabel("Date")
plt.ylabel("Price")
plt.legend()
plt.grid()

plt.show()

# =====================================
# STEP 11 : EQUITY CURVE
# =====================================

plt.figure(figsize=(12,6))

plt.plot(
    data.index,
    data["Market_Cumulative"],
    label="Buy & Hold"
)

plt.plot(
    data.index,
    data["Strategy_Cumulative"],
    label="Strategy"
)

plt.title("Strategy vs Buy & Hold")

plt.xlabel("Date")
plt.ylabel("Growth of $1")

plt.legend()
plt.grid()

plt.show()

# =====================================
# STEP 12 : SAVE RESULTS
# =====================================

data.to_csv("strategy_results.csv")

print("\nResults saved to strategy_results.csv")

