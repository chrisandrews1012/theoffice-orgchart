import networkx as nx
import streamlit as st
from models.orgchart import SQLEmployee, SQLManager, SQLExecutive
from utilities.connection_helper import get_db_connection
from sqlalchemy import text
from utilities.session_helper import get_readonly_session
from utilities.errors import handle_db_errors

client = get_db_connection()

@handle_db_errors("build organizational graph", default_return=nx.DiGraph())
def build_org_graph(emp_table: SQLEmployee = None, mgr_table: SQLManager = None, exec_table: SQLExecutive = None) -> nx.DiGraph:
    """
    Builds a networkx DiGraph from the three employee SQL tables using a single SQL query.
    Parameters are kept for compatibility but not used in SQL approach.
    """

    # Single SQL query to get all employees and their supervisor relationships
    query = """
    SELECT emp_id, first_name, last_name, position, supervisor_id
    FROM (
        SELECT emp_id, first_name, last_name, position, supervisor_id FROM executive
        UNION ALL
        SELECT emp_id, first_name, last_name, position, supervisor_id FROM manager
        UNION ALL
        SELECT emp_id, first_name, last_name, position, supervisor_id FROM employee
    ) AS all_employees
    ORDER BY emp_id
    """

    G = nx.DiGraph()

    # execute the query
    with get_readonly_session(client.connection) as session:
        result = session.execute(text(query))
        all_employees = result.fetchall()

    # add all nodes first
    for row in all_employees:
        emp_id, first_name, last_name, position, supervisor_id = row
        full_name = f"{first_name.strip()} {last_name.strip()}".strip()
        G.add_node(emp_id, label=full_name, position=position)

    # add edges for supervisor relationships
    for row in all_employees:
        emp_id, _, _, _, supervisor_id = row
        if supervisor_id and supervisor_id in G.nodes:
            G.add_edge(emp_id, supervisor_id)

    return G