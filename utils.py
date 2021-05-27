#Check if username has logged in or not. If not this returns error.
def checklogin(session):
    if len(session) == 0 or session["username"] == None or session["user_id"] == None:
    	raise Exception("Et ole kirjautunut sisään!")


#Check if form contains csrf token and needs to be same as session token.    	
def check_csrf_token(form, session):
    if len(session) == 0 or form == None or session["csrf_token"] != form["csrf_token"]:
    	raise Exception("Mahdollinen csrf hyökkäys")


#Check if user is deck owner    	
def userloggedin(user_id, session):
    if session['user_id'] != user_id:
    	raise Exception("Väärä käyttäjä")
