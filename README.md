# DigitalHub Retail Database Manager

A command-line retail database application for customers, stores, products and orders.

**Technology:** Python and MySQL.

## Run or inspect

Use Python and a compatible MySQL server. Start with an empty `digitalhub` database and import `database/schema.sql`, for example in MySQL Workbench. The schema intentionally contains no original customer records or user credentials.

```sh
python -m pip install -r requirements.txt
```

Set the environment variables listed in `.env.example` in your terminal. The program uses the process environment; it does not automatically load `.env` files. For example in PowerShell:

```powershell
$env:DIGITALHUB_DB_HOST = "localhost"
$env:DIGITALHUB_DB_USER = "root"
$env:DIGITALHUB_DB_PASSWORD = "YOUR_LOCAL_DATABASE_PASSWORD"
$env:DIGITALHUB_DB_NAME = "digitalhub"
python src/main.py
```

Register a new user through the application. Populate an empty database using your own test records. Original schema and application behaviour are otherwise retained. MySQL table-name case handling can differ across operating systems; the original queries use mixed case. This is coursework, not a reviewed production access-control system.

## Repository preparation

Source and required assets were organised from existing coursework. Build outputs and IDE state are excluded. Original reports, slides and course handouts remain in the separate full backup; they are not bundled for public upload. Real credentials and original database records are not included. See the collection `UPLOAD_GUIDE.md` for upload steps and preparation notes.

## Validation status

The preparation checked file paths, Python syntax where applicable, structured files, credential removal and package integrity. Windows desktop apps, Flutter apps, hardware and online services have not been built or run in this environment.
