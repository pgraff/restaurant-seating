"""
Reservations management page
Allows adding, editing, and removing reservations
"""

import streamlit as st
import sys
import os
from datetime import datetime, date, timedelta

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api_client import RestaurantAPIClient

def show():
    """Display the reservations management page"""
    st.markdown('<h1 class="main-header">Reservation Management</h1>', unsafe_allow_html=True)
    
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
    tab1, tab2, tab3 = st.tabs(["View Reservations", "Add New Reservation", "Edit Reservation"])
    
    with tab1:
        show_reservations_list(api_client, selected_restaurant_id)
    
    with tab2:
        show_add_reservation_form(api_client, selected_restaurant_id)
    
    with tab3:
        show_edit_reservation_form(api_client, selected_restaurant_id)

def show_reservations_list(api_client, restaurant_id):
    """Display list of reservations"""
    st.subheader("Current Reservations")
    
    # Date filter
    col1, col2 = st.columns([1, 3])
    with col1:
        date_filter = st.date_input("Filter by Date:", value=date.today())
    with col2:
        status_filter = st.selectbox("Filter by Status:", 
                                   ["All", "CONFIRMED", "PENDING", "CANCELLED", "COMPLETED", "NO_SHOW"])
    
    # Get reservations
    reservations = api_client.get_reservations(
        restaurant_id=restaurant_id,
        date_filter=date_filter,
        status=status_filter if status_filter != "All" else None
    )
    
    if not reservations:
        st.info("No reservations found for the selected criteria")
        return
    
    # Display reservations
    for i, reservation in enumerate(reservations):
        with st.expander(f"Reservation {i+1}: {reservation['customer_name']} - {reservation['reservation_time'][:16]}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Customer:** {reservation['customer_name']}")
                st.write(f"**Phone:** {reservation['customer_phone']}")
                st.write(f"**Email:** {reservation.get('customer_email', 'N/A')}")
                st.write(f"**Party Size:** {reservation['party_size']}")
            
            with col2:
                st.write(f"**Reservation Time:** {reservation['reservation_time'][:16]}")
                st.write(f"**Status:** {reservation['status']}")
                st.write(f"**Created:** {reservation['created_at'][:16]}")
                if reservation.get('special_requests'):
                    st.write(f"**Special Requests:** {reservation['special_requests']}")
            
            # Action buttons
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button(f"Edit", key=f"edit_{reservation['id']}"):
                    st.session_state.edit_reservation_id = reservation['id']
                    st.rerun()
            
            with col2:
                if st.button(f"Cancel", key=f"cancel_{reservation['id']}"):
                    if api_client.cancel_reservation(reservation['id']):
                        st.success("Reservation cancelled successfully")
                        st.rerun()
                    else:
                        st.error("Failed to cancel reservation")
            
            with col3:
                if st.button(f"Delete", key=f"delete_{reservation['id']}"):
                    if api_client.cancel_reservation(reservation['id']):
                        st.success("Reservation deleted successfully")
                        st.rerun()
                    else:
                        st.error("Failed to delete reservation")

def show_add_reservation_form(api_client, restaurant_id):
    """Display form to add new reservation"""
    st.subheader("Add New Reservation")
    
    with st.form("add_reservation_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            customer_name = st.text_input("Customer Name *", placeholder="Enter customer name")
            customer_phone = st.text_input("Phone Number *", placeholder="Enter phone number")
            customer_email = st.text_input("Email Address", placeholder="Enter email address")
            party_size = st.number_input("Party Size *", min_value=1, max_value=20, value=2)
        
        with col2:
            reservation_date = st.date_input("Reservation Date *", value=date.today())
            reservation_time = st.time_input("Reservation Time *", value=datetime.now().time())
            special_requests = st.text_area("Special Requests", placeholder="Any special requests or notes")
        
        # Combine date and time
        reservation_datetime = datetime.combine(reservation_date, reservation_time)
        
        submitted = st.form_submit_button("Create Reservation", use_container_width=True)
        
        if submitted:
            if not all([customer_name, customer_phone, party_size]):
                st.error("Please fill in all required fields (marked with *)")
            else:
                reservation_data = {
                    "restaurant_id": restaurant_id,
                    "customer_name": customer_name,
                    "customer_phone": customer_phone,
                    "customer_email": customer_email if customer_email else None,
                    "party_size": party_size,
                    "reservation_time": reservation_datetime.isoformat(),
                    "special_requests": special_requests if special_requests else None
                }
                
                result = api_client.create_reservation(reservation_data)
                if result:
                    st.success("Reservation created successfully!")
                    st.rerun()
                else:
                    st.error("Failed to create reservation. Please check the details and try again.")

def show_edit_reservation_form(api_client, restaurant_id):
    """Display form to edit existing reservation"""
    st.subheader("Edit Reservation")
    
    # Get reservations for selection
    reservations = api_client.get_reservations(restaurant_id=restaurant_id)
    
    if not reservations:
        st.info("No reservations found to edit")
        return
    
    # Reservation selector
    reservation_options = {
        f"{r['customer_name']} - {r['reservation_time'][:16]}": r for r in reservations
    }
    selected_reservation_name = st.selectbox("Select Reservation to Edit:", list(reservation_options.keys()))
    selected_reservation = reservation_options[selected_reservation_name]
    
    if not selected_reservation:
        return
    
    # Pre-fill form with existing data
    with st.form("edit_reservation_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            customer_name = st.text_input("Customer Name *", value=selected_reservation['customer_name'])
            customer_phone = st.text_input("Phone Number *", value=selected_reservation['customer_phone'])
            customer_email = st.text_input("Email Address", value=selected_reservation.get('customer_email', ''))
            party_size = st.number_input("Party Size *", min_value=1, max_value=20, 
                                       value=selected_reservation['party_size'])
        
        with col2:
            # Parse existing datetime
            existing_datetime = datetime.fromisoformat(selected_reservation['reservation_time'].replace('Z', '+00:00'))
            reservation_date = st.date_input("Reservation Date *", value=existing_datetime.date())
            reservation_time = st.time_input("Reservation Time *", value=existing_datetime.time())
            special_requests = st.text_area("Special Requests", 
                                          value=selected_reservation.get('special_requests', ''))
            status = st.selectbox("Status", 
                                ["CONFIRMED", "PENDING", "CANCELLED", "COMPLETED", "NO_SHOW"],
                                index=["CONFIRMED", "PENDING", "CANCELLED", "COMPLETED", "NO_SHOW"].index(selected_reservation['status']))
        
        # Combine date and time
        reservation_datetime = datetime.combine(reservation_date, reservation_time)
        
        submitted = st.form_submit_button("Update Reservation", use_container_width=True)
        
        if submitted:
            if not all([customer_name, customer_phone, party_size]):
                st.error("Please fill in all required fields (marked with *)")
            else:
                reservation_data = {
                    "customer_name": customer_name,
                    "customer_phone": customer_phone,
                    "customer_email": customer_email if customer_email else None,
                    "party_size": party_size,
                    "reservation_time": reservation_datetime.isoformat(),
                    "special_requests": special_requests if special_requests else None,
                    "status": status
                }
                
                result = api_client.update_reservation(selected_reservation['id'], reservation_data)
                if result:
                    st.success("Reservation updated successfully!")
                    st.rerun()
                else:
                    st.error("Failed to update reservation. Please check the details and try again.")
