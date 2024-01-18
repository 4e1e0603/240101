# Solution (cs)

Vytvořil jsem Python balík s názvem `company-orders` a jednoduchým ukázkovým konzolovým rohraním (skript).  

## Doménová vrstva

Implementujeme tyto [agregáty](https://martinfowler.com/bliki/DDD_Aggregate.html) uložené v modulu `company.orders._domain.py`:

- `User`: představuje uživatele aplikace.
- `Product`: představuje produkt, který uživatel opřidává do objednávky.
- `Order`:  představuje objednávku uživatele a obsahuje rederence na uživatele a proukty skrze jejich ID.

Jde o kořenové entity agregátu tzn., že mají životní cyklus. Například jméno uživatele, název nebo cena produktu se mohou měnit, avšak jde stále o stejného uživatele respektive produkt. Samotná třída `Order` neobsahuje reference na objekty `User` a `Product` (kolekce), ale jen jejich hodnoty jejich identifikátorů [^1].

Doménová vrstva neobsahuje žádné vstupně/výstupní funkce (metody) a lze ji proto snadno testovat pomoocí jednotkových testů. Spolu s doménovým modelme obsahuje také rozhraní (protokoly) pro perzistenci doménového modelu -- zde používám návrhový vzor [Repository](https://martinfowler.com/eaaCatalog/repository.html).

## Servisní vrstva

&hellip;

## Poznámky

- Namísto vyhazování výjimek v doménové vrstvě, lze uvažovat o vracení chyby hodnotou nebo jako speciální typ `Result = Value | Error`.
- V případě produkční služby, je servisní třída většinou schována za REST API (např. pomocí balíku Flask) a nasazena
jako kontejner (např. Docker/Podman, Kubernetes).

## References

- Evans, E. (2004). *Domain-Driven Design: Tackling Complexity in the Heart of Software*. Addison-Wesley. ISBN: 9780321125217
- Vernon, V. (2013). *Implementing Domain-Driven Design*. Upper Saddle River, Addison-Wesley. ISBN: 9780321834577
- Percival H., Gregory B., (2021) . *Architecture Patterns with Python*, O'Reilly Media. ISBN: 9781492052203
- <https://martinfowler.com/bliki/DomainDrivenDesign.html>
- <https://ndjson.org/>, <https://jsonlines.org/>

[^1]: *In general, you should avoid holding object references to other aggregates but rather reference other aggregates by ID.*

<small>
Hudba pro code review:

- [*Metal Gear Solid 2: Sons of Liberty Original Soundtrack – Revolver Ocelot (2001)*](https://youtu.be/rEwb5mXxOls?si=vytNUV_jnK-t-Qql)
- [*Metal Gear Solid 2: Sons of Liberty Original Soundtrack – Twilight Sniping (2001)*](https://youtu.be/iroXKdSqSPo?si=ZS2LRkEI3accxks5)
- [*Metal Gear Solid 2: Sons of Liberty Original Soundtrack – Countdown to Disaster (2001)*](https://youtu.be/z31HzRBW1qU?si=hqTfjFFpTxwpxg_-)
</small>