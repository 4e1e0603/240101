# company-orders

[![build](https://github.com/4e1e0603/230101/actions/workflows/main.yml/badge.svg)](https://github.com/4e1e0603/230101/actions/workflows/main.yml)
[![docs](https://github.com/4e1e0603/230101/actions/workflows/docs.yml/badge.svg)](https://github.com/4e1e0603/230101/actions/workflows/docs.yml)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/a70ed10bc4b949f7a236e67d1ff0287f)](https://app.codacy.com/gh/4e1e0603/230101/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)

(work-in-progress)

## Assignment (cs)

- Vytvoř třídu `OrderService`, která bude poskytovat následující rozhraní/metody:
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

**Solution** is described in [documentation](https://4e1e0603.github.io/230101/).

## Usage

A database is created when the script is executed from the package data file, see [src/company/orders/schema.sql](schema.sql). You can also creata schema by hand with a `sqlite3` binary e.g.

```shell
./sqlite3 orders.sqlite
sqlite> .read path/to/schema.sql
```

The package contains simple command line interface

```shell
company-orders --data [file_path]
```

## Installation

- Clone the repository.

  ```powershell
  git clone https://github.com/4e1e0603/230101.git company-orders
  ```

- Create  virtual environment.

  ```powershell
  py -3.12 -m venv .venv && .\.venv\Scripts\activate
  ````

- Install runtime dependencies.

  ```powershell
  python -m pip install .\company-orders
  ```

## Development

- Go to project directory.

  ```powershell
  cd company-orders
  ```

- Install package in editable mode.

  ```powershell
  python -m pip install -e .
  ```

- Install development dependencies.

  ```powershell
  python -m pip install -r requirements.txt
  ```

- Use [`mypy`](https://mypy-lang.org/) for type checking.

  ```powershell
  mypy --show-error-codes .
  ```

- Use [`ruff`](https://docs.astral.sh/ruff/) for formating and linting.

  ```powershell
  ruff format . && ruff check --fix .
  ```

- Run all available tests.

  ```shell
  pytest  
  ```

- Run only domain (unit) tests.

  ```shell
  pytest -m domain
  ```

- Create a documentation site.

    ```powershell
    python -m pip install -r docs/requirements.txt
    ```

    ```powershell
    sphinx-build.exe .\source\ .\build\
    ```
  
- We use [`setuptools-scm`](https://setuptools-scm.readthedocs.io/en/latest/) to manage package version.
