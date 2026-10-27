import base64
import os
from random import choice

import bcrypt
import mysql.connector


# Function to create a secure connection to the database
def create_connection():
    try:
        connection = mysql.connector.connect(
            host=os.environ.get("DIGITALHUB_DB_HOST", "localhost"),
            user=os.environ.get("DIGITALHUB_DB_USER", "root"),
            password=os.environ.get("DIGITALHUB_DB_PASSWORD", ""),
            database=os.environ.get("DIGITALHUB_DB_NAME", "digitalhub")
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None


def register_user(username, password):
    # Generate a random pepper (16 bytes) and encode it as a base64 string
    pepper = base64.urlsafe_b64encode(os.urandom(16)).decode('utf-8')

    # Combine password and pepper
    combined_password = password.encode() + pepper.encode()

    # Hash the combined password using bcrypt
    hashed_password = bcrypt.hashpw(combined_password, bcrypt.gensalt())

    # Store the username, hashed_password, and pepper in the database
    query = "INSERT INTO users (username, hashed_password, pepper) VALUES (%s, %s, %s)"
    values = (username, hashed_password.decode('utf-8'), pepper)

    connection = create_connection()
    if not connection:
        print("\nError: Unable to connect to the database.")
        return

    try:
        cursor = connection.cursor()
        cursor.execute(query, values)
        connection.commit()
        print("User registered successfully!")
    except Exception as e:
        print(f"Error during registration: {e}")
    finally:
        connection.close()


def authenticate_user(username, password):
    query = "SELECT hashed_password, pepper FROM users WHERE username = %s"

    connection = create_connection()
    if not connection:
        print("\nError: Unable to connect to the database.")
        return False

    try:
        cursor = connection.cursor()
        cursor.execute(query, (username,))
        result = cursor.fetchone()

        if result:
            stored_hashed_password, stored_pepper = result

            # Ensure pepper is treated as a string and concatenate with the provided password
            combined_password = password + stored_pepper

            # Verify the password (bcrypt expects the password to be hashed before comparison)
            if bcrypt.checkpw(combined_password.encode(), stored_hashed_password.encode()):
                print("\nAuthentication successful!")
                return True
            else:
                print("\nInvalid password.")
        else:
            print("\nUsername not found.")

    except Exception as e:
        print(f"Error during authentication: {e}")
    finally:
        connection.close()

    return False



# Read records function modified to allow staff to choose number of records
def read_records(table):
    while True:
        print('\n-' + '-' * 29)
        print(f"Choose how many records to display for {table}:")
        print('-' * 30)
        print("1. Show all records\n2. Show limited records\n3. Back")
        print('-' * 30)
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            # Show all records (implement fetching all records from the database)
            records = fetch_records(table)
            display_records(table, records)
        elif choice == "2":
            limit = input("Enter the number of records to display: ").strip()
            try:
                limit = int(limit)
                records = fetch_records(table, limit)  # Implement fetching limited records
                display_records(table, records)
                break
            except ValueError:
                print("\nInvalid input. Please enter a valid number.")
        elif choice == "3":
            break
        else:
            print("\nInvalid choice.")


# Fetch records from the database, with optional limit
def fetch_records(table, limit=None):
    connection = create_connection()
    if not connection:
        return []

    query = f"SELECT * FROM {table}"
    if limit:
        query += f" LIMIT {limit}"

    try:
        cursor = connection.cursor()
        cursor.execute(query)
        records = cursor.fetchall()
        connection.close()
        return records
    except mysql.connector.Error as err:
        print(f"\nError fetching records: {err}")
        connection.close()
        return []


# Display records in a readable format
def display_records(table, records):
    print("\n" + "-" * 99)
    print(f"Records in {table}:")

    headers = {
        "Stores": ["Stores_ID", "Stores_Country", "Stores_State", "Stores_Square_Meters", "Stores_Open_Date"],
        "Customers": ["Customers_ID", "Customers_Name", "Customers_Gender", "Customers_City", "Customers_State_Code",
                      "Customers_State", "Customers_Zip_Code", "Customers_Country", "Customers_Continent",
                      "Customers_Birthday"],
        "Products": ["Products_ID", "Product_Name", "Product_Brand", "Product_Color", "Product_Unit_Cost",
                     "Product_Unit_Price", "Product_Category", "Product_Subcategory"],
        "Orders": ["Orders_ID", "Order_Details_ID", "Order_Date", "Delivery_Date", "Customers_ID", "Stores_ID",
                   "Product_ID"],
        "Order_Details": ["Order_Details_ID", "Order_Number", "Line_Item", "Purchased_Quantity"]
    }

    table_headers = headers.get(table, [])
    col_widths = [len(header) for header in table_headers]

    for record in records:
        for i, value in enumerate(record):
            col_widths[i] = max(col_widths[i], len(str(value)))

    print("  |".join([header.ljust(col_widths[i]) for i, header in enumerate(table_headers)]))
    print('-' * 100)

    for record in records:
        print("  |".join([str(value).ljust(col_widths[i]) for i, value in enumerate(record)]))
    print('-' * 100)


# Choose table to read
def choose_table():
    while True:
        print('\n-' + '-' * 29)
        print(f"{'Choose a table to read data':>28}")
        print('-' * 30)
        print("1. Stores")
        print("2. Customers")
        print("3. Products")
        print("4. Orders")
        print("5. Order_Details")
        print("6. Back")
        print('-' * 30)
        table_choice = input("Enter the number corresponding to the table: ").strip()

        if table_choice == "1":
            return "Stores"
        elif table_choice == "2":
            return "Customers"
        elif table_choice == "3":
            return "Products"
        elif table_choice == "4":
            return "Orders"
        elif table_choice == "5":
            return "Order_Details"
        elif table_choice == "6":
            return None
        else:
            print('\nInvalid choice')


def create_record(table):
    print('\n' + '-' * 30)
    print(f"Create a new record for {table}")
    print('-' * 30)

    connection = create_connection()
    if not connection:
        print("\nError: Unable to connect to the database.")
        return

    try:
        cursor = connection.cursor()
        inputs = {}
        if table == "Stores":
            inputs = {
                "Stores_Country": input("Enter Stores Country: ").strip(),
                "Stores_State": input("Enter Stores State: ").strip(),
                "Stores_Square_Meters": input("Enter Stores Square Meters: ").strip(),
                "Stores_Open_Date": input("Enter Stores Open Date (YYYY-MM-DD): ").strip(),
            }
        elif table == "Orders":
            inputs = {
                "Order_Details_ID": input("Enter Order Details ID: ").strip(),
                "Order_Date": input("Enter Order Date (YYYY-MM-DD): ").strip(),
                "Delivery_Date": input("Enter Delivery Date (YYYY-MM-DD): ").strip(),
                "Customers_ID": input("Enter Customer ID: ").strip(),
                "Stores_ID": input("Enter Store ID: ").strip(),
                "Product_ID": input("Enter Product ID: ").strip(),
            }
        elif table == "Order_Details":
            inputs = {
                "Order_Number": input("Enter Order Number: ").strip(),
                "Line_Item": input("Enter Line Item: ").strip(),
                "Purchased_Quantity": input("Enter Purchased Quantity: ").strip(),
            }
        elif table == "Customers":
            inputs = {
                "Customers_Name": input("Enter Customer Name: ").strip(),
                "Customers_Gender": input("Enter Customer Gender: ").strip(),
                "Customers_City": input("Enter Customer City: ").strip(),
                "Customers_State_Code": input("Enter Customer State Code: ").strip(),
                "Customers_State": input("Enter Customer State: ").strip(),
                "Customers_Zip_Code": input("Enter Customer Zip Code: ").strip(),
                "Customers_Country": input("Enter Customer Country: ").strip(),
                "Customers_Continent": input("Enter Customer Continent: ").strip(),
                "Customers_Birthday": input("Enter Customer Birthday (YYYY-MM-DD): ").strip(),
            }
        elif table == "Products":
            inputs = {
                "Product_Name": input("Enter Product Name: ").strip(),
                "Product_Brand": input("Enter Product Brand: ").strip(),
                "Product_Color": input("Enter Product Color: ").strip(),
                "Product_Unit_Cost": input("Enter Product Unit Cost: ").strip(),
                "Product_Unit_Price": input("Enter Product Unit Price: ").strip(),
                "Product_Category": input("Enter Product Category: ").strip(),
                "Product_Subcategory": input("Enter Product Subcategory: ").strip(),
            }
        # Check for empty values
        null_fields = [key for key, value in inputs.items() if value == ""]
        if null_fields:
            print("\nYou left the following fields blank, which will be set to NULL:")
            for field in null_fields:
                print(f" - {field}")

            print("\n1. Proceed with NULL values")
            print("2. Re-enter inputs")
            print("3. Return to Main Menu")
            while True:
                confirm = input("\nEnter your choice: ").strip()
                if confirm == "1":
                    for key in null_fields:
                        inputs[key] = None
                    break
                elif confirm == "2":
                    create_record(table)
                elif confirm == "3":
                    display_main_menu(1)
                else:
                    print("Invalid choice. Please enter 1, 2, or 3.")

        # Build and execute the insert query
        columns = ", ".join(inputs.keys())
        placeholders = ", ".join(["%s"] * len(inputs))
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        cursor.execute(query, tuple(inputs.values()))
        connection.commit()

        # Fetch the newly added record using LAST_INSERT_ID()
        last_id_query = f"SELECT * FROM {table} WHERE {table}_ID = LAST_INSERT_ID()"
        cursor.execute(last_id_query)
        new_record = cursor.fetchone()

        # Display the newly added record
        if new_record:
            display_records(table, [new_record])
        else:
            print("\nUnable to fetch the newly added record.")



    except mysql.connector.Error as err:
        print(f"\nError during CREATE operation: {err}")
        while True:
            print('\n' + '-' * 30)
            print("1. Re-enter your input \n2. Return to Main Menu")
            print('-' * 30)
            try:
                x = int(input("Enter your choice: ").strip())
                if x == 1:
                    create_record(table)
                elif x == 2:
                    return
                else:
                    print("Invalid choice. Please enter 1 or 2.")
            except ValueError:
                print("Invalid input. Please enter 1 or 2.")
    finally:
        connection.close()


def update_record(table):
    while True:
        print('\n-' + '-' * 29)

        # Initialize variables for the update operation
        updates = []
        values = []

        if table == "Order_Details":
            Order_Details_ID = input("Enter Order Details ID to update: ")
            Order_Number = input("Enter new Order Number (leave blank to skip): ")
            Line_Item = input("Enter new Line Item (leave blank to skip): ")
            Purchased_Quantity = input("Enter new Purchased Quantity (leave blank to skip): ")
            updates = []
            values = []
            if Order_Number:
                updates.append("Order_Number = %s")
                values.append(Order_Number)
            if Line_Item:
                updates.append("Line_Item = %s")
                values.append(Line_Item)
            if Purchased_Quantity:
                updates.append("Purchased_Quantity = %s")
                values.append(Purchased_Quantity)
            if Order_Details_ID != 0 or Order_Details_ID == "":
                updates.append("Order_Details_ID = %s")
                values.append(Order_Details_ID)
            else:
                print("Enter a Order_Details_ID")
                return

            query = f"UPDATE {table} SET {', '.join(updates)} WHERE Order_Details_ID = %s"
            values.append(Order_Details_ID)

        elif table == "Customers":
            Customers_ID = input("Enter Customer ID to update: ")
            Customers_Name = input("Enter new Customer Name (leave blank to skip): ")
            Customers_Gender = input("Enter new Customer Gender (leave blank to skip): ")
            Customers_City = input("Enter new Customer City (leave blank to skip): ")
            Customers_State_Code = input("Enter new Customer State Code (leave blank to skip): ")
            Customers_State = input("Enter new Customer State (leave blank to skip): ")
            Customers_Zip_Code = input("Enter new Customer Zip Code (leave blank to skip): ")
            Customers_Country = input("Enter new Customer Country (leave blank to skip): ")
            Customers_Continent = input("Enter new Customer Continent (leave blank to skip): ")
            Customers_Birthday = input("Enter new Customer Birthday (YYYY-MM-DD) (leave blank to skip): ")

            updates = []
            values = []
            if Customers_Name:
                updates.append("Customers_Name = %s")
                values.append(Customers_Name)
            if Customers_Gender:
                updates.append("Customers_Gender = %s")
                values.append(Customers_Gender)
            if Customers_City:
                updates.append("Customers_City = %s")
                values.append(Customers_City)
            if Customers_State_Code:
                updates.append("Customers_State_Code = %s")
                values.append(Customers_State_Code)
            if Customers_State:
                updates.append("Customers_State = %s")
                values.append(Customers_State)
            if Customers_Zip_Code:
                updates.append("Customers_Zip_Code = %s")
                values.append(Customers_Zip_Code)
            if Customers_Country:
                updates.append("Customers_Country = %s")
                values.append(Customers_Country)
            if Customers_Continent:
                updates.append("Customers_Continent = %s")
                values.append(Customers_Continent)
            if Customers_Birthday:
                updates.append("Customers_Birthday = %s")
                values.append(Customers_Birthday)
            if Customers_ID != 0 or Customers_ID=="":
                updates.append("Customers_ID = %s")
                values.append(Customers_ID)
            else:
                print("Enter a Customers_ID")
                return

            query = f"UPDATE {table} SET {', '.join(updates)} WHERE Customers_ID = %s"
            values.append(Customers_ID)

        elif table == "Products":
            Products_ID = input("Enter Product ID to update: ")
            Product_Name = input("Enter new Product Name (leave blank to skip): ")
            Product_Brand = input("Enter new Product Brand (leave blank to skip): ")
            Product_Color = input("Enter new Product Color (leave blank to skip): ")
            Product_Unit_Cost = input("Enter new Product Unit Cost (leave blank to skip): ")
            Product_Unit_Price = input("Enter new Product Unit Price (leave blank to skip): ")
            Product_Category = input("Enter new Product Category (leave blank to skip): ")
            Product_Subcategory = input("Enter new Product Subcategory (leave blank to skip): ")

            updates = []
            values = []
            if Product_Name:
                updates.append("Product_Name = %s")
                values.append(Product_Name)
            if Product_Brand:
                updates.append("Product_Brand = %s")
                values.append(Product_Brand)
            if Product_Color:
                updates.append("Product_Color = %s")
                values.append(Product_Color)
            if Product_Unit_Cost:
                updates.append("Product_Unit_Cost = %s")
                values.append(Product_Unit_Cost)
            if Product_Unit_Price:
                updates.append("Product_Unit_Price = %s")
                values.append(Product_Unit_Price)
            if Product_Category:
                updates.append("Product_Category = %s")
                values.append(Product_Category)
            if Product_Subcategory:
                updates.append("Product_Subcategory = %s")
                values.append(Product_Subcategory)
            if Products_ID != 0 or Products_ID == "":
                updates.append("Products_ID = %s")
                values.append(Products_ID)
            else:
                print("Enter a Products_ID")
                return

            query = f"UPDATE {table} SET {', '.join(updates)} WHERE Products_ID = %s"
            values.append(Products_ID)

        elif table == "Orders":
            Orders_ID = input("Enter Order ID to update: ")
            Order_Date = input("Enter new Order Date (YYYY-MM-DD) (leave blank to skip): ")
            Delivery_Date = input("Enter new Delivery Date (YYYY-MM-DD) (leave blank to skip): ")

            updates = []
            values = []
            if Order_Date:
                updates.append("Order_Date = %s")
                values.append(Order_Date)
            if Delivery_Date:
                updates.append("Delivery_Date = %s")
                values.append(Delivery_Date)
            if Orders_ID != 0 or Orders_ID == "":
                updates.append("Orders_ID = %s")
                values.append(Orders_ID)
            else:
                print("Enter a Orders_ID")
                return

            query = f"UPDATE {table} SET {', '.join(updates)} WHERE Orders_ID = %s"
            values.append(Orders_ID)

        elif table == "Stores":
            Stores_ID = input("Enter Store ID to update: ")
            Stores_Country = input("Enter new Stores Country (leave blank to skip): ")
            Stores_State = input("Enter new Stores State (leave blank to skip): ")
            Stores_Square_Meters = input("Enter new Stores Square Meter   (leave blank to skip): ")
            Stores_Open_Date = input("Enter new Stores Open Date (YYYY-MM-DD) (leave blank to skip): ")

            updates = []
            values = []
            if Stores_Country:
                updates.append("Stores_Country = %s")
                values.append(Stores_Country)
            if Stores_State:
                updates.append("Stores_State = %s")
                values.append(Stores_State)
            if Stores_Square_Meters:
                updates.append("Stores_Square_Meters = %s")
                values.append(Stores_Square_Meters)
            if Stores_ID != 0 or Stores_ID == "":
                updates.append("Stores_ID = %s")
                values.append(Stores_ID)
            else:
                print("Enter a Stores_ID")
                return
            if Stores_Open_Date:
                updates.append("Stores_Open_Date = %s")
                values.append(Stores_Open_Date)

            query = f"UPDATE {table} SET {', '.join(updates)} WHERE Stores_ID = %s"
            values.append(Stores_ID)
        # Connect to the database
        connection = create_connection()
        if not connection:
            print("\nError: Unable to connect to the database.")
            return

        try:
            cursor = connection.cursor()
            cursor.execute(query, values)
            connection.commit()
            print(f"\nRecord updated in {table}.")

            # Fetch and display the updated record
            select_query = f"SELECT * FROM {table} WHERE {table}_ID = %s"
            cursor.execute(select_query, (values[-1],))
            updated_record = cursor.fetchone()

            if updated_record:
                print("\nUpdated Record:")
                display_records(table, [updated_record])
            else:
                print("\nUnable to fetch the updated record.")

        except mysql.connector.Error as err:
            print(f"\nError during UPDATE operation: {err}")
            while True:
                print('\n' + '-' * 30)
                print("1. Re-enter your input \n2. Return to Main Menu")
                print('-' * 30)
                try:
                    x = int(input("Enter your choice: ").strip())
                    if x == 1:
                        update_record(table)
                    elif x == 2:
                        return
                    else:
                        print("Invalid choice. Please enter 1 or 2.")
                except ValueError:
                    print("Invalid input. Please enter 1 or 2.")
        finally:
            connection.close()
        return


# Delete record
def delete_record(table):
    while True:
        print('\n-' + '-' * 29)
        record_id = input(
            f"Enter the ID of the record you want to delete from {table} (Type * to go back to main menu): ")
        if record_id == "*":
            return
        query = f"DELETE FROM {table} WHERE {table}_ID = %s"
        values = (record_id,)

        connection = create_connection()
        if not connection:
            print("\nError: Unable to connect to the database.")
            continue

        try:
            cursor = connection.cursor()
            cursor.execute(query, values)
            connection.commit()
            print(f"\nRecord {record_id} deleted from {table}.")
        except mysql.connector.Error as err:
            print(f"\nError during DELETE operation: {err}")
            while True:
                print('\n' + '-' * 30)
                print("1. Re-enter your input \n2. Return to Main Menu")
                print('-' * 30)
                try:
                    x = int(input("Enter your choice: ").strip())
                    if x == 1:
                        update_record(table)
                    elif x == 2:
                        display_main_menu(1)
                    else:
                        print("Invalid choice. Please enter 1 or 2.")
                except ValueError:
                    print("Invalid input. Please enter 1 or 2.")
        finally:
            connection.close()
        return


def display_report(country=None, start_date=None, end_date=None, store_id=None, product_category=None):
    connection = create_connection()
    if not connection:
        return

    # Base query
    query = """
              SELECT 
                  Orders.Orders_ID,
                  Products.Product_Name,
                  Products.Product_Unit_Price,
                  Order_Details.Purchased_Quantity,
                  (Products.Product_Unit_Price * Order_Details.Purchased_Quantity) AS Sales_Report,
                  Stores.Stores_Country,
                  Orders.Order_Date
              FROM Orders
              INNER JOIN Order_Details ON Orders.Order_Details_ID = Order_Details.Order_Details_ID
              INNER JOIN Products ON Orders.Product_ID = Products.Products_ID
              INNER JOIN Customers ON Orders.Customers_ID = Customers.Customers_ID
              INNER JOIN Stores ON Orders.Stores_ID = Stores.Stores_ID
      """
    params = []
    filters = []

    # Add filters based on user input
    if country:
        filters.append("Stores.Stores_Country = %s")
        params.append(country)
    if start_date and end_date:
        filters.append("Orders.Order_Date BETWEEN %s AND %s")
        params.extend([start_date, end_date])
    if store_id:
        filters.append("Stores.Stores_ID = %s")
        params.append(store_id)
    if product_category:
        filters.append("Products.Product_Category = %s")
        params.append(product_category)

    # Append filters to the query if any
    if filters:
        query += " WHERE " + " AND ".join(filters)

    try:
        cursor = connection.cursor()
        cursor.execute(query, params)
        results = cursor.fetchall()

        # Let the user decide how many rows to print
        while True:
            print('\n-' + '-' * 29)
            print("Choose how many rows to display:")
            print('-' * 30)
            print("1. Print all rows")
            print("2. Print limited rows")
            print("3. Exit")
            print('-' * 30)
            choice = input("Enter your choice: ").strip()

            if choice == "1":
                display_report_rows(results)  # Print all rows
                break
            elif choice == "2":
                try:
                    limit = int(input("Enter the number of rows to display: ").strip())
                    display_report_rows(results[:limit])  # Print the specified number of rows
                    break
                except ValueError:
                    print("\nInvalid input. Please enter a valid number.")
            elif choice == "3":
                return
            else:
                print("\nInvalid choice. Please select 1 or 2.")
    except mysql.connector.Error as err:
        print(f"\nError fetching the report: {err}")
    finally:
        connection.close()


# Helper function to display rows
def display_report_rows(rows):
    if not rows:
        print("\nNo records found.")
        return

    headers = ["Order ID", "Product Name", "Unit Price", "Quantity", "Sales Report", "Customer Name", "Store Country",
               "Order Date"]
    col_widths = [len(header) for header in headers]

    for row in rows:
        for i, value in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(value)))

    print("\n" + "-" * (sum(col_widths) + 3 * (len(headers) - 1)))
    print(" | ".join(header.ljust(col_widths[i]) for i, header in enumerate(headers)))
    print("-" * (sum(col_widths) + 3 * (len(headers) - 1)))

    for row in rows:
        print(" | ".join(str(value).ljust(col_widths[i]) for i, value in enumerate(row)))

    print("\n" + "-" * (sum(col_widths) + 3 * (len(headers) - 1)))


def search_records(table):
    connection = create_connection()
    if not connection:
        print("\nError: Unable to connect to the database.")
        return

    try:
        cursor = connection.cursor()

        # Show column names to guide the user
        cursor.execute(f"SHOW COLUMNS FROM {table}")
        columns = cursor.fetchall()
        column_names = [col[0] for col in columns]

        print("\nAvailable columns for search:")
        for idx, column in enumerate(column_names, start=1):
            print(f"{idx}. {column}")

        # Let user select a column
        while True:
            try:
                column_choice = int(input("\nSelect a column by number: ").strip())
                if 1 <= column_choice <= len(column_names):
                    column = column_names[column_choice - 1]
                    break
                else:
                    print("Invalid choice. Please select a valid column number.")
            except ValueError:
                print("Invalid input. Please enter a number.")

        # Let user select an operator
        operators = ["LIKE", "=", ">", "<", "BETWEEN", "IN"]
        print("\nAvailable operators:")
        for idx, operator in enumerate(operators, start=1):
            print(f"{idx}. {operator}")

        while True:
            try:
                operator_choice = int(input("\nSelect an operator by number: ").strip())
                if 1 <= operator_choice <= len(operators):
                    operator = operators[operator_choice - 1]
                    break
                else:
                    print("Invalid choice. Please select a valid operator number.")
            except ValueError:
                print("Invalid input. Please enter a number.")

        # Get value(s) based on the chosen operator
        if operator == "LIKE":
            value = input(f"Enter value for {operator} (e.g., '%keyword%'): ").strip()
            query = f"SELECT * FROM {table} WHERE {column} LIKE %s"
            params = [value]

        elif operator in ["=", ">", "<"]:
            value = input(f"Enter value for {operator}: ").strip()
            query = f"SELECT * FROM {table} WHERE {column} {operator} %s"
            params = [value]

        elif operator == "BETWEEN":
            value1 = input("Enter the starting value: ").strip()
            value2 = input("Enter the ending value: ").strip()
            query = f"SELECT * FROM {table} WHERE {column} BETWEEN %s AND %s"
            params = [value1, value2]

        elif operator == "IN":
            values = input("Enter values separated by commas (e.g., 'value1,value2,value3'): ").strip()
            value_list = [v.strip() for v in values.split(",")]
            placeholders = ",".join(["%s"] * len(value_list))
            query = f"SELECT * FROM {table} WHERE {column} IN ({placeholders})"
            params = value_list

        # Execute the search query
        cursor.execute(query, params)
        results = cursor.fetchall()

        # Display the search results
        if results:
            display_records(table, results)
        else:
            print("\nNo matching records found.")

    except mysql.connector.Error as err:
        print(f"\nError during search operation: {err}")

    finally:
        connection.close()


def display_login_menu():
    print('\n-' + '-' * 29)
    print(f"{'Login':>17}")
    print('-' * 30)
    print("1. Register")
    print("2. Login")
    print("3. Exit")
    print('-' * 30)


# Helper function: Privilege Menu
def display_privilege_menu():
    print('\n-' + '-' * 29)
    print(f"{'Choose your privilege':>25}")
    print('-' * 30)
    print("1. Admin")
    print("2. Staff")
    print("3. Logout")
    print('-' * 30)


# Helper function: Main Menu
def display_main_menu(role):
    print('\n-' + '-' * 29)
    print(f"{'Main Menu':>20}")
    print('-' * 30)
    if role == "1":  # Admin options
        print("1. Read Records")
        print("2. Create Records")
        print("3. Update Records")
        print("4. Delete Records")
        print("5. Display Report")
        print("6. Search")
        print("7. Logout")
    elif role == "2":  # Staff options
        print("1. Read records")
        print("2. Search")
        print("3. Logout")
    print('-' * 30)


# Handle Admin Actions
def handle_admin_actions():
    while True:
        display_main_menu("1")
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            current_table = choose_table()
            if current_table:
                read_records(current_table)
        elif choice == "2":
            current_table = choose_table()
            if current_table:
                create_record(current_table)
        elif choice == "3":
            current_table = choose_table()
            if current_table:
                update_record(current_table)
        elif choice == "4":
            current_table = choose_table()
            if current_table:
                delete_record(current_table)
        elif choice == "5":
            print("\nDisplay Report - Apply Filters (Leave blank for no filter):")
            country = input("Enter Store Country (optional): ").strip()
            start_date = input("Enter Start Date (YYYY-MM-DD, optional): ").strip()
            end_date = input("Enter End Date (YYYY-MM-DD, optional): ").strip()
            store_id = input("Enter Store ID (optional): ").strip()
            product_category = input("Enter Product Category (optional): ").strip()
            display_report(
                country=country or None,
                start_date=start_date or None,
                end_date=end_date or None,
                store_id=store_id or None,
                product_category=product_category or None
            )
        elif choice == "6":
            current_table = choose_table()
            if current_table:
                search_records(current_table)
        elif choice == "7":
            print("Logging Out...")
            exit()
        else:
            print("\nInvalid choice. Please try again.")


# Handle Staff Actions
def handle_staff_actions():
    while True:
        display_main_menu("2")
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            current_table = choose_table()
            if current_table:
                read_records(current_table)
        elif choice == "2":
            current_table = choose_table()
            if current_table:
                search_records(current_table)
        elif choice == "3":
            print("Logging Out...")
            exit()
        else:
            print("\nInvalid choice. Please try again.")


# Handle Login
def handle_login():
    username = input("Enter your username: ").strip()
    password = input("Enter your password: ").strip()
    if authenticate_user(username, password):
        while True:
            display_privilege_menu()
            role = input("Enter your role: ").strip()
            if role == "1":
                confirm = input(
                    "Admins have full control over the database (Create, Update, Delete, Read). Proceed as Admin? (y/n): ").strip().lower()
                if confirm == 'y':
                    handle_admin_actions()
            elif role == "2":
                handle_staff_actions()
            elif role == "3":
                print("Logging Out...")
                return
            else:
                print("\nInvalid choice. Please enter 1 for Admin or 2 for Staff.")


# Handle Registration
def handle_registration():
    username = input("Enter your username: ").strip()
    password = input("Enter your password: ").strip()
    confirm_password = input("Re-enter your password: ").strip()
    if username == "" or password == "":
        print("\nUsername or password cannot be blank. Please try again")
    elif password == confirm_password:
        register_user(username, password)
    else:
        print("\nPasswords do not match. Please try again.")


# Main Function
def main():
    while True:
        display_login_menu()
        choice = input("Enter your choice: ").strip()
        if choice == "3":
            print("\nExiting system. Goodbye!")
            exit()
        elif choice == "1":
            handle_registration()
        elif choice == "2":
            handle_login()
        else:
            print("\nInvalid choice. Please try again.")


# Run the program
if __name__ == "__main__":
    main()