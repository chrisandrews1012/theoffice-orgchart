from pydantic import BaseModel
from sqlalchemy import Column, VARCHAR, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from enum import Enum   

Base = declarative_base()

class DepartmentType(Enum):
    SALES = "Sales"
    ACCOUNTING = "Accounting"
    CUSTOMER_SERVICE = "Customer Service"
    HUMAN_RESOURCES = "Human Resources"
    WAREHOUSE = "Warehouse"
    MANAGEMENT = "Management"
    FINANCE = "Finance"
    GROWTH = "Growth"
    
class SQLExecutive(Base):
    __tablename__ = "executive"
    emp_id = Column(VARCHAR, primary_key=True)
    first_name = Column(VARCHAR)
    last_name = Column(VARCHAR)
    position = Column(VARCHAR)
    department = Column(VARCHAR)
    supervisor_id = Column(VARCHAR, default=None)
    
class SQLManager(Base):
    __tablename__ = "manager"
    emp_id = Column(VARCHAR, primary_key=True)
    first_name = Column(VARCHAR)
    last_name = Column(VARCHAR)
    position = Column(VARCHAR)
    department = Column(VARCHAR)
    supervisor_id = Column(VARCHAR, ForeignKey("executive.emp_id"), default=None)
    
class SQLEmployee(Base):
    __tablename__ = "employee"
    emp_id = Column(VARCHAR, primary_key=True)
    first_name = Column(VARCHAR)
    last_name = Column(VARCHAR)
    position = Column(VARCHAR)
    department = Column(VARCHAR)
    supervisor_id = Column(VARCHAR, ForeignKey("manager.emp_id"), default=None)
    
class Employee(BaseModel):
    emp_id: str | None = None
    first_name: str
    last_name: str
    position: str
    department: str
    supervisor_id: str|None = None
