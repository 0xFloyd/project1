import os

from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session  #an additional extension to sessions which allows them to be stored server-side
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from helpers import login_required


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Configure session to use filesystem

app.config['FLASK_APP'] = 'application.py'       
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["TEMPLATES_AUTO_RELOAD"] = True      # Ensure templates are auto-reloaded
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']  #same command as os.getenv. allows us to use database_url environemntt variable to find database 
db = SQLAlchemy(app)

Session(app)

# Set up database
#engine = create_engine(os.getenv("DATABASE_URL"))       #same command as os.getenv
#db = scoped_session(sessionmaker(bind=engine))


# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

@app.route("/", methods=["GET", "POST"])
#@login_required
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    session.clear()     #forget if there's a user_id

    if request.method == "POST":
        if not request.form.get("username"):
            errorMessage = "Must provide username"
            return errorMessage

        # Ensure password was submitted
        elif not request.form.get("password"):
            errorMessage = "Must provide password"
            return errorMessage

        return redirect("/")
        
    else:
        return render_template("login.html")


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/logout")
#@login_required
def logout():
    return render_template("logout.html")


