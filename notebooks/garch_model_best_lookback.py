import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import yfinance as yf
from arch import arch_model

##################################################
# DOWNLOAD DATA
##################################################

df = yf.download(
    "GOOGL",
    period="2y",
    interval="1d",
    auto_adjust=True,
    progress=False
)

df["ret"] = np.log(df["Close"]).diff()
df = df.dropna()

returns = df["ret"]

##################################################
# LOOKBACKS
##################################################

LOOKBACKS = {
   "1_week": 35,      # 5 trading days × 7 hours/day
    "1_month": 150,
    "3_month": 450,
    "6_month": 900,
    "1_year": 1800
}

##################################################
# FORECAST HORIZONS
##################################################

HORIZONS = {
    "1_hour": 1,
    "1_day": 7,
    "1_week": 35
}

##################################################
# FUNCTION
##################################################

def test_garch(returns, lookback, horizon):

    preds = []
    actuals = []

    start = lookback
    end = len(returns) - horizon

    # Evaluate every 5th day
    for i in range(start, end, 5):

        train = returns.iloc[i-lookback:i]

        try:

            model = arch_model(
                train * 100,
                mean="Zero",
                vol="GARCH",
                p=1,
                q=1
            )

            fit = model.fit(disp="off")

            forecast = fit.forecast(
                horizon=horizon,
                reindex=False
            )

            pred_var = forecast.variance.iloc[-1].sum()

            pred_vol = np.sqrt(pred_var)

            future = returns.iloc[i:i+horizon]

            realized_vol = np.sqrt(
                np.sum(
                    (future * 100) ** 2
                )
            )

            preds.append(pred_vol)
            actuals.append(realized_vol)

        except:
            pass

    preds = np.array(preds)
    actuals = np.array(actuals)

    rmse = np.sqrt(
        np.mean(
            (preds - actuals) ** 2
        )
    )

    return rmse

##################################################
# RUN
##################################################

results = []

for lb_name, lb in LOOKBACKS.items():

    for h_name, h in HORIZONS.items():

        print(
            f"Testing {lb_name} -> {h_name}"
        )

        rmse = test_garch(
            returns,
            lb,
            h
        )

        results.append(
            [lb_name, h_name, rmse]
        )

##################################################
# RESULTS
##################################################

results_df = pd.DataFrame(
    results,
    columns=[
        "Lookback",
        "Horizon",
        "RMSE"
    ]
)

print("\nAll Results")
print(results_df)

##################################################
# BEST
##################################################

best = results_df.loc[
    results_df.groupby(
        "Horizon"
    )["RMSE"].idxmin()
]

print("\nBest Lookbacks")
print(best)