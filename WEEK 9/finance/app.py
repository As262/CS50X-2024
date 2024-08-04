from flask import Flask, render_template, request, redirect, session, url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from cs50 import SQL
from functools import wraps
import requests
import os
import urllib.parse

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

def login_required(f):
    """Decorator to require login for certain routes."""
    @wraps(f)
    def wrapped_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return wrapped_function

@app.context_processor
def utility_processor():
    def usd(value):
        """Format value as USD."""
        return f"${value:,.2f}"
    return dict(usd=usd)

def lookup(symbol):
    """Look up quote for symbol."""
    try:
        api_key = os.environ.get("API_KEY")
        url = f"https://cloud.iexapis.com/stable/stock/{urllib.parse.quote_plus(symbol)}/quote?token={api_key}"
        response = requests.get(url)
        print(f"Request URL: {url}")  # Debug: Print URL
        print(f"Response Status Code: {response.status_code}")  # Debug: Print Status Code
        response.raise_for_status()

        quote = response.json()
        print(f"API Response: {quote}")  # Debug: Print API Response

        return {
            "name": quote.get("companyName", "Unknown"),
            "price": float(quote.get("latestPrice", 0)),
            "symbol": quote.get("symbol", symbol)
        }
    except (requests.RequestException, KeyError, TypeError, ValueError) as e:
        print(f"Error in lookup: {e}")
        return None

@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    user_id = session["user_id"]

    # Get user cash
    rows = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
    cash = rows[0]["cash"]

    # Get user's stocks
    stocks = db.execute("""
        SELECT symbol, SUM(shares) AS total_shares
        FROM transactions
        WHERE user_id = ?
        GROUP BY symbol
        HAVING SUM(shares) > 0
    """, user_id)

    total = 0
    for stock in stocks:
        quote = lookup(stock["symbol"])
        if quote:
            stock["name"] = quote["name"]
            stock["price"] = quote["price"]
            stock["total"] = stock["total_shares"] * stock["price"]
            total += stock["total"]
        else:
            stock["name"] = "Unknown"
            stock["price"] = 0
            stock["total"] = 0

    return render_template("index.html", stocks=stocks, cash=cash, total=total + cash)

@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        symbol = request.form.get("symbol")

        if not symbol:
            return apology("must provide symbol", 400)

        quote = lookup(symbol.upper())
        if quote is None:
            return apology("invalid symbol", 400)

        return render_template("quoted.html", name=quote["name"], symbol=quote["symbol"], price=usd(quote["price"]))
    else:
        return render_template("quote.html")

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock."""
    if request.method == "POST":
        symbol = request.form.get("symbol").upper()
        shares = request.form.get("shares")

        if not symbol:
            return apology("must provide symbol", 400)
        if not shares or not shares.isdigit() or int(shares) <= 0:
            return apology("must provide a positive number of shares", 400)

        shares = int(shares)
        quote = lookup(symbol)
        if quote is None:
            return apology("invalid symbol", 400)

        cost = quote["price"] * shares
        print(f"Cost: {cost}")  # Debug: Print cost

        rows = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        cash = rows[0]["cash"]
        print(f"User Cash: {cash}")  # Debug: Print user cash

        if cost > cash:
            return apology("can't afford", 400)

        db.execute("UPDATE users SET cash = cash - ? WHERE id = ?", cost, session["user_id"])
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)",
                   session["user_id"], symbol, shares, quote["price"])

        return redirect(url_for("index"))
    else:
        return render_template("buy.html")

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock."""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        if not symbol:
            return apology("must provide symbol", 400)
        if not shares or not shares.isdigit() or int(shares) <= 0:
            return apology("must provide a positive number of shares", 400)

        shares = int(shares)
        rows = db.execute("SELECT shares FROM transactions WHERE user_id = ? AND symbol = ?",
                          session["user_id"], symbol.upper())
        total_shares = sum(row["shares"] for row in rows)
        if shares > total_shares:
            return apology("not enough shares", 400)

        quote = lookup(symbol.upper())
        if quote is None:
            return apology("invalid symbol", 400)

        # Update user's cash and record transaction
        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", quote["price"] * shares, session["user_id"])
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)",
                   session["user_id"], symbol.upper(), -shares, quote["price"])

        return redirect(url_for("index"))
    else:
        symbols = db.execute("SELECT DISTINCT symbol FROM transactions WHERE user_id = ?", session["user_id"])
        return render_template("sell.html", symbols=symbols)

@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    transactions = db.execute("""
        SELECT symbol, shares, price, transacted
        FROM transactions
        WHERE user_id = ?
        ORDER BY transacted DESC
    """, session["user_id"])

    return render_template("history.html", transactions=transactions)

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Check if fields are empty
        if not username or not password or not confirmation:
            return apology("must fill out all fields", 400)

        # Check if passwords match
        if password != confirmation:
            return apology("passwords must match", 400)

        hash_password = generate_password_hash(password)

        # Check for existing username
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(rows) > 0:
            return apology("username already taken", 400)

        # Register user
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash_password)

        return redirect(url_for("login"))
    else:
        return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            return apology("must provide username and password", 400)

        # Fetch user details from the database
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(rows) != 1:
            return apology("invalid username and/or password", 400)

        # Check password hash
        user = rows[0]
        if not check_password_hash(user["hash"], password):
            return apology("invalid username and/or password", 400)

        # Log user in
        session["user_id"] = user["id"]

        return redirect(url_for("index"))
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""
    session.clear()
    return redirect(url_for("index"))

def apology(message, code=400):
    """Render message as an apology to user."""
    return render_template("apology.html", bottom=message), code

if __name__ == "__main__":
    app.run(debug=True)
