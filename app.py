#to run this app use the terminal command "flask run"
#set enviroment variables:
#set FLASK_APP app.py
from flask import Flask, render_template, session, redirect
from flask_session import Session
import testing_variables as testing
import sqlite3 as sql

conn = sql.connect("TrimilEnterpreses.db") #initialise Database
cursor = conn.cursor() #initilise cursor to execute SQL commands
app = Flask(__name__) #initialise the flask application
#config to set up sessions for a secure login system
app.config["SESSION_TYPE"] = 'filesystem'
app.config["SESSION_PERMANENT"] = False
Session(app)

@app.route("/")
#this is the home route
def index():
    return render_template("index.html", )

@app.route("/blog",methods=["GET","POST"])
def blog():
    return render_template("blog-home.html", posts = testing.posts )

@app.route("/blog/<int:id>",methods=["GET","POST"])
#route for all blog posts.
def posts(id):
    return render_template("blog-post.html",content = testing.posts_list_full_items[id-1])

@app.route("/login",methods=["GET","POST"])
def login():
    return render_template("login.html")

@app.route("/review")
def review():

    return render_template("listOfReviews.html")

@app.route("/review/create")
def create_review():
    
    return render_template("createReview.html")