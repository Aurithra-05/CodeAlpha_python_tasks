import requests
import json
import os
from tabulate import tabulate
from datetime import datetime

# Configuration
API_KEY = "your key here"  # My Alpha Vantage API key
PORTFOLIO_FILE = "portfolio.json"

# Load portfolio from file
def load_portfolio():
    if os.path.exists(PORTFOLIO_FILE):
        with open(PORTFOLIO_FILE, 'r') as f:
            return json.load(f)
    return []

# Save portfolio to file
def save_portfolio(portfolio):
    with open(PORTFOLIO_FILE, 'w') as f:
        json.dump(portfolio, f, indent=4)

# Fetch real-time stock price
def get_stock_price(ticker):
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticker}&apikey={API_KEY}"
    response = requests.get(url)
    data = response.json()
    if "Global Quote" in data and "05. price" in data["Global Quote"]:
        return float(data["Global Quote"]["05. price"])
    return None

# Add stock to portfolio
def add_stock(portfolio, ticker, shares, purchase_price):
    price = get_stock_price(ticker)
    if price is None:
        print(f"Error: Could not fetch data for {ticker}. Check ticker or API limits.")
        return
    portfolio.append({
        "ticker": ticker.upper(),
        "shares": shares,
        "purchase_price": purchase_price,
        "current_price": price,
        "date_added": datetime.now().strftime("%Y-%m-%d")
    })
    save_portfolio(portfolio)
    print(f"Added {shares} shares of {ticker} to portfolio.")

# Remove stock from portfolio
def remove_stock(portfolio, ticker):
    ticker = ticker.upper()
    portfolio[:] = [stock for stock in portfolio if stock["ticker"] != ticker]
    save_portfolio(portfolio)
    print(f"Removed {ticker} from portfolio.")

# Update portfolio with current prices
def update_portfolio(portfolio):
    for stock in portfolio:
        price = get_stock_price(stock["ticker"])
        if price:
            stock["current_price"] = price
    save_portfolio(portfolio)

# Calculate portfolio summary
def portfolio_summary(portfolio):
    total_value = 0
    total_invested = 0
    table = []
    for stock in portfolio:
        value = stock["shares"] * stock["current_price"]
        invested = stock["shares"] * stock["purchase_price"]
        gain_loss = value - invested
        allocation = (value / sum(s["shares"] * s["current_price"] for s in portfolio)) * 100 if portfolio else 0
        total_value += value
        total_invested += invested
        table.append([
            stock["ticker"],
            stock["shares"],
            f"${stock['purchase_price']:.2f}",
            f"${stock['current_price']:.2f}",
            f"${value:.2f}",
            f"${gain_loss:.2f}",
            f"{allocation:.2f}%"
        ])
    headers = ["Ticker", "Shares", "Purchase Price", "Current Price", "Value", "Gain/Loss", "Allocation"]
    print("\nPortfolio Summary:")
    print(tabulate(table, headers=headers, tablefmt="grid"))
    print(f"\nTotal Portfolio Value: ${total_value:.2f}")
    print(f"Total Invested: ${total_invested:.2f}")
    print(f"Total Gain/Loss: ${total_value - total_invested:.2f}")

# Main menu
def main():
    portfolio = load_portfolio()
    while True:
        print("\nStock Portfolio Tracker")
        print("1. Add Stock")
        print("2. Remove Stock")
        print("3. View Portfolio")
        print("4. Update Prices")
        print("5. Exit")
        choice = input("Enter choice (1-5): ")
        
        if choice == "1":
            ticker = input("Enter stock ticker (e.g., AAPL): ")
            shares = float(input("Enter number of shares: "))
            purchase_price = float(input("Enter purchase price per share: "))
            add_stock(portfolio, ticker, shares, purchase_price)
        elif choice == "2":
            ticker = input("Enter stock ticker to remove: ")
            remove_stock(portfolio, ticker)
        elif choice == "3":
            if portfolio:
                update_portfolio(portfolio)
                portfolio_summary(portfolio)
            else:
                print("Portfolio is empty.")
        elif choice == "4":
            update_portfolio(portfolio)
            print("Portfolio prices updated.")
        elif choice == "5":
            print("Exiting. Portfolio saved.")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()