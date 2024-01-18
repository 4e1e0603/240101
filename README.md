# company-orders

[![build](https://github.com/4e1e0603/230101/actions/workflows/main.yml/badge.svg)](https://github.com/4e1e0603/230101/actions/workflows/main.yml)
[![docs](https://github.com/4e1e0603/230101/actions/workflows/docs.yml/badge.svg)](https://github.com/4e1e0603/230101/actions/workflows/docs.yml)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/a70ed10bc4b949f7a236e67d1ff0287f)](https://app.codacy.com/gh/4e1e0603/230101/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)

(work-in-progress)
me

## Assignment (cs)

- Vytvoř třídu `OrderService`, která bude poskytovat následující rozhraní:
  - Načtení záznamů ze vstupního souboru `orders.jsonl` a jejich uložení do **relační** databáze s vhodným databázovým modelem (cesta k souboru předaná parametrem).
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

Implementujeme tyto [agregáty](https://martinfowler.com/bliki/DDD_Aggregate.html) uložené v modulu `company.orders._domain.py`:

- `User`: představuje uživatele aplikace.
- `Product`: představuje produkt, který uživatel opřidává do objednávky.
- `Order`:  představuje objednávku uživatele a obsahuje rederence na uživatele a proukty skrze jejich ID.

Jde o kořenové entity agregátu tzn., že mají životní cyklus. Například jméno uživatele, název nebo cena produktu se mohou měnit, avšak jde stále o stejného uživatele respektive produkt. Samotná třída `Order` neobsahuje reference na objekty `User` a `Product` (kolekce), ale jen jejich hodnoty jejich identifikátorů [^1].

Doménová vrstva neobsahuje žádné vstupně/výstupní funkce (metody) a lze ji proto snadno testovat pomoocí jednotkových testů. Spolu s doménovým modelme obsahuje také rozhraní (protokoly) pro perzistenci doménového modelu -- zde používám návrhový vzor [Repository](https://martinfowler.com/eaaCatalog/repository.html).

### Servisní vrstva

&hellip;

### Poznámky

- Namísto vyhazování výjimek v doménové vrstvě, lze uvažovat o vracení chyby hodnotou nebo jako speciální typ `Result = Value | Error`.
- V případě produkční služby, je servisní třída většinou schována za REST API (např. pomocí balíku Flask) a nasazena
jako kontejner (např. Docker/Podman, Kubernetes).

### References

- Evans, E. (2004). *Domain-Driven Design: Tackling Complexity in the Heart of Software*. Addison-Wesley. ISBN: 9780321125217
- Vernon, V. (2013). *Implementing Domain-Driven Design*. Upper Saddle River, Addison-Wesley. ISBN: 9780321834577
- Percival H., Gregory B., (2021) . *Architecture Patterns with Python*, O'Reilly Media. ISBN: 9781492052203
- <https://martinfowler.com/bliki/DomainDrivenDesign.html>
- <https://ndjson.org/>, <https://jsonlines.org/>

[^1]: *In general, you should avoid holding object references to other aggregates but rather reference other aggregates by ID.*

<small>

Music for code review:

- [*Metal Gear Solid 2: Sons of Liberty Original Soundtrack – Revolver Ocelot (2001)*](https://youtu.be/rEwb5mXxOls?si=vytNUV_jnK-t-Qql)
- [*Metal Gear Solid 2: Sons of Liberty Original Soundtrack – Twilight Sniping (2001)*](https://youtu.be/iroXKdSqSPo?si=ZS2LRkEI3accxks5)
- [*Metal Gear Solid 2: Sons of Liberty Original Soundtrack – Countdown to Disaster (2001)*](https://youtu.be/z31HzRBW1qU?si=hqTfjFFpTxwpxg_-)

</small>

## Installation

-

  ```powershell
  git clone https://github.com/4e1e0603/230101.git company-orders
  ```

-

  ```powershell
  py -3.12 -m venv .venv && .\.venv\Scripts\activate
  ````

-

  ```powershell
  python -m pip install .\company-orders
  ```

## Development

-

  ```powershell
  cd company-orders
  ```

-

  ```powershell
  python -m pip install -e .
  ```

-

  ```powershell
  python -m pip install -r requirements.txt
  ```

- We use [`mypy`](https://mypy-lang.org/) for type checking.

  ```powershell
  mypy --show-error-codes .
  ```

- We use [`ruff`](https://docs.astral.sh/ruff/) for formating and linting.

  ```powershell
  ruff format . && ruff check --fix .
  ```

- Run all tests.
s

  ```shell
  pytest  
  ```

- Run domain (unit) tests.

  ```shell
  pytest -m domain
  ```

- We use [`setuptools-scm`](https://setuptools-scm.readthedocs.io/en/latest/) to manage package version.
  
## Usage

Database is created when the script is executed from the package data file, see [src/company/orders/schema.sql](schema.sql). You can also creata the schma by hand with `sqlite3` binary.

```shell
./sqlite3 orders.sqlite
sqlite> .read schema.sql
```

The package contains simple command line interface

```shell
company-orders --import [file_path]
company-orders (search-users) // NOT IMPLEMENTED
company-orders (search-orders) // NOT IMPLEMENTED   
```
