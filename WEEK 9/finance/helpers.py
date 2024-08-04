import os
import requests
import urllib.parse

from flask import redirect, render_template, request, session
from functools import wraps

def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s

    # Render apology.html with error code and message
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """Decorate routes to require login."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def lookup(symbol):
    """Look up quote for symbol using the IEX API."""
    try:
        # API key should be set as an environment variable
        api_key = os.environ.get("API_KEY")
        if not api_key:
            raise RuntimeError("API_KEY not set")

        # Construct API URL
        url = f"https://cloud.iexapis.com/stable/stock/{urllib.parse.quote_plus(symbol)}/quote?token={api_key}"

        # Make API request
        response = requests.get(url)
        response.raise_for_status()

        # Parse JSON response
        quote = response.json()
        return {
            "name": quote["companyName"],
            "price": float(quote["latestPrice"]),
            "symbol": quote["symbol"]
        }
    except requests.RequestException:
        return None
    except (KeyError, TypeError, ValueError):
        return None


def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"


def validate_symbol(symbol):
    """Check if the stock symbol is valid by attempting to look it up."""
    return lookup(symbol) is not None


def get_user_cash(user_id):
    """Retrieve the cash balance for the specified user."""
    rows = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
    if rows:
        return rows[0]["cash"]
    return None


def update_user_cash(user_id, amount):
    """Update the user's cash balance by adding or subtracting the given amount."""
    db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", amount, user_id)


def log_transaction(user_id, symbol, shares, price):
    """Log a transaction (buy or sell) in the database."""
    db.execute(
        "INSERT INTO transactions (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)",
        user_id, symbol.upper(), shares, price
    )


def get_user_stocks(user_id):
    """Retrieve a summary of stocks owned by the user."""
    return db.execute(
        "SELECT symbol, SUM(shares) as total_shares FROM transactions WHERE user_id = ? GROUP BY symbol HAVING total_shares > 0",
        user_id
    )
