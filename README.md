# DigitalHub Retail Database Manager

A Python command-line application for maintaining a retail database and exploring joined sales records. Developed for EGE311 Database Design & Applications, it combines a MySQL schema with menus for record management, search, reporting, and account registration.

**Stack:** Python 3 · MySQL · `mysql-connector-python` · `bcrypt`

## Features

- Register and authenticate application users using bcrypt password hashes.
- Read, create, update, and delete records through the admin menu.
- Use a smaller read/search menu for staff.
- Search selected columns with the operators exposed by the application.
- Filter reports by country, date range, store, and product category.
- Display all report rows or limit the number printed.

**Access-control limitation:** the original application asks the signed-in user to choose Admin or Staff. This is menu separation, not enforced role-based authorization. Do not use it to protect real retail records.

## Database structure

| Table | Stored information |
| --- | --- |
| `customers` | Customer details and locations |
| `stores` | Store locations, floor area, and opening dates |
| `products` | Product attributes, cost, price, and category |
| `order_details` | Order number, line item, and purchased quantity |
| `orders` | Dates and references to customer, store, product, and order details |
| `users` | Usernames, password hashes, per-user pepper values, and creation timestamps |

The committed [schema](database/schema.sql) is the implementation reference. It includes foreign keys from `orders` to the other retail tables. Customer deletion cascades to related orders; the other referenced records use restrictive deletion rules. The schema has no original rows, accounts, hashes, or pepper values.

## Reproduce locally

**Prerequisites:** Git, Python 3, a running MySQL server, and MySQL Workbench or the `mysql` client. For the unchanged coursework queries, use an instance with case-insensitive table names, as is usual with MySQL on Windows. Check `SHOW VARIABLES LIKE 'lower_case_table_names';`: an instance returning `0` needs query/schema casing reconciled before every feature will work. Do not change this server setting blindly on an existing database.

### 1. Clone and install

```powershell
git clone https://github.com/ChuaJiaSheng/digitalhub-retail-manager.git
cd digitalhub-retail-manager
python -m venv .venv
.\\.venv\\Scripts\\python.exe -m pip install -r requirements.txt
```

### 2. Create the schema

In MySQL Workbench, connect to your local server, open `database/schema.sql`, and execute it. The file creates `digitalhub` and six tables. Check:

```sql
USE digitalhub;
SHOW TABLES;
```

Expect `customers`, `stores`, `products`, `order_details`, `orders`, and `users`.

### 3. Configure and launch

In the same PowerShell terminal as the cloned project:

```powershell
$env:DIGITALHUB_DB_HOST = "localhost"
$env:DIGITALHUB_DB_USER = "YOUR_LOCAL_DATABASE_USER"
$env:DIGITALHUB_DB_PASSWORD = "YOUR_LOCAL_DATABASE_PASSWORD"
$env:DIGITALHUB_DB_NAME = "digitalhub"
.\\.venv\\Scripts\\python.exe src/main.py
```

Use a local database user with privileges on `digitalhub`. These are MySQL credentials; they are separate from the application account you create next. The script reads process environment variables, not an automatically loaded `.env` file.

### 4. Check an empty installation

Choose **Register**, create a demo application account, then log in. Choose Staff to read/search the empty tables, or Admin for the CRUD/report menus. The login/menu flow should appear even before you insert retail data. A new database correctly returns empty results.

### 5. Add a synthetic report example

On a fresh demo database, execute this SQL in Workbench once:

```sql
USE digitalhub;
INSERT INTO customers (Customers_Name) VALUES ('Demo Customer');
SET @customer_id = LAST_INSERT_ID();
INSERT INTO stores (Stores_Country) VALUES ('Singapore');
SET @store_id = LAST_INSERT_ID();
INSERT INTO products (Product_Name, Product_Unit_Price, Product_Category)
VALUES ('Demo Keyboard', 20.00, 'Accessories');
SET @product_id = LAST_INSERT_ID();
INSERT INTO order_details (Order_Number, Line_Item, Purchased_Quantity)
VALUES (1001, 1, 2);
SET @detail_id = LAST_INSERT_ID();
INSERT INTO orders
(Order_Details_ID, Order_Date, Customers_ID, Stores_ID, Product_ID)
VALUES (@detail_id, '2024-01-01', @customer_id, @store_id, @product_id);
```

Select **Display Report** in the Admin menu, leave filters empty, then print all rows. **Expected result:** the demo row should show `Demo Keyboard`, quantity `2`, unit price `20.00`, and calculated sales `40.00`. This is a reproduction check, not a real transaction. Re-running the inserts creates another demo order.

If connection fails, verify the server, credentials, and selected database. If reporting fails with a table-not-found error, check table-name case handling before changing the report logic.

## Source guide

| Path | Purpose |
| --- | --- |
| [src/main.py](src/main.py) | Connection handling, authentication, CRUD, search, reports, and menus |
| [database/schema.sql](database/schema.sql) | Six-table schema without source data |
| [requirements.txt](requirements.txt) | Python dependencies |

## Troubleshooting and limitations

- Connection errors: check that MySQL is running, the variables are set in the active terminal, and the database user has the necessary privileges.
- Table-not-found errors: the historical application mixes table-name case. MySQL case handling can differ between operating systems; review query names against the schema.
- Empty reports: a fresh import contains no business data. Related customer, store, product, and order-detail records must exist before linked orders can be inserted.
- Password input is ordinary console input, and peppers are stored alongside hashes. This is preserved coursework rather than a production authentication design.

## Author

Chua Jia Sheng.
