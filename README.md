Overview
This Python script calculates the Value-at-Risk (VaR) for a single stock based on historical price data. VaR is a commonly used risk metric that estimates the potential loss in a portfolio over a specified time horizon at a given confidence level.
The calculator allows users to:
        Enter a stock ticker symbol.
        Specify the portfolio value invested in that stock.
        Compute VaR for 1-day or 1-week horizons at a 95% confidence level.
Features:
        Retrieves historical stock prices using yfinance.
        Computes daily returns and calculates VaR using the parametric method (normal distribution).
        Scales VaR for weekly horizon using √5 rule.
        Handles multi-year historical data starting from 2020.
