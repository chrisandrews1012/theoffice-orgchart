"""
Unit tests for employee ID generation utilities
"""
import pytest
from utilities.id_generator import generate_employee_id


class TestIDGenerator:
    """Test cases for generate_employee_id function"""

    def test_generate_employee_id_basic(self):
        """Test basic ID generation"""
        emp_id = generate_employee_id("Michael", "Scott")
        assert emp_id is not None
        assert len(emp_id) == 32  # MD5 hash length

    def test_generate_employee_id_consistency(self):
        """Test that same input generates same ID"""
        emp_id1 = generate_employee_id("Michael", "Scott")
        emp_id2 = generate_employee_id("Michael", "Scott")
        assert emp_id1 == emp_id2

    def test_generate_employee_id_uniqueness(self):
        """Test that different inputs generate different IDs"""
        emp_id1 = generate_employee_id("Michael", "Scott")
        emp_id2 = generate_employee_id("Dwight", "Schrute")
        assert emp_id1 != emp_id2

    def test_generate_employee_id_case_sensitive(self):
        """Test that ID generation is case-sensitive"""
        emp_id1 = generate_employee_id("Michael", "Scott")
        emp_id2 = generate_employee_id("michael", "scott")
        assert emp_id1 != emp_id2

    def test_generate_employee_id_with_spaces(self):
        """Test ID generation with names containing spaces"""
        emp_id = generate_employee_id("Jim ", " Halpert")
        assert emp_id is not None
        assert len(emp_id) == 32

    def test_generate_employee_id_special_characters(self):
        """Test ID generation with special characters"""
        emp_id = generate_employee_id("Mary-Beth", "O'Connor")
        assert emp_id is not None
        assert len(emp_id) == 32

    def test_generate_employee_id_empty_strings(self):
        """Test ID generation with empty strings"""
        emp_id = generate_employee_id("", "")
        assert emp_id is not None
        assert len(emp_id) == 32

    def test_generate_employee_id_order_matters(self):
        """Test that name order affects the generated ID"""
        emp_id1 = generate_employee_id("Michael", "Scott")
        emp_id2 = generate_employee_id("Scott", "Michael")
        assert emp_id1 != emp_id2
