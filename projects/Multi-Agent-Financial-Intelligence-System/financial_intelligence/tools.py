from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
import pandas as pd


@dataclass
class MarketData:
    ticker: str
    prices: pd.Series


def get_stock_data(ticker: str, period: str = "1y", use_mock_data: bool = False) -> MarketData:
    """Fetch historical closes, with deterministic mock data for offline execution."""
    if use_mock_data:
        rng = np.random.default_rng(abs(hash(ticker.upper())) % (2**32))
        dates = pd.bdate_range(end=pd.Timestamp.today().normalize(), periods=252)
        returns = rng.normal(0.0005, 0.018, len(dates))
        prices = pd.Series(100 * np.exp(np.cumsum(returns)), index=dates, name="Close")
        return MarketData(ticker.upper(), prices)

    try:
        import yfinance as yf
    except ImportError as exc:
        raise RuntimeError("Install yfinance or run with --mock.") from exc

    data = yf.download(ticker, period=period, auto_adjust=True, progress=False)
    if data.empty:
        raise ValueError(f"No market data returned for {ticker}.")
    closes = data["Close"]
    if isinstance(closes, pd.DataFrame):
        closes = closes.iloc[:, 0]
    return MarketData(ticker.upper(), closes.dropna())


def assess_risk_metrics(prices: pd.Series, risk_free_rate: float = 0.04) -> dict[str, Any]:
    """Calculate common historical risk/return metrics."""
    prices = pd.Series(prices, dtype=float).dropna()
    returns = prices.pct_change().dropna()
    if len(returns) < 2:
        raise ValueError("At least two price observations are required.")

    annual_return = (prices.iloc[-1] / prices.iloc[0]) ** (252 / len(returns)) - 1
    volatility = returns.std() * np.sqrt(252)
    daily_rf = (1 + risk_free_rate) ** (1 / 252) - 1
    sharpe = ((returns.mean() - daily_rf) / returns.std()) * np.sqrt(252)
    drawdown = prices / prices.cummax() - 1
    var_95 = float(returns.quantile(0.05))

    if volatility < 0.20 and drawdown.min() > -0.20:
        level = "Low"
    elif volatility < 0.35 and drawdown.min() > -0.35:
        level = "Moderate"
    else:
        level = "High"

    return {
        "annualized_return": float(annual_return),
        "annualized_volatility": float(volatility),
        "sharpe_ratio": float(sharpe),
        "max_drawdown": float(drawdown.min()),
        "historical_var_95": var_95,
        "risk_level": level,
    }


def format_financial_report(ticker: str, research: dict[str, Any], risk: dict[str, Any]) -> str:
    """Format agent outputs as a recruiter-friendly Markdown report."""
    return f"""# Financial Intelligence Report: {ticker}\n\n## Research Summary\n- Latest Close: ${research['latest_close']:.2f}\n- Period Return: {research['period_return']:.2%}\n- 50-Day Moving Average: ${research['ma_50']:.2f}\n- Annualized Volatility: {risk['annualized_volatility']:.2%}\n\n## Risk Assessment\n- Annualized Return: {risk['annualized_return']:.2%}\n- Sharpe Ratio: {risk['sharpe_ratio']:.2f}\n- Maximum Drawdown: {risk['max_drawdown']:.2%}\n- 95% Historical VaR: {risk['historical_var_95']:.2%}\n- Risk Level: **{risk['risk_level']}**\n\n## Conclusion\nHistorical market metrics provide a quantitative snapshot of return and risk. They should be combined with fundamentals, valuation, current events, and individual risk tolerance before making investment decisions.\n\n> This project is for educational purposes only and does not provide financial advice or execute trades.\n"""
