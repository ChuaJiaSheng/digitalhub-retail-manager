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

## Local setup

1. Start a compatible MySQL server and open `database/schema.sql` in MySQL Workbench or another SQL client. Execute it to create the empty `digitalhub` database and its tables.
2. From the repository root, install the Python dependencies:

   ```sh
   python -m pip install -r requirements.txt
   ```

3. Set the connection variables in the same terminal that launches the program. For PowerShell:

   ```powershell
   $env:DIGITALHUB_DB_HOST = "localhost"
   $env:DIGITALHUB_DB_USER = "YOUR_LOCAL_DATABASE_USER"
   $env:DIGITALHUB_DB_PASSWORD = "YOUR_LOCAL_DATABASE_PASSWORD"
   $env:DIGITALHUB_DB_NAME = "digitalhub"
   python src/main.py
   ```

4. Choose **Register**, create your own application account, then log in. Use synthetic records to explore the database features.

[.env.example](.env.example) documents the variable names. The script reads the process environment; merely copying that file to `.env` will not load it.

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

## Credits and verification

The original EGE311 project report identifies **Chua Jia Sheng**. Python syntax and the schema's source structure were inspected; a live MySQL import, database operations, and authentication flows have not been tested here. The original database export and report are not published in this repository.
