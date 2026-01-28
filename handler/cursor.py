import os
from utilities.validation import EmployeeValidator
from utilities.id_generator import generate_employee_id
from utilities.errors import handle_db_errors
from utilities.session_helper import get_session, get_readonly_session
from sqlalchemy import create_engine, insert, select, delete, exists, URL
from models.orgchart import SQLExecutive, SQLManager, SQLEmployee, Employee
from config.employee_types import get_config_by_table


class Connection:
    def __init__(self):
        try:
            self.db_conn_str = URL.create(drivername="postgresql+psycopg2",
                                     host=os.getenv("DB_HOST"),
                                     database=os.getenv("PG_DATABASE"),
                                     port=os.getenv("PG_PORT"),
                                     username=os.getenv("DB_USER"),
                                     password=os.getenv("DB_USER_PW"))
            self.connection = create_engine(self.db_conn_str)
       
        except Exception as e:
            print(f"Error creating DB connection engine: {repr(e)}")
    
    
    def get_db_conn_str(self):
        return self.db_conn_str
    
    
    @handle_db_errors("add employee", default_return=False)
    def addEmployee(self, person:Employee, table: SQLExecutive | SQLManager | SQLEmployee):
        # validate fields
        is_valid, error = EmployeeValidator.validate_employee_data(
            person.first_name, person.last_name, person.position
        )
        if not is_valid:
            print(f"Validation failed: {error}")
            return False

        # generate employee ID
        if not person.emp_id:
            person.emp_id = generate_employee_id(person.first_name, person.last_name)

        with get_session(self.connection) as session:
            # check for existing employee
            exist_stmt = select(exists().where(table.emp_id==person.emp_id))
            result = session.scalar(exist_stmt)

            if not result:
                # insert new employee
                insert_stmt = insert(table).values(person.model_dump(mode="json"))
                session.execute(insert_stmt)
        return True            

    @handle_db_errors("fetch employees", default_return=[])
    def fetchEmployee(self, table: SQLExecutive | SQLManager | SQLEmployee):
        with get_readonly_session(self.connection) as session:
            result = session.query(table).all()
        return result
            
            
    @handle_db_errors("update employee", default_return=False)
    def updateEmployee(self, updated_employee:Employee, table: SQLExecutive | SQLManager | SQLEmployee, emp_id:str) -> bool:
        with get_session(self.connection) as session:
            employee = session.query(table).filter_by(emp_id=emp_id).first()
            if not employee:
                return False

            update_data = updated_employee.model_dump(mode="json", exclude={'emp_id'})
            for field, value in update_data.items():
                setattr(employee, field, value)
            return True    
            
    @handle_db_errors("delete employee", default_return=False)
    def deleteEmployee(self, table: SQLExecutive | SQLManager | SQLEmployee, emp_id:str, reassign_to: str | None = None) -> bool:
        with get_session(self.connection) as session:
            employee = session.query(table).filter_by(emp_id=emp_id).first()
            if not employee:
                return False

            # handle reassignment logic
            if reassign_to:
                # Get configuration for this employee type
                config = get_config_by_table(table)

                if config and config.subordinate_table:
                    target_table = config.table_class
                    subordinate_table = config.subordinate_table

                    # validate reassignment target exists
                    target_exists = session.query(exists().where(target_table.emp_id == reassign_to)).scalar()
                    if not target_exists:
                        return False

                    # reassign subordinates
                    session.query(subordinate_table).filter(
                        subordinate_table.supervisor_id == emp_id
                    ).update(
                        {subordinate_table.supervisor_id: reassign_to},
                        synchronize_session=False
                    )

            # Delete employee - database automatically handles subordinates if reassign_to is None
            session.delete(employee)
            return True
