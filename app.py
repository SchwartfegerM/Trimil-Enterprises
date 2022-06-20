#to run this app use the terminal command "flask run"
#set enviroment variables:
#set FLASK_APP app.py
from flask import Flask, render_template, session, redirect, request
from flask_session import Session
import sqlite3 as sql


app = Flask(__name__) #initialise the flask application
#config to set up sessions for a secure login system
app.config["SESSION_TYPE"] = 'filesystem'
app.config["SESSION_PERMANENT"] = False
Session(app)

def get_database_connection():
  conn = sql.connect('TrimilEnterprises.db')
  conn.row_factory = sql.Row
  return conn

@app.route("/")
#route for the home page
def index():
    return render_template("index.html", )

@app.route("/blog",methods=["GET","POST"])
#route for the list of blog posts
def blog():
  conn=get_database_connection()
  posts = conn.execute("SELECT * FROM BlogPosts").fetchall()
  conn.close()
  return render_template("blog-home.html", posts = posts )

@app.route("/blog/<int:id>",methods=["GET","POST"])
#generates a route for each blog post in the database
def posts(id):
  conn=get_database_connection()
  posts = conn.execute("SELECT * FROM BlogPosts").fetchall()
  conn.close()
  return render_template("blog-post.html",content = posts[id-1])

@app.route("/blog/list", methods=["GET","POST"])
#this is the list of posts visable to ADMIN accounts
def blog_posts_list():

  return render_template("admin-list-of-posts.html")

@app.route('/blog/create')
def create_blog_post():
  #tutorial on BLOB data https://pynative.com/python-sqlite-blob-insert-and-retrieve-digital-data/
  #some season checking code HERE
  return render_template("createBlogPost.html")

@app.route("/login",methods=["GET","POST"])
def login():
    return render_template("login.html")

@app.route("/login/verify",methods=["GET","POST"])
def verify():
  username = request.form.get("username",None)
  password = request.form.get("password",None)
  conn=get_database_connection()
  account = conn.execute("SELECT * FROM Login WHERE Username = ?", username).fetchall()
  if account["Password"] == password:
    return redirect("/blog/list") 
  else:
    return redirect("/login")
  conn.close()

@app.route("/reviews")
def review():
  conn=get_database_connection()
  reviews=conn.execute("SELECT * FROM Reviews").fetchall()
  conn.close()
  return render_template("listOfReviews.html", reviews=reviews)

@app.route("/reviews/create")
def create_review():
    
    return render_template("createReview.html")

@app.route("/reviews/submitted",methods=["POST"])
#thank the user for the review
def thanks_for_the_review():
  first_name = request.form.get("first_name",None)
  last_name = request.form.get("last_name",None)
  content = request.form.get("content",None)
  organisation = request.form.get("organisation",None)
  return render_template("submittedReview.html",first_name=first_name,last_name=last_name,content=content,organisation=organisation)



@app.route('/TODO',methods=["POST"])
#remove this when blog post handling is done
def temp():
  post_name=request.form.get("post_name",None)
  post_thumbnail=request.form.get("post_thumbnail",None) #currently not working FIX TODO
  post_date=request.form.get("post_date",None)
  post_summary=request.form.get("post_summary",None)
  post_content=request.form.get("post_content",None)
  return render_template("temp.html",name=post_name,thumbnail=post_thumbnail,date=post_date,summary=post_summary,content=post_content)

@app.route("/blog/<int:id>/edit")
def blog_post_edit(id):

  return render_template("")

@app.route("/invoicing")
def invoiceing():

  return render_template("")



if __name__ == "__main__":
  app.run(host='0.0.0.0', port=81,debug=True)
