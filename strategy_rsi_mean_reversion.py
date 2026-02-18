"""
RSI Mean Reversion Strategy for QQQ (2013-2023)
-------------------------------------------------
Signal logic:
  - RSI < 30  => oversold => go long (leverage = +1.5)
  - RSI > 70  => overbought => go short (leverage = -1.0)
  - Otherwise => neutral / scale linearly between extremes

Execution model: signal computed at close, applied to next-day close return.
No lookahead bias: RSI uses only past prices.
"""

import pandas as pd
import numpy as np


# ── Data loading ─────────────────────────────────────────────────────────────

def load_data(path: str = "QQQ Data 2013 - 2023 - Sheet1.csv") -> pd.DataFrame:
    df = pd.read_csv(path)
    df["Date"] = pd.to_datetime(df["Time"], format="%m/%d/%y")
    df = df.sort_values("Date").reset_index(drop=True)
    df["%Change"] = df["%Change"].str.rstrip("%").astype(float) / 100
    return df


# ── Indicators ───────────────────────────────────────────────────────────────

def compute_rsi(prices: pd.Series, period: int = 14) -> pd.Series:
    delta = prices.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    # Use Wilder's smoothing (exponential moving average)
    avg_gain = gain.ewm(alpha=1 / period, min_periods=period, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1 / period, min_periods=period, adjust=False).mean()
    rs = avg_gain / avg_loss.replace(0, np.nan)
    rsi = 100 - (100 / (1 + rs))
    return rsi


# ── Signal generation ────────────────────────────────────────────────────────

def generate_signal(
    rsi: pd.Series,
    oversold: float = 30,
    overbought: float = 70,
    max_long: float = 1.5,
    max_short: float = -1.0,
) -> pd.Series:
    """
    Map RSI to leverage linearly:
      RSI <= oversold  => max_long
      RSI >= overbought => max_short
      Between          => linear interpolation
    """
    leverage = np.where(
        rsi <= oversold,
        max_long,
        np.where(
            rsi >= overbought,
            max_short,
            # linear interp from max_long (at oversold) to max_short (at overbought)
            max_long + (rsi - oversold) / (overbought - oversold) * (max_short - max_long),
        ),
    )
    return pd.Series(leverage, index=rsi.index, name="leverage")


# ── Backtest ─────────────────────────────────────────────────────────────────

def backtest(df: pd.DataFrame, signal: pd.Series) -> pd.DataFrame:
    """
    Apply leverage to next-day return.
    Signal at day t is applied to the return from day t close to day t+1 close.
    """
    # Next-day return
    daily_ret = df["%Change"].shift(-1)  # return earned on day t+1, known at t+1 close

    strat_ret = signal * daily_ret
    strat_ret = strat_ret.dropna()

    results = pd.DataFrame(
        {
            "date": df["Date"].iloc[strat_ret.index],
            "leverage": signal.iloc[strat_ret.index],
            "daily_ret": daily_ret.iloc[strat_ret.index],
            "strat_ret": strat_ret,
        }
    )
    results = results.reset_index(drop=True)
    return results


# ── Performance metrics ───────────────────────────────────────────────────────

def sharpe(returns: pd.Series, periods_per_year: int = 252) -> float:
    mean = returns.mean()
    std = returns.std()
    if std == 0:
        return 0.0
    return (mean / std) * np.sqrt(periods_per_year)


def print_metrics(label: str, returns: pd.Series) -> None:
    sr = sharpe(returns)
    total = (1 + returns).prod() - 1
    ann_ret = (1 + returns.mean()) ** 252 - 1
    max_dd = ((1 + returns).cumprod() / (1 + returns).cumprod().cummax() - 1).min()
    print(f"\n{'='*50}")
    print(f"  {label}")
    print(f"{'='*50}")
    print(f"  Sharpe Ratio (ann.)  : {sr:+.4f}")
    print(f"  Total Return         : {total:+.2%}")
    print(f"  Ann. Return          : {ann_ret:+.2%}")
    print(f"  Max Drawdown         : {max_dd:+.2%}")
    print(f"  Num trading days     : {len(returns)}")


# ── Robustness: parameter sweep ───────────────────────────────────────────────

def robustness_sweep(df: pd.DataFrame, base_period: int = 14) -> None:
    """±10% shift on RSI period."""
    print("\n--- Robustness sweep (RSI period ±10%) ---")
    for period in [round(base_period * 0.9), base_period, round(base_period * 1.1)]:
        rsi = compute_rsi(df["Last"], period=period)
        sig = generate_signal(rsi)
        bt = backtest(df, sig)
        sr = sharpe(bt["strat_ret"])
        print(f"  RSI period={period:3d} => Sharpe={sr:+.4f}")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    df = load_data()

    # Base parameters
    RSI_PERIOD = 14
    OVERSOLD = 30
    OVERBOUGHT = 70

    rsi = compute_rsi(df["Last"], period=RSI_PERIOD)
    signal = generate_signal(rsi, oversold=OVERSOLD, overbought=OVERBOUGHT)
    bt = backtest(df, signal)

    print_metrics(
        f"RSI Mean Reversion  (period={RSI_PERIOD}, OS={OVERSOLD}, OB={OVERBOUGHT})",
        bt["strat_ret"],
    )

    # Benchmark: buy-and-hold QQQ
    bh_ret = df["%Change"].shift(-1).dropna()
    print_metrics("Buy & Hold QQQ (benchmark)", bh_ret)

    robustness_sweep(df, base_period=RSI_PERIOD)


if __name__ == "__main__":
    main()
