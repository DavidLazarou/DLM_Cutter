import yfinance as yf
import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt

# ========== CONFIG ==========
ticker = "XLK"
lookback_days = 252  # 1-year lookback for IV rank
today = dt.date.today()
# Manually set macro dates for simplicity
next_cpi_date = dt.date(2024, 4, 10)
next_fed_date = dt.date(2024, 5, 1)

# ========== 1. PRICE DATA ==========
data = yf.download(ticker, period="1y", interval="1d")
data.dropna(inplace=True)
data["20ma"] = data["Close"].rolling(20).mean()
data["stddev"] = data["Close"].rolling(20).std()
data["upper_band"] = data["20ma"] + (2 * data["stddev"])
data["lower_band"] = data["20ma"] - (2 * data["stddev"])
data["bb_width"] = (data["upper_band"] - data["lower_band"]) / data["Close"]

# ATR (14)
data["H-L"] = data["High"] - data["Low"]
data["H-PC"] = abs(data["High"] - data["Close"].shift(1))
data["L-PC"] = abs(data["Low"] - data["Close"].shift(1))
data["TR"] = data[["H-L", "H-PC", "L-PC"]].max(axis=1)
data["ATR"] = data["TR"].rolling(14).mean()
atr_pct = data["ATR"].iloc[-1] / data["Close"].iloc[-1] * 100

# MACD
ema_12 = data["Close"].ewm(span=12, adjust=False).mean()
ema_26 = data["Close"].ewm(span=26, adjust=False).mean()
macd = ema_12 - ema_26
signal = macd.ewm(span=9, adjust=False).mean()
macd_trend = "Neutral"
if macd.iloc[-1] > signal.iloc[-1]:
    macd_trend = "Bullish"
elif macd.iloc[-1] < signal.iloc[-1]:
    macd_trend = "Bearish"

# Bollinger Band Width (%)
bb_width_pct = data["bb_width"].iloc[-1] * 100

# ========== 2. OPTIONS DATA ==========
opt = yf.Ticker(ticker)
expirations = opt.options
exp_chain = opt.option_chain(expirations[2])  # ~30-45 DTE
calls = exp_chain.calls
puts = exp_chain.puts

# Approx IV: take mid IV from at-the-money call
atm_strike = round(data["Close"].iloc[-1])
iv_call = calls.loc[calls["strike"] == atm_strike, "impliedVolatility"]
if iv_call.empty:
    iv = np.nan
else:
    iv = iv_call.iloc[0] * 100

# IV Rank: compare current IV to 1y range
iv_history = []
for exp in expirations[:12]:  # sample expirations
    try:
        chain = opt.option_chain(exp)
        mid_iv = chain.calls["impliedVolatility"].mean()
        iv_history.append(mid_iv * 100)
    except:
        continue
iv_rank = (iv - np.min(iv_history)) / (np.max(iv_history) - np.min(iv_history)) * 100 if len(iv_history) > 0 else np.nan

# ========== 3. CHECKS ==========
price = data["Close"].iloc[-1]
has_high_iv = iv_rank > 50
is_rangebound = atr_pct < 1.5 and bb_width_pct < 10
is_macd_neutral = macd_trend == "Neutral"
no_catalyst = today < next_cpi_date - dt.timedelta(days=3)
has_30dte = True if expirations[2] else False

# ========== 4. PRINT RESULTS ==========
print("\n🔍 XLK Iron Condor Screener")
print("=" * 35)
print(f"Current Price:              ${price:.2f}")
print(f"Implied Volatility (30D):   {iv:.2f}%")
print(f"IV Rank (1Y):               {iv_rank:.2f}")
print(f"ATR (% of price):           {atr_pct:.2f}%")
print(f"MACD Trend:                 {macd_trend}")
print(f"Bollinger Band Width:       {bb_width_pct:.2f}%")
print(f"Next Macro Event:           CPI on {next_cpi_date}")
print(f"Option Chain ~30DTE:        {'Available' if has_30dte else 'Not Available'}")

print("\n🧮 Conditions Check")
print("-" * 35)
print(f"✅ High IV?                  {'✔' if has_high_iv else '✖'}")
print(f"✅ Rangebound / Low ATR?     {'✔' if is_rangebound else '✖'}")
print(f"✅ No big catalysts ahead?   {'✔' if no_catalyst else '✖'}")
print(f"✅ Decay zone (~30DTE)?      {'✔' if has_30dte else '✖'}")

signal = has_high_iv and is_rangebound and no_catalyst and has_30dte
print("\n📣 Final Verdict:            " + ("✅ YES — Sell Iron Condor" if signal else "❌ NO — Conditions Not Ideal"))
print("=" * 35)
