from flask import Flask
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from os import getenv

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///sorjonet"
db = SQLAlchemy(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    # TODO: check username and password from database users table
    # user name, password
    result = db.session.execute(f"SELECT password FROM dictionary_users WHERE username = '{username}'")
    right_password = result.fetchone()[0]
    #result = db.session.execute("SELECT COUNT(*) FROM messages")
    #count = result.fetchone()[0]
    #return render_template("index.html", count=count, messages='höpö')
    if password == right_password:
    	session["username"] = username
    	return redirect("/")
    else:
        session["username"] = username
        return redirect("/logout") 

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/new")
def new():
    del session["username"]
    return render_template("new.html")

@app.route("/test")
def test():
    return render_template("test.html")

@app.route("/result", methods=["POST"])
def result():
    del session["username"]
    return render_template("result.html",car=request.form["car"],
    dog=request.form["dog"], cat=request.form["cat"])


@app.route("/new_user", methods=["GET"])
def new_user():
    #del session["username"]
    return render_template("new_user.html")

 
@app.route("/add_new_user",methods=["POST"])
def add_new_user():
    username = request.form["username"]
    password = request.form["password"]
    teacher = 0
    if "teacher" in request.form:
        teacher = 1        
    sql = "INSERT INTO dictionary_users (username, password, teacher) VALUES (:username, :password, :teacher)"
    result = db.session.execute(sql, {"username":username, "password":password, "teacher":teacher})
    db.session.commit()
    return redirect("/")
    
@app.route("/new_word", methods=["GET"])
def new_word():
    #del session["username"]
    return render_template("new_word.html")
    
@app.route("/add_new_word", methods=["POST"])
def add_new_word():
    #del session["username"]
    word = request.form["word"]
    translation = request.form["translation"]
    sql = "INSERT INTO words (word, translation) VALUES (:word, :translation)"
    result = db.session.execute(sql, {"word":word, "translation":translation})
    db.session.commit()
    return redirect("/")

