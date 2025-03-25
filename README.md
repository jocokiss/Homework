# Feladat megoldás

A feladat megoldásához a **COINGECKO_API** által nyújtott cryptocurrency adatokat választottam, mivel az API friss és pontos információkat ad a kriptovaluták piaci helyzetéről. Az applikáció elindulásakor az API-ról gyűjtöm be az aktuális adatokat, majd betöltöm őket egy **PostgreSQL** adatbázisba.

A **PostgreSQL** választása mellett döntöttem, mert az adat struktúrája jól illik a relációs adatbázisokhoz, könnyen kezelhető és gyorsan beállítható. Emellett a skálázhatósága és a stabilitása miatt hosszú távon is kényelmes választás, ha a projekt bővül.

A megoldásom három fő lépésből áll:
1. **Adatgyűjtés**: Az API segítségével begyűjtöm a legfrissebb kriptovaluta adatokat, így mindig naprakész információkat kapunk.
2. **Adattárolás**: Az összegyűjtött adatokat egy PostgreSQL adatbázisban tárolom, ami lehetővé teszi a gyors keresést és a hatékony adatkezelést.
3. **Adatfeldolgozás és publikálás**: Az adatokat elemzem, hogy olyan érdekes betekintéseket nyújtsak, mint a legnagyobb nyerteseik és veszteseik, a volatilitás vagy a piaci kapitalizáció növekedése. Ezeket az eredményeket webes felületen keresztül jelenítem meg.
### 1. Top Gainer & Top Loser
Itt azt figyelhetjük meg, hogy az elmúlt 24 órában melyik cryptocurrency értéke nőtt a legtöbbet és melyiké zuhant a legnagyobbat. Ez segít azonosítani a legjobb és legrosszabb teljesítményt nyújtó valutákat az adott időszakban.

### 2. Most Volatile
Azt megmutatja, hogy melyik valuta a legvolatilisebb, azaz melyik ingadozik a legjobban 24 óra alatt. Ezzel megtudhatjuk, melyik kriptovaluta számít a legkockázatosabbnak az időszakban.

### 3. Top Volatility to Market Cap Ratio
Ez az insight a legnagyobb **Volatility to Market Cap Ratio**-val rendelkező kriptovalutát mutatja, amelyek kisebb piaci kapitalizációval, de magas volatilitással rendelkeznek. Ezek a valuták nagy ingadozásokon mennek keresztül, így magas kockázatú, de potenciálisan nagy nyereséget hozó lehetőségek.

### 4. Biggest Market Cap Growth
Ez az insight azt mutatja meg, hogy az elmúlt 24 órában melyik kriptovaluta piaci kapitalizációja nőtt a legnagyobb mértékben. A növekvő kapitalizáció gyakran arra utal, hogy a valuta iránti érdeklődés nőtt, így potenciálisan erősödő valutákat azonosíthatunk.

![graph.png](graph.png)

# Hogyan futtathatod a projektet:

A feladatkiírásból feltételezem, hogy a docker, docker-compose telepítve van, ha mégsem akkor szükséges lesz letölteni őket!

A projektet a root könyvtárból az alábbi paranccsal tudjátok futtatni:

```bash
docker-compose build && docker-compose up
```
Ha minden jól ment, akkor a megoldás elérhető itt:

http://127.0.0.1:5001