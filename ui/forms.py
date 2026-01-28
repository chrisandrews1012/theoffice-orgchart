import streamlit as st
from typing import Dict, Optional
from models.orgchart import Employee, DepartmentType


class EmployeeFormBuilder:
    """Build reusable employee forms"""

    @staticmethod
    def render_basic_fields(employee: Optional[Employee] = None) -> Dict[str, str]:
        """Render name and position fields"""
        col_a, col_b = st.columns(2)

        with col_a:
            first_name = st.text_input(
                "First Name",
                value=employee.first_name if employee else "",
                placeholder="Enter first name"
            )
            position = st.text_input(
                "Position",
                value=employee.position if employee else "",
                placeholder="Enter job position"
            )

        with col_b:
            last_name = st.text_input(
                "Last Name",
                value=employee.last_name if employee else "",
                placeholder="Enter last name"
            )

            # Department dropdown
            dept_options = [d.value for d in DepartmentType]
            dept_index = 0
            if employee and employee.department:
                try:
                    dept_index = dept_options.index(employee.department)
                except ValueError:
                    dept_index = 0

            department = st.selectbox("Department", options=dept_options, index=dept_index)

        return {
            'first_name': first_name,
            'last_name': last_name,
            'position': position,
            'department': department
        }
