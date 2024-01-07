# OrderService

**work-in-progress**

Music for code review: [*Metal Gear Solid 2: Sons of Liberty Original Soundtrack (2001)*](https://youtu.be/ZUd7myd0NK8?si=BM32dlPiFP9iO1-m)

## Installation

```powershell
git clone https://github.com/4e1e0603/230101.git
```

```powershell
cd 230101
```

```powershell
py -3.12 -m venv .venv
````

```powershell
.\.venv\Scripts\activate
```

```powershell
python -m pip install -e .
```

## Development

```powershell
python -m pip install -r requirements.txt
```

We use `mypy` for type checking.

```powershell
mypy --show-error-codes .
```

We use `ruff` for formating and linting.

```powershell
ruff format .
ruff check --fix .
```

## Usage

The package contains simple command line interface

```powershell
meiro-orders --insert [file_path]
meiro-orders (search users)
meiro-orders (search orders)   
```

## Assignment (cs)

- Vytvoř třídu `OrdersService`, která bude poskytovat následující rozhraní (veřejné metody):
  - [ ] Načtení záznamů ze vstupního souboru a jejich uložení do **relační** databáze s vhodným databázovým modelem (cesta k souboru předaná parametrem).
    - Charakter vstupního souboru (data.ndjson):
      - V každém řádku se nachází denormalizovaná data objednávek uživatelů.
      - Atributy uživatelů a produktů (id, name, price, city) se napříč souborem nemění.
  - [ ] Získání objednávek za daný časový úsek (časový úsek předán parametrem).
  - [ ] Získání uživatelů, kteří nakoupili za celou historii nejvíce produktů (počet uživatelů předán parametrem).

- Poznámky k implementaci:
  - Pro demonstraci kódu není třeba žádné UI ani API. Vše stačí zavolat v main.py souboru a výsledek vypsat na standardní výstup.
  - Důkladný OOP návrh je pro hodnocení klíčový. Dbej na to, aby byl výsledný kód znovupoužitelný a snadno rozšiřitelný.
  - [x] Použij statické typování (<https://docs.python.org/3/library/typing.html>).
    - mypy, ruff
  - [ ] Testy nejsou povinné, ale kód musí být napsán tak, aby na něj bylo možné testy snadno napsat.
    - pytest
  - [ ] Nezapomeň na ošetření vnějších vstupů.
  - [x] Výsledné řešení ulož do veřejného Git repozitáře.

## Solution (cs)

Vytvořil jsem Python balík s názvem `merio-order-service` ten představuje knihovnu, která se dá dále upravit na aplikaci npř. s REST či CLI rozhraním. Provedl jsem ukzáku pro oboje možnosti.

Orientoval jsem se podle zadaného datového soubory a identifikoval tyto
doménové objekty, přesněji řečeno doménové entity, s následujícími atributy:

- `User(id, name, city, created)`
- `Product(id, name, price, created)`
- `Order(id, name, user, products, created)`

Jde o entity, protože mají životní cyklus. Např. název nebo cena se mění, avšak jde stále o stějného uživatele respektive produkt.
Tyto entioty navíc představují samostatné agregáty (<https://martinfowler.com/bliki/DDD_Aggregate.html>).
Z předchozího vyplývá, že třída `Order`` neosahuje reference na objekty User a Product(s), ale jen jejich ID, viz
> In general, you should avoid holding object references to other aggregates but rather reference other aggregates by id.

Namísto vyhazování výjimek v doménové vrstvě, lze uvažovat o vracení chyby hodnotou nebo jako speciální typ `Result = Value | Error`.

V případě produkční služby, je servisní třída většinou schována za REST API (např. pomocí balíku Flask) a nasazena
jako kontejner (např. Docker/Podman, Kubernetes).

## References

- Evans E., (2003)
- Vernon V., (2013)
- <https://martinfowler.com/bliki/DomainDrivenDesign.html>
