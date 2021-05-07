from flask import Flask
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from os import getenv

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
#app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://musenyxyafkmob:1949fc7810991bad9aca3776aec3ce6bab7e04aa5952f2268020e8ea77af669a@ec2-54-78-36-245.eu-west-1.compute.amazonaws.com:5432/dff2medqhagcfq"
#app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://owkiheatxgznon:1038a0c805536c3d5ac8b8022074896b83c02bcc07a08a14b53f4c29d05701f0@ec2-79-125-30-28.eu-west-1.compute.amazonaws.com:5432/dcbkim9c0n99al"
db = SQLAlchemy(app)

def checklogin():
    #Check if username is login or not. If not this return error.
    if len(session) == 0 or session["username"] == None or session["user_id"] == None:
    	raise Exception("Et ole kirjautunut sisään!")
        #return render_template('error.html', error = 'Et ole kirjautunut sisään')
    
@app.route("/")
def index():
    return render_template("index.html")
    
@app.route("/styles")
def styles():
    #CSS Styles
    return render_template("styles.css")

@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    
    #Takes user information from database where the username you provided is "username"
    result = db.session.execute(f"SELECT password, user_id, teacher FROM dictionary_users WHERE username = '{username}'")
    result_list = result.fetchone()
    right_password = result_list[0]
    user_id = result_list[1]
    teacher = result_list[2]
    
    #Check if the username have right password
    if password == right_password:
        session["username"] = username  
        session["user_id"] = user_id
        session["teacher"] = teacher
    return redirect("/") 

@app.route("/logout")
def logout():

    #Deletes all sessions and returns back to login screen
    del session["username"]
    del session["user_id"]
    del session["teacher"]
    return redirect("/")

@app.route("/select_deck")
def select_deck():
    checklogin()
    
    #Select all decks and their information
    result = db.session.execute("SELECT deck.deck_id, deck.name, deck.difficulty, COUNT(words.word) FROM deck, words WHERE deck.deck_id = words.deck_id GROUP BY deck.deck_id")
    name = result.fetchall()
    return render_template("select_deck.html", name=name)
    
@app.route("/test")
def test():
    checklogin()
    deck_id = request.args.get("deck_id")
    
    #SELECT every word from database where deck_id is the same as what you selected
    result = db.session.execute(f"SELECT card_id, word, deck_id FROM words WHERE deck_id = {deck_id}")
    word = result.fetchall()
    return render_template("test.html", word=word, deck_id=deck_id)

@app.route("/result", methods=["POST"])
def result():
    checklogin()
    form_data = request.form
    
    #There is three arrays. One with all words, one with right answers and last with wrong answers
    words = {}
    rights = {}
    wrongs = {}
    deck_id = request.form["deck_id"]
    user_id = session['user_id']
    
    #Takes all keys and values from test.html and if it starts with translation_, we take a id one after split. 
    #And then we take all words and translations from database where card_id is splitted card_id.
    for key,value in form_data.items():
    	if key.startswith("translation_"):
    	    card_id = int(key.split("translation_")[1])
    	    result = db.session.execute(f"SELECT translation, word FROM words WHERE card_id = {card_id}")
    	    result_list = result.fetchone()
    	    word = result_list[1]
    	    right_translation = result_list[0]
    	    words[card_id] = value
    	    
    	    #Now we check if your guess is right or not.
    	    if right_translation == value:
    	        rights[word] = right_translation
    	    else:
    	        wrongs[word] = value
    
    
    #Here we put all right_answers and wrong_aswers into database
    right_answers = len(rights)
    wrong_answers = len(wrongs)
    sql = "INSERT INTO test_results (user_id, deck_id, right_answers, wrong_answers) VALUES (:user_id, :deck_id, :right_answers, :wrong_answers)"
    db.session.execute(sql, {"user_id":user_id, "deck_id":deck_id, "right_answers":right_answers, "wrong_answers":wrong_answers})
    db.session.commit()
    return render_template("result.html", rights = rights, wrongs = wrongs, deck_id = deck_id, words = words)


@app.route("/new_user", methods=["GET"])
def new_user():
    return render_template("new_user.html")

 
@app.route("/add_new_user",methods=["POST"])
def add_new_user():
    username = request.form["username"]
    password = request.form["password"]
    teacher = 0
    #Check if your new user is a teacher or not and put user in database
    if "teacher" in request.form:
        teacher = 1        
    sql = "INSERT INTO dictionary_users (username, password, teacher) VALUES (:username, :password, :teacher)"
    db.session.execute(sql, {"username":username, "password":password, "teacher":teacher})
    db.session.commit()
    return redirect("/")
    
@app.route("/new_word", methods=["GET"])
def new_word():
    checklogin()
    result = db.session.execute("SELECT deck_id, name FROM deck")
    name = result.fetchall()
    return render_template("new_word.html", name=name)
    
@app.route("/add_new_word", methods=["POST"])
def add_new_word():
    checklogin()
    word = request.form["word"]
    translation = request.form["translation"]
    deck_id = request.form["deck_id"]
    sql = "INSERT INTO words (deck_id, word, translation) VALUES (:deck_id, :word, :translation)"
    result = db.session.execute(sql, {"deck_id":deck_id, "word":word, "translation":translation})
    db.session.commit()
    return redirect("/new_word")
    
@app.route("/new_deck", methods=["GET"])
def new_deck():
    checklogin()
    return render_template("new_deck.html")
    
@app.route("/add_new_deck", methods=["POST"])    
def add_new_deck(): 
    checklogin()   
    name = request.form["name"]
    difficulty = request.form["difficulty"]
    sql = "INSERT INTO deck (difficulty, name) VALUES (:difficulty, :name)"
    result = db.session.execute(sql, {"difficulty":difficulty, "name":name})
    db.session.commit()
    return redirect("/")
    
@app.route("/estimate")
def estimate():
    checklogin()
    deck_id = request.args.get("deck_id")
    return render_template("new_estimate.html", deck_id = deck_id)
    
@app.route("/add_new_estimate", methods=["POST"])
def add_new_estimate():
    checklogin()
    deck_id = request.form["deck_id"]
    user_id = session['user_id']
    comment = request.form["estimate"]
    if comment == '':
    	comment = 'Ei arvointia'
    grade = int(request.form["grade"])
    sql = "INSERT INTO estimate (user_id, deck_id, grade, comment) VALUES (:user_id, :deck_id, :grade, :comment)"
    result = db.session.execute(sql, {"user_id":user_id, "deck_id":deck_id, "grade":grade, "comment":comment})
    db.session.commit()
    return redirect("/")
    
@app.route("/all_estimates")
def all_estimates():
    checklogin()
    result = db.session.execute("SELECT estimate.comment, estimate.grade, deck.deck_id, deck.name FROM estimate, deck WHERE estimate.deck_id = deck.deck_id ORDER BY deck.deck_id")
    estimates_list = result.fetchall()
    return render_template("all_estimates.html", estimates_list = estimates_list)
    
@app.route("/delete_deck")
def delete_deck():
    checklogin()
    result = db.session.execute("SELECT deck_id, name, difficulty FROM deck")
    decks = result.fetchall()
    return render_template("delete_deck.html", decks = decks)
    
@app.route("/delete_one_deck", methods=["POST"])
def delete_one_deck():
    checklogin()
    deck_id = int(request.form["deck_id"])
    print(deck_id)
    db.session.execute(f"DELETE FROM words WHERE deck_id = {deck_id}")
    db.session.execute(f"DELETE FROM test_results WHERE deck_id = {deck_id}")
    db.session.execute(f"DELETE FROM estimate WHERE deck_id = {deck_id}")
    db.session.execute(f"DELETE FROM deck WHERE deck_id = {deck_id}")
    db.session.commit()
    return redirect("/")
    
@app.route("/select_one_student")
def select_one_student():
    checklogin()
    result = db.session.execute("SELECT user_id, username FROM dictionary_users WHERE teacher = 0")
    users = result.fetchall()
    print(users)
    return render_template("select_one_student.html", users = users)
    
@app.route("/student_result", methods=["POST"])
def student_result():
    checklogin()
    student_id = int(request.form["student_id"])
    result = db.session.execute(f"SELECT test_results.right_answers, test_results.wrong_answers, deck.name FROM test_results, deck WHERE test_results.user_id = {student_id} AND test_results.deck_id = deck.deck_id")
    student_results = result.fetchall()
    student_data = db.session.execute(f"SELECT username FROM dictionary_users WHERE user_id = {student_id}")
    student = student_data.fetchone()[0]
    return render_template("/student_results.html", student_results = student_results, student = student)
    
@app.route("/own_results")
def own_results():
    checklogin()
    student_id = session['user_id']
    result = db.session.execute(f"SELECT test_results.right_answers, test_results.wrong_answers, deck.name FROM test_results, deck WHERE test_results.user_id = {student_id} AND test_results.deck_id = deck.deck_id")
    student_results = result.fetchall()
    #student_data = db.session.execute(f"SELECT username FROM dictionary_users WHERE user_id = {student_id}")
    #student = student_data.fetchone()[0]
    return render_template("/own_results.html", student_results = student_results)
    
@app.errorhandler(Exception)
def server_error(err):
    return render_template('error.html', error = err), 500

