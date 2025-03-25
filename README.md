# Feladat részletei

## Adatok beszerzése egy publikus forrásból
Használj egy nyilvánosan elérhető API-t vagy egy könnyen scrape-elhető weboldalt. Gyűjtsd az adatokat egy SQL vagy noSQL adatbázisba, amely jobban illik a kiválasztott adatszerkezethez. Az adatok lehetnek például tőzsdei árak, piactér hirdetések, helyi éttermek ebédmenüi – olyan forrást válassz, ami üzleti szempontból releváns. 

**Tipp:** kérlek, ne használj SQLite-ot, mert a megoldásod kiértékelését megnehezíti. Köszönjük.

## Adatok feldolgozása
Végezz az adatokon valamilyen hasznos műveletet, ami üzleti értékkel bírhat. Nem szükséges gépi tanulási modellt építened; inkább arra vagyunk kíváncsiak, hogyan elemzed a nyers adatokat és milyen információkat tudsz kinyerni belőlük. Például vizsgálhatod az árváltozásokat, trendeket vagy egy adott termékkategória keresleti ingadozásait.

## A megoldás publikálása
A megoldásod tedd lokálisan használhatóvá frontend alkalmazás vagy REST API formájában, ahol az eredmények könnyen hozzáférhetők. A frontend lehet egy egyszerű dashboard vagy interaktív webes felület, míg az API biztosítson lehetőséget a feldolgozott adatok lekérdezésére és az eredmények visszaadására.

---

## Technikai követelmények

- **Programozási nyelv:** A feladatot olyan programozási nyelven oldd meg, amelyben komfortosan dolgozol. Tipp: a Python előnyt jelent számunkra.
- **Architektúra:** A megoldás alapja legyen microservice architektúra, amely modularizálja az adatgyűjtési, feldolgozási és publikálási lépéseket.
- **Kipróbálhatóság:** Fontos feltétel, hogy az elkészült kódod lokálisan kipróbálható legyen. Kérjük, biztosítsd, hogy minden szükséges leírás és konfiguráció elérhető legyen a GitHub-on. Tipp: használd a Dockert, hogy a megoldásodat mi is könnyen ki tudjuk próbálni. Ha a feladat megoldása során a deploy-ra már nem jutott időd, akkor a Readme-ben emlékezz meg arról, hogyan is csinálnád azt meg.
- **Dokumentálás:** Kérünk, hogy a munkád alapszinten dokumentáld. Néhány szóban írd le, hogy miért az adott probléma megoldását választottad, miért az adott technológiákkal dolgoztál, a megoldásod főbb részeinek működését.

---

## Példák lehetséges megoldásokra

- **Ebédmenük összegyűjtése és megjelenítése egy adott lokáció környékén:** Keresd meg, hogy a helyi éttermek milyen ebédmenüket kínálnak, és jelenítsd meg egy felületen a napi kínálatot.
  
- **Tőzsdei (energia-, részvény- vagy nyersanyag-) árak elemzése:** API segítségével gyűjts adatokat egy adott tőzsdei termékről, és mutasd meg az árváltozások trendjeit.

- **Piactérárak követése:** Egy adott termékkategóriában (pl. ingatlanok, használt autók) figyeld meg a hirdetési árak alakulását. Ez segíthet megérteni az ármozgások trendjeit az adott termékcsoportban.

- **Sportesemények statisztikáinak gyűjtése és elemzése:** Gyűjts adatokat egy népszerű sportágról, és mutasd be, hogyan alakulnak a csapatok vagy játékosok statisztikái.

- **Időjárás-előrejelzés és tényadatok elemzése és megjelenítése:** Gyűjts időjárás előrejelzési és tény adatokat és jelenítsd meg azokat vizuálisan, akár egy városra koncentrálva.


# Feladat megoldás

A feladat megoldásához a **COINGECKO_API** által nyújtott cryptocurrency adatokat választottam, mivel az API friss és pontos információkat ad a kriptovaluták piaci helyzetéről. Az applikáció elindulásakor az API-ról gyűjtöm be az aktuális adatokat, majd betöltöm őket egy **PostgreSQL** adatbázisba.

A **PostgreSQL** választása mellett döntöttem, mert az adat struktúrája jól illik a relációs adatbázisokhoz, könnyen kezelhető és gyorsan beállítható. Emellett a skálázhatósága és a stabilitása miatt hosszú távon is kényelmes választás, ha a projekt bővül.

A megoldásom három fő lépésből áll:
1. **Adatgyűjtés**: Az API segítségével begyűjtöm a legfrissebb kriptovaluta adatokat, így mindig naprakész információkat kapunk.
2. **Adattárolás**: Az összegyűjtött adatokat egy PostgreSQL adatbázisban tárolom, ami lehetővé teszi a gyors keresést és a hatékony adatkezelést.
3. **Adatfeldolgozás és publikálás**: Az adatokat elemzem, hogy olyan érdekes betekintéseket nyújtsak, mint a legnagyobb nyerteseik és veszteseik, a volatilitás vagy a piaci kapitalizáció növekedése. Ezeket az eredményeket webes felületen vagy API-n keresztül jelenítem meg.
### 1. Top Gainer & Top Loser
Itt azt figyelhetjük meg, hogy az elmúlt 24 órában melyik cryptocurrency értéke nőtt a legtöbbet és melyiké zuhant a legnagyobbat. Ez segít azonosítani a legjobb és legrosszabb teljesítményt nyújtó valutákat az adott időszakban.

### 2. Most Volatile
Azt megmutatja, hogy melyik valuta a legvolatilisebb, azaz melyik ingadozik a legjobban 24 óra alatt. Ezzel megtudhatjuk, melyik kriptovaluta számít a legkockázatosabbnak az időszakban.

### 3. Top Volatility to Market Cap Ratio
Ez az insight a legnagyobb **Volatility to Market Cap Ratio**-val rendelkező kriptovalutát mutatja, amelyek kisebb piaci kapitalizációval, de magas volatilitással rendelkeznek. Ezek a valuták nagy ingadozásokon mennek keresztül, így magas kockázatú, de potenciálisan nagy nyereséget hozó lehetőségek.

### 4. Biggest Market Cap Growth
Ez az insight azt mutatja meg, hogy az elmúlt 24 órában melyik kriptovaluta piaci kapitalizációja nőtt a legnagyobb mértékben. A növekvő kapitalizáció gyakran arra utal, hogy a valuta iránti érdeklődés nőtt, így potenciálisan erősödő valutákat azonosíthatunk.

![graph.png](graph.png)

# Értékelés

Nem igazán foglalkoztam még hasonló projekttel, de nagyon élveztem a megoldás elkészítését. Úgy gondolom, hogy sikerült remekül kitalálni a feladatot: pont ad egy éles irányt, de egyáltalán nem túl szigorú vagy korlátozó. Nagyjából eltöltöttem vele 6 órát, úgyhogy ezen a ponton befejezem. Valószinüleg nem leszek a következő Warren Buffett ezekből az insightoktól, de nézzétek el nekem, nem vagyok közgazdász.

#### Hogyan futtathatod a projektet:

A projektet a root könyvtárból az alábbi command-dal tudjátok futtatni:

```bash
docker build -t cryptoapp . && docker run -p 5001:5000 cryptoapp
```
Ha minden jól ment, akkor a megoldás elérhető itt:

http://127.0.0.1:5001