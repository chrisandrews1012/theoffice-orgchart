from enum import Enum
from dataclasses import dataclass
from typing import Type, Optional
from models.orgchart import SQLExecutive, SQLManager, SQLEmployee


class EmployeeLevel(Enum):
    """Employee hierarchy levels"""
    EXECUTIVE = "Executive"
    MANAGER = "Manager"
    EMPLOYEE = "Regular Employee"


@dataclass
class EmployeeTypeConfig:
    """Configuration for each employee type"""
    display_name: str
    table_class: Type
    supervisor_table: Optional[Type]
    subordinate_table: Optional[Type]


# Single source of truth for employee type configurations
EMPLOYEE_TYPES = {
    EmployeeLevel.EXECUTIVE: EmployeeTypeConfig(
        display_name="Executive",
        table_class=SQLExecutive,
        supervisor_table=None,  # Executives have no supervisors
        subordinate_table=SQLManager  # Their subordinates are Managers
    ),
    EmployeeLevel.MANAGER: EmployeeTypeConfig(
        display_name="Manager",
        table_class=SQLManager,
        supervisor_table=SQLExecutive,  # Managers report to Executives
        subordinate_table=SQLEmployee  # Managers supervise Employees
    ),
    EmployeeLevel.EMPLOYEE: EmployeeTypeConfig(
        display_name="Regular Employee",
        table_class=SQLEmployee,
        supervisor_table=SQLManager,  # Employees report to Managers
        subordinate_table=None  # Employees have no subordinates
    )
}


def get_config_by_name(display_name: str) -> Optional[EmployeeTypeConfig]:
    """
    Get employee type config by display name (e.g., 'Manager')
    
    :param display_name: The display name of the employee type
    :type display_name: str
    :return: Corresponding EmployeeTypeConfig or None if not found
    :rtype: Optional[EmployeeTypeConfig]
    """
    for config in EMPLOYEE_TYPES.values():
        if config.display_name == display_name:
            return config
    return None


def get_config_by_table(table_class: Type) -> Optional[EmployeeTypeConfig]:
    """
    Get employee type config by table class (e.g., SQLManager)
    
    :param table_class: The table class of the employee type
    :type table_class: Type
    :return: Corresponding EmployeeTypeConfig or None if not found
    :rtype: Optional[EmployeeTypeConfig]
    """
    for config in EMPLOYEE_TYPES.values():
        if config.table_class == table_class:
            return config
    return None
