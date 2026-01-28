"""
Reusable UI components for Streamlit pages.
Eliminates UI pattern duplication across pages.
"""

import streamlit as st
import time
from typing import List, Optional
from models.orgchart import Employee


class UIHelper:
    """Common UI patterns and interactions"""

    @staticmethod
    def show_success_and_rerun(message: str, delay: int = 2):
        """
        Show success message and rerun page after delay.

        Eliminates 3x duplication in ChainOfCommand.py.

        :param message: Success message to display
        :type message: str
        :param delay: Delay in seconds before rerun
        :type delay: int
        """
        st.success(message)
        time.sleep(delay)
        st.rerun()

    @staticmethod
    def show_error(message: str):
        """
        Show error message.

        :param message: Error message to display
        :type message: str
        """
        st.error(message)


class EmployeeSelector:
    """Reusable employee selection component"""

    @staticmethod
    def render(
        employees: List[Employee],
        label: str = "Select Employee",
        placeholder: str = "Choose employee...",
        key: Optional[str] = None
    ) -> Optional[Employee]:
        """
        Render employee dropdown and return selected employee.

        Eliminates 2x duplication in ChainOfCommand.py (Update and Delete tabs).

        :param employees: List of employees to choose from
        :type employees: List[Employee]
        :param label: Dropdown label
        :type label: str
        :param placeholder: Placeholder text
        :type placeholder: str
        :param key: Unique key for Streamlit widget
        :type key: Optional[str]
        :return: Selected employee or None
        :rtype: Optional[Employee]
        """
        if not employees:
            st.info("No employees found")
            return None

        emp_options = {f"{emp.first_name} {emp.last_name}": emp for emp in employees}
        selected_name = st.selectbox(
            label,
            options=emp_options.keys(),
            placeholder=placeholder,
            key=key
        )

        if selected_name:
            return emp_options[selected_name]
        return None


class SupervisorSelector:
    """Reusable supervisor selection component"""

    @staticmethod
    def render(
        supervisors: Optional[List],
        label: str = "Select Supervisor",
        current_supervisor_id: Optional[str] = None,
        exclude_emp_id: Optional[str] = None
    ) -> Optional[str]:
        """
        Render supervisor dropdown and return supervisor ID.

        Eliminates 3x duplication in ChainOfCommand.py (Add, Update, Delete tabs).

        :param supervisors: List of potential supervisors
        :type supervisors: Optional[List]
        :param label: Dropdown label
        :type label: str
        :param current_supervisor_id: Current supervisor ID (for updates)
        :type current_supervisor_id: Optional[str]
        :param exclude_emp_id: Employee ID to exclude from options (for delete reassignment)
        :type exclude_emp_id: Optional[str]
        :return: Selected supervisor ID or None
        :rtype: Optional[str]
        """
        if not supervisors:
            return None

        # Build options dictionary, excluding specific employee if needed
        options = {
            f"{s.first_name} {s.last_name}": s.emp_id
            for s in supervisors
            if not exclude_emp_id or s.emp_id != exclude_emp_id
        }

        if not options:
            return None

        # Find current index for updates
        index = 0
        if current_supervisor_id:
            supervisor_ids = list(options.values())
            if current_supervisor_id in supervisor_ids:
                index = supervisor_ids.index(current_supervisor_id)

        selected_name = st.selectbox(label, options=options.keys(), index=index)
        return options.get(selected_name)
