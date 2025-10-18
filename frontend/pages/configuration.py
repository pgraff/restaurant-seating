"""
Configuration page for setting up restaurants, sections, tables, and servers
"""

import streamlit as st
import sys
import os
from datetime import datetime, date, timedelta

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api_client import RestaurantAPIClient

def show():
    """Display the configuration page"""
    st.markdown('<h1 class="main-header">System Configuration</h1>', unsafe_allow_html=True)
    
    # Initialize API client
    api_client = RestaurantAPIClient()
    
    # Tabs for different configuration areas
    tab1, tab2, tab3, tab4 = st.tabs(["Restaurants", "Sections", "Tables", "Servers"])
    
    with tab1:
        show_restaurant_configuration(api_client)
    
    with tab2:
        show_section_configuration(api_client)
    
    with tab3:
        show_table_configuration(api_client)
    
    with tab4:
        show_server_configuration(api_client)

def show_restaurant_configuration(api_client):
    """Display restaurant configuration interface"""
    st.subheader("Restaurant Configuration")
    
    # Get existing restaurants
    restaurants = api_client.get_restaurants()
    
    # Display existing restaurants
    if restaurants:
        st.markdown("### Existing Restaurants")
        for restaurant in restaurants:
            with st.expander(f"{restaurant['name']} - {restaurant['address']}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Name:** {restaurant['name']}")
                    st.write(f"**Address:** {restaurant['address']}")
                    st.write(f"**Phone:** {restaurant['phone']}")
                
                with col2:
                    st.write(f"**Opening Time:** {restaurant['opening_time']}")
                    st.write(f"**Closing Time:** {restaurant['closing_time']}")
                    st.write(f"**Max Capacity:** {restaurant['max_capacity']}")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"Edit", key=f"edit_restaurant_{restaurant['id']}"):
                        st.session_state.edit_restaurant_id = restaurant['id']
                        st.rerun()
                with col2:
                    if st.button(f"Delete", key=f"delete_restaurant_{restaurant['id']}"):
                        if api_client.delete_restaurant(restaurant['id']):
                            st.success("Restaurant deleted successfully")
                            st.rerun()
                        else:
                            st.error("Failed to delete restaurant")
    
    # Add new restaurant form
    st.markdown("### Add New Restaurant")
    
    with st.form("add_restaurant_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Restaurant Name *", placeholder="Enter restaurant name")
            address = st.text_area("Address *", placeholder="Enter full address")
            phone = st.text_input("Phone Number *", placeholder="Enter phone number")
        
        with col2:
            opening_time = st.time_input("Opening Time *", value=datetime.strptime("09:00", "%H:%M").time())
            closing_time = st.time_input("Closing Time *", value=datetime.strptime("22:00", "%H:%M").time())
            max_capacity = st.number_input("Max Capacity *", min_value=1, max_value=1000, value=100)
        
        submitted = st.form_submit_button("Create Restaurant", use_container_width=True)
        
        if submitted:
            if not all([name, address, phone, max_capacity]):
                st.error("Please fill in all required fields (marked with *)")
            else:
                restaurant_data = {
                    "name": name,
                    "address": address,
                    "phone": phone,
                    "opening_time": opening_time.strftime("%H:%M"),
                    "closing_time": closing_time.strftime("%H:%M"),
                    "max_capacity": max_capacity
                }
                
                result = api_client.create_restaurant(restaurant_data)
                if result:
                    st.success("Restaurant created successfully!")
                    st.rerun()
                else:
                    st.error("Failed to create restaurant. Please check the details and try again.")

def show_section_configuration(api_client):
    """Display section configuration interface"""
    st.subheader("Section Configuration")
    
    # Get restaurants for selection
    restaurants = api_client.get_restaurants()
    
    if not restaurants:
        st.warning("No restaurants found. Please create a restaurant first.")
        return
    
    # Restaurant selector
    restaurant_options = {f"{r['name']} ({r['id']})": r['id'] for r in restaurants}
    selected_restaurant_name = st.selectbox("Select Restaurant:", list(restaurant_options.keys()))
    selected_restaurant_id = restaurant_options[selected_restaurant_name]
    
    if not selected_restaurant_id:
        return
    
    # Get existing sections
    sections = api_client.get_sections(selected_restaurant_id)
    
    # Display existing sections
    if sections:
        st.markdown("### Existing Sections")
        for section in sections:
            with st.expander(f"{section['name']} - Capacity: {section['capacity']}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Name:** {section['name']}")
                    st.write(f"**Description:** {section.get('description', 'N/A')}")
                    st.write(f"**Capacity:** {section['capacity']}")
                
                with col2:
                    st.write(f"**Active:** {'Yes' if section['is_active'] else 'No'}")
                    st.write(f"**Restaurant ID:** {section['restaurant_id']}")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"Edit", key=f"edit_section_{section['id']}"):
                        st.session_state.edit_section_id = section['id']
                        st.rerun()
                with col2:
                    if st.button(f"Delete", key=f"delete_section_{section['id']}"):
                        if api_client.delete_section(section['id']):
                            st.success("Section deleted successfully")
                            st.rerun()
                        else:
                            st.error("Failed to delete section")
    
    # Add new section form
    st.markdown("### Add New Section")
    
    with st.form("add_section_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Section Name *", placeholder="Enter section name")
            description = st.text_area("Description", placeholder="Enter section description")
        
        with col2:
            capacity = st.number_input("Capacity *", min_value=1, max_value=1000, value=20)
            is_active = st.checkbox("Active", value=True)
        
        submitted = st.form_submit_button("Create Section", use_container_width=True)
        
        if submitted:
            if not all([name, capacity]):
                st.error("Please fill in all required fields (marked with *)")
            else:
                section_data = {
                    "name": name,
                    "description": description if description else None,
                    "capacity": capacity,
                    "is_active": is_active,
                    "restaurant_id": selected_restaurant_id
                }
                
                result = api_client.create_section(selected_restaurant_id, section_data)
                if result:
                    st.success("Section created successfully!")
                    st.rerun()
                else:
                    st.error("Failed to create section. Please check the details and try again.")

def show_table_configuration(api_client):
    """Display table configuration interface"""
    st.subheader("Table Configuration")
    
    # Get restaurants for selection
    restaurants = api_client.get_restaurants()
    
    if not restaurants:
        st.warning("No restaurants found. Please create a restaurant first.")
        return
    
    # Restaurant selector
    restaurant_options = {f"{r['name']} ({r['id']})": r['id'] for r in restaurants}
    selected_restaurant_name = st.selectbox("Select Restaurant:", list(restaurant_options.keys()))
    selected_restaurant_id = restaurant_options[selected_restaurant_name]
    
    if not selected_restaurant_id:
        return
    
    # Get sections for this restaurant
    sections = api_client.get_sections(selected_restaurant_id)
    
    # Get existing tables
    tables = api_client.get_tables(selected_restaurant_id)
    
    # Display existing tables
    if tables:
        st.markdown("### Existing Tables")
        for table in tables:
            with st.expander(f"Table {table['table_number']} - {table['location']}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Table Number:** {table['table_number']}")
                    st.write(f"**Location:** {table['location']}")
                    st.write(f"**Capacity:** {table['capacity']}")
                
                with col2:
                    st.write(f"**Status:** {table['status']}")
                    st.write(f"**Active:** {'Yes' if table['is_active'] else 'No'}")
                    if table.get('section_ids'):
                        st.write(f"**Sections:** {', '.join(table['section_ids'])}")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"Edit", key=f"edit_table_{table['id']}"):
                        st.session_state.edit_table_id = table['id']
                        st.rerun()
                with col2:
                    if st.button(f"Delete", key=f"delete_table_{table['id']}"):
                        if api_client.delete_table(table['id']):
                            st.success("Table deleted successfully")
                            st.rerun()
                        else:
                            st.error("Failed to delete table")
    
    # Add new table form
    st.markdown("### Add New Table")
    
    with st.form("add_table_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            table_number = st.text_input("Table Number *", placeholder="Enter table number")
            location = st.text_input("Location *", placeholder="Enter table location")
            capacity = st.number_input("Capacity *", min_value=1, max_value=20, value=4)
        
        with col2:
            status = st.selectbox("Status", ["AVAILABLE", "OCCUPIED", "RESERVED", "OUT_OF_ORDER", "CLEANING"])
            is_active = st.checkbox("Active", value=True)
            
            # Section selection (if sections exist)
            if sections:
                section_options = {f"{s['name']} (Capacity: {s['capacity']})": s['id'] for s in sections}
                selected_sections = st.multiselect("Sections", list(section_options.keys()))
                section_ids = [section_options[s] for s in selected_sections]
            else:
                section_ids = []
        
        submitted = st.form_submit_button("Create Table", use_container_width=True)
        
        if submitted:
            if not all([table_number, location, capacity]):
                st.error("Please fill in all required fields (marked with *)")
            else:
                table_data = {
                    "table_number": table_number,
                    "location": location,
                    "capacity": capacity,
                    "status": status,
                    "is_active": is_active,
                    "restaurant_id": selected_restaurant_id,
                    "section_ids": section_ids
                }
                
                result = api_client.create_table(selected_restaurant_id, table_data)
                if result:
                    st.success("Table created successfully!")
                    st.rerun()
                else:
                    st.error("Failed to create table. Please check the details and try again.")

def show_server_configuration(api_client):
    """Display server configuration interface"""
    st.subheader("Server Configuration")
    
    # Get restaurants for selection
    restaurants = api_client.get_restaurants()
    
    if not restaurants:
        st.warning("No restaurants found. Please create a restaurant first.")
        return
    
    # Restaurant selector
    restaurant_options = {f"{r['name']} ({r['id']})": r['id'] for r in restaurants}
    selected_restaurant_name = st.selectbox("Select Restaurant:", list(restaurant_options.keys()))
    selected_restaurant_id = restaurant_options[selected_restaurant_name]
    
    if not selected_restaurant_id:
        return
    
    # Get existing servers
    servers = api_client.get_servers(restaurant_id=selected_restaurant_id)
    
    # Display existing servers
    if servers:
        st.markdown("### Existing Servers")
        for server in servers:
            with st.expander(f"{server['first_name']} {server['last_name']} - {server['employee_id']}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Name:** {server['first_name']} {server['last_name']}")
                    st.write(f"**Employee ID:** {server['employee_id']}")
                    st.write(f"**Active:** {'Yes' if server['is_active'] else 'No'}")
                
                with col2:
                    if server.get('shift_start'):
                        st.write(f"**Shift Start:** {server['shift_start'][:16]}")
                    if server.get('shift_end'):
                        st.write(f"**Shift End:** {server['shift_end'][:16]}")
                    st.write(f"**Restaurant ID:** {server['restaurant_id']}")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"Edit", key=f"edit_server_{server['id']}"):
                        st.session_state.edit_server_id = server['id']
                        st.rerun()
                with col2:
                    if st.button(f"Delete", key=f"delete_server_{server['id']}"):
                        if api_client.delete_server(server['id']):
                            st.success("Server deleted successfully")
                            st.rerun()
                        else:
                            st.error("Failed to delete server")
    
    # Add new server form
    st.markdown("### Add New Server")
    
    with st.form("add_server_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            first_name = st.text_input("First Name *", placeholder="Enter first name")
            last_name = st.text_input("Last Name *", placeholder="Enter last name")
            employee_id = st.text_input("Employee ID *", placeholder="Enter employee ID")
        
        with col2:
            is_active = st.checkbox("Active", value=True)
            shift_start = st.time_input("Shift Start Time", value=datetime.strptime("09:00", "%H:%M").time())
            shift_end = st.time_input("Shift End Time", value=datetime.strptime("17:00", "%H:%M").time())
        
        submitted = st.form_submit_button("Create Server", use_container_width=True)
        
        if submitted:
            if not all([first_name, last_name, employee_id]):
                st.error("Please fill in all required fields (marked with *)")
            else:
                server_data = {
                    "first_name": first_name,
                    "last_name": last_name,
                    "employee_id": employee_id,
                    "is_active": is_active,
                    "shift_start": datetime.combine(date.today(), shift_start).isoformat(),
                    "shift_end": datetime.combine(date.today(), shift_end).isoformat(),
                    "restaurant_id": selected_restaurant_id
                }
                
                result = api_client.create_server(server_data)
                if result:
                    st.success("Server created successfully!")
                    st.rerun()
                else:
                    st.error("Failed to create server. Please check the details and try again.")
