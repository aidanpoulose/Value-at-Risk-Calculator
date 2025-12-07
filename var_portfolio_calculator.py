import yfinance as yf
from math import floor, ceil
import datetime


def main(portfolio):
    if not isinstance(portfolio, dict):
        raise TypeError("Portfolio must be a dictionary.")
    for stock, value in portfolio.items():
        if not isinstance(value, (int, float)) or value <= 0:
            raise ValueError(f"Amount for {stock} must be positive.")
    total = sum(portfolio.values())
    weights = {}
    stocks = list(portfolio.keys())
    tod = datetime.datetime.today().strftime("%Y-%m-%d")
    for stock in stocks:
        weights[stock] = portfolio[stock]/total
    try:
        data = yf.download(stocks, start = "2020-01-01", end = tod, interval = "1d", auto_adjust = True)
    except Exception as e:
        raise ValueError(f"Failed to download stock data: {e}")
    missing = []
    for stock in stocks:
        if stock not in data["Close"].columns:
            missing.append(stock)
    if missing:
        raise ValueError(f"No data found for the following stock(s): {', '.join(missing)}")
    prices = data["Close"]
    prices = prices.dropna()
    returns = prices.copy()
    for stock in prices.columns:
        stock_prices = prices[stock].values
        stock_returns = []
        for i in range(1, len(stock_prices)):
            r = (stock_prices[i] - stock_prices[i-1])/stock_prices[i-1]
            stock_returns.append(r)
        returns[stock] = [None] + stock_returns
    returns = returns.dropna()
    portfolio_returns = []
    for index, row in returns.iterrows():
        daily_return = 0
        for stock in returns.columns:
            daily_return += row[stock] * weights[stock]
        portfolio_returns.append(daily_return)
    portfolio_returns = sorted(portfolio_returns)
    N = len(portfolio_returns)
    index = N * 0.05
    lower_index = floor(index)
    upper_index = ceil(index)
    percentile = portfolio_returns[lower_index] + (index - lower_index) * (portfolio_returns[upper_index] - portfolio_returns[lower_index])
    VaR = round(abs(percentile * total), 2)
    print(f"The Estimated Potential Loss at 95% confidence level is ${VaR}")

portfolio = {"AAPL":5000, "APLD":1000, "NVDA":10000}
main(portfolio)
