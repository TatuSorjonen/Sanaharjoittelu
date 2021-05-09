from flask import Flask
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from os import getenv

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db = SQLAlchemy(app)

#Check if username has logged in or not. If not this returns error.
def checklogin():
    if len(session) == 0 or session["username"] == None or session["user_id"] == None:
    	raise Exception("Et ole kirjautunut sisään!")
    
@app.route("/")
def index():
    result = db.session.execute("SELECT COUNT(*) FROM words")
    word_count = result.fetchone()[0]
    result = db.session.execute("SELECT COUNT(deck_id) FROM deck")
    deck_count = result.fetchone()[0]
    login_failed = False
    return render_template("index.html", deck_count = deck_count, word_count = word_count, login_failed = login_failed)

#CSS Styles
@app.route("/styles")
def styles():
    return render_template("styles.css")

#User login
@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    login_failed = False
    
    #Takes user information from database where the username you provided is "username"
    result = db.session.execute(f"SELECT password, user_id, teacher FROM dictionary_users WHERE username = '{username}'")
    result_list = result.fetchone()
    
    #Check if username exists or not
    if result_list == None:
    	login_failed = True
    	return render_template("index.html", login_failed = login_failed)
    right_password = result_list[0]
    user_id = result_list[1]
    teacher = result_list[2]
    
    #Check if the username has right password
    if password == right_password:
        session["username"] = username  
        session["user_id"] = user_id
        session["teacher"] = teacher
    else:
        login_failed = True
        return render_template("index.html", login_failed = login_failed)
    return redirect("/") 

#Deletes all sessions and returns back to login screen
@app.route("/logout")
def logout():
    del session["username"]
    del session["user_id"]
    del session["teacher"]
    return redirect("/")

#Select all decks and their informations
@app.route("/select_deck")
def select_deck():
    checklogin()   
    result = db.session.execute("SELECT deck.deck_id, deck.name, deck.difficulty, COUNT(words.word) FROM deck, words WHERE deck.deck_id = words.deck_id GROUP BY deck.deck_id")
    deck_info = result.fetchall()
    return render_template("select_deck.html", deck_info=deck_info)
    
#The test itself
@app.route("/test")
def test():
    checklogin()
    deck_id = request.args.get("deck_id")
    
    #Select every words from database where deck_id is the same as what you selected
    result = db.session.execute(f"SELECT card_id, word, deck_id FROM words WHERE deck_id = {deck_id}")
    word = result.fetchall()
    return render_template("test.html", word=word, deck_id=deck_id)

#User results
@app.route("/result", methods=["POST"])
def result():
    checklogin()
    form_data = request.form
    
    #There is three arrays. One with all words, one with right answers and last with wrong answers
    all_words = {}
    rights = {}
    wrongs = {}
    deck_id = request.form["deck_id"]
    user_id = session['user_id']
    
    #Takes all keys and values from test.html and if it starts with translation_, we take a id one, after split. 
    #And then we take all words and translations from database where card_id is splitted card_id.
    for key,value in form_data.items():
    	if key.startswith("translation_"):
    	    card_id = int(key.split("translation_")[1])
    	    result = db.session.execute(f"SELECT translation, word, card_id FROM words WHERE card_id = {card_id}")
    	    result_list = result.fetchone()
    	    word = result_list[1]
    	    right_translation = result_list[0]
    	    all_words[word] = right_translation
    	    
    	    #Now we check if your guess is right or not.
    	    if right_translation.lower().strip() == value.lower().strip():
    	        rights[word] = right_translation
    	    else:
    	        wrongs[word] = value    
    
    #Here we put all right answers and wrong answers into database
    right_answers = len(rights)
    wrong_answers = len(wrongs)
    sql = "INSERT INTO test_results (user_id, deck_id, right_answers, wrong_answers) VALUES (:user_id, :deck_id, :right_answers, :wrong_answers)"
    db.session.execute(sql, {"user_id":user_id, "deck_id":deck_id, "right_answers":right_answers, "wrong_answers":wrong_answers})
    db.session.commit()
    return render_template("result.html", rights = rights, wrongs = wrongs, deck_id = deck_id, all_words = all_words)

#Returns html-page where you can do a new user
@app.route("/new_user", methods=["GET"])
def new_user():
    return render_template("new_user.html", error = False)

#Adds new user into database
@app.route("/add_new_user",methods=["POST"])
def add_new_user():
    username = request.form["username"]
    password = request.form["password"]
    teacher = 0
    
    #Check if your new user is a teacher or not and puts user in database
    if "teacher" in request.form:
        teacher = 1 
    try:      
    	sql = "INSERT INTO dictionary_users (username, password, teacher) VALUES (:username, :password, :teacher)"
    	db.session.execute(sql, {"username":username, "password":password, "teacher":teacher})
    	db.session.commit()
    except:
    	return render_template("new_user.html", error = True)
    return redirect("/")

#Returns html-page where you can type new words into the database  
@app.route("/new_word", methods=["GET"])
def new_word():
    checklogin()
    selected_deck = -1
    if request.args.get("deck_id") != None:
    	selected_deck = int(request.args.get("deck_id"))
    result = db.session.execute("SELECT deck_id, name FROM deck")
    name = result.fetchall()
    return render_template("new_word.html", name=name, selected_deck = selected_deck)

#This adds new word what you writed into database    
@app.route("/add_new_word", methods=["POST"])
def add_new_word():
    checklogin()    
    word = request.form["word"]
    translation = request.form["translation"]
    deck_id = request.form["deck_id"]
    try:
    	sql = "INSERT INTO words (deck_id, word, translation) VALUES (:deck_id, :word, :translation)"
    	result = db.session.execute(sql, {"deck_id":deck_id, "word":word, "translation":translation})
    	db.session.commit()
    except:
    	raise Exception("Sanan '" + word + "' lisääminen epäonnistui. (Älä anna jo pakassa olevaa sanaa tai tyhjiä arvoja.)")
    return redirect(f"/new_word?deck_id={deck_id}")

#Returns html-page where you can add new deck    
@app.route("/new_deck", methods=["GET"])
def new_deck():
    checklogin()
    return render_template("new_deck.html")

#Adds a new deck to the database    
@app.route("/add_new_deck", methods=["POST"])    
def add_new_deck(): 
    checklogin()   
    name = request.form["name"]
    difficulty = request.form["difficulty"]
    try:
    	sql = "INSERT INTO deck (difficulty, name) VALUES (:difficulty, :name)"
    	result = db.session.execute(sql, {"difficulty":difficulty, "name":name})
    	db.session.commit()
    except:
    	raise Exception("Pakan '" + name + "' lisääminen epäonnistui. (Älä anna olemassa olevaa pakan nimeä tai tyhjää nimeä.)")
    return redirect("/")

#Returns html-page where you can add a new estimate into the test    
@app.route("/estimate")
def estimate():
    checklogin()
    deck_id = request.args.get("deck_id")
    return render_template("new_estimate.html", deck_id = deck_id)

#Adds a new estimate to the database    
@app.route("/add_new_estimate", methods=["POST"])
def add_new_estimate():
    checklogin()
    deck_id = request.form["deck_id"]
    user_id = session['user_id']
    comment = request.form["estimate"]
    
    #Check if comment is empty or not
    if comment == '':
    	comment = 'Ei arvointia'
    	
    grade = int(request.form["grade"])
    sql = "INSERT INTO estimate (user_id, deck_id, grade, comment) VALUES (:user_id, :deck_id, :grade, :comment)"
    result = db.session.execute(sql, {"user_id":user_id, "deck_id":deck_id, "grade":grade, "comment":comment})
    db.session.commit()
    return redirect("/")

#Returns all estimates and print them order by deck    
@app.route("/all_estimates")
def all_estimates():
    checklogin()
    result = db.session.execute("SELECT estimate.comment, estimate.grade, deck.deck_id, deck.name FROM estimate, deck WHERE estimate.deck_id = deck.deck_id ORDER BY deck.deck_id")
    estimates_list = result.fetchall()
    return render_template("all_estimates.html", estimates_list = estimates_list)

#Returns html-page where teacher can delete decks    
@app.route("/delete_deck")
def delete_deck():
    checklogin()
    result = db.session.execute("SELECT deck_id, name, difficulty FROM deck")
    decks = result.fetchall()
    return render_template("delete_deck.html", decks = decks)

#Removes all values referring to the pack from other tables. Also removes the deck itself.  
@app.route("/delete_one_deck", methods=["POST"])
def delete_one_deck():
    checklogin()
    deck_id = int(request.form["deck_id"])
    db.session.execute(f"DELETE FROM words WHERE deck_id = {deck_id}")
    db.session.execute(f"DELETE FROM test_results WHERE deck_id = {deck_id}")
    db.session.execute(f"DELETE FROM estimate WHERE deck_id = {deck_id}")
    db.session.execute(f"DELETE FROM deck WHERE deck_id = {deck_id}")
    db.session.commit()
    return redirect("/")

#Returns html-page where you can select a deck from which to delete the word.  
@app.route("/select_deck_word_remove")
def select_deck_word_remove():
    checklogin()
    result = db.session.execute("SELECT deck_id, name, difficulty FROM deck")
    decks = result.fetchall()
    return render_template("select_deck_word_remove.html", decks = decks)

#Returns html-page where you can remove one word.    
@app.route("/delete_word", methods=["POST"])
def delete_word():
    checklogin()
    deck_id = int(request.form["deck_id"])
    result = db.session.execute(f"SELECT card_id, word, translation FROM words WHERE deck_id = {deck_id}")
    words = result.fetchall()
    return render_template("delete_selected_word.html", words = words)

#Removes one word.    
@app.route("/delete_selected_word", methods=["POST"])
def delete_selected_word():
    checklogin()
    word_id = int(request.form["word_id"])
    db.session.execute(f"DELETE FROM words WHERE card_id = {word_id}")
    db.session.commit()
    return redirect("/")

#Returns hltm-page where the teacher can choose one student results  
@app.route("/select_one_student")
def select_one_student():
    checklogin()
    result = db.session.execute("SELECT user_id, username FROM dictionary_users WHERE teacher = 0")
    users = result.fetchall()
    return render_template("select_one_student.html", users = users)

#After selection, retrieves all the results of the selected student and takes you to an html-page    
@app.route("/student_result", methods=["POST"])
def student_result():
    checklogin()
    student_id = int(request.form["student_id"])
    result = db.session.execute(f"SELECT test_results.right_answers, test_results.wrong_answers, deck.name FROM test_results, deck WHERE test_results.user_id = {student_id} AND test_results.deck_id = deck.deck_id")
    student_results = result.fetchall()
    student_data = db.session.execute(f"SELECT username FROM dictionary_users WHERE user_id = {student_id}")
    student = student_data.fetchone()[0]
    return render_template("/student_results.html", student_results = student_results, student = student)

#This retrieves all the results of the logged-in user  
@app.route("/own_results")
def own_results():
    checklogin()
    student_id = session['user_id']
    result = db.session.execute(f"SELECT test_results.right_answers, test_results.wrong_answers, deck.name FROM test_results, deck WHERE test_results.user_id = {student_id} AND test_results.deck_id = deck.deck_id")
    student_results = result.fetchall()
    #student_data = db.session.execute(f"SELECT username FROM dictionary_users WHERE user_id = {student_id}")
    #student = student_data.fetchone()[0]
    return render_template("/own_results.html", student_results = student_results)

#Errorhandler if there happens some error    
@app.errorhandler(Exception)
def server_error(err):
    return render_template('error.html', error = err), 500

