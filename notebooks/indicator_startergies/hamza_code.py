import pandas as pd
import numpy as np
import yfinance as yf
from pathlib import Path

# ==========================================
# LOCAL CACHE
# ==========================================

CACHE_DIR = Path(".yfinance-cache")
CACHE_DIR.mkdir(exist_ok=True)

try:
    yf.cache.set_cache_location(str(CACHE_DIR))
except:
    pass

# ==========================================
# FUNCTIONS
# ==========================================

def donchian(high, low, length):
    lower = low.rolling(length).min()
    upper = high.rolling(length).max()
    middle = (upper + lower) / 2
    return lower, middle, upper


def atr(high, low, close, length=14):
    prev_close = close.shift(1)

    tr = pd.concat([
        high - low,
        (high - prev_close).abs(),
        (low - prev_close).abs()
    ], axis=1).max(axis=1)

    return tr.rolling(length).mean()


# ==========================================
# PARAMETERS
# ==========================================

TICKER = "AAPL"

START_DATE = "2022-01-01"
END_DATE = None

INITIAL_CAPITAL = 100000

DONCHIAN_ENTRY = 55
DONCHIAN_EXIT = 10

EMA_FAST = 50
EMA_SLOW = 200

ATR_PERIOD = 14
ATR_MULTIPLIER = 2

# ==========================================
# DOWNLOAD DATA
# ==========================================

df = yf.download(
    TICKER,
    start=START_DATE,
    end=END_DATE,
    auto_adjust=True,
    progress=False
)

if isinstance(df.columns, pd.MultiIndex):
    df = df.xs(TICKER, axis=1, level="Ticker")

df.dropna(inplace=True)

# ==========================================
# INDICATORS
# ==========================================

# Donchian Channels

df["DC_LOW_55"], _, df["DC_HIGH_55"] = donchian(
    df["Low"],
    df["High"],
    DONCHIAN_ENTRY
)

df["DC_LOW_10"], _, _ = donchian(
    df["Low"],
    df["High"],
    DONCHIAN_EXIT
)

# Shifted channels (avoids look-ahead bias)

df["DC_HIGH_55_SHIFT"] = df["DC_HIGH_55"].shift(1)
df["DC_LOW_10_SHIFT"] = df["DC_LOW_10"].shift(1)

# EMAs

df["EMA50"] = (
    df["Close"]
    .ewm(span=EMA_FAST, adjust=False)
    .mean()
)

df["EMA200"] = (
    df["Close"]
    .ewm(span=EMA_SLOW, adjust=False)
    .mean()
)

# ATR

df["ATR"] = atr(
    df["High"],
    df["Low"],
    df["Close"],
    ATR_PERIOD
)

df.dropna(inplace=True)

# ==========================================
# BACKTEST
# ==========================================

cash = INITIAL_CAPITAL
shares = 0

stop_loss = np.nan

equity_curve = []
trades = []

for date, row in df.iterrows():

    price = row["Close"]

    # ==========================
    # ENTRY
    # ==========================

    if shares == 0:

        breakout = price > row["DC_HIGH_55_SHIFT"]
        trend = row["EMA50"] > row["EMA200"]

        if breakout and trend:

            qty = int(cash // price)

            if qty > 0:

                shares = qty
                cash -= qty * price

                stop_loss = (
                    price
                    - ATR_MULTIPLIER * row["ATR"]
                )

                trades.append({
                    "Type": "BUY",
                    "Date": date,
                    "Price": float(price),
                    "Shares": qty
                })

    # ==========================
    # POSITION MANAGEMENT
    # ==========================

    else:

        trailing_stop = (
            price
            - ATR_MULTIPLIER * row["ATR"]
        )

        stop_loss = max(
            stop_loss,
            trailing_stop
        )

        exit_donchian = (
            price < row["DC_LOW_20_SHIFT"]
        )

        exit_stop = (
            price <= stop_loss
        )

        if exit_donchian or exit_stop:

            cash += shares * price

            trades.append({
                "Type": "SELL",
                "Date": date,
                "Price": float(price),
                "Shares": shares
            })

            shares = 0
            stop_loss = np.nan

    portfolio_value = cash + shares * price
    equity_curve.append(portfolio_value)

# ==========================================
# FINAL LIQUIDATION
# ==========================================

if shares > 0:

    final_price = df["Close"].iloc[-1]

    cash += shares * final_price

    trades.append({
        "Type": "SELL",
        "Date": df.index[-1],
        "Price": float(final_price),
        "Shares": shares
    })

    shares = 0

final_value = cash

# ==========================================
# PERFORMANCE METRICS
# ==========================================

equity = pd.Series(
    equity_curve,
    index=df.index
)

years = (
    (df.index[-1] - df.index[0]).days
    / 365.25
)

cagr = (
    (final_value / INITIAL_CAPITAL)
    ** (1 / years)
    - 1
)

daily_returns = equity.pct_change().dropna()

sharpe = (
    np.sqrt(252)
    * daily_returns.mean()
    / daily_returns.std()
)

rolling_max = equity.cummax()

drawdown = (
    equity - rolling_max
) / rolling_max

max_drawdown = drawdown.min()

# ==========================================
# TRADE STATISTICS
# ==========================================

trade_pnl = []

for i in range(0, len(trades)-1, 2):

    buy = trades[i]
    sell = trades[i+1]

    pnl = (
        sell["Price"]
        - buy["Price"]
    ) * buy["Shares"]

    trade_pnl.append(pnl)

win_rate = (
    np.mean(np.array(trade_pnl) > 0)
    if len(trade_pnl)
    else 0
)

# ==========================================
# RESULTS
# ==========================================

print("\n" + "="*60)
print("DONCHIAN TREND FOLLOWING STRATEGY")
print("="*60)

print(f"Ticker:            {TICKER}")
print(f"Initial Capital:   ${INITIAL_CAPITAL:,.2f}")
print(f"Final Capital:     ${final_value:,.2f}")
print(f"Total Return:      {(final_value/INITIAL_CAPITAL-1)*100:.2f}%")
print(f"CAGR:              {cagr*100:.2f}%")
print(f"Sharpe Ratio:      {sharpe:.2f}")
print(f"Max Drawdown:      {max_drawdown*100:.2f}%")
print(f"Win Rate:          {win_rate*100:.2f}%")
print(f"Total Trades:      {len(trade_pnl)}")

print("\nCompleted Trades")
print("-"*60)

if trades:
    print(pd.DataFrame(trades))
else:
    print("No trades generated.")