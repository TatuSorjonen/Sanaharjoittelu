def getwordcount(db):
    sql = "SELECT COUNT(*) FROM words"
    result = db.session.execute(sql)
    word_count = result.fetchone()[0]
    return word_count

def getdeckcount(db):    
    sql = "SELECT COUNT(deck_id) FROM deck"
    result = db.session.execute(sql)
    deck_count = result.fetchone()[0]
    return deck_count

def getuserinformation(db, username):    
    sql = "SELECT password, user_id, teacher FROM dictionary_users WHERE username = :username"
    result = db.session.execute(sql, {"username":username})
    result_list = result.fetchone()
    return result_list
    
def getdeckinformation(db):
    sql = "SELECT deck.deck_id, deck.name, deck.difficulty, COUNT(words.word) FROM deck, words WHERE deck.deck_id = words.deck_id GROUP BY deck.deck_id"
    result = db.session.execute(sql)
    deck_info = result.fetchall()
    return deck_info
    
def gettestinfo(db, deck_id):
    sql = "SELECT card_id, word, deck_id FROM words WHERE deck_id = :deck_id"
    result = db.session.execute(sql, {"deck_id":deck_id})
    word = result.fetchall()
    return word
    
def getword(db, card_id):
    sql = "SELECT translation, word, card_id FROM words WHERE card_id = :card_id"
    result = db.session.execute(sql, {"card_id":card_id})
    result_list = result.fetchone()
    return result_list

def insert_test_results(db, user_id, deck_id, right_answers, wrong_answers):
    sql = "INSERT INTO test_results (user_id, deck_id, right_answers, wrong_answers) VALUES (:user_id, :deck_id, :right_answers, :wrong_answers)"
    db.session.execute(sql, {"user_id":user_id, "deck_id":deck_id, "right_answers":right_answers, "wrong_answers":wrong_answers})
    db.session.commit()
    
def checkusername(db, username):
    sql = "SELECT 1 FROM dictionary_users WHERE username = :username"
    result = db.session.execute(sql, {"username":username})
    if result.fetchone() != None:
    	 return False
    return True  
    
def insertuser(db, username, hash_value, teacher):
    sql = "INSERT INTO dictionary_users (username, password, teacher) VALUES (:username, :password, :teacher)"
    db.session.execute(sql, {"username":username, "password":hash_value, "teacher":teacher})
    db.session.commit()
    
def checkword(db, word, deck_id):
    sql = "SELECT 1 FROM words WHERE word = :word and deck_id = :deck_id"
    result = db.session.execute(sql, {"word":word, "deck_id":deck_id})
    if result.fetchone() != None:
    	return False
    return True
    
def getuserdecks(db, user_id):
    sql = "SELECT deck_id, name FROM deck WHERE user_id = :user_id"
    result = db.session.execute(sql, {"user_id":user_id})
    deck_list = result.fetchall()
    return deck_list
    
def getdeckowner(db, deck_id):
    sql = "SELECT user_id FROM deck WHERE deck_id = :deck_id"
    result = db.session.execute(sql, {"deck_id":deck_id})
    user_id = result.fetchone()[0]
    return user_id
    
def insertword(db, deck_id, word, translation):    
    sql = "INSERT INTO words (deck_id, word, translation) VALUES (:deck_id, :word, :translation)"
    db.session.execute(sql, {"deck_id":deck_id, "word":word, "translation":translation})
    db.session.commit()
    
def checkdeck(db, name):
    sql = "SELECT 1 FROM deck WHERE name = :name"
    result = db.session.execute(sql, {"name":name})
    if result.fetchone() != None:
    	 return False
    return True 

def insertdeck(db, difficulty, name, user_id):
    sql = "INSERT INTO deck (difficulty, name, user_id) VALUES (:difficulty, :name, :user_id)"
    result = db.session.execute(sql, {"difficulty":difficulty, "name":name, "user_id":user_id})
    db.session.commit()
    
def insertestimate(db, user_id, deck_id, grade, comment):
    sql = "INSERT INTO estimate (user_id, deck_id, grade, comment) VALUES (:user_id, :deck_id, :grade, :comment)"
    result = db.session.execute(sql, {"user_id":user_id, "deck_id":deck_id, "grade":grade, "comment":comment})
    db.session.commit()
    
def getestimates(db):
    sql = "SELECT estimate.comment, estimate.grade, deck.deck_id, deck.name FROM estimate, deck WHERE estimate.deck_id = deck.deck_id ORDER BY deck.deck_id"
    result = db.session.execute(sql)
    estimates_list = result.fetchall()
    return estimates_list
    
def getselecteddeck(db, user_id):
    sql = "SELECT deck_id, name, difficulty FROM deck WHERE user_id = :user_id"
    result = db.session.execute(sql, {"user_id":user_id})
    decks = result.fetchall()
    return decks
    
def getuserbasedondeck(db, deck_id):    
    sql = "SELECT user_id FROM deck WHERE deck_id = :deck_id"
    result = db.session.execute(sql, {"deck_id":deck_id})
    user_id = result.fetchone()[0]
    return user_id
    
def deletedeck(db, deck_id):
    sql = "DELETE FROM words WHERE deck_id = :deck_id"
    sql2 = "DELETE FROM test_results WHERE deck_id = :deck_id"
    sql3 = "DELETE FROM estimate WHERE deck_id = :deck_id"
    sql4 = "DELETE FROM deck WHERE deck_id = :deck_id"
    db.session.execute(sql, {"deck_id":deck_id})
    db.session.execute(sql2, {"deck_id":deck_id})
    db.session.execute(sql3, {"deck_id":deck_id})
    db.session.execute(sql4, {"deck_id":deck_id})
    db.session.commit()
    
def getselectedwords(db, deck_id):
    sql = "SELECT card_id, word, translation FROM words WHERE deck_id = :deck_id"
    result = db.session.execute(sql, {"deck_id":deck_id})
    words = result.fetchall()
    return words
    
def deleteword(db, word_id):
    sql = "DELETE FROM words WHERE card_id = :word_id"
    db.session.execute(sql, {"word_id":word_id})
    db.session.commit()
    
def getstudentusername(db):
    sql = "SELECT user_id, username FROM dictionary_users WHERE teacher = 0"
    result = db.session.execute(sql)
    users = result.fetchall()
    return users
    
def getstudentresults(db, student_id):
    sql = "SELECT test_results.right_answers, test_results.wrong_answers, deck.name FROM test_results, deck WHERE test_results.user_id = :student_id AND test_results.deck_id = deck.deck_id"
    result = db.session.execute(sql, {"student_id":student_id})
    student_results = result.fetchall()
    return student_results
    
def getstudentname(db, student_id):
    sql = "SELECT username FROM dictionary_users WHERE user_id = :student_id"
    student_data = db.session.execute(sql, {"student_id":student_id})
    student = student_data.fetchone()[0]
    return student
    
def getstudentresults(db, student_id):
    sql = "SELECT test_results.right_answers, test_results.wrong_answers, deck.name FROM test_results, deck WHERE test_results.user_id = :student_id AND test_results.deck_id = deck.deck_id"
    result = db.session.execute(sql, {"student_id":student_id})
    student_results = result.fetchall()
    return student_results
