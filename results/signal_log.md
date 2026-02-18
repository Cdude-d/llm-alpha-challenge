# Signal Research Log
**Project:** LLM Alpha Discovery Challenge — QQQ 2013–2022
**Goal:** Achieve Sharpe Ratio ≥ 0.8 via signal ensemble
**Leverage range:** -1.0 (full short) to +1.5 (full long)
**Execution:** Signal at close → applied to next-day close return

---

## Benchmark

| Signal | Sharpe | Total Return | Ann. Return | Max Drawdown |
|--------|--------|-------------|-------------|--------------|
| Buy & Hold QQQ | +0.80 | +335.08% | +18.48% | -35.09% |

> The benchmark itself hits 0.80 Sharpe. Any signal we add must either match this or combine with others to exceed it while improving risk-adjusted returns.

---

## Signal 001 — RSI Mean Reversion

**Date tested:** 2025
**File:** `strategy_rsi_mean_reversion.py`

### Hypothesis
QQQ exhibits short-term mean reversion: when the 14-day RSI drops below 30 (oversold), price is likely to bounce → go max long (1.5x). When RSI exceeds 70 (overbought), price is likely to fall → go max short (-1.0x). Between extremes, leverage scales linearly.

### Parameters
| Parameter | Value |
|-----------|-------|
| RSI Period | 14 |
| Oversold threshold | 30 |
| Overbought threshold | 70 |
| Max long leverage | +1.5 |
| Max short leverage | -1.0 |

### Results
| Metric | Value |
|--------|-------|
| Sharpe Ratio (ann.) | +0.5027 |
| Total Return | +103.30% |
| Ann. Return | +8.97% |
| Max Drawdown | -20.21% |
| Trading days | 2,503 |

### Robustness (±10% RSI period)
| RSI Period | Sharpe |
|------------|--------|
| 13 (-10%) | +0.5004 |
| 14 (base) | +0.5027 |
| 15 (+10%) | +0.5199 |

✅ **Robust** — Sharpe is stable across parameter shifts. Not overfit.
❌ **Below target** — Sharpe of 0.50 is well short of the 0.8 goal.

### Analysis
The strategy significantly underperforms buy-and-hold. The core issue is that QQQ spent 2013–2022 in a powerful secular bull market — mean reversion logic (sell when it rises) directly fights the prevailing trend. The strategy is essentially trying to short a bull market.

**One positive:** Max drawdown is meaningfully lower (-20% vs -35%), showing the signal does provide some downside protection. This makes it a candidate as a *risk filter* within an ensemble, even if it fails as a standalone strategy.

### Conclusion
❌ **Rejected as standalone signal.** Sharpe 0.50 < 0.8 target.
⚠️ **Potential ensemble component** — its drawdown-reducing properties may add value when combined with a high-return momentum signal.

### Forward Plan
- The underperformance strongly suggests QQQ is better suited to **momentum strategies** during this period.
- Next: Build a momentum signal (SMA crossover or MACD) to test the opposite hypothesis.
- Also test **RSI(2)** — the 2-day RSI variant designed for very short-term micro-bounces, which behaves very differently from RSI(14).

---

*Log continues below as new signals are tested...*
