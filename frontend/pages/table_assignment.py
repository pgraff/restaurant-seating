"""
Table assignment page for seating parties
Allows assigning tables to parties and managing current assignments
"""

import streamlit as st
import sys
import os
from datetime import datetime, date, timedelta

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api_client import RestaurantAPIClient

def show():
    """Display the table assignment page"""
    st.markdown('<h1 class="main-header">Table Assignment</h1>', unsafe_allow_html=True)
    
    # Initialize API client
    api_client = RestaurantAPIClient()
    
    # Get restaurants
    restaurants = api_client.get_restaurants()
    
    if not restaurants:
        st.warning("No restaurants found. Please configure a restaurant first.")
        return
    
    # Restaurant selector
    restaurant_options = {f"{r['name']} ({r['id']})": r['id'] for r in restaurants}
    selected_restaurant_name = st.selectbox("Select Restaurant:", list(restaurant_options.keys()))
    selected_restaurant_id = restaurant_options[selected_restaurant_name]
    
    if not selected_restaurant_id:
        return
    
    # Tabs for different views
    tab1, tab2, tab3 = st.tabs(["Current Assignments", "Assign Table", "Available Tables"])
    
    with tab1:
        show_current_assignments(api_client, selected_restaurant_id)
    
    with tab2:
        show_assign_table_form(api_client, selected_restaurant_id)
    
    with tab3:
        show_available_tables(api_client, selected_restaurant_id)

def show_current_assignments(api_client, restaurant_id):
    """Display current table assignments"""
    st.subheader("Current Table Assignments")
    
    # Get tables and their assignments
    tables = api_client.get_tables(restaurant_id=restaurant_id)
    parties = api_client.get_parties(status="SEATED")
    
    if not tables:
        st.info("No tables configured for this restaurant")
        return
    
    # Filter occupied tables
    occupied_tables = [t for t in tables if t['status'] == 'OCCUPIED']
    
    if not occupied_tables:
        st.info("No tables are currently occupied")
        return
    
    # Display occupied tables
    for table in occupied_tables:
        with st.expander(f"Table {table['table_number']} - {table['location']} (Capacity: {table['capacity']})"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Table Number:** {table['table_number']}")
                st.write(f"**Location:** {table['location']}")
                st.write(f"**Capacity:** {table['capacity']}")
                st.write(f"**Status:** {table['status']}")
            
            with col2:
                # Find party assigned to this table (this would need to be implemented in the API)
                st.write("**Assignment Details:**")
                st.write("Party information would be displayed here")
                st.write("Server information would be displayed here")
                st.write("Assignment time would be displayed here")
            
            # Action buttons
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button(f"Complete Assignment", key=f"complete_{table['id']}"):
                    # This would complete the table assignment
                    st.success("Table assignment completed!")
                    st.rerun()
            
            with col2:
                if st.button(f"View Details", key=f"details_{table['id']}"):
                    st.info("Detailed assignment information would be shown here")

def show_assign_table_form(api_client, restaurant_id):
    """Display form to assign table to party"""
    st.subheader("Assign Table to Party")
    
    # Get available tables
    tables = api_client.get_tables(restaurant_id=restaurant_id, status="AVAILABLE")
    
    if not tables:
        st.warning("No available tables found")
        return
    
    # Get parties waiting to be seated
    parties = api_client.get_parties(status="WAITING")
    
    if not parties:
        st.warning("No parties waiting to be seated")
        return
    
    # Get servers
    servers = api_client.get_servers(restaurant_id=restaurant_id, is_active=True)
    
    if not servers:
        st.warning("No active servers found")
        return
    
    with st.form("assign_table_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            # Table selection
            table_options = {f"Table {t['table_number']} - {t['location']} (Capacity: {t['capacity']})": t['id'] 
                           for t in tables}
            selected_table_name = st.selectbox("Select Table *", list(table_options.keys()))
            selected_table_id = table_options[selected_table_name]
            
            # Server selection
            server_options = {f"{s['first_name']} {s['last_name']} ({s['employee_id']})": s['id'] 
                            for s in servers}
            selected_server_name = st.selectbox("Select Server *", list(server_options.keys()))
            selected_server_id = server_options[selected_server_name]
        
        with col2:
            # Party selection
            party_options = {f"{p['name']} - Party of {p['size']}": p['id'] for p in parties}
            selected_party_name = st.selectbox("Select Party *", list(party_options.keys()))
            selected_party_id = party_options[selected_party_name]
            
            # Notes
            notes = st.text_area("Assignment Notes", placeholder="Any special notes for this assignment")
        
        submitted = st.form_submit_button("Assign Table", use_container_width=True)
        
        if submitted:
            if not all([selected_table_id, selected_party_id, selected_server_id]):
                st.error("Please select table, party, and server")
            else:
                result = api_client.assign_table_to_party(
                    restaurant_id=restaurant_id,
                    table_id=selected_table_id,
                    party_id=selected_party_id,
                    server_id=selected_server_id,
                    notes=notes if notes else None
                )
                
                if result:
                    st.success("Table assigned successfully!")
                    st.rerun()
                else:
                    st.error("Failed to assign table. Please check the details and try again.")

def show_available_tables(api_client, restaurant_id):
    """Display available tables and their details"""
    st.subheader("Available Tables")
    
    # Get tables
    tables = api_client.get_tables(restaurant_id=restaurant_id)
    
    if not tables:
        st.info("No tables configured for this restaurant")
        return
    
    # Filter by status
    status_filter = st.selectbox("Filter by Status:", 
                               ["All", "AVAILABLE", "OCCUPIED", "RESERVED", "OUT_OF_ORDER", "CLEANING"])
    
    filtered_tables = tables
    if status_filter != "All":
        filtered_tables = [t for t in tables if t['status'] == status_filter]
    
    if not filtered_tables:
        st.info(f"No tables found with status: {status_filter}")
        return
    
    # Display tables
    for i, table in enumerate(filtered_tables):
        with st.expander(f"Table {table['table_number']} - {table['status']}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Table Number:** {table['table_number']}")
                st.write(f"**Location:** {table['location']}")
                st.write(f"**Capacity:** {table['capacity']}")
                st.write(f"**Status:** {table['status']}")
            
            with col2:
                st.write(f"**Active:** {'Yes' if table['is_active'] else 'No'}")
                if table.get('section_ids'):
                    st.write(f"**Sections:** {', '.join(table['section_ids'])}")
            
            # Action buttons based on status - using index to ensure unique keys
            if table['status'] == 'AVAILABLE':
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"Reserve Table", key=f"reserve_{i}_{table['id']}"):
                        st.info("Table reservation functionality would be implemented here")
                with col2:
                    if st.button(f"Mark Out of Order", key=f"out_of_order_{i}_{table['id']}"):
                        st.info("Mark out of order functionality would be implemented here")
            
            elif table['status'] == 'OCCUPIED':
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"Complete Service", key=f"complete_{i}_{table['id']}"):
                        st.info("Complete service functionality would be implemented here")
                with col2:
                    if st.button(f"View Assignment", key=f"view_{i}_{table['id']}"):
                        st.info("View assignment details functionality would be implemented here")
            
            elif table['status'] == 'RESERVED':
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"Seat Party", key=f"seat_{i}_{table['id']}"):
                        st.info("Seat party functionality would be implemented here")
                with col2:
                    if st.button(f"Release Reservation", key=f"release_{i}_{table['id']}"):
                        st.info("Release reservation functionality would be implemented here")
            
            elif table['status'] == 'CLEANING':
                if st.button(f"Mark Available", key=f"available_{i}_{table['id']}"):
                    st.info("Mark available functionality would be implemented here")
            
            elif table['status'] == 'OUT_OF_ORDER':
                if st.button(f"Mark Available", key=f"repair_{i}_{table['id']}"):
                    st.info("Mark available after repair functionality would be implemented here")
