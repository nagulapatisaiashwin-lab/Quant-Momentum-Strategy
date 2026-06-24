from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# ==========================
# 1. Load Data
# ==========================


csv_path = Path(__file__).parent / "NIFTY_50_minute.csv"
df = pd.read_csv(csv_path)

# Convert datetime column
df["date"] = pd.to_datetime(df["date"], dayfirst=True)

# Create trading session column
df["session"] = df["date"].dt.date

# ==========================
# 2. Define Candle Color
# ==========================
# Green = 1, Red = 0
df["green"] = (df["close"] >= df["open"]).astype(int)

# Base probability
base_prob = df["green"].mean()

# ==========================
# 3. Find Exact 5-Green Sequences
# ==========================
green_total = 0
green_next_green = 0

# ==========================
# 4. Find Exact 5-Red Sequences
# ==========================
red_total = 0
red_next_green = 0

# Process each trading day separately
for _, day_data in df.groupby("session"):

    colors = day_data["green"].tolist()
    n = len(colors)

    for i in range(n - 5):

        window = colors[i:i+5]
        sixth = colors[i+5]

        # EXACTLY 5 greens
        if all(x == 1 for x in window):

            left_ok = (i == 0) or (colors[i-1] == 0)

            if left_ok:
                green_total += 1

                if sixth == 1:
                    green_next_green += 1

        # EXACTLY 5 reds
        if all(x == 0 for x in window):

            left_ok = (i == 0) or (colors[i-1] == 1)

            if left_ok:
                red_total += 1

                if sixth == 1:
                    red_next_green += 1

# ==========================
# 5. Probabilities
# ==========================
p_green_after_5_green = green_next_green / green_total
p_red_after_5_green = 1 - p_green_after_5_green

p_green_after_5_red = red_next_green / red_total
p_red_after_5_red = 1 - p_green_after_5_red

# ==========================
# 6. Results
# ==========================
print("\n----- RESULTS -----\n")

print(f"Base P(Green): {base_prob:.4%}")

print("\nAfter Exactly 5 Green Candles")
print(f"Count: {green_total}")
print(f"P(6th Green | 5 Green) = {p_green_after_5_green:.4%}")
print(f"P(6th Red   | 5 Green) = {p_red_after_5_green:.4%}")

print("\nAfter Exactly 5 Red Candles")
print(f"Count: {red_total}")
print(f"P(6th Green | 5 Red) = {p_green_after_5_red:.4%}")
print(f"P(6th Red   | 5 Red) = {p_red_after_5_red:.4%}")



plt.figure(figsize=(8,5))
plt.bar(
    ["Base","After 5G","After 5R"],
    [base_prob,
     p_green_after_5_green,
     p_green_after_5_red]
)

plt.ylabel("Probability of Green")
plt.title("Probability of Green Candle")
plt.show()