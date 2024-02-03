# company-orders

[![build](https://github.com/4e1e0603/230101/actions/workflows/main.yml/badge.svg)](https://github.com/4e1e0603/230101/actions/workflows/main.yml)
[![docs](https://github.com/4e1e0603/230101/actions/workflows/docs.yml/badge.svg)](https://github.com/4e1e0603/230101/actions/workflows/docs.yml)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/a70ed10bc4b949f7a236e67d1ff0287f)](https://app.codacy.com/gh/4e1e0603/230101/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)

<p align="center">
  <img src="./snake.png" width=100px />
</p>

## Assignment

Create an `OrderService` class that will provide the following interfaces/methods:

1. Reading records from the `orders.jsonl` file and storing them in a relational database with a suitable database model (path to the file passed in parameters).
    1. Each row contains the data of user orders.
    2. User and product attributes do not change across the file.
2. Obtaining orders for a given time period (time period passed by parameters).
3. Getting the users who have bought the most products in the entire history (number of users passed as parameters).

Implementation notes:

- No UI or API required to demonstrate the code. You just need to call everything in the main.py file and write the result to the standard output.
- A thorough OO design is key to evaluation. Make sure that the resulting code is reusable and easily extensible.
- Use static typing (<https://docs.python.org/3/library/typing.html>).
- Tests are not required, but code must be written in such a way that tests can be easily written on it.
- Do not forget about the treatment of external inputs.
- Save the resulting solution to the public GitHub repository.

**Solution** is described in [documentation](https://4e1e0603.github.io/230101/).

## Usage

A database is created when the script is executed from the package data file, see [https://github.com/4e1e0603/230101/blob/main/src/company/orders/schema.sql](schema.sql). You can also creata schema by hand with a `sqlite3` binary e.g.

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
 company-orders --data .\orders.jsonl

===[TASK 1]===

Import records from file 'orders.jsonl'...

===[DONE]===


===[TASK 2]===

Select orders between 2018-11-16 01:29:04 and 2018-11-16 10:45:30...

Order(id=75,created='2018-11-16 03:52:51')
Order(id=124,created='2018-11-16 04:34:02')
Order(id=431,created='2018-11-16 10:48:18')
Order(id=579,created='2018-11-16 05:46:49')
Order(id=686,created='2018-11-16 04:23:26')
Order(id=865,created='2018-11-16 09:45:41')
Order(id=1232,created='2018-11-16 02:42:20')
Order(id=1307,created='2018-11-16 05:43:19')
Order(id=1451,created='2018-11-16 03:42:03')
Order(id=1464,created='2018-11-16 05:34:18')
Order(id=1688,created='2018-11-16 09:40:15')
Order(id=1706,created='2018-11-16 09:45:34')
Order(id=1880,created='2018-11-16 09:31:12')
Order(id=1890,created='2018-11-16 02:39:49')
Order(id=2171,created='2018-11-16 02:53:52')
Order(id=2245,created='2018-11-16 07:39:23')
Order(id=2409,created='2018-11-16 05:04:44')
Order(id=2665,created='2018-11-16 07:33:48')
Order(id=2667,created='2018-11-16 05:43:33')
Order(id=3069,created='2018-11-16 08:56:50')
Order(id=3085,created='2018-11-16 11:43:14')
Order(id=3166,created='2018-11-16 08:32:41')
Order(id=3620,created='2018-11-16 06:26:43')
Order(id=3650,created='2018-11-16 06:33:00')
Order(id=3897,created='2018-11-16 09:46:00')
Order(id=4083,created='2018-11-16 10:18:56')
Order(id=4105,created='2018-11-16 11:09:50')
Order(id=4106,created='2018-11-16 04:50:03')
Order(id=4135,created='2018-11-16 07:47:09')
Order(id=4519,created='2018-11-16 03:21:35')
Order(id=4995,created='2018-11-16 04:47:57')

===[DONE]===

===[TASK 3]===

Select top 5 users with most products...

User(city=Singapore,identifier=2,name=User C)
User(city=Melbourne,identifier=4,name=User E)
User(city=Prague,identifier=0,name=User A)
User(city=Hong Kong,identifier=6,name=User G)
User(city=Kuala Lumpur,identifier=7,name=User H)

===[DONE]===

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
