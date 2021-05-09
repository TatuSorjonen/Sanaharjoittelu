# Sanaharjoittelu

- Sovellus on toimiva sanaharjoittelu kenelle tahansa, mihin voit laittaa esimerkiksi omia suomi-englanti käännöksiä, mitkä ovat sinulle vaikeita. Mitkä vaan sanat ja käännökset käyvät tai voit käyttää sovellusta muihin sana-käännös testeihin mitä haluat testata tarvittaessa.
- Kun teet ensimmäisen käyttäjäsi, suosittelen tekemään opettajan, jotta sovelluksen kaikki ominaisuudet saadaan hyvin näkyviin. Oppilas ei pysty tekemään paljoa muuta, kuin opettajien tekemiä testejä tai katsomaan arvosteluja tai omia tuloksiaan. Melkein kaikki oikeudet ovat opettajalla.
- Kuka tahansa voi tehdä opettaja käyttäjän ja opettajat voivat muuttaa toistensa tekemiä pakkoja.


<h3> Kirjautuminen </h3>

- Käyttäjä voi tehdä uuden käyttäjän, joko oppilaana tai opettajana.
- Käyttäjä voi kirjautua sisään omalla käyttäjätunnuksellaan. 


<h3> Testi opettajan näkökulmasta </h3>

- Opettaja voi luoda uuden pakan ja antaa sille vaikeusasteen, mihin hän sitten voi laittaa uusia sanoja ja niiden käännöksiä. Hän voi myös poistaa pakan tarvittaessa.
- Opettaja voi myös poistaa pakasta sanoja halutessaan.
- Käyttäjä ei voi tehdä testiä ennen kuin opettaja on luonut pakan, missä on sanoja.
- Opettaja pystyy tekemään testin, missä hän valitsee testiin pakan ja tämän jälkeen tämä tulostaa kaikki sanat taulukkoon, mihin hän kokeilee saada sanoja oikein. Tämän jälkeen käyttäjä saa tulokset, mitkä sanat menivät oikein ja mitkä väärin ja montako meni oikein sekä mikä olisi ollut oikea vastaus.
- Tuloksien yhteydesä käyttäjä voi mennä testivaiheen alkuun, missä hän voi joko valita uuden testin tai tehdä saman testin.
- Testin loppuvaiheessa käyttäjä voi antaa arvion testistä, oman vapaavalintaisen kommentin, sekä arvosanan 1-5. 
- Opettaja pystyy katsomaan oppilaiden tuloksia tai omia tuloksiaan, mutta ei pysty näkemään toisten opettajien tuloksia. 
- Käyttäjä näkee kaikki arvostelut jokaisesta pakasta.


<h3> Testi oppilaan näkökulmasta </h3>

- Oppilas voi vain tehdä testin samalla tavalla kuin opettaja ja katsoa omia tuloksiaan, sekä katsomaan arvioinnit.
- Oppilaalla ei ole oikeuksia luoda uutta pakkaa, poistaa pakkaa tai lisätä siihen sanoja ja niiden käännöksiä. Ei ole myöskään oikeutta poistaa sanoja.
- Oppilas ei pysty katsomaan muiden oppilaiden tuloksia.


<h3> Taulut </h3>

- Käyttäjätunnukset ovat UNIQUE eli ei voi olla monta saman nimistä käyttäjää. Käyttäjätunnukselle on laitettu 20 merkin raja sekä salasanalle myös.
- Pakka taulussa nimet ovat UNIQUE eli ei voi olla saman nimisiä pakkoja ja niiden nimi on laitettu olemaan maksimissaan 35 merkkiä pitkä.
- Sanat taulu ottaa viitteen pakka taulusta ja sanat sekä käännökset on laitettu maksimi 35 merkkiä pitkiksi (Eivät voi myöskään olla tyhjiä).
- test_results taulu ottaa viiteen pakka ja käyttäjä tauluista. Pitää yllä kuinka monta oikein ja väärin käyttäjä on saanut.
- estimate taulu ottaa myös viitteen pakka ja käyttäjä tauluihin. Siinä on myös käyttäjän antama arvosana sekä max 1000 merkkiä pitkä arvostelu testistä.  

Jos yrität huijata oppilaana esimerkiksi menemällä pakkojen luomista varten tarkoitetulle sivulle ilman, että sovelluksessa on linkkiä sinne. Tämä ei onnistunu ja sivu heittää ilmoituksen "Älä yritä huijata".

[Voit testata sovellusta Herokussa tästä](https://sanaharjoittelu.herokuapp.com/) <br />

