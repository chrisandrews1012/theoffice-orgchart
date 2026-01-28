import regex as re
from typing import Tuple


class EmployeeValidator:
    """Centralized validation for employee data"""

    NAME_PATTERN = r"[^A-Za-z,\s-]"
    POSITION_PATTERN = r"[^A-Za-z\d\s,&-]"

    @staticmethod
    def validate_name(value: str) -> Tuple[bool, str]:
        """
        Validate employee name.

        :param value: Name to validate
        :type value: str
        :return: Tuple of (is_valid, error_message)
        :rtype: Tuple[bool, str]
        """
        if not value or not value.strip():
            return False, "Name cannot be empty"
        if re.search(EmployeeValidator.NAME_PATTERN, value):
            return False, "Name contains invalid characters"
        return True, ""

    @staticmethod
    def validate_position(value: str) -> Tuple[bool, str]:
        """
        Validate employee position.

        :param value: Position to validate
        :type value: str
        :return: Tuple of (is_valid, error_message)
        :rtype: Tuple[bool, str]
        """
        if not value or not value.strip():
            return False, "Position cannot be empty"
        if re.search(EmployeeValidator.POSITION_PATTERN, value):
            return False, "Position contains invalid characters"
        return True, ""

    @staticmethod
    def validate_employee_data(first_name: str, last_name: str, position: str) -> Tuple[bool, str]:
        """
        Validate all employee fields at once.

        :param first_name: Employee first name
        :type first_name: str
        :param last_name: Employee last name
        :type last_name: str
        :param position: Employee position
        :type position: str
        :return: Tuple of (is_valid, error_message)
        :rtype: Tuple[bool, str]
        """
        is_valid, error = EmployeeValidator.validate_name(first_name + last_name)
        if not is_valid:
            return False, f"Name: {error}"

        is_valid, error = EmployeeValidator.validate_position(position)
        if not is_valid:
            return False, f"Position: {error}"

        return True, ""
