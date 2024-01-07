# meiro-orders

(work-in-progress)

Music for code review:

- [*The Legend of Zelda: Breath of The Wild (2017)*](https://youtu.be/Hgd8aYjE0Bs?si=UeVbTcC4kLQvykVT)
- [*Metal Gear Solid 2: Sons of Liberty Original Soundtrack (2001)*](https://youtu.be/ZUd7myd0NK8?si=BM32dlPiFP9iO1-m)

## Installation

```powershell
git clone https://github.com/4e1e0603/230101.git meiro-orders
```

```powershell
py -3.12 -m venv .venv && .\.venv\Scripts\activate
````

```powershell
python -m pip install .\meiro-orders
```

## Development

```powershell
cd meiro-orders
```

```powershell
python -m pip install -e .
```

```powershell
python -m pip install -r requirements.txt
```

We use [`mypy`](https://mypy-lang.org/) for type checking.

```powershell
mypy --show-error-codes .
```

We use [`ruff`](https://docs.astral.sh/ruff/) for formating and linting.

```powershell
ruff format . && ruff check --fix .
```

### Tests

```shell
pytest                          # Run all tests.
pytest -m domain                # Run domain (unit) tests.
```

### Versions

We use [`setuptools-scm`](https://setuptools-scm.readthedocs.io/en/latest/) to manage package version.
  
## Usage

The package contains simple command line interface

```shell
meiro-orders --insert [file_path]
meiro-orders (search-users) // NOT IMPLEMENTED
meiro-orders (search-orders) // NOT IMPLEMENTED   
```

---

## Assignment (cs)

- Vytvoř třídu `OrdersService`, která bude poskytovat následující rozhraní:
  - Načtení záznamů ze vstupního souboru `data/orders.jsonl` a jejich uložení do **relační** databáze s vhodným databázovým modelem (cesta k souboru předaná parametrem).
    - V každém řádku se nachází data objednávek uživatelů.
    - Atributy uživatelů a produktů se napříč souborem nemění.
  - Získání objednávek za daný časový úsek (časový úsek předán parametrem).
  - Získání uživatelů, kteří nakoupili za celou historii nejvíce produktů (počet uživatelů předán parametrem).

Poznámky k implementaci:

- Pro demonstraci kódu není třeba žádné UI ani API. Vše stačí zavolat v main.py souboru a výsledek vypsat na standardní výstup.
- Důkladný OOP návrh je pro hodnocení klíčový. Dbej na to, aby byl výsledný kód znovupoužitelný a snadno rozšiřitelný.
- Použij statické typování (<https://docs.python.org/3/library/typing.html>).
- Testy nejsou povinné, ale kód musí být napsán tak, aby na něj bylo možné testy snadno napsat.
- Nezapomeň na ošetření vnějších vstupů.
- Výsledné řešení ulož do veřejného GitHub repozitáře.

## Solution (cs)

Vytvořil jsem Python balík s názvem `merio-orders` a jednoduchým ukázkovým konzolovým rohraním (skript).  

### Doménová vrstva

 Orientoval jsem se podle daného datového souboru a identifikoval [agregáty](https://martinfowler.com/bliki/DDD_Aggregate.html) ( uložené v modulu `meiro.orders._domain.py`:

- `User`: představuje uživatele aplikace.
- `Product`: představuje produkt, který uživatel opřidává do objednávky.
- `Order`:  představuje objednávku uživatele a obsahuje rederence na uživatele a proukty skrze jejich ID.

Jde o kořenové entity agregátu tzn., že mají životní cyklus. Například jméno uživatele, název nebo cena produktu se mohou měnit, avšak jde stále o stejného uživatele respektive produkt. Samotná třída `Order` neobsahuje reference na objekty `User` a `Product` (kolekce), ale jen jejich hodnoty jejich identifikátorů [^1].

Doménová vrstva neobsahuje žádné vstupně/výstupní funkce (metody) a lze ji proto snadno testovat pomoocí jednotkových testů. Spolu s doménovým modelme obsahuje také rozhraní (protokoly) pro perzistenci doménového modelu -- zde používám návrhový vzor [Repository](https://martinfowler.com/eaaCatalog/repository.html).

### Servisní vrstva

&hellip;

### Verzování

### Poznámky

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
