import streamlit as st
from models.orgchart import SQLEmployee, SQLManager, SQLExecutive, Employee
from utilities.connection_helper import get_db_connection
from config.employee_types import get_config_by_name, EMPLOYEE_TYPES
from ui.styles import get_base_styles, render_page_header
from ui.components import UIHelper, EmployeeSelector, SupervisorSelector
from ui.forms import EmployeeFormBuilder
import json
from utilities.graph_builder import build_org_graph
import networkx as nx

# Page Configurations
st.set_page_config(
    page_title="The Office Employee Management",
    layout="wide"
)

client = get_db_connection()

# Apply shared CSS styles
st.markdown(get_base_styles(), unsafe_allow_html=True)

# Main Header
st.markdown(
    render_page_header(
        "Dunder Mifflin Chain of Command Management",
        "Manage the Organizational Structure with Ease"
    ),
    unsafe_allow_html=True
)


# ====== Employee Management Section ======

# Create tabs for different operations
tab1, tab2, tab3, tab4 = st.tabs(["Add Employee", "Update Employee", "Delete Employee", "Build Graph"])

# Get all employee type display names from configuration
employee_type_options = [config.display_name for config in EMPLOYEE_TYPES.values()]


# Tab 1: Adding an employee
with tab1:
    st.markdown('<div class="section-header">Add Employee to Dunder Mifflin</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("### Select Employee Type")
        employee_type = st.selectbox(
            "Choose Employee Type:",
            options=employee_type_options,
            index=None,
            placeholder="Select employee type...",
            key="add_emp_type"
        )

        if employee_type:
            st.success(f"Selected: {employee_type}")

    with col2:
        if employee_type:
            st.markdown("### Employee Details")

            # Get config and fetch potential supervisors
            config = get_config_by_name(employee_type)
            supervisor = (
                client.fetchEmployee(config.supervisor_table)
                if config.supervisor_table
                else None
            )
            
            with st.container(border=True):
                with st.form("add_employee_form", clear_on_submit=True):
                    # input fields
                    fields = EmployeeFormBuilder.render_basic_fields()
                    first_name = fields['first_name']
                    last_name = fields['last_name']
                    position = fields['position']
                    department = fields['department']

                    # supervisor selection
                    supervisor_id = SupervisorSelector.render(supervisor)
                        
                    st.markdown("---")
                    if st.form_submit_button("Add Employee", use_container_width=True):
                        new_employee = Employee(first_name=first_name,
                                                last_name=last_name,
                                                position=position,
                                                department=department,
                                                supervisor_id=supervisor_id)
                        if client.addEmployee(new_employee, config.table_class):
                            UIHelper.show_success_and_rerun("Employee successfully created and added to the DB")
                        else:
                            UIHelper.show_error("Failed to add employee. Please check input validation.")
                            
                            
# Tab 2: Update Employee
with tab2:
    st.markdown('<div class="section-header">Update Employee from Dunder Mifflin</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("### Select Employee")
        update_employee_type = st.selectbox(
            "Choose Employee Type:",
            options=employee_type_options,
            index=None,
            placeholder="Select employee type...",
            key="update_emp_type"
        )

        employee = None
        if update_employee_type:
            update_config = get_config_by_name(update_employee_type)
            employees = client.fetchEmployee(update_config.table_class)
            employee = EmployeeSelector.render(
                employees,
                "Select Employee to Update",
                "Choose employee...",
                key="update_employee_select"
            )
    
    with col2:
        if update_employee_type and employee:
            st.markdown("### Update Details")
            with st.container(border=True):
                with st.form("update_employee_form", clear_on_submit=True):
                    # input fields
                    fields = EmployeeFormBuilder.render_basic_fields(employee)
                    first_name = fields['first_name']
                    last_name = fields['last_name']
                    position = fields['position']
                    department = fields['department']

                    # supervisor selection
                    supervisor = (
                        client.fetchEmployee(update_config.supervisor_table)
                        if update_config.supervisor_table
                        else None
                    )
                    supervisor_id = SupervisorSelector.render(
                        supervisor,
                        "Supervisor",
                        employee.supervisor_id
                    )

                    st.markdown("---")
                    if st.form_submit_button("Update Employee", use_container_width=True):
                        updated_employee = Employee(first_name=first_name,
                                                    last_name=last_name,
                                                    position=position,
                                                    department=department,
                                                    supervisor_id=supervisor_id)
                        if client.updateEmployee(updated_employee, update_config.table_class, emp_id=employee.emp_id):
                            UIHelper.show_success_and_rerun("Employee successfully updated in the DB")
                        else:
                            UIHelper.show_error("Failed to update employee. Please try again.")
                            
                            
# Tab 3: Delete Employee
with tab3:
    st.markdown('<div class="section-header">Delete Employee from Dunder Mifflin</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("### Select Employee")
        delete_employee_type = st.selectbox(
            "Choose Employee Type:",
            options=employee_type_options,
            index=None,
            placeholder="Select employee type...",
            key="delete_emp_type"
        )

        employee = None
        if delete_employee_type:
            delete_config = get_config_by_name(delete_employee_type)
            employees = client.fetchEmployee(delete_config.table_class)
            employee = EmployeeSelector.render(
                employees,
                "Select Employee to Delete",
                "Choose employee...",
                key="delete_employee_select"
            )
    
    with col2:
        if delete_employee_type and employee:
            st.markdown("### Deletion Options")
            with st.container(border=True):
                st.warning(f"You are about to delete: **{employee.first_name} {employee.last_name}**")
                
                reassign_to = None
                show_reassign = False

                # Check if this employee type has subordinates (can be reassigned)
                if delete_config.subordinate_table:
                    show_reassign = st.checkbox("Reassign Subordinates to Another Supervisor?", value=False)

                    if show_reassign:
                        # Fetch potential supervisors from the same level
                        potential_supervisors = client.fetchEmployee(delete_config.table_class)

                        if potential_supervisors:
                            reassign_to = SupervisorSelector.render(
                                potential_supervisors,
                                "Select New Supervisor",
                                exclude_emp_id=employee.emp_id
                            )
                            if not reassign_to:
                                # info box when no reassignment options available
                                employee_type_lower = delete_employee_type.lower()
                                st.info(
                                    f"**No other {employee_type_lower}s available for reassignment.**\n\n"
                                    f"This is the only {employee_type_lower} in the system. "
                                    f"Subordinates will have their supervisor set to NULL when deleted."
                                )

                st.markdown("---")
                if st.button("Delete Employee", type="primary", use_container_width=True):
                    if client.deleteEmployee(delete_config.table_class, employee.emp_id, reassign_to):
                        UIHelper.show_success_and_rerun("Employee successfully deleted.")
                    else:
                        UIHelper.show_error("Failed to delete employee. Please check reassignment or permissions.")
                        
                        
# Tab 4: Build Graph
with tab4:
    st.markdown('<div class="section-header">Build Dunder Mifflin Organizational Graph</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("### Graph Operations")
        st.info("Click the button below to build a graph from the current organizational data.")
        
        if st.button("Build Graph", type="primary", use_container_width=True):
            with st.spinner("Building organizational graph..."):
                G = build_org_graph(SQLEmployee, SQLManager, SQLExecutive)
                st.session_state.org_graph = G
        
        # Export to Cytoscape button
        if 'org_graph' in st.session_state:
            st.markdown("---")
            if st.button("Export to Cytoscape", use_container_width=True):
                G = st.session_state.org_graph
                if isinstance(G, nx.Graph):
                    cytoscape_data = nx.cytoscape_data(G)
                   
                    # Convert to JSON string for download
                    json_str = json.dumps(cytoscape_data, indent=2)
                    st.success("Cytoscape JSON generated! Ready for download.")

                    # Optional preview
                    with st.expander("Preview Cytoscape JSON"):
                        st.code(json_str[:1000], language="json")  # preview first 1000 characters

                    # Download button
                    st.download_button(
                        label="Download Cytoscape JSON",
                        data=json_str,
                        file_name="dunder_mifflin_org_chart.json",
                        mime="application/json",
                        use_container_width=True
                    )
                else:
                    st.error("Invalid graph format. Please check your org chart structure.")
        
    with col2:
        if 'org_graph' in st.session_state:
            G = st.session_state.org_graph
            st.markdown("### Graph Statistics")
            
            with st.container(border=True):
                metric_col1, metric_col2 = st.columns(2)
                with metric_col1:
                    st.metric("Total Nodes", G.number_of_nodes())
                with metric_col2:
                    st.metric("Total Edges", G.number_of_edges())
                
                st.markdown("### Sample Data")
                with st.expander("View 10 Sample Nodes"):
                    sample_nodes = list(G.nodes(data=True))[:10]
                    for i, (node, attrs) in enumerate(sample_nodes, 1):
                        name = attrs.get("label", node) # fallback to node ID if label missing
                        st.write(f"{i}. **{name}** -- Position: {attrs.get('position', 'N/A')}")
                
                with st.expander("View 10 Sample Edges"):
                    sample_edges = list(G.edges())[:10]
                    for i, edge in enumerate(sample_edges, 1):
                        source_name = G.nodes[edge[0]].get("label", edge[0])
                        target_name = G.nodes[edge[1]].get("label", edge[1])
                        st.write(f"{i}. **{source_name}** → **{target_name}**")
        else:
            st.markdown("### Graph Statistics")
            st.info("No graph data available. Click 'Build Graph' to generate statistics.")
    
    