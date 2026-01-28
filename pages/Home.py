import streamlit as st
from utilities.connection_helper import get_db_connection
from ui.styles import get_base_styles

st.set_page_config(
    page_title="*The Office* Chain of Command Builder", 
    layout="wide"
)

client = get_db_connection()

# Apply shared CSS styles
st.markdown(get_base_styles(), unsafe_allow_html=True)

# Main Header
st.markdown("""
<div class="main-header">
    <h1>Build Your Dunder Mifflin Dream Team!</h1>
    <p style="font-size: 1.2rem; margin: 0; opacity: 0.9;">Streamline Dunder Mifflin's Organizational Management</p>
</div>
""", unsafe_allow_html=True)

# Getting Started
st.markdown("""
<div class="white-section">
    <h4>Getting Started</h4>
    <p>Use the navigation menu to add, update, or delete employees in Dunder Mifflin organizational structure.</p>
</div>
""", unsafe_allow_html=True)

# System Overview
st.markdown("""
<div class="white-section">
    <h4>System Overview</h4>
    <p>This application manages a three-tier organizational hierarchy:</p>
    <ul>
        <li><strong>Executives:</strong> Top-level leadership with no supervisors</li>
        <li><strong>Managers:</strong> Middle management reporting to executives</li>
        <li><strong>Regular Employees:</strong> Team members reporting to managers</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# Key Features
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="white-section">
        <h4>Employee Management</h4>
        <p>Add, delete, and update employees across three hierarchical levels: Executives, Managers, and Regular Employees with comprehensive management tools.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="white-section">
        <h4>Graph Visualization</h4>
        <p>Build and visualize organizational structures using NetworkX graphs with enhanced Cytoscape export capabilities for advanced visualization.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="white-section">
        <h4>Database Integration</h4>
        <p>Persistent storage with PostgreSQL database ensuring data integrity through proper foreign key relationships and organizational structure validation.</p>
    </div>
    """, unsafe_allow_html=True)

