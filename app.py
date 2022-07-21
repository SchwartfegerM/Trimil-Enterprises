#to run this app use the terminal command "flask run"
#set enviroment variables:
#set FLASK_APP app.py
from os import urandom
from flask import Flask, render_template, session, redirect, request, url_for, jsonify
from flask_session import Session
from database_funtions import get_database_connection

app = Flask(__name__) #initialise the flask application
#config to set up sessions for a secure login system
app.config["SESSION_TYPE"] = 'filesystem'
app.config["SESSION_PERMANENT"] = False
app.secret_key = urandom(24)
Session(app)


@app.route("/")
#route for the home page
def index():
  conn=get_database_connection()
  posts = conn.execute("SELECT * FROM BlogPosts").fetchall()
  conn.close()
  return render_template("index.html", posts = posts)

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

@app.route("/login",methods=["GET","POST"])
def login():
    return render_template("login.html")

@app.route("/login/verify",methods=["GET","POST"])
def verify():
  if request.method == "POST":
    try:
      username = request.form.get("username",None)
      password = request.form.get("password",None)
      conn=get_database_connection()
      account = conn.execute("SELECT * FROM Login WHERE Username = ?", (username,)).fetchall()
      if account[0][2] == password:
        session["username"] = username
        return redirect("/blog/list") 
      else:
        return redirect("/login")
      conn.close()
    except:
      return redirect("/login")
  else:
    return redirect(url_for("index"))

@app.route("/logout",methods=["GET","POST"])
def logout():
  session.pop("username", None)
  return redirect("/")

#routes and funtions for the reviews component

@app.route("/reviews")
#servs the list of all reviews in the database
def review():
  conn=get_database_connection()
  reviews=conn.execute("SELECT * FROM Reviews").fetchall()
  conn.close()
  return render_template("listOfReviews.html", reviews=reviews)

@app.route("/reviews/create")
#serves the create a review html template
def create_review():
    return render_template("createReview.html")

@app.route("/reviews/submitted",methods=["POST"])
#stores the contents in the review form and serves the page to thanks the user for the review.
def review_submitted():
  #get items from the review form
  first_name = request.form.get("first_name",None)
  last_name = request.form.get("last_name",None)
  content = request.form.get("content",None)
  organisation = request.form.get("organisation",None)
  email = request.form.get("email",None)
  conn=get_database_connection() #connect to the database
  conn.execute("INSERT INTO Reviews(FirstName,LastName,Content,organisation,email) VALUES (?,?,?,?,?)",(first_name,last_name,content,organisation,email)) #insert values into the database
  conn.commit() #commit changes to the database
  conn.close() #close connection to the databse
  return render_template("submittedReview.html") #render the review submitted template

#routes and functions for the ADMIN side of the blog component

@app.route("/blog/list", methods=["GET","POST"])
#this is the list of posts visable to ADMIN accounts
def blog_posts_list():
  if "username" in session:
    conn = get_database_connection()
    posts = conn.execute("SELECT * FROM BlogPosts").fetchall()
    conn.close()
    return render_template("admin-list-of-posts.html",posts = posts)
  else:
    return redirect(url_for("index"))

@app.route('/blog/create')
def create_blog_post():
  if "username" in session:
    return render_template("createBlogPost.html")
  else: 
    return redirect(url_for("index"),post_url="blogpost/submit")

@app.route('/blogpost/submit',methods=["POST"])
#remove this when blog post handling is done
def blog_post_submit():
  post_name=request.form.get("post_name",None)
  post_date=request.form.get("post_date",None)
  post_summary=request.form.get("post_summary",None)
  post_content=request.form.get("post_content",None)
  conn = get_database_connection()
  conn.execute("INSERT INTO BlogPosts(Title,Date,Summary,Content) VALUES (?,?,?,?)",(post_name,post_date,post_summary,post_content))
  conn.commit()
  conn.close()
  return redirect(url_for("blog_posts_list"),code="307")

@app.route("/blog/<int:id>/edit")
def blog_post_edit(id):
  conn = get_database_connection()
  post_data = conn.execute("SELECT * FROM BlogPosts WHERE id=?",(id,)).fetchall()
  conn.close()
  return render_template("createBlogPost.html", post=post_data, post_url="/blog/{}/edit/update".format(id))

@app.route("/blog/<int:id>/edit/update",methods=["POST"])
def update_post(id):
  post_name=request.form.get("post_name",None)
  post_date=request.form.get("post_date",None)
  post_summary=request.form.get("post_summary",None)
  post_content=request.form.get("post_content",None)
  conn=get_database_connection()
  conn.execute("UPDATE BlogPosts SET title=?,date=?,Summary=?,content=? WHERE id=?",(post_name,post_date,post_summary,post_content,id))
  conn.commit()
  conn.close()
  return redirect(url_for("blog_posts_list"),code=307)

@app.route("/blog/<int:id>/delete")
def blog_post_delete(id):
  conn = get_database_connection()
  conn.execute("DELETE FROM BlogPosts WHERE id=?",(id,))
  conn.commit()
  conn.close()
  return redirect("/blog/list")

#routes and functions for the invoicing system component

@app.route("/invoicing")
def invoicing():
  return render_template("invoicing.html")

@app.route("/json")
def json():
  conn = get_database_connection()
  invoices = conn.execute("SELECT * FROM invoices").fetchall()
  conn.close()
  invoice = [dict(row) for row in invoices]
  return jsonify(invoice)

@app.route("/add/<string:action>/<int:id>/<string:part>/<string:new_value>", methods=["POST"])
def add_invoice(action,id,part,new_value):
  conn = get_database_connection()
  if action == "UPDATE":
    conn.execute("UPDATE invoices SET "+part+"=? WHERE id=?",(new_value,id))
  elif action == "DELETE":
    conn.execute("DELETE FROM invoices WHERE id=?",(id,))
  else:
    return "Not a valid action"
  conn.commit()
  conn.close()
  return redirect(url_for("invoicing"))

@app.route("/invoices/create", methods=["POST"])
def create_invoice():
  if request.method == "POST":
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    office_charges = request.form["office_charges"]
    project_management = request.form["project_management"]
    travel_expenses = request.form["travel_charges"]
    consulation_fee = request.form["consultancy_charges"]
    conn = get_database_connection()
    conn.execute("INSERT INTO invoices(first_name,last_name,office_charges,project_management,travel_charges,consultancy_charges) VALUES (?,?,?,?,?,?)",(first_name,last_name,office_charges,project_management,travel_expenses,consulation_fee))
    conn.commit()
    conn.close()
    return redirect(url_for("invoicing"))
    #could put in a total here if time presents itself


if __name__ == "__main__":
  app.run(host='0.0.0.0', port=81,debug=True)
