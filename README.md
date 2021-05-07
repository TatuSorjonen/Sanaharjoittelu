# Sanaharjoittelu

<h3> Kirjautuminen </h3>

- Käyttäjä voi tehdä uuden käyttäjän, joko oppilaana tai opettajana. Jos käyttäjänimi tai salasana ovat liian pitkiä tai kokonaan tyhjiä uuden käyttäjän tekemisen seurauksena, sovellus heittää virheilmoituksen.
- Käyttäjä voi kirjautua sisään omalla käyttäjätunnuksellaan. Jos käyttäjätunnus on väärin, niin sovellus heittää virheilmoituksen asiasta. 

<h3> Testi opettajan näkökulmasta </h3>

- Opettaja voi luoda uuden pakan ja antaa sille vaikeusasteen, mihin hän sitten voi laittaa uusia sanoja ja niiden käännöksiä. Hän voi myös poistaa pakan tarvittaessa.
- Opettaja pystyy tekemään testin, missä hän valitsee testiin pakan ja tämän jälkeen tämä tulostaa kaikki sanat taulukkoon, mihin hän kokeilee saada sanoja oikein. Tämän jälkeen käyttäjä saa tulokset, mitkä sanat menivät oikein ja mitkä väärin ja montako meni oikein. 
- Testin loppuvaiheessa käyttäjä voi antaa arvion testistä. Oman vapaavalintaisen kommentin, sekä arvosanan 1-5. 
- Opettaja pystyy katsomaan oppilaiden tuloksia tai omia tuloksiaan, mutta ei pysty näkemään toisten opettajien tuloksia. 
- Käyttäjä näkee kaikki arvostelut jokaisesta pakasta.


<h3> Testi oppilaan näkökulmasta </h3>

- Oppilas voi vain tehdä testin samalla tavalla kuin opettaja ja katsoa omia tuloksiaan, sekä katsoa arvioinnit.
- Oppilaalla ei ole oikeuksia luoda uutta pakkaa, poistaa pakkaa tai lisätä siihen sanoja ja niiden käännöksiä.
- Oppilas ei myöskään pysty katsomaan muiden oppilaiden tuloksia.

[Voit testata Herokussa tästä](https://sanaharjoittelu.herokuapp.com/) <br />

<h2> Tästä alaspäin tullaan poistamaan piakkoin </h2>

<h3> Ensimmäinen vaihe: </h3>

Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden käyttäjän. <br />
Käyttäjä voi nähdä omat tuloksensa montako hän on saanut oikein. <br />
Käyttäjä voi aloittaa testin tekemisen. <br />
Jos saa oikean vastauksen ohjelma kertoo sen ja jos ei saa nii ohjelma kertoo mikä oli oikein. <br />
Tämä jatkuu kunnes kaikki sanat on käyty läpi. <br />
Käyttäjä pystyy lopettamaan testin milloin tahansa. <br />
Lopuksi käyttäjä voi arvioida testin.


<h3> Toinen vaihe: </h3>

Olen tehnyt että käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden käyttäjän. Käyttäjät tallentuvat tietokantaan. Ei vielä toimi jos käyttäjä kirjoittaa väärin kirjautumisessa vaadittavat arvot ja ei toimi jos username on jo tietokannassa. Käyttäjä voi myös kirjautua ulos.

Käyttäjä pystyy lisäämään sanoja ja käännöksiä tietokantaan, mutta niitä ei vielä näy missään. Testi osuudessa ei ole vielä oikein mitään. Siinä on tällähetkellä vain minun harjoittelua ja ei sisällä mitään tietokantaa.
Muuta en ole kerennyt tekemään.

Suurin osa ajasta meni opetteluun ja Herokun kanssa säätämiseen, kun en ole tällaisia ennen tehnyt.

ps. Vaihdoin labtooliin githubin osoitteen ja työn nimen siitä edellisestä, mutta kopsasin ton ensimmäisen vaiheen tähän README.md, jos joku pitää ylhäällä edellisiä.

Älä laita tyhjää salasanaa tai käyttäjänimeä uuden käyttäjän luomisessa. Sovellus voi mennä tällähetkellä rikki jos näin tekee.


<h3> Kolmas vaihe: </h3> 

Olen tehnyt että käyttäjä voi lisätä pakkoja ja katsoa arvostelut. 

Testi osuutta en ole vielä kerennyt aloittaamaan. Siinä on vieläkin minun omia kokeilujani. 

Taulut on tehty valmiiksi (5kpl) ja käyttäjä voi tehdä arvioinnin testin lopuksi. 

Käyttäjä voi kirjautua milloin vain ulos tai palata alkuun. 

Ulkoasua muunneltu paljon. Saatan vielä muutella joitain kohtia, mutta ajattelin pitää ulkomuodon tämän näköisenä näin pääpiirteittäin. 

Virheistä tulee error.html sivu mikä laittaa sinut alkuun palaa nappulaa painamalla. Muita virheilmoituksia ei pitäisi tulla. Jos tulee niin olisin kiitollinen, jos kertoisit mistä tämä virhe aiheutuu niin muokkaan tämän. (Voi olla, että on joitain mistä tulee, en ole testannu aivan kaikkia mahdollisuuksia)

28.04.2021 klo.1.52am: Huomasin, että jokin oli rikkonut sovelluksen eikä se enään ottanut yhteyttä tietokantaan jostain minulle tuntemattomasta syystä. Tein uuden tietokannan, mutta muuten koodia ei ole muutettu palautuksen jälkeen. 

[Voit testata Herokussa tästä](https://sanaharjoittelu.herokuapp.com/) <br />

