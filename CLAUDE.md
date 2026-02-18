# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is **The LLM Alpha Discovery Challenge** — a quantitative finance research project focused on developing trading signals for QQQ (NASDAQ-100 ETF) using LLM-assisted hypothesis generation. The goal is to produce signals or signal ensembles achieving a **Sharpe Ratio >= 0.8** over the backtest period 01/01/2013 through 01/01/2023.

## Data

- **`QQQ Data 2013 - 2023 - Sheet1.csv`** — 2,517 rows of daily OHLCV data
- Columns: `Time, Open, High, Low, Last, Change, %Change, Volume`
- Date range: January 2, 2013 through December 30, 2022
- `Last` is the closing price; `%Change` includes a `%` suffix (parse accordingly)

## Strategy Constraints

- **Leverage range:** -1.0 (100% short) to +1.5 (150% long) per day
- **Execution model:** All trades/leverage changes happen at market close, held until next close
- **No lookahead bias:** Signals must use only information available at or before trade time. Do not compute dataset-wide statistics (full-period Z-scores, means, etc.) and apply them retroactively.
- **Robustness requirement:** A ±10% shift in key parameters (lookback windows, thresholds) must not destroy the signal. Overfitted signals are rejected.

## Workflow

1. **Hypothesis generation** — Brainstorm novel signal ideas (unconventional logic, alternative data correlations, novel factor combinations)
2. **Backtesting** — Implement and test each signal against the CSV data
3. **Signal library** — Build multiple independent signals/portfolios with Sharpe > 0.8
4. **Ensemble construction** — Combine signals to maximize the portfolio Sharpe ratio
5. **Robustness validation** — Run ±10% parameter sensitivity tests on all signals

## Key Metrics

- **Primary metric:** Sharpe Ratio (annualized, target >= 0.8)
- Sharpe = (mean daily return / std daily return) * sqrt(252)
- Daily return = leverage * daily price change of QQQ

## Implementation Notes

- No build system, package manager, or test framework is currently configured
- Python with pandas/numpy is the expected stack for backtesting
- When parsing the CSV, handle the `%Change` column's percent sign and the `Time` column's M/D/YY date format
- The challenge originally targets Gemini 3.0 via Google AI Studio, but any LLM-assisted approach works
