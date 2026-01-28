from dotenv import load_dotenv
from handler.cursor import Connection
from models.orgchart import SQLEmployee, SQLManager, SQLExecutive
from sqlalchemy.orm import Session
from utilities.id_generator import generate_employee_id
from collections import defaultdict
import sys

def clear_database(client: Connection):
    """Clear all employees from database in proper order (respecting foreign keys)"""
    with Session(client.connection) as session:
        print("Clearing employees...")
        session.query(SQLEmployee).delete()

        print("Clearing managers...")
        session.query(SQLManager).delete()

        print("Clearing executives...")
        session.query(SQLExecutive).delete()

        session.commit()
        print("Database cleared successfully!")


def run_build(client: Connection):
    """Populate database with employee data using bulk insert for optimal performance"""
    # Employees to insert
    employees = [
        # Executives
        {'type': SQLExecutive, 'id': 'DavidWallace', 'first': 'David', 'last': 'Wallace', 'position': 'CFO', 'dept': 'Finance', 'supervisor': None},
        {'type': SQLExecutive, 'id': 'JanLevinson', 'first': 'Jan', 'last': 'Levinson', 'position': 'VP of Sales', 'dept': 'Growth', 'supervisor': None},
        # Managers
        {'type': SQLManager, 'id': 'MichaelScott', 'first': 'Michael', 'last': 'Scott', 'position': 'Regional Manager', 'dept': 'Sales', 'supervisor': 'JanLevinson'},
        # Employees
        {'type': SQLEmployee, 'id': 'JimHalpert', 'first': 'Jim', 'last': 'Halpert', 'position': 'Sales Representative', 'dept': 'Sales', 'supervisor': 'MichaelScott'},
        {'type': SQLEmployee, 'id': 'DwightSchrute', 'first': 'Dwight', 'last': 'Schrute', 'position': 'Sales Representative', 'dept': 'Sales', 'supervisor': 'MichaelScott'},
        {'type': SQLEmployee, 'id': 'PamBeesly', 'first': 'Pam', 'last': 'Beesly', 'position': 'Receptionist', 'dept': 'Admin', 'supervisor': 'MichaelScott'},
        {'type': SQLEmployee, 'id': 'KellyKapoor', 'first': 'Kelly', 'last': 'Kapoor', 'position': 'Customer Service Rep', 'dept': 'Customer Service', 'supervisor': 'MichaelScott'},
        {'type': SQLEmployee, 'id': 'AngelaMartin', 'first': 'Angela', 'last': 'Martin', 'position': 'Senior Accountant', 'dept': 'Finance', 'supervisor': 'MichaelScott'},
        {'type': SQLEmployee, 'id': 'OscarMartinez', 'first': 'Oscar', 'last': 'Martinez', 'position': 'Accountant', 'dept': 'Finance', 'supervisor': 'MichaelScott'},
        {'type': SQLEmployee, 'id': 'KevinMalone', 'first': 'Kevin', 'last': 'Malone', 'position': 'Accountant', 'dept': 'Finance', 'supervisor': 'MichaelScott'},
        {'type': SQLEmployee, 'id': 'CreedBratton', 'first': 'Creed', 'last': 'Bratton', 'position': 'Quality Assurance', 'dept': 'Operations', 'supervisor': 'MichaelScott'},
        {'type': SQLEmployee, 'id': 'MeredithPalmer', 'first': 'Meredith', 'last': 'Palmer', 'position': 'Supplier Relations', 'dept': 'Operations', 'supervisor': 'MichaelScott'},
        {'type': SQLEmployee, 'id': 'RyanHoward', 'first': 'Ryan', 'last': 'Howard', 'position': 'Temp', 'dept': 'Sales', 'supervisor': 'MichaelScott'},
        {'type': SQLEmployee, 'id': 'DarrylPhilbin', 'first': 'Darryl', 'last': 'Philbin', 'position': 'Warehouse Manager', 'dept': 'Warehouse', 'supervisor': 'MichaelScott'}
    ]

    # Build supervisor ID map and prepare insert data
    id_map = {}
    data_by_table = defaultdict(list)

    for emp in employees:
        emp_id = generate_employee_id(emp['first'], emp['last'])
        id_map[emp['id']] = emp_id

        data_by_table[emp['type']].append({
            'emp_id': emp_id,
            'first_name': emp['first'],
            'last_name': emp['last'],
            'position': emp['position'],
            'department': emp['dept'],
            'supervisor_id': id_map.get(emp['supervisor'])
        })

    # Bulk insert by table type
    with Session(client.connection) as session:
        for table, data in data_by_table.items():
            session.bulk_insert_mappings(table, data)
            print(f"Added {len(data)} {table.__name__}(s)")

        session.commit()

    print("Successfully initialized the DB")


if __name__ == "__main__":
    load_dotenv()
    client = Connection()

    command = sys.argv[1] if len(sys.argv) > 1 else "rebuild"

    if command == "clear":
        clear_database(client)
    elif command == "rebuild":
        clear_database(client)
        run_build(client)
    else:
        print(f"Unknown command: {command}")
        print("Usage: python build.py [clear|rebuild]")