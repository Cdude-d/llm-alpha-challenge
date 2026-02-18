# QQQ Alpha Discovery — Research Guide & Literature Review

## Purpose

This guide supports the LLM Alpha Discovery Challenge: building trading signals for QQQ (NASDAQ-100 ETF) that achieve a Sharpe Ratio ≥ 0.8 over 2013–2022. Beyond the challenge itself, the goal is to demonstrate understanding of quantitative trading fundamentals to potential employers.

---

## 1. Core Signal Families to Explore

### Momentum / Trend-Following

Momentum strategies exploit the tendency of assets that have been rising (or falling) to continue doing so over intermediate time horizons. Research consistently shows momentum is strongest at the 3–12 month horizon, while very short-term (intraday to a few days) and very long-term (3–5 year) horizons tend to exhibit *mean reversion* instead.

**Signals to implement:**

- **Moving average crossovers** — e.g., 10-day vs. 50-day SMA/EMA. Go long when fast crosses above slow, short when it crosses below. Vary the lookback windows.
- **Rate of change (ROC)** — Simple percentage change over N days. Positive ROC → long bias, negative → short bias.
- **MACD (Moving Average Convergence/Divergence)** — Difference between 12-day and 26-day EMA, with a 9-day signal line. Crossovers and histogram direction indicate momentum shifts.
- **ADX (Average Directional Index)** — Measures trend strength regardless of direction. High ADX (>25) confirms a tradeable trend; low ADX suggests a range-bound market where momentum signals will whipsaw.

### Mean Reversion

Mean reversion strategies bet that prices stretched far from a "normal" level will snap back. These work best in range-bound or choppy markets.

**Signals to implement:**

- **RSI (Relative Strength Index)** — Classic overbought/oversold indicator. RSI > 70 suggests overbought (short bias), RSI < 30 suggests oversold (long bias). The RSI(2) variant (2-day lookback) is popular for short-term mean reversion.
- **Bollinger Bands** — Price relative to its 20-day moving average ± 2 standard deviations. Touches of the upper band suggest overbought; lower band suggests oversold.
- **Z-score of returns** — Standardize recent returns against a rolling window. Extreme Z-scores (e.g., > 2 or < -2) signal reversion opportunities.
- **Percent rank** — Where does today's return rank within the last N days? Extreme percentiles suggest reversion.

### Volatility-Based

Volatility itself carries information. Periods of low volatility tend to precede large moves, and high volatility tends to cluster and then decay.

**Signals to implement:**

- **Historical volatility regime** — Rolling standard deviation of returns. Low vol → expect a breakout (increase position size); high vol → expect calming (reduce or wait).
- **Volatility breakout (Donchian/Keltner channels)** — Trade breakouts of N-day high/low channels. The width of the channel adapts to recent volatility.
- **ATR-based sizing** — Use Average True Range to normalize position sizes, so you take less risk in volatile periods and more in calm ones.
- **Volume-price divergence** — Rising price on declining volume (or vice versa) can signal weakening momentum. Volume spikes often mark turning points.

### Calendar / Seasonal

Markets exhibit well-documented time-based patterns.

**Signals to implement:**

- **Day-of-week effects** — Historically, Mondays have been weaker and Fridays stronger for equities. Test whether this holds for QQQ in your sample.
- **Month-of-year / "Sell in May"** — The November–April period has historically outperformed May–October. Simple binary signal.
- **Turn-of-month** — The last trading day and first few trading days of each month tend to be stronger due to fund flows and payroll timing.
- **Quadruple witching / options expiration** — Heightened volatility around expiration dates can create short-term signals.

### Composite / Ensemble

The real power comes from combining uncorrelated signals. This is what employers want to see — not just one clever signal, but a systematic framework.

- **Equal-weight ensemble** — Average the leverage recommendations of multiple independent signals.
- **Volatility-weighted ensemble** — Weight each signal inversely by its recent tracking error.
- **Correlation-aware ensemble** — Down-weight signals that are highly correlated with each other.

---

## 2. Key Academic Literature

### Foundational Papers

- **Jegadeesh & Titman (1993)** — "Returns to Buying Winners and Selling Losers" — the seminal momentum paper showing that stocks with high past returns continue to outperform over 3–12 months.
- **De Bondt & Thaler (1985)** — "Does the Stock Market Overreact?" — early evidence for long-term mean reversion (3–5 year reversals).
- **Fama & French (1993)** — The three-factor model (market, size, value) — foundational framework for understanding equity returns beyond simple beta.
- **Carhart (1997)** — Extended Fama-French with a momentum factor, creating the four-factor model still widely used today.

### Recent & Relevant Research

- **Sepp & Lucic (2025)** — "The Science and Practice of Trend-Following Systems" — performance attribution framework for trend-following, with analysis of autocorrelation evolution in futures markets. Available on SSRN.
- **Requejo (2024)** — "Efficacy of a Mean Reversion Trading Strategy Using True Strength Index" — practical assessment of mean reversion in equity markets using TSI. Available on SSRN.
- **Combining Mean Reversion and Momentum in FX Markets** — Shows that hybrid strategies outperform either approach alone, with the combined signal yielding ~20% annualized returns vs. ~11% for momentum alone (ScienceDirect).
- **arXiv: Trends, Reversion, and Critical Phenomena** — Finds that medium-strength trends persist at multi-day to multi-year scales, while reversion dominates at very short and very long horizons.

### Books (Highly Recommended)

1. **"Quantitative Trading" by Ernest P. Chan** — Practical guide to building and backtesting strategies. Great starting point.
2. **"Algorithmic Trading: Winning Strategies and Their Rationale" by Ernest P. Chan** — Deeper dive into specific strategy types with real examples.
3. **"Advances in Financial Machine Learning" by Marcos López de Prado** — More advanced, but excellent for showing employers you understand modern approaches (triple barrier labeling, meta-labeling, feature importance).
4. **"Quantitative Trading Strategies Using Python" by Peng Liu (Springer)** — Covers fundamentals through ML-based signal generation with Python implementations.
5. **"Python for Finance" by Yves Hilpisch** — Comprehensive Python-for-finance reference.

---

## 3. Free Data Sources to Supplement Your Analysis

Your CSV covers QQQ OHLCV 2013–2022. Here's what else could improve your signals:

| Source | What It Offers | Why It Helps |
|--------|---------------|--------------|
| **FRED** (fred.stlouisfed.org) | Interest rates, VIX, yield curve, GDP, unemployment, inflation | Macro regime detection — momentum works differently in recessions vs. expansions |
| **Yahoo Finance** (via `yfinance` Python library) | Additional ETF prices, sector ETFs, VIX history | Cross-asset signals (e.g., QQQ vs. IWM relative strength) |
| **Alpha Vantage** (alphavantage.co) | Technical indicators, sector performance, economic indicators | Pre-computed indicators, good for validation |
| **Kenneth French Data Library** | Fama-French factor returns (daily) | Decompose your signal's returns into factor exposures |
| **SEC EDGAR** | Corporate filings, earnings dates | Event-driven signals around earnings |
| **Quandl / Nasdaq Data Link** | Futures, options, economic data | VIX futures term structure, put/call ratios |

### Python Libraries for Data Access

```python
# Core stack
pip install pandas numpy matplotlib

# Data access
pip install yfinance            # Yahoo Finance historical data
pip install fredapi             # FRED economic data (free API key)
pip install alpha_vantage       # Alpha Vantage (free API key)

# Technical analysis
pip install ta                  # Technical analysis indicators
pip install ta-lib              # TA-Lib (more comprehensive, harder to install)

# Backtesting frameworks
pip install backtesting         # Backtesting.py — simple, visual
pip install backtrader          # Backtrader — more flexible
```

---

## 4. Backtesting Best Practices

These are the things that separate a good quant project from a mediocre one — and what employers look for:

### Avoid Lookahead Bias
Never compute statistics over the full dataset and apply them retroactively. All indicators must use only data available at the time of the trade. Use rolling windows, not expanding windows with full-period stats.

### Avoid Overfitting
- **Parameter sensitivity**: If your signal only works with a 17-day lookback but fails at 15 or 19, it's overfit. The challenge requires ±10% parameter robustness.
- **Out-of-sample testing**: Split your 10-year dataset. Train on 2013–2017, test on 2018–2022 (or use walk-forward analysis).
- **Simplicity**: Fewer parameters = less overfitting. A 2-parameter signal that achieves Sharpe 0.9 is far more impressive than a 10-parameter signal at Sharpe 1.5.

### Report the Right Metrics
- **Sharpe Ratio** (primary): `mean(daily_returns) / std(daily_returns) * sqrt(252)`
- **Maximum drawdown**: Largest peak-to-trough decline. Employers care about this as much as Sharpe.
- **Calmar Ratio**: Annualized return / max drawdown.
- **Win rate and profit factor**: What percentage of days are profitable? Is the average win bigger than the average loss?
- **Turnover**: How often does the signal change leverage? High turnover = high transaction costs in practice.

### Show Your Work
Document your hypothesis *before* running the backtest. This shows scientific thinking rather than data mining. A rejected hypothesis that you explain thoughtfully is more impressive than a cherry-picked winner.

---

## 5. What Employers Want to See

For a quant research or trading role, this project can demonstrate:

1. **Structured thinking** — Clear hypotheses, systematic testing, honest reporting of results (including failures).
2. **Technical competency** — Clean Python code, proper data handling, correct statistical calculations.
3. **Risk awareness** — Discussion of drawdowns, overfitting, parameter sensitivity, transaction costs.
4. **Signal combination** — Building an ensemble shows you understand portfolio construction, not just single-signal backtesting.
5. **Communication** — A well-organized notebook or report that a non-technical interviewer could follow.

### Suggested Project Structure

```
project/
├── data/                    # Raw CSV + any supplementary data
├── notebooks/               # Jupyter notebooks for exploration
├── signals/                 # Individual signal implementations
│   ├── momentum.py
│   ├── mean_reversion.py
│   ├── volatility.py
│   └── calendar.py
├── backtest/                # Backtesting engine
│   ├── engine.py            # Core backtest logic
│   └── metrics.py           # Sharpe, drawdown, etc.
├── ensemble/                # Signal combination logic
├── results/                 # Output charts, tables, reports
└── README.md                # Project overview and findings
```

---

## 6. Suggested Learning Path

**Week 1**: Read Ernest Chan's "Quantitative Trading" chapters 1–4. Load and explore the QQQ CSV in Python. Compute basic statistics (daily returns, annualized vol, drawdowns).

**Week 2**: Implement 2–3 momentum signals (SMA crossover, MACD, ROC). Backtest each one. Learn what Sharpe ratios you get with simple approaches.

**Week 3**: Implement 2–3 mean reversion signals (RSI, Bollinger Bands, Z-score). Compare performance to momentum signals. Notice they tend to work in different market regimes.

**Week 4**: Add volatility and calendar signals. Build a simple ensemble. Run parameter sensitivity tests. Write up your findings.

---

## 7. Online Learning Platforms

- **QuantConnect** (quantconnect.com) — Cloud-based backtesting with free data. Great for building a portfolio of strategies.
- **QuantStart** (quantstart.com) — Tutorials on backtesting frameworks, portfolio optimization, and ML applications.
- **Coursera: "Machine Learning for Trading"** (Georgia Tech) — Covers ML applied to trading.
- **freeCodeCamp** — Free algorithmic trading tutorial in Python.
- **Investopedia** — Good for understanding individual indicators if you're unfamiliar with any.

---

*This guide was compiled as part of the LLM Alpha Discovery Challenge. The research and signal ideas here are starting points — the value of the project comes from your own implementation, analysis, and critical thinking about what works and why.*
