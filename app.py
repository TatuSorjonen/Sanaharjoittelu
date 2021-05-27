from flask import Flask
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from os import getenv
from werkzeug.security import check_password_hash, generate_password_hash
import secrets
import database, utils


app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db = SQLAlchemy(app)
 
    
#Takes you into index.html page where you can login or if you are already logged in you can see starting screen.
@app.route("/")
def index():
    word_count = database.getwordcount(db)
    deck_count = database.getdeckcount(db)
    login_failed = False
    return render_template("index.html", deck_count = deck_count, word_count = word_count, login_failed = login_failed)


#User login
@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    login_failed = False
    
    #Takes user information from database where the username you provided is "username"
    result_list = database.getuserinformation(db, username)
    
    #Check if username exists or not
    if result_list == None:
    	login_failed = True
    	return render_template("index.html", login_failed = login_failed)
    	
    right_password = result_list[0]
    user_id = result_list[1]
    teacher = result_list[2]
    
    #Check if the username has right password
    if check_password_hash(right_password,password):
        session["username"] = username  
        session["user_id"] = user_id
        session["teacher"] = teacher
        session["csrf_token"] = secrets.token_hex(16)
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
    del session["csrf_token"]
    return redirect("/")


#Select all decks and their informations
@app.route("/select_deck")
def select_deck():
    utils.checklogin(session) 
    deck_info = database.getdeckinformation(db)
    return render_template("select_deck.html", deck_info=deck_info)

    
#The test itself
@app.route("/test")
def test():
    utils.checklogin(session)
    deck_id = request.args.get("deck_id")
    
    #Select every words from database where deck_id is the same as what you selected
    word = database.gettestinfo(db, deck_id)
    return render_template("test.html", word=word, deck_id=deck_id)


#User results
@app.route("/result", methods=["POST"])
def result():
    utils.checklogin(session)
    form_data = request.form
    utils.check_csrf_token(form_data, session)
    
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
    	    result_list = database.getword(db, card_id)
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
    database.insert_test_results(db, user_id, deck_id, right_answers, wrong_answers)
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
    hash_value = generate_password_hash(password)
    teacher = 0
    
    #Check if username is already taken
    if database.checkusername(db, username) == False:
    	return render_template("new_user.html", error = True, errorcode = 1)
    	
    #Check if your new user is a teacher or not and puts user in database
    if "teacher" in request.form:
        teacher = 1    
    database.insertuser(db, username, hash_value, teacher)
    
    return redirect("/")


#Returns html-page where you can type new words into the database  
@app.route("/new_word", methods=["GET"])
def new_word():
    utils.checklogin(session)
    selected_deck = -1
    errorcode = -1
    user_id = session['user_id']
    
    #Check if errorcode parameter exists
    if request.args.get("errorcode") != None:
    	errorcode = int(request.args.get("errorcode"))
    
    #Check if deck_id is selected
    if request.args.get("deck_id") != None:
    	selected_deck = int(request.args.get("deck_id"))
    
    #Get user decks
    deck_list = database.getuserdecks(db, user_id)
    
    return render_template("new_word.html", deck_list = deck_list, selected_deck = selected_deck, errorcode = errorcode)


#This adds new word into database    
@app.route("/add_new_word", methods=["POST"])
def add_new_word():
    utils.checklogin(session)    
    utils.check_csrf_token(request.form, session)
    word = request.form["word"]
    translation = request.form["translation"]
    deck_id = int(request.form["deck_id"])
    
    if database.checkword(db, word, deck_id) == False:
    	return redirect(f"new_word?deck_id={deck_id}&errorcode=2")
    	
    user_id = database.getdeckowner(db, deck_id)
    utils.userloggedin(user_id, session)
    
    database.insertword(db, deck_id, word, translation)
    
    return redirect(f"/new_word?deck_id={deck_id}")


#Returns html-page where you can add new deck    
@app.route("/new_deck", methods=["GET"])
def new_deck():
    utils.checklogin(session)
    return render_template("new_deck.html", error = False)


#Adds a new deck to the database    
@app.route("/add_new_deck", methods=["POST"])    
def add_new_deck(): 
    utils.checklogin(session)
    utils.check_csrf_token(request.form, session)  
    name = request.form["deck"]
    difficulty = request.form["difficulty"]
    user_id = session['user_id']
    if database.checkdeck(db, name) == False:
    	return render_template("new_deck.html", error = True, errorcode = 3)
    	
    database.insertdeck(db, difficulty, name, user_id)
    	
    return redirect("/")


#Returns html-page where you can add a new estimate into the test    
@app.route("/estimate")
def estimate():
    utils.checklogin(session)
    deck_id = request.args.get("deck_id")
    return render_template("new_estimate.html", deck_id = deck_id)


#Adds a new estimate to the database    
@app.route("/add_new_estimate", methods=["POST"])
def add_new_estimate():
    utils.checklogin(session)
    utils.check_csrf_token(request.form, session)
    deck_id = request.form["deck_id"]
    user_id = session['user_id']
    comment = request.form["estimate"]
    grade = int(request.form["grade"])
    
    #Check if comment is empty
    if comment == '':
    	comment = 'Ei arvointia'
    	   
    database.insertestimate(db, user_id, deck_id, grade, comment)
    
    return redirect("/")


#Returns all estimates and print them order by deck    
@app.route("/all_estimates")
def all_estimates():
    utils.checklogin(session)
    
    estimates_list = database.getestimates(db)
    
    return render_template("all_estimates.html", estimates_list = estimates_list)


#Returns html-page where teacher can delete decks    
@app.route("/delete_deck")
def delete_deck():
    utils.checklogin(session)
    user_id = session['user_id']
    decks = database.getselecteddeck(db, user_id)
    return render_template("delete_deck.html", decks = decks)


#Removes all values referring to the pack from other tables. Also removes the deck itself.  
@app.route("/delete_one_deck", methods=["POST"])
def delete_one_deck():
    utils.checklogin(session)
    utils.check_csrf_token(request.form, session)
    deck_id = int(request.form["deck_id"])
    user_id = database.getuserbasedondeck(db, deck_id)
    utils.userloggedin(user_id, session)
    database.deletedeck(db, deck_id)
    return redirect("/")


#Returns html-page where you can select a deck from which to delete the word.  
@app.route("/select_deck_word_remove")
def select_deck_word_remove():
    utils.checklogin(session)
    user_id = session['user_id']
    decks = database.getselecteddeck(db, user_id)
    return render_template("select_deck_word_remove.html", decks = decks)


#Returns html-page where you can remove one word.    
@app.route("/delete_word", methods=["POST"])
def delete_word():
    utils.checklogin(session)
    utils.check_csrf_token(request.form, session)
    deck_id = int(request.form["deck_id"])
    user_id = database.getuserbasedondeck(db, deck_id)
    utils.userloggedin(user_id, session)
    words = database.getselectedwords(db, deck_id)
    return render_template("delete_selected_word.html", words = words, deck_id = deck_id)

#Removes one word.    
@app.route("/delete_selected_word", methods=["POST"])
def delete_selected_word():
    utils.checklogin(session)
    utils.check_csrf_token(request.form, session)
    deck_id = request.form["deck_id"]
    
    user_id = database.getuserbasedondeck(db, deck_id)
    utils.userloggedin(user_id, session)
    word_id = int(request.form["word_id"])
    database.deleteword(db, word_id)
    
    return redirect("/")

#Returns hltm-page where the teacher can choose one student results  
@app.route("/select_one_student")
def select_one_student():
    utils.checklogin(session)
    users = database.getstudentusername(db)
    return render_template("select_one_student.html", users = users)

#After selection, retrieves all the results of the selected student and takes you to an html-page    
@app.route("/student_result", methods=["POST"])
def student_result():
    utils.checklogin(session)
    utils.check_csrf_token(request.form, session)
    student_id = int(request.form["student_id"])
    
    student_results = database.getstudentresults(db, student_id)
    student = database.getstudentname(db, student_id)
    
    return render_template("/student_results.html", student_results = student_results, student = student)

#This retrieves all the results of the logged-in user  
@app.route("/own_results")
def own_results():
    utils.checklogin(session)
    student_id = session['user_id']
    student_results = database.getstudentresults(db, student_id)
    return render_template("/own_results.html", student_results = student_results)

#Errorhandler if there happens some error    
@app.errorhandler(Exception)
def server_error(err):
    return render_template('error.html', error = err), 500

