from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp

from helpers import *

# configure application
app = Flask(__name__)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# custom filter
app.jinja_env.filters["usd"] = usd

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

@app.route("/")
@login_required
def index():
    #select each symbol owned by the user and its amount
    portfolio_symbols = db.execute("SELECT shares, symbol FROM portfolio WHERE id = :id", id= session["user_id"])

    #ceate a temporary variable to store total(cash+share)
    total_cash = 0

    #update each symbol prices and total
    for portfolio_symbol in portfolio_symbols:
        symbol = portfolio_symbol["symbol"]
        shares = portfolio_symbol["shares"]
        stock = lookup(symbol)
        total = shares * stock["price"]
        total_cash += total
        db.execute("UPDATE portfolio SET price = :price, total=:total WHERE id = :id AND symbol=:symbol",\
        price = usd(stock["price"]), total = usd(total), id = session["user_id"], symbol=symbol)

    #update user's cash in portfolio
    updated_cash = db.execute("SELECT cash FROM users WHERE id=:id", id = session["user_id"])

    #update total cash
    total_cash += updated_cash[0]["cash"]

    #print portfolio in index homepage
    updated_portfolio = db.execute("SELECT * FROM portfolio WHERE id= :id", id = session["user_id"])

    return render_template("index.html", stocks=updated_portfolio, cash=usd(updated_cash[0]["cash"]), total= usd(total_cash) )

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock."""
    if request.method == "GET":
        return render_template("buy.html")
    else:
        stock = lookup(request.form.get("symbol"))
        if not stock:
            return apology("Invalid symbol")

    #ensure proper number of shares
    try:
        shares = int(request.form.get("shares"))
        if shares < 0:
            return apology("shares must be positive integer")
    except:
        return apology("shares must be positive integer")

    #select user's cash
    money = db.execute("SELECT cash FROM users WHERE id = :id", id = session["user_id"])

    #check if enough money to buy
    if not money or float(money[0]["cash"])< stock["price"]*shares:
        return apology("Not enough money")
    #update history
    db.execute("INSERT INTO history (symbol, shares, price, id) VALUES(:symbol, :shares, :price, :id)", symbol = stock["symbol"],\
    shares=shares, price = usd(stock["price"]), id = session["user_id"])

    #update user's cash
    db.execute("UPDATE users SET cash = cash - :purchase WHERE id = :id", id=session["user_id"], purchase=stock["price"] * float(shares))

    #select user's share of that symbol
    user_shares= db.execute("SELECT shares FROM portfolio WHERE id = :id AND symbol = :symbol", id=session["user_id"], symbol=stock["symbol"])

    #if user's doesn't have shares of that symbol. create newstock object
    if not user_shares:
        db.execute("INSERT INTO portfolio (name, shares, price, total, symbol, id) VALUES(:name, :shares, :price, :total, :symbol, :id)",\
        name=stock["name"], shares=shares, price=usd(stock["price"]),total=usd(shares * stock["price"]), symbol=stock["symbol"], id=session["user_id"])
    #else increment the shares count
    else:
        shares_total = user_shares[0]["shares"] + shares
        db.execute("UPDATE portfolio SET shares=:shares WHERE id=:id AND symbol=:symbol",shares=shares_total, id=session["user_id"],\
        symbol=stock["symbol"])

        # return to index
    return redirect(url_for("index"))

@app.route("/history")
@login_required
def history():
    """Show history of transactions."""
    history = db.execute("SELECT * FROM history WHERE id = :id", id = session["user_id"])
    return render_template("history.html",history = history)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
            return apology("invalid username and/or password")

        # remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # redirect user to home page
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out."""

    # forget any user_id
    session.clear()

    # redirect user to login form
    return redirect(url_for("login"))

@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        rows = lookup(request.form.get("symbol"))
        if not rows:
            return apology("Invalid symbol")

        return render_template("quoted.html", stock=rows)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""
    if request.method == "POST":
        if not request.form.get("username"):
            return apololgy("must provide username")
        elif not request.form.get("password"):
            return apology("must provide password")
        elif request.form.get("password") != request.form.get("passwordagain"):
            return apology("password doesnot match")

        # insert the new user into users, storing the hash of the user's password
        result = db.execute("INSERT INTO users(username, hash) VALUES(:username, :hash)", username = request.form.get("username"), hash = pwd_context.encrypt(request.form.get("password")))

        if not result:
            return apology("user name already exist")

        #remeber user who has logged in
        session_id["user_id"] = result

        #redirect user to homepage
        return redirect(url_for("index"))
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock."""
    if request.method == "GET":
        return render_template("sell.html")
    else:
        # ensure proper symbol
        stock = lookup(request.form.get("symbol"))
        if not stock:
            return apology("Invalid symbol")
        # ensure proper number of shares
        try:
            shares = int(request.form.get("shares"))
            if shares < 0:
                return apology("shares must be positive integer")
        except:
            return apology("share must be a positive integer")

        # select the symbol shares of that user
        user_shares = db.execute("SELECT shares FROM portfolio WHERE id = :id AND symbol= :symbol", id = session["user_id"], symbol = stock["symbol"])
        # check if enough shares to sell
        if not user_shares or int(user_shares[0]["shares"]) < shares:
            return apology("not enough shares")

        #update history of sell
        db.execute("INSERT INTO history (symbol,shares,price,id) VALUES (:symbol, :shares, :price, :id)", symbol= stock["symbol"], shares=-shares)

        #update user cash
        db.execute("UPDATE users SET cash = cash + :purchase WHERE id = :id", id = session["user_id"], symbol = stock["symbol"])

        #decrement the shares count
        shares_total = user_shares[0]["shares"] - shares

        #if decrement is zero, delete shares from portfolio
        if shares_total == 0:
            db.execute("DELETE FROM portfolio where id = :id AND symbol= :symbol", id=session["user_id"], symbol = stock["symbol"])

        #otherwise update portfolio shares count
        else:
            db.execute("UPDATE portfolio SET shares=:shares WHERE id=:id AND symbol=:symbol", shares=shares_total, id=session["user_id"],symbol=stock["symbol"])

        #return to index
        return redirect(url_for("index"))


