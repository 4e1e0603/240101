# Solution

(czech)

Vytvořil jsem dle zadání Python balík `company-orders` s jednoduchým konzolovým rozhraním pro ukázku implementovaných funkcí.  

## Doménová vrstva

Po prostudování datového souboru jsem identifikoval následující [agregáty](https://martinfowler.com/bliki/DDD_Aggregate.html) uložené v modulu `company.orders._domain.py`.

- `User`: Představuje uživatele aplikace či zákazníka, který může objednávat produkty. Model uživatel obsahuje atributy `id`, `name`, `city`,
- `Product`: Představuje produkt, který uživatel objednává a přidává do výsledné objednávky. Uživatel může jeden produkt objednat i vícekrát, jak je vidět ze zadaného datového souboru. Modul produktu obsahuje atributy `id`, `name`, `price`.
- `Order`: Představuje objednávku uživatele a obsahuje reference na uživatele, který ji vytvořil a dále produkty, které si objednal. Protože se produkty v dodaných datech mohou opakovat,
  nepřidával jsem produkty přímo k objednávce ale vytvořil jsem pomocný hodnotový objekt `OrderLine`, který obsahuje produkt a jejich počet. Samotná třída `Order` neobsahuje referenci na objekt `User` ale jen odkaz na jeho identifikátor. Podobně `OrderLine` obsahuje jen odkaz na identifikátor produktu. Proč to tak je vysvětleno např. v [^1].

Doménová vrstva neobsahuje žádné vstupně/výstupní funkce (metody) a lze ji proto snadno testovat pomocí jednotkových testů. Spolu se samotným doménovým modelem, obsahuje také rozhraní (protokoly) pro perzistenci doménového modelu např. do relační databáze. Zde používám návrhový vzor [Repository](https://martinfowler.com/eaaCatalog/repository.html).

## Servisní vrstva

Servisní vrstva je uložena v modulu `company.orders._service.py`. a obsahuje hlavní třídu představující aplikační službu a to `OrderService`. Každá z jejích metod reprezentuje požadovanou funkcionalitu aplikace nebo-li *use case*. Jde v podstatě o jedinou třídu, která by zbalíku mohla být dostupná, protože představuje rozhraní pro práci s celou aplikací.

Aplikační servisní třída je závislá na dalších třídách spadajícíh do infrastruktury např. konkrétní třídy pro perzistenci (`Repository`).

Servisní třída přebírá externí data od uživatele systému (např. z konzolového rohraní nebo poslané skrze HTTP/REST), zpracovává je a výsledek operace vrací uživateli. Pokud je aplikace dobře rozvrstvěná, mělo by být jednoduché zaměnit např. zde implementovaé konzolové rozhraní za REST server (mohu doplnit).

## Infrastrukturní vrstva (perzistence)

Pro ukázaku jsem vytvořil jednoduché databázové schema pomocí SQLite v souboru `src/company/orders/schema.sql`, který je přidán jako data balíku.

Jak již bylo zmíněno, přístup do databáze je abstrahován pomocí *repository pattern*. Ty jsou reprezentováný rohraními (protokoly) uloženými v doménové vrstvě a implementací v servisní/infrastrukturní vrstvě `company.orders._storage.py`.

Lze tak jednoduše implementovat perzistenci pro jiný databázový server nebo ukládání do paměti či souboru.

V produkční aplikaci by zřejmě chtělo ještě implementovat *Unit of Work* neboli transakční přístup do úložiště.

## Ukázka funckionality

Demonstrační příklad s jednoduchým konzolovým rohraním je uložen v modulu `company.orders.__main__`. ten obsahuje tři úlohy dle zadání:

1. vloží data objednávek ze zadaného souboru (`ndjson`/`jsonl`),
2. vybere objednávky v zadaném časovém období,
3. vybere horních deset uživatelů s nejvíce objednávkami za celou historii.

## Testování

Testy se dají rozdělit na jednotkové a integrační. Doménová vrstva se testuje pomocí jednotkových testů. Servisní vrstva, při použití *dependency injection*, kdy mokujeme nějaké závislé třídy/metody, se dá také jednotkově testovat.

Pokud bychom ale chtěli testovat reálnou aplikaci, musíme zapojit reálnou databázi např. běžící v kontejneru. To zde zatím není ukázáno.

Testování servisní vrstvy je pouze nazančeno, ale mohu doplnit/vylepšit.

## Poznámky

- Používám [*namespace pakage*](https://youtu.be/iroXKdSqSPo?si=ZS2LRkEI3accxks5) viz `company`.
- Pro dokumentaci používím [Sphinx](https://www.sphinx-doc.org/en/master/), ta by si zasloužila ještě větší péči a to
  jak dokumentovat více kód balíku s exportovaným API, tak nějaký *design decision document* atd.
- Namísto vyhazování výjimek v doménové vrstvě, lze uvažovat o vracení chyby hodnotou např. pomocé speciálního typu `Result = Value | Error`.
- V případě produkční služby, je servisní třída většinou schována za REST API (např. pomocí balíku Flask) a nasazena jako kontejner (např. Docker/Podman, Kubernetes).

## References

- Evans, E. (2004). *Domain-Driven Design: Tackling Complexity in the Heart of Software*. Addison-Wesley. ISBN: 9780321125217
- Vernon, V. (2013). *Implementing Domain-Driven Design*. Upper Saddle River, Addison-Wesley. ISBN: 9780321834577
- Percival H., Gregory B., (2021) . *Architecture Patterns with Python*, O'Reilly Media. ISBN: 9781492052203
- <https://martinfowler.com/bliki/DomainDrivenDesign.html>
- <https://ndjson.org/>, <https://jsonlines.org/>

[^1]: *In general, you should avoid holding object references to other aggregates but rather reference other aggregates by ID.*

<small>

Hudba pro code review:

- [*Metal Gear Solid 2: Sons of Liberty Original Soundtrack – Countdown To Disaster (2001)*](https://www.youtube.com/watch?v=Vmp6e5H_4s8)

</small>
