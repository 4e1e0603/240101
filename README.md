# company-orders

[![build](https://github.com/4e1e0603/230101/actions/workflows/main.yml/badge.svg)](https://github.com/4e1e0603/230101/actions/workflows/main.yml)
[![docs](https://github.com/4e1e0603/230101/actions/workflows/docs.yml/badge.svg)](https://github.com/4e1e0603/230101/actions/workflows/docs.yml)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/a70ed10bc4b949f7a236e67d1ff0287f)](https://app.codacy.com/gh/4e1e0603/230101/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)

<p align="center">
  <img src="./snake.png" width=250px />
</p>

## Assignment

- Create an `OrderService` class that will provide the following interfaces/methods:
  - Reading records from the orders.jsonl input file and storing them in a relational database with a suitable database model (path to the file passed in parameters).
    - Each row contains the data of user orders.
    - User and product attributes do not change across the file.
  - Obtaining orders for a given time period (time period passed by parameters).
  - Getting the users who have bought the most products in the entire history (number of users passed as parameters).

Implementation notes:

- No UI or API required to demonstrate the code. You just need to call everything in the main.py file and write the result to the standard output.
- A thorough OO design is key to evaluation. Make sure that the resulting code is reusable and easily extensible.
- Use static typing (<https://docs.python.org/3/library/typing.html>).
- Tests are not required, but code must be written in such a way that tests can be easily written on it.
- Do not forget about the treatment of external inputs.
- Save the resulting solution to the public GitHub repository.

**Solution** is described in [documentation](https://4e1e0603.github.io/230101/).

## Usage

A database is created when the script is executed from the package data file, see [./src/company/orders/schema.sql](schema.sql). You can also creata schema by hand with a `sqlite3` binary e.g.

```shell
./sqlite3 orders.sqlite
sqlite> .read path/to/schema.sql
```

The package contains simple command line interface for functionality demonstration.

```shell
company-orders --data [file_path] [--verbose]
```

The console output should look like this:

```powershell
===[TASK 1]===

Processed records 5000/5000

===[TASK 2]===

Order(id=15,created='2018-11-16 14:09:34')
Order(id=31,created='2018-11-18 16:50:38')
Order(id=56,created='2018-11-18 00:40:23')
Order(id=67,created='2018-11-19 06:55:10')
Order(id=75,created='2018-11-16 03:52:51')
Order(id=81,created='2018-11-17 18:02:58')
Order(id=97,created='2018-11-20 01:47:55')
...
Order(id=4995,created='2018-11-16 04:47:57')
Order(id=4999,created='2018-11-17 23:29:51')

===[TASK 3]===

User(city=Singapore,identifier=2,name=User C)
User(city=Melbourne,identifier=4,name=User E)
User(city=Prague,identifier=0,name=User A)
User(city=Hong Kong,identifier=6,name=User G)
User(city=Kuala Lumpur,identifier=7,name=User H)

--SUCCESS--
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
  cd src/  # because Mypy weird error, see comment bellow
  mypy --show-column-numbers --namespace-packages --explicit-package-bases .
  ```

  Sometimes mypy has some obscure errors: <https://notes.jml.io/2021-02-06-15-26/>, e.g:

  ```shell
  src\company\orders\_domain.py: error: Source file found twice under different module names: "src.company.orders._domain" and "company.orders._domain"
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

    I hope you know the rest&hellip;

  
- We use [`setuptools-scm`](https://setuptools-scm.readthedocs.io/en/latest/) to manage package version.
