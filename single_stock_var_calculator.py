import yfinance as yf
import math
import datetime

z_scores = {
        0.90: 1.2816,
        0.95: 1.6449,
        0.975: 1.96,
        0.99: 2.3263}

def calculator(prices, confidence, portfolio_value):
    returns = []
    for i in range(1, len(prices)):
        daily = (prices[i] - prices[i-1])/prices[i-1]
        returns.append(daily)
    N = len(returns)
    mean_returns = sum(returns)/N
    variance = sum((r - mean_returns) ** 2 for r in returns)/ (N-1)
    std_dev = variance ** 0.5
    z = z_scores[confidence]
    var = -(mean_returns - z * std_dev)*portfolio_value
    return var

def main():
    stock = input("Enter stock:").upper()
    try:
        tod = datetime.datetime.today().strftime("%Y-%m-%d")
        data = yf.download(stock, start = "2020-01-01", end = tod, interval = "1d")
        if data.empty:
            raise ValueError("Stock not found")
        value = float(input("Enter your portfolio ($):"))
        price = list(data[("Close", stock)])
        res = round(calculator(price, 0.95, value), 2)
        days = input("Choose time horizon 1-day/1-week:")
        if days == "1-week":
            n = 5
            res = round(res * (n ** 0.5), 2)
        print(f"For 95% confidence level with a {days} horizon, the Estimated Potential Loss is {res}")
    except Exception as error:
        print("Error", error)
main()
