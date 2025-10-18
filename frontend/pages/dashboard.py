"""
Dashboard page for the Restaurant Seating System
Shows overview metrics and current status
"""

import streamlit as st
import sys
import os
from datetime import datetime, date, timedelta

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api_client import RestaurantAPIClient

def show():
    """Display the dashboard page"""
    st.markdown('<h1 class="main-header">Restaurant Dashboard</h1>', unsafe_allow_html=True)
    
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
    
    # Get restaurant details
    restaurant = api_client.get_restaurant(selected_restaurant_id)
    if not restaurant:
        st.error("Failed to load restaurant details")
        return
    
    # Display restaurant info
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Restaurant", restaurant['name'])
    
    with col2:
        st.metric("Max Capacity", restaurant['max_capacity'])
    
    with col3:
        st.metric("Opening Time", restaurant['opening_time'])
    
    with col4:
        st.metric("Closing Time", restaurant['closing_time'])
    
    st.markdown("---")
    
    # Get current data
    tables = api_client.get_tables(selected_restaurant_id)
    reservations = api_client.get_reservations(restaurant_id=selected_restaurant_id, 
                                             date_filter=date.today())
    waiting_list = api_client.get_waiting_list(restaurant_id=selected_restaurant_id, 
                                             status="WAITING")
    
    # Calculate metrics
    total_tables = len(tables)
    occupied_tables = len([t for t in tables if t['status'] == 'OCCUPIED'])
    available_tables = len([t for t in tables if t['status'] == 'AVAILABLE'])
    reserved_tables = len([t for t in tables if t['status'] == 'RESERVED'])
    
    today_reservations = len([r for r in reservations if r['status'] == 'CONFIRMED'])
    waiting_parties = len(waiting_list)
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Tables", total_tables)
        st.metric("Available", available_tables)
    
    with col2:
        st.metric("Occupied", occupied_tables)
        st.metric("Reserved", reserved_tables)
    
    with col3:
        st.metric("Today's Reservations", today_reservations)
        st.metric("Waiting Parties", waiting_parties)
    
    with col4:
        occupancy_rate = (occupied_tables / total_tables * 100) if total_tables > 0 else 0
        st.metric("Occupancy Rate", f"{occupancy_rate:.1f}%")
    
    st.markdown("---")
    
    # Table status overview
    st.subheader("Table Status Overview")
    
    if tables:
        # Create table status data
        table_data = []
        for table in tables:
            table_data.append({
                "Table Number": table['table_number'],
                "Capacity": table['capacity'],
                "Status": table['status'],
                "Location": table['location']
            })
        
        st.dataframe(table_data, use_container_width=True)
    else:
        st.info("No tables configured for this restaurant")
    
    # Recent reservations
    st.subheader("Today's Reservations")
    
    if reservations:
        reservation_data = []
        for res in reservations[:10]:  # Show only first 10
            reservation_data.append({
                "Time": res['reservation_time'][:16],  # Remove seconds
                "Customer": res['customer_name'],
                "Party Size": res['party_size'],
                "Status": res['status'],
                "Phone": res['customer_phone']
            })
        
        st.dataframe(reservation_data, use_container_width=True)
    else:
        st.info("No reservations for today")
    
    # Waiting list
    if waiting_parties > 0:
        st.subheader("Current Waiting List")
        
        waiting_data = []
        for party in waiting_list[:10]:  # Show only first 10
            waiting_data.append({
                "Customer": party['customer_name'],
                "Party Size": party['party_size'],
                "Wait Time": f"{party.get('estimated_wait_time', 0)} min",
                "Request Time": party['request_time'][:16]
            })
        
        st.dataframe(waiting_data, use_container_width=True)
    
    # Quick actions
    st.subheader("Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Add New Reservation", use_container_width=True):
            st.session_state.page = "Reservations"
            st.rerun()
    
    with col2:
        if st.button("Manage Tables", use_container_width=True):
            st.session_state.page = "Table Assignment"
            st.rerun()
    
    with col3:
        if st.button("View Waiting List", use_container_width=True):
            st.session_state.page = "Waiting List"
            st.rerun()
