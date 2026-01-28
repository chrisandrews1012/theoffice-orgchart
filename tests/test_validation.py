"""
Unit tests for employee validation utilities
"""
import pytest
from utilities.validation import EmployeeValidator


class TestEmployeeValidator:
    """Test cases for EmployeeValidator"""

    def test_validate_name_valid(self):
        """Test validation of valid names"""
        is_valid, error = EmployeeValidator.validate_name("Michael")
        assert is_valid is True
        assert error == ""

    def test_validate_name_with_hyphen(self):
        """Test validation of names with hyphens"""
        is_valid, error = EmployeeValidator.validate_name("Mary-Beth")
        assert is_valid is True
        assert error == ""

    def test_validate_name_with_space(self):
        """Test validation of names with spaces"""
        is_valid, error = EmployeeValidator.validate_name("Van Buren")
        assert is_valid is True
        assert error == ""

    def test_validate_name_empty(self):
        """Test validation of empty names"""
        is_valid, error = EmployeeValidator.validate_name("")
        assert is_valid is False
        assert "empty" in error.lower()

    def test_validate_name_whitespace_only(self):
        """Test validation of whitespace-only names"""
        is_valid, error = EmployeeValidator.validate_name("   ")
        assert is_valid is False
        assert "empty" in error.lower()

    def test_validate_name_invalid_characters(self):
        """Test validation of names with invalid characters"""
        is_valid, error = EmployeeValidator.validate_name("Michael123")
        assert is_valid is False
        assert "invalid" in error.lower()

    def test_validate_name_special_characters(self):
        """Test validation of names with special characters"""
        is_valid, error = EmployeeValidator.validate_name("Scott@#$")
        assert is_valid is False
        assert "invalid" in error.lower()

    def test_validate_position_valid(self):
        """Test validation of valid positions"""
        is_valid, error = EmployeeValidator.validate_position("Regional Manager")
        assert is_valid is True
        assert error == ""

    def test_validate_position_with_numbers(self):
        """Test validation of positions with numbers"""
        is_valid, error = EmployeeValidator.validate_position("Sales Rep 2")
        assert is_valid is True
        assert error == ""

    def test_validate_position_with_ampersand(self):
        """Test validation of positions with ampersands"""
        is_valid, error = EmployeeValidator.validate_position("HR & Recruitment")
        assert is_valid is True
        assert error == ""

    def test_validate_position_empty(self):
        """Test validation of empty positions"""
        is_valid, error = EmployeeValidator.validate_position("")
        assert is_valid is False
        assert "empty" in error.lower()

    def test_validate_position_invalid_characters(self):
        """Test validation of positions with invalid characters"""
        is_valid, error = EmployeeValidator.validate_position("Manager@#$%")
        assert is_valid is False
        assert "invalid" in error.lower()

    def test_validate_employee_data_valid(self, sample_employee_data):
        """Test validation of complete valid employee data"""
        is_valid, error = EmployeeValidator.validate_employee_data(
            sample_employee_data['first_name'],
            sample_employee_data['last_name'],
            sample_employee_data['position']
        )
        assert is_valid is True
        assert error == ""

    def test_validate_employee_data_invalid_name(self):
        """Test validation of employee data with invalid name"""
        is_valid, error = EmployeeValidator.validate_employee_data(
            "Michael123",
            "Scott",
            "Regional Manager"
        )
        assert is_valid is False
        assert "Name" in error

    def test_validate_employee_data_invalid_position(self):
        """Test validation of employee data with invalid position"""
        is_valid, error = EmployeeValidator.validate_employee_data(
            "Michael",
            "Scott",
            ""
        )
        assert is_valid is False
        assert "Position" in error