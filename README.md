# Sanaharjoittelu

- Sovellus on toimiva sanaharjoittelu. Voit harjoitella esimerkiksi omia suomi-englanti käännöksiä, jotka ovat sinulle vaikeita. Kaikki sanat ja käännökset käyvät tai voit käyttää sovellusta muihin sana-käännös testeihin, joita haluat testata.
- Kun teet ensimmäisen käyttäjäsi, suosittelen tekemään opettajan, jotta sovelluksen kaikki ominaisuudet saadaan hyvin näkyviin. Oppilas ei pysty tekemään paljoa muuta, kuin opettajien tekemiä testejä, katsomaan arvosteluja tai omia tuloksiaan. Melkein kaikki oikeudet ovat opettajalla.
- Kuka tahansa voi tehdä itselleen opettaja käyttäjän testausta varten. Normaalisti kukaan muu ei pystyisi tekemään opettajaa kuin admininin oikeuksille annetut käyttäjät.

- Ohjelman Python koodi on jaettu kolmeen osaan: apumetodit, tietokantakyselyt sekä kyleinen sovellus ja reititys logiikka.
- CSS tyyleillä on toteutettu HTML-sivujen ulkoasu.
- Javascriptilla tarkistetaan etteivät lomakkeen syötekentät ole tyhjiä. Maksimipituus tarkistetaan HTML-sivulla ja tietokannassa.


<h3> Kirjautuminen </h3>

- Käyttäjä voi tehdä uuden käyttäjän, joko oppilaana tai opettajana.
- Käyttäjä voi kirjautua sisään omalla käyttäjätunnuksellaan. 


<h3> Testi opettajan näkökulmasta </h3>

- Opettaja voi luoda uuden pakan ja antaa sille vaikeusasteen. Pakkaan hän voi laittaa uusia sanoja ja niiden käännöksiä. Hän voi myös poistaa pakan tarvittaessa.
- Opettaja voi myös poistaa pakasta sanoja halutessaan.
- Käyttäjä ei voi tehdä testiä ennen kuin opettaja on luonut pakan, missä on sanoja.
- Opettaja pystyy tekemään testin, missä hän valitsee testiin pakan ja tämän jälkeen tämä tulostaa kaikki sanat taulukkoon, mihin hän kokeilee saada sanoja oikein. Tämän jälkeen käyttäjä saa tulokset, mitkä sanat menivät oikein ja mitkä väärin ja montako meni oikein sekä mikä olisi ollut oikea vastaus.
- Tuloksien yhteydesä käyttäjä voi mennä testivaiheen alkuun, missä hän voi joko valita uuden testin tai tehdä saman testin.
- Testin loppuvaiheessa käyttäjä voi antaa arvion testistä, oman vapaavalintaisen kommentin, sekä arvosanan 1-5. 
- Opettaja pystyy katsomaan oppilaiden tuloksia tai omia tuloksiaan, mutta ei pysty näkemään toisten opettajien tuloksia. 
- Käyttäjä näkee kaikki arvostelut jokaisesta pakasta.
- Opettajat eivät voi poistaa toistensa pakkoja.


<h3> Testi oppilaan näkökulmasta </h3>

- Oppilas voi vain tehdä testin samalla tavalla kuin opettaja ja katsoa omia tuloksiaan, antamaan arvion testistä sekä katsomaan muiden arvioinnit.
- Oppilaalla ei ole oikeuksia luoda uutta pakkaa, poistaa pakkaa tai lisätä siihen sanoja ja niiden käännöksiä. Ei ole myöskään oikeutta poistaa sanoja.
- Oppilas ei pysty katsomaan muiden oppilaiden tuloksia.


<h3> Taulut </h3>

<h4> dictionary_users </h4>
<ul>
  <li>user_id: Pääavain</li>
  <li>username: Käyttäjätunnus, UNIQUE, NOT NULL, Ei myöskään tyhjä, maksimipituus 20 merkkiä</li>
  <li>password: Salasana hajautettuna, NOT NULL, Ei myöskään tyhjä</li>
  <li>teacher: Onko opettaja, '1' jos opettaja, muutoin 0, NOT NULL</li>
</ul>

<h4> deck </h4>
<ul>
  <li>deck_id: Pääavain</li>
  <li>user_id: Viite dictionary_users taulun pääavaimeen, NOT NULL</li>
  <li>difficulty: Pakan vaikeusaste, NOT NULL</li>
  <li>name: Pakan nimi UNIQUE, NOT NULL, Ei myöskään tyhjä, maksimipituus 35 merkkiä</li>
</ul>

<h4> words </h4>
<ul>
  <li>card_id: Pääavain</li>
  <li>deck_id: Viite deck taulun pääavaimeen, NOT NULL</li>
  <li>word: Sana, UNIQUE jokaisessa pakassa, NOT NULL, Ei myöskään tyhjä, maksimipituus 35 merkkiä</li>
  <li>translation: Sanan käännös, NOT NULL, Ei myöskään tyhjä, maksimipituus 35 merkkiä</li>
</ul>

<h4> test_results </h4>
<ul>
  <li>test_id: Pääavain</li>
  <li>user_id: Viite dictionary_users taulun pääavaimeen, NOT NULL</li>
  <li>deck_id: Viite deck taulun pääavaimeen, NOT NULL</li>
  <li>right_answers: Oikeiden vastauksien lukumäärä, NOT NULL</li>
  <li>wrong_answers_ Väärien vastauksien lukumäärä, NOT NULL</li>
</ul>

<h4> estimate </h4>
<ul>
  <li>estimate_id: Pääavain</li>
  <li>user_id: Viite dictionary_users taulun pääavaimeen, NOT NULL</li>
  <li>deck_id: Viite deck taulun pääavaimeen, NOT NULL</li>
  <li>grade: Käyttäjän antama arvosana testille, NOT NULL </li>
  <li>comment: Käyttäjän antama kommentti testille, maksimipituus 1000 merkkiä</li>
</ul>


<h3> Tietoturva </h3>

- SQL-injektion uhka estetty SQL parametrien avulla. Hyökkääjä ei voi muuttaa SQL lausetta omilla syötteillään.
- XSS-haavoittuvuus estetty käyttämällä Flaskin sivupohjia. Hyökkääjä ei voi muuttaa HTML-sivua.
- CSRF-haavoittuvuus estetty. Kirjautuessa sisään käyttäjän sessioon laitetaan CSRF_token jota käytetään myös html formissa ja lomaketta vastaanotettaessa tarkastetaan ovatko nämä samat.
- Salasanaa ei tallenneta tietokantaan selkokielisenä.

