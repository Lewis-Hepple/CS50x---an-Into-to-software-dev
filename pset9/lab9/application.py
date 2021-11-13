import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        IDlist = db.execute("SELECT max(id) FROM birthdays")
        ID = IDlist[0]['max(id)'] + 1
        name = request.form.get("name")
        day = request.form.get("day")
        month = request.form.get("month")

        if name == None or name == "" or int(month)>12 or int(month)<1 or int(day)>31 or int(day)<1:
            return redirect('/error')

        foo = db.execute("INSERT INTO birthdays(id, name, month, day) VALUES (?, ?, ?, ?)", ID, name, month, day)
        return redirect("/")

    else:
        info = db.execute("SELECT * FROM birthdays")
        return render_template("index.html", info=info)

@app.route("/error", methods=['GET', 'POST'])
def error():
    if request.method == "GET":
        return render_template("error.html")

    if request.method == "POST":
        return redirect("/")