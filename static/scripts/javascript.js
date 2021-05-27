function checklogin(form) {
    var username = form.username.value;
    var password = form.password.value;
    if (checkstring(username) == false) {
        alert("Käyttäjätunnus ei kelpaa");
        return false;
    }
    if (checkstring(password) == false) {
    	alert("Salasana ei kelpaa");
    	return false;
    }
    return true;
}

function checkdeck(form) {
    var deck = form.deck.value;
    if (checkstring(deck) == false) {
        alert("Pakan nimi ei saa olla tyhjä")
        return false;
    }
    return true;
}

function checkword(form) {
    var word = form.word.value;
    var translation = form.translation.value;
    if (checkstring(word) == false) {
        alert("Sana ei saa olla tyhjä");
        return false;
    }
    if (checkstring(translation) == false) {
    	alert("Käännös ei saa olla tyhjä");
    	return false;
    }
    return true;
}

function checkstring(mystring) {
    if (mystring.length == 0) {
        return false;
    }
    return true;
}   
