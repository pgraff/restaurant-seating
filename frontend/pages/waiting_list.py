"""
Waiting list management page
Allows managing the waiting list and seating parties when tables become available
"""

import streamlit as st
import sys
import os
from datetime import datetime, date, timedelta

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api_client import RestaurantAPIClient

def show():
    """Display the waiting list management page"""
    st.markdown('<h1 class="main-header">Waiting List Management</h1>', unsafe_allow_html=True)
    
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
    tab1, tab2, tab3 = st.tabs(["Current Waiting List", "Add to Waiting List", "Seat Next Party"])
    
    with tab1:
        show_waiting_list(api_client, selected_restaurant_id)
    
    with tab2:
        show_add_to_waiting_list_form(api_client, selected_restaurant_id)
    
    with tab3:
        show_seat_next_party(api_client, selected_restaurant_id)

def show_waiting_list(api_client, restaurant_id):
    """Display current waiting list"""
    st.subheader("Current Waiting List")
    
    # Get waiting list entries
    waiting_list = api_client.get_waiting_list(restaurant_id=restaurant_id, status="WAITING")
    
    if not waiting_list:
        st.info("No parties currently on the waiting list")
        return
    
    # Sort by request time (oldest first)
    waiting_list.sort(key=lambda x: x['request_time'])
    
    # Display waiting list
    for i, entry in enumerate(waiting_list):
        with st.expander(f"#{i+1} - {entry['customer_name']} - Party of {entry['party_size']}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Customer:** {entry['customer_name']}")
                st.write(f"**Phone:** {entry['customer_phone']}")
                st.write(f"**Party Size:** {entry['party_size']}")
                st.write(f"**Request Time:** {entry['request_time'][:16]}")
            
            with col2:
                st.write(f"**Estimated Wait:** {entry.get('estimated_wait_time', 0)} minutes")
                st.write(f"**Status:** {entry['status']}")
                if entry.get('notes'):
                    st.write(f"**Notes:** {entry['notes']}")
            
            # Action buttons
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button(f"Seat Now", key=f"seat_{entry['id']}"):
                    st.session_state.seat_party_id = entry['id']
                    st.rerun()
            
            with col2:
                if st.button(f"Update Wait Time", key=f"update_{entry['id']}"):
                    st.session_state.update_wait_id = entry['id']
                    st.rerun()
            
            with col3:
                if st.button(f"Remove", key=f"remove_{entry['id']}"):
                    if api_client.remove_from_waiting_list(entry['id']):
                        st.success("Party removed from waiting list")
                        st.rerun()
                    else:
                        st.error("Failed to remove party from waiting list")
    
    # Summary statistics
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Waiting", len(waiting_list))
    
    with col2:
        if waiting_list:
            avg_wait = sum(entry.get('estimated_wait_time', 0) for entry in waiting_list) / len(waiting_list)
            st.metric("Average Wait Time", f"{avg_wait:.0f} min")
        else:
            st.metric("Average Wait Time", "0 min")
    
    with col3:
        if waiting_list:
            longest_wait = max(entry.get('estimated_wait_time', 0) for entry in waiting_list)
            st.metric("Longest Wait", f"{longest_wait} min")
        else:
            st.metric("Longest Wait", "0 min")

def show_add_to_waiting_list_form(api_client, restaurant_id):
    """Display form to add party to waiting list"""
    st.subheader("Add Party to Waiting List")
    
    with st.form("add_waiting_list_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            customer_name = st.text_input("Customer Name *", placeholder="Enter customer name")
            customer_phone = st.text_input("Phone Number *", placeholder="Enter phone number")
            party_size = st.number_input("Party Size *", min_value=1, max_value=20, value=2)
        
        with col2:
            estimated_wait_time = st.number_input("Estimated Wait Time (minutes)", 
                                               min_value=0, max_value=300, value=30)
            notes = st.text_area("Notes", placeholder="Any special notes or requests")
        
        submitted = st.form_submit_button("Add to Waiting List", use_container_width=True)
        
        if submitted:
            if not all([customer_name, customer_phone, party_size]):
                st.error("Please fill in all required fields (marked with *)")
            else:
                waiting_list_data = {
                    "restaurant_id": restaurant_id,
                    "customer_name": customer_name,
                    "customer_phone": customer_phone,
                    "party_size": party_size,
                    "estimated_wait_time": estimated_wait_time,
                    "notes": notes if notes else None
                }
                
                result = api_client.add_to_waiting_list(waiting_list_data)
                if result:
                    st.success("Party added to waiting list successfully!")
                    st.rerun()
                else:
                    st.error("Failed to add party to waiting list. Please check the details and try again.")

def show_seat_next_party(api_client, restaurant_id):
    """Display interface to seat the next party from waiting list"""
    st.subheader("Seat Next Party")
    
    # Get next party from waiting list
    next_party = api_client.get_next_waiting_party(restaurant_id)
    
    if not next_party:
        st.info("No parties currently on the waiting list")
        return
    
    # Display next party details
    st.markdown("### Next Party in Line")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**Customer:** {next_party['customer_name']}")
        st.write(f"**Phone:** {next_party['customer_phone']}")
        st.write(f"**Party Size:** {next_party['party_size']}")
        st.write(f"**Request Time:** {next_party['request_time'][:16]}")
    
    with col2:
        st.write(f"**Estimated Wait:** {next_party.get('estimated_wait_time', 0)} minutes")
        st.write(f"**Status:** {next_party['status']}")
        if next_party.get('notes'):
            st.write(f"**Notes:** {next_party['notes']}")
    
    st.markdown("---")
    
    # Get available tables
    available_tables = api_client.get_tables(restaurant_id=restaurant_id, status="AVAILABLE")
    
    if not available_tables:
        st.warning("No available tables found. Cannot seat party at this time.")
        return
    
    # Filter tables by capacity
    suitable_tables = [t for t in available_tables if t['capacity'] >= next_party['party_size']]
    
    if not suitable_tables:
        st.warning(f"No tables available for party size {next_party['party_size']}")
        return
    
    # Get servers
    servers = api_client.get_servers(restaurant_id=restaurant_id, is_active=True)
    
    if not servers:
        st.warning("No active servers found")
        return
    
    # Seat party form
    with st.form("seat_party_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            # Table selection
            table_options = {f"Table {t['table_number']} - {t['location']} (Capacity: {t['capacity']})": t['id'] 
                           for t in suitable_tables}
            selected_table_name = st.selectbox("Select Table *", list(table_options.keys()))
            selected_table_id = table_options[selected_table_name]
        
        with col2:
            # Server selection
            server_options = {f"{s['first_name']} {s['last_name']} ({s['employee_id']})": s['id'] 
                            for s in servers}
            selected_server_name = st.selectbox("Select Server *", list(server_options.keys()))
            selected_server_id = server_options[selected_server_name]
        
        # Notes
        notes = st.text_area("Assignment Notes", placeholder="Any special notes for this assignment")
        
        submitted = st.form_submit_button("Seat Party", use_container_width=True)
        
        if submitted:
            if not all([selected_table_id, selected_server_id]):
                st.error("Please select table and server")
            else:
                # First create a party from the waiting list entry
                party_data = {
                    "name": next_party['customer_name'],
                    "size": next_party['party_size'],
                    "phone": next_party['customer_phone'],
                    "status": "WAITING"
                }
                
                party_result = api_client.create_party(party_data)
                if not party_result:
                    st.error("Failed to create party")
                    return
                
                # Then assign the table
                assignment_result = api_client.assign_table_to_party(
                    restaurant_id=restaurant_id,
                    table_id=selected_table_id,
                    party_id=party_result['id'],
                    server_id=selected_server_id,
                    notes=notes if notes else None
                )
                
                if assignment_result:
                    # Update waiting list entry status
                    api_client.update_waiting_list_entry(next_party['id'], {"status": "SEATED"})
                    st.success("Party seated successfully!")
                    st.rerun()
                else:
                    st.error("Failed to seat party. Please try again.")
    
    # Alternative actions
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Skip This Party", use_container_width=True):
            st.info("Skip functionality would be implemented here")
    
    with col2:
        if st.button("Update Wait Time", use_container_width=True):
            st.info("Update wait time functionality would be implemented here")
