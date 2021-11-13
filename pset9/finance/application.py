import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    # initialises users ID and finds username and cash value
    user = session['user_id']
    username = db.execute("SELECT username FROM users WHERE id=?", user)[0]['username']
    userCash = db.execute("SELECT cash FROM users WHERE id=?", user)[0]['cash']

    # initialises all shares that user holds and initialises 2 variables.
    # user_invested tallys the current value of share holdings
    # info creates a list of dictionaries with information for every stock option user holds
    user_invested_info = db.execute("SELECT shares, shareSymbol FROM holdings WHERE userID=?", user)
    user_invested = 0
    info = []

    # itterates of all of users holdings and tallys user_invested and apps new dictionaries of information to the info list
    for index in range(len(user_invested_info)):
        user_invested += user_invested_info[index]['shares'] * lookup(user_invested_info[index]['shareSymbol'])['price']
        infoDict = {'symbol': user_invested_info[index]['shareSymbol'], 'name' : lookup(user_invested_info[index]['shareSymbol'])['name'] , 'shares' : user_invested_info[index]['shares'] , 'price' : usd(lookup(user_invested_info[index]['shareSymbol'])['price']), 'total' : usd(user_invested_info[index]['shares'] * lookup(user_invested_info[index]['shareSymbol'])['price'])}
        infoDict_copy = infoDict.copy()
        info.append(infoDict_copy)

    # formats information for display
    grandtotal = usd(userCash + user_invested)
    userCash = usd(userCash)
    user_invested = usd(user_invested)

    # renders the template passing through information for display
    return render_template("index.html", cash=userCash, username=username, invested=user_invested, grandtotal=grandtotal, info=info, )


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    #proccess buy requestid method is "POST"
    if request.method == "POST":

        #initialise symbol from form
        symbol = request.form.get("symbol").upper()

        #initialise shares from form and cast to an int
        shares = int(request.form.get("shares"))

        #intialise information for the Stock
        info = lookup(symbol)

        #check that symbol corresponds to a Stock
        if info == None:
            return apology("Incorrect Stock Symbol")

        #intialise user ID anf corresponding cash levels
        user = session['user_id']
        userCash = db.execute("SELECT cash FROM users WHERE id=?", user)[0]['cash']

        # check if user has enough cash to proccess
        if userCash < info['price'] * shares:
            return apology("not enough funds to proccess transaction")

        # if user has the cash inset into history database, update holdings database and reduce cash in users databse
        else:
            #insert transaction to history database
            foo = db.execute("INSERT INTO history(userID, shareSymbol, sharePrice, shareAmount, totalPrice, type) VALUES (?, ?, ?, ?, ?, ?)",
                              user, symbol, info['price'], shares, shares*info['price'], "BUY")

            # checking if first holdings of specifc share and either insert if first or update if not first
            bash = db.execute("SELECT shares FROM holdings WHERE shareSymbol=? AND userID=?", symbol, user)
            if not bash:
                boo = db.execute("INSERT INTO holdings(userID, shares, shareSymbol) VALUES (?, ?, ?)", user, shares, symbol)
            else:
                boo = db.execute("UPDATE holdings SET shares=? WHERE userID=? AND shareSymbol=?", bash[0]['shares'] + shares, user, symbol)

            # update cash values in users database
            gee = db.execute("UPDATE users SET cash=? WHERE id=?", userCash - shares*info['price'], user)

        #redirect user to index
        return redirect("/")

    # renders the buy html template if request method is "GET"
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    # intitialises ID and username of user
    user = session['user_id']
    username = db.execute("SELECT username FROM users WHERE id=?", user)[0]['username']

    # creates list of all values to pass to history.html from the history database
    history = db.execute("SELECT type, shareSymbol, sharePrice, shareAmount, totalPrice, date FROM history WHERE userID=?", user)

    return render_template("history.html", history=history, username=username)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():

    # proccess the quote and find pricing
    if request.method == "POST":
        # find Stock information and save to info
        info = lookup(request.form.get("symbol"))


        # if there is no stock info then return apology
        if info == None:
            return apology("No stock information found for symbol")

        # find name and price of stock and render the quoted template
        else:
            name = info["name"]
            price = usd(info["price"])
            return render_template("quoted.html", name=name, price=price)

    # if request method == "GET" render the quote template
    else:
        return render_template("quote.html")

@app.route

@app.route("/register", methods=["GET", "POST"])
def register():
    # registers user and adds to DATABASE and redirects to index
    if request.method == 'POST':
        # checks for a username error if non
        username = request.form.get('username')
        if not username:
            return apology("Must enter a Username")

        # check if username is taken and already in Database
        elif len(db.execute("SELECT username FROM users WHERE username=?", username)) != 0:
            return apology("Username already taken :(")

        # check for password and error if none
        password = request.form.get('password')
        if not password:
            return apology("Must enter a Password")

        # check if password matches confirmation
        elif password != request.form.get('confirmation'):
            return apology("Passwords do not Match")

        #insert User into database
        foo = db.execute("INSERT INTO users(username, hash) VALUES (?, ?)", username, generate_password_hash(password))

        # redirect user to login
        return redirect("/login")


    # if request method == 'GET'  render the register template
    else:
        return render_template("register.html")






@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    #proccess sell requestid method is "POST"
    if request.method == "POST":

        #initialise symbol from form
        symbol = request.form.get("symbol").upper()

        #initialise shares from form and cast to an int
        shares = int(request.form.get("shares"))

        #intialise information for the Stock
        info = lookup(symbol)

        #check that symbol corresponds to a Stock
        if info == None:
            return apology("Incorrect Stock Symbol")

        #intialise user ID, corresponding cash levels
        user = session['user_id']
        userCash = db.execute("SELECT cash FROM users WHERE id=?", user)[0]['cash']

        # check users stock level returning error if not held
        if len(db.execute("SELECT shares FROM holdings WHERE userID=? AND shareSymbol=?", user, symbol)) != 0:
            userStock = db.execute("SELECT shares FROM holdings WHERE userID=? AND shareSymbol=?", user, symbol)[0]['shares']
        else:
            return apology("do not posses stocks to sell")

        # check if user has enough stock to proccess
        if userStock <  shares:
            return apology("not enough shares to proccess transaction")

        # if user has the stocks, add to history database, update holdings database and increase cash in users databse
        else:
            #insert transaction to history database
            foo = db.execute("INSERT INTO history(userID, shareSymbol, sharePrice, shareAmount, totalPrice, type) VALUES (?, ?, ?, ?, ?, ?)",
                              user, symbol, info['price'], shares, shares*info['price'], "SELL")

            # update holding database and remove entities with no share holdings
            boo = db.execute("UPDATE holdings SET shares=? WHERE userID=? AND shareSymbol=?", userStock - shares, user, symbol)
            bash = db.execute("DELETE FROM holdings WHERE shares=0 AND userID=?", user)

            # update cash values in users database
            gee = db.execute("UPDATE users SET cash=? WHERE id=?", userCash + shares*info['price'], user)

        #redirect user to index
        return redirect("/")

    # renders the sell html template if request method is "GET"
    else:
        return render_template("sell.html")

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)

# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
