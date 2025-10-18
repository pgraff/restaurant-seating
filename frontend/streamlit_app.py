"""
Restaurant Seating System - Streamlit Frontend
Main application entry point
"""

import streamlit as st
import sys
import os

# Add the parent directory to the path to import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pages import (
    dashboard,
    reservations,
    table_assignment,
    waiting_list,
    configuration
)

# Page configuration
st.set_page_config(
    page_title="Restaurant Seating System",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #c3e6cb;
    }
    .error-message {
        background-color: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #f5c6cb;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Main application function"""
    
    # Sidebar navigation
    st.sidebar.title("🍽️ Restaurant Seating")
    st.sidebar.markdown("---")
    
    # Navigation menu
    page = st.sidebar.selectbox(
        "Navigate to:",
        [
            "Dashboard",
            "Reservations",
            "Table Assignment", 
            "Waiting List",
            "Configuration"
        ]
    )
    
    # Display selected page
    if page == "Dashboard":
        dashboard.show()
    elif page == "Reservations":
        reservations.show()
    elif page == "Table Assignment":
        table_assignment.show()
    elif page == "Waiting List":
        waiting_list.show()
    elif page == "Configuration":
        configuration.show()

if __name__ == "__main__":
    main()
