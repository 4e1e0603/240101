# OrderService

## Assignment

- Vytvoř třídu `OrdersService`, která bude poskytovat následující rozhraní (veřejné metody):
  - Načtení záznamů ze vstupního souboru a jejich uložení do relační databáze s vhodným databázovým modelem (cesta k souboru předaná parametrem).
    - Charakter vstupního souboru (data.ndjson):
      - V každém řádku se nachází denormalizovaná data objednávek uživatelů.
      - Atributy uživatelů a produktů (id, name, price, city) se napříč souborem nemění.
  - Získání objednávek za daný časový úsek (časový úsek předán parametrem).
  - Získání uživatelů, kteří nakoupili za celou historii nejvíce produktů (počet uživatelů předán parametrem).

- Poznámky k implementaci:
  - Pro demonstraci kódu není třeba žádné UI ani API. Vše stačí zavolat v main.py souboru a výsledek vypsat na standardní výstup.
  - Důkladný OOP návrh je pro hodnocení klíčový. Dbej na to, aby byl výsledný kód znovupoužitelný a snadno rozšiřitelný.
  - Použij statické typování (https://docs.python.org/3/library/typing.html). 
  - Testy nejsou povinné, ale kód musí být napsán tak, aby na něj bylo možné testy snadno napsat.
  - Nezapomeň na ošetření vnějších vstupů.
  - Výsledné řešení ulož do veřejného Git repozitáře.


## Solution

Orientoval jsem se podle zadaného datového soubory a identifikoval tyto 
doménové objekty s následujícími atributy: 

- User(id, name, city)
- Order()
- Product(name, price, )


Vytvořil jsem Python balík s názvem `merio-order-service` ten představuje knihovnu, která se dá dále upravit na aplikaci npř. s REST či CLI rozhraním. Provedl jsem ukzáku pro oboje možnosti.

