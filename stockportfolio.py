import requests

class StockPortfolioTracker:
    def __init__(self, api_key):
        self.api_key = api_key
        self.portfolio = {}

    def fetch_stock_price(self, symbol):
        """Fetch the current stock price for a given symbol."""
        base_url = 'https://www.alphavantage.co/query'
        function = 'GLOBAL_QUOTE'
        api_url = f'{base_url}?function={function}&symbol={symbol}&apikey={self.api_key}'

        try:
            response = requests.get(api_url)
            response.raise_for_status()
            data = response.json()
            if 'Global Quote' in data and '05. price' in data['Global Quote']:
                return float(data['Global Quote']['05. price'])
            else:
                print(f"Error: Invalid response for symbol '{symbol}'.")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error fetching stock price for '{symbol}': {e}")
            return None

    def add_stock_to_portfolio(self, symbol, quantity):
        """Add a stock to the portfolio or increase its quantity."""
        if quantity <= 0:
            print("Error: Quantity must be greater than zero.")
            return

        if symbol not in self.portfolio:
            self.portfolio[symbol] = 0
        self.portfolio[symbol] += quantity
        print(f"Added {quantity} shares of {symbol} to your portfolio.")

    def remove_stock_from_portfolio(self, symbol, quantity):
        """Remove a stock from the portfolio or decrease its quantity."""
        if symbol not in self.portfolio:
            print(f"Error: Stock '{symbol}' not found in portfolio.")
            return

        if quantity <= 0:
            print("Error: Quantity must be greater than zero.")
            return

        if self.portfolio[symbol] < quantity:
            print(f"Error: You cannot remove more shares than you own ({self.portfolio[symbol]}).")
            return

        self.portfolio[symbol] -= quantity
        if self.portfolio[symbol] == 0:
            del self.portfolio[symbol]
        print(f"Removed {quantity} shares of {symbol} from your portfolio.")

    def display_portfolio_value(self):
        """Display the portfolio's total value and individual stock performance."""
        if not self.portfolio:
            print("Your portfolio is empty.")
            return

        total_value = 0
        print("\nStock Portfolio:")
        print("---------------------------------------------------")
        for symbol, quantity in self.portfolio.items():
            price = self.fetch_stock_price(symbol)
            if price is not None:
                value = price * quantity
                total_value += value
                print(f"{symbol}: {quantity} shares | Price: ${price:.2f} | Value: ${value:.2f}")
            else:
                print(f"{symbol}: {quantity} shares | Price: Unavailable")

        print("---------------------------------------------------")
        print(f"Total Portfolio Value: ${total_value:.2f}\n")

    def view_portfolio(self):
        """View the current portfolio holdings."""
        if not self.portfolio:
            print("Your portfolio is empty.")
        else:
            print("\nCurrent Portfolio:")
            for symbol, quantity in self.portfolio.items():
                print(f"{symbol}: {quantity} shares")
            print()

# Example Usage
api_key = 'H0E7LEV3MMG57AHX'  # Replace with your Alpha Vantage API key
tracker = StockPortfolioTracker(api_key)

# Add stocks to the portfolio
tracker.add_stock_to_portfolio('AAPL', 10)
tracker.add_stock_to_portfolio('GOOGL', 5)

# View portfolio
tracker.view_portfolio()

# Display portfolio value
tracker.display_portfolio_value()

# Remove stocks from the portfolio
tracker.remove_stock_from_portfolio('AAPL', 5)
tracker.display_portfolio_value()