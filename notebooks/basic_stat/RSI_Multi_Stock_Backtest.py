import yfinance as yf
import pandas as pd
import numpy as np

# Stocks to test
tickers = [
    "AAPL",
    "MSFT",
    "NVDA",
    "GOOGL",
    "AMZN",
    "TSLA"
]

results = []

for ticker in tickers:

    print(f"Processing {ticker}...")

    data = yf.download(
        ticker,
        period="5y",
        auto_adjust=True
    )

    data.columns = data.columns.get_level_values(0)

    if data.empty:
        print(f"Failed download: {ticker}")
        continue

    print(data.head())

    # Daily Returns
    data["Return"] = data["Close"].pct_change()

    # -------------------
    # RSI Calculation
    # -------------------

    delta = data["Close"].diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(14).mean()
    avg_loss = loss.rolling(14).mean()

    rs = avg_gain / avg_loss

    data["RSI"] = 100 - (100 / (1 + rs))

    # -------------------
    # Signals
    # -------------------

    data["Signal"] = np.nan

    data.loc[data["RSI"] < 30, "Signal"] = 1
    data.loc[data["RSI"] > 70, "Signal"] = 0

    # Hold previous position
    data["Signal"] = data["Signal"].ffill()

    # If still NaN at beginning
    data["Signal"] = data["Signal"].fillna(0)

    # -------------------
    # Strategy Returns
    # -------------------

    data["Strategy_Return"] = (
        data["Return"]
        * data["Signal"].shift(1)
    )

    # -------------------
    # Equity Curves
    # -------------------

    data["Market_Cumulative"] = (
        1 + data["Return"]
    ).cumprod()

    data["Strategy_Cumulative"] = (
        1 + data["Strategy_Return"]
    ).cumprod()

    # -------------------
    # Metrics
    # -------------------

    market_return = (
        data["Market_Cumulative"].iloc[-1] - 1
    ) * 100

    strategy_return = (
        data["Strategy_Cumulative"].iloc[-1] - 1
    ) * 100

    strategy_returns = (
        data["Strategy_Return"]
        .dropna()
    )

    sharpe = (
        strategy_returns.mean()
        /
        strategy_returns.std()
    ) * np.sqrt(252)

    rolling_max = (
        data["Strategy_Cumulative"]
        .cummax()
    )

    drawdown = (
        data["Strategy_Cumulative"]
        - rolling_max
    ) / rolling_max

    max_drawdown = (
        drawdown.min()
        * 100
    )

    results.append({
        "Ticker": ticker,
        "Market Return %": round(market_return, 2),
        "RSI Return %": round(strategy_return, 2),
        "Sharpe": round(sharpe, 2),
        "Max Drawdown %": round(max_drawdown, 2)
    })

# -------------------
# Final Table
# -------------------

results_df = pd.DataFrame(results)

print("\nResults:\n")
print(results_df)

results_df.to_csv(
    "RSI_MultiStock_Backtest.csv",
    index=False
)
