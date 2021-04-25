from flask import Flask
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from os import getenv

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///sorjonet"
#app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://fayzaydkuxqoez:c642c128e75d01856fe93e1acf1c558fd092a27ba906206948367486efc4b417@ec2-35-174-35-242.compute-1.amazonaws.com:5432/d30ggv0nvmot3l"
db = SQLAlchemy(app)

@app.route("/")
def index():
    return render_template("index.html")
    
@app.route("/styles")
def styles():
    return render_template("styles.css")

@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    # TODO: check username and password from database users table
    # user name, password
    if username == "" or password == "":
    	return render_template("error.html")
    result = db.session.execute(f"SELECT password FROM dictionary_users WHERE username = '{username}'")
    user = db.session.execute(f"SELECT username FROM dictionary_users WHERE username = '{username}'")
    right_password = result.fetchone()[0]
    right_username = user.fetchone()[0]    
    #print( user.fetchone()[0])
    #result = db.session.execute("SELECT COUNT(*) FROM messages")
    #count = result.fetchone()[0]
    #return render_template("index.html", count=count, messages='höpö')
    if password == right_password and username == right_username:
    	session["username"] = username
    	return redirect("/")
    else:
        #session["username"] = username
        return render_template("error.html") 

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/new")
def new():
    del session["username"]
    return render_template("new.html")

@app.route("/select_deck")
def select_deck():
    result = db.session.execute("SELECT deck_id, name FROM deck")
    name = result.fetchall()
    return render_template("select_deck.html", name=name)
    
@app.route("/test")
def test():
    result = db.session.execute("SELECT deck_id, test_id FROM test")
    deck = result.fetchall()
    return render_template("test.html", deck=deck)

@app.route("/result", methods=["POST"])
def result():
    #del session["username"]
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
    if username == "" or password == "":
    	return render_template("error.html")
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
    if word == "" or translation == "":
    	return render_template("error.html")
    sql = "INSERT INTO words (word, translation) VALUES (:word, :translation)"
    result = db.session.execute(sql, {"word":word, "translation":translation})
    db.session.commit()
    return redirect("/")
    
@app.route("/new_deck", methods=["GET"])
def new_deck():
    return render_template("new_deck.html")
    
@app.route("/add_new_deck", methods=["POST"])    
def add_new_deck():    
    name = request.form["name"]
    difficulty = request.form["difficulty"]
    if name == "" or difficulty == "" or (difficulty != "1" and difficulty != "2" and difficulty != "3" and difficulty != "4" and difficulty != "5"):
    	return render_template("error.html")
    sql = "INSERT INTO deck (difficulty, name) VALUES (:difficulty, :name)"
    result = db.session.execute(sql, {"difficulty":difficulty, "name":name})
    db.session.commit()
    return redirect("/")
    
@app.route("/estimate", methods=["GET"])
def estimate():
    return render_template("new_estimate.html")
    
@app.route("/add_new_estimate", methods=["POST"])
def add_new_estimate():
    comment = request.form["estimate"]
    if comment != "":
        sql = "INSERT INTO estimate (comment) VALUES (:comment)"
        result = db.session.execute(sql, {"comment":comment})
        db.session.commit()
        return redirect("/")
    return redirect("/")
    
@app.route("/all_estimates")
def all_estimates():
    result = db.session.execute("SELECT comment FROM estimate")
    estimate = result.fetchall()
    return render_template("all_estimates.html", estimate=estimate)
