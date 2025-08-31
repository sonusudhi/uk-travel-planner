import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
from PIL import Image

# Page configuration
st.set_page_config(
    page_title="UK Epic Christmas Trip - Finally Shine is Leaving!",
    page_icon="🎄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with background image
st.markdown("""
<style>
    .main-header {
        font-size: 3.5rem;
        color: #ffffff;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.7);
        background: linear-gradient(135deg, rgba(31,78,121,0.9), rgba(44,90,160,0.9));
        padding: 2rem;
        border-radius: 20px;
        backdrop-filter: blur(10px);
    }
    .main-container {
        background: linear-gradient(rgba(0,0,0,0.3), rgba(0,0,0,0.3)), url('1.jpg');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        min-height: 100vh;
        padding: 2rem 0;
    }
    .content-card {
        background: rgba(255,255,255,0.95);
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.2);
        backdrop-filter: blur(10px);
    }
    .day-card {
        background: rgba(255,255,255,0.98);
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        border-left: 5px solid #ff6b6b;
    }
    .cost-table {
        background: white;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .edit-section {
        background: linear-gradient(135deg, #f0f8ff, #e6f3ff);
        padding: 1.5rem;
        border-radius: 15px;
        border: 2px dashed #2c5aa0;
        margin: 1rem 0;
    }
    .price-table {
        background: white;
        border: 1px solid #ddd;
        border-radius: 8px;
        overflow: hidden;
    }
</style>
""", unsafe_allow_html=True)

# Main container with background
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# Title
st.markdown('''
<div class="main-header">
    🎄 UK Epic Christmas Trip 🎄<br>
    <h2 style="margin-top: 1rem; font-size: 2rem;">Finally Shine is Leaving the District, State and Country Hurray!</h2>
    <p style="font-size: 1.2rem; margin-top: 1rem;">Group of 4: Couple + 2 Individuals | Dec 25, 2024 - Jan 1, 2025</p>
</div>
''', unsafe_allow_html=True)

# Initialize session state for editable content
if 'itinerary_data' not in st.session_state:
    st.session_state.itinerary_data = {
        'flight_cost': 700,
        'group_size': 4,
        'trip_title': 'UK Epic Christmas Trip - Finally Shine is Leaving the District, State and Country Hurray',
        'days': {
            1: {'date': 'Dec 25', 'title': 'Christmas Day - Tower Thames Area', 'location': 'London'},
            2: {'date': 'Dec 26', 'title': 'Boxing Day - Royal London & Lights', 'location': 'London'},
            3: {'date': 'Dec 27', 'title': 'Final London + Travel North', 'location': 'London → Northallerton'},
            4: {'date': 'Dec 28', 'title': 'Northern England Tour', 'location': 'Durham, Newcastle, Whitby'},
            5: {'date': 'Dec 29', 'title': 'Edinburgh + Highland Travel', 'location': 'Edinburgh → Fort William'},
            6: {'date': 'Dec 30', 'title': 'Scottish Highlands', 'location': 'Fort William'},
            7: {'date': 'Dec 31', 'title': 'Edinburgh Hogmanay', 'location': 'Edinburgh'},
            8: {'date': 'Jan 1', 'title': 'Departure Day', 'location': 'Edinburgh → Bangalore'}
        }
    }

# Initialize cost data
if 'cost_data' not in st.session_state:
    st.session_state.cost_data = {
        'Flights': 700,
        'London Accommodation (3 nights)': 300,
        'Edinburgh/Highland Accommodation': 200,
        'Transport (all trains/buses)': 180,
        'Attractions': 150,
        'Food Budget': 350,
        'Shopping & Souvenirs': 200,
        'Emergency Fund': 100
    }

# Initialize price tables
if 'price_tables' not in st.session_state:
    st.session_state.price_tables = {
        'Day 1': {
            'activities': [
                {'Activity': 'Heathrow Express', 'Individual': 25, 'Couple': 50, 'Total_4': 100},
                {'Activity': 'Tower Bridge (walk)', 'Individual': 0, 'Couple': 0, 'Total_4': 0},
                {'Activity': 'Tower of London', 'Individual': 29.90, 'Couple': 59.80, 'Total_4': 119.60},
                {'Activity': 'London Eye', 'Individual': 32, 'Couple': 64, 'Total_4': 128},
                {'Activity': 'London Day Travel Card', 'Individual': 15, 'Couple': 30, 'Total_4': 60}
            ]
        },
        'Day 2': {
            'activities': [
                {'Activity': 'Buckingham Palace', 'Individual': 0, 'Couple': 0, 'Total_4': 0},
                {'Activity': 'Hyde Park Winter Wonderland', 'Individual': 0, 'Couple': 0, 'Total_4': 0},
                {'Activity': 'Ice Skating', 'Individual': 17, 'Couple': 34, 'Total_4': 68},
                {'Activity': 'London Day Travel Card', 'Individual': 15, 'Couple': 30, 'Total_4': 60}
            ]
        },
        'Day 3': {
            'activities': [
                {'Activity': 'The Shard', 'Individual': 32, 'Couple': 64, 'Total_4': 128},
                {'Activity': 'British Museum', 'Individual': 0, 'Couple': 0, 'Total_4': 0},
                {'Activity': 'Borough Market', 'Individual': 0, 'Couple': 0, 'Total_4': 0},
                {'Activity': 'Train to Northallerton', 'Individual': 45, 'Couple': 90, 'Total_4': 180},
                {'Activity': 'London Day Travel Card', 'Individual': 15, 'Couple': 30, 'Total_4': 60}
            ]
        },
        'Day 4': {
            'activities': [
                {'Activity': 'Train to Durham', 'Individual': 15, 'Couple': 30, 'Total_4': 60},
                {'Activity': 'Durham Cathedral', 'Individual': 0, 'Couple': 0, 'Total_4': 0},
                {'Activity': 'Train Durham-Newcastle', 'Individual': 8, 'Couple': 16, 'Total_4': 32},
                {'Activity': 'Bus Newcastle-Whitby', 'Individual': 12, 'Couple': 24, 'Total_4': 48},
                {'Activity': 'Whitby Abbey', 'Individual': 7.20, 'Couple': 14.40, 'Total_4': 28.80},
                {'Activity': 'Bus Whitby-Northallerton', 'Individual': 10, 'Couple': 20, 'Total_4': 40}
            ]
        },
        'Day 5': {
            'activities': [
                {'Activity': 'Train to Edinburgh', 'Individual': 35, 'Couple': 70, 'Total_4': 140},
                {'Activity': 'Edinburgh Castle', 'Individual': 19.50, 'Couple': 39, 'Total_4': 78},
                {'Activity': 'Royal Mile (free)', 'Individual': 0, 'Couple': 0, 'Total_4': 0},
                {'Activity': 'Train Edinburgh-Fort William', 'Individual': 45, 'Couple': 90, 'Total_4': 180},
                {'Activity': 'Fort William Accommodation', 'Individual': 40, 'Couple': 80, 'Total_4': 160}
            ]
        },
        'Day 6': {
            'activities': [
                {'Activity': 'Highland Day Tour', 'Individual': 65, 'Couple': 130, 'Total_4': 260},
                {'Activity': 'Glenfinnan Viaduct', 'Individual': 0, 'Couple': 0, 'Total_4': 0},
                {'Activity': 'Glen Coe Views', 'Individual': 0, 'Couple': 0, 'Total_4': 0},
                {'Activity': 'Fort William Accommodation', 'Individual': 40, 'Couple': 80, 'Total_4': 160}
            ]
        },
        'Day 7': {
            'activities': [
                {'Activity': 'Train Fort William-Edinburgh', 'Individual': 45, 'Couple': 90, 'Total_4': 180},
                {'Activity': 'Holyrood Palace', 'Individual': 17.50, 'Couple': 35, 'Total_4': 70},
                {'Activity': 'Arthur\'s Seat (free)', 'Individual': 0, 'Couple': 0, 'Total_4': 0},
                {'Activity': 'Hogmanay Street Party', 'Individual': 0, 'Couple': 0, 'Total_4': 0},
                {'Activity': 'Edinburgh Airport Hotel', 'Individual': 37.50, 'Couple': 75, 'Total_4': 150}
            ]
        },
        'Day 8': {
            'activities': [
                {'Activity': 'Airport Bus', 'Individual': 8, 'Couple': 16, 'Total_4': 32},
                {'Activity': 'Flight to Bangalore', 'Individual': 700, 'Couple': 1400, 'Total_4': 2800}
            ]
        }
    }

# Main content tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📅 Editable Itinerary", 
    "✈️ Flight Details", 
    "💰 Cost Calculator", 
    "📊 Editable Price Tables",
    "🗺️ Interactive Map"
])

# Tab 1: Editable Itinerary
with tab1:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown("# 📅 Editable Day-by-Day Itinerary")
    
    # Edit mode toggle
    edit_mode = st.toggle("✏️ Edit Mode", help="Turn on to edit itinerary details")
    
    if edit_mode:
        st.markdown('<div class="edit-section">', unsafe_allow_html=True)
        st.markdown("## ✏️ Edit Trip Details")
        
        # Editable trip details
        col1, col2 = st.columns(2)
        with col1:
            new_title = st.text_input("Trip Title", st.session_state.itinerary_data['trip_title'])
            new_flight_cost = st.number_input("Flight Cost (£ per person)", value=st.session_state.itinerary_data['flight_cost'])
        with col2:
            new_group_size = st.number_input("Group Size", value=st.session_state.itinerary_data['group_size'], min_value=1, max_value=20)
        
        # Update session state
        if st.button("💾 Save Changes"):
            st.session_state.itinerary_data['trip_title'] = new_title
            st.session_state.itinerary_data['flight_cost'] = new_flight_cost
            st.session_state.itinerary_data['group_size'] = new_group_size
            st.success("✅ Changes saved!")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Display itinerary days
    for day_num, day_info in st.session_state.itinerary_data['days'].items():
        with st.expander(f"Day {day_num}: {day_info['date']} - {day_info['title']}", expanded=True):
            
            if edit_mode:
                # Editable fields
                col1, col2, col3 = st.columns(3)
                with col1:
                    new_date = st.text_input(f"Date", day_info['date'], key=f"date_{day_num}")
                with col2:
                    new_title = st.text_input(f"Title", day_info['title'], key=f"title_{day_num}")
                with col3:
                    new_location = st.text_input(f"Location", day_info['location'], key=f"location_{day_num}")
                
                # Update button for each day
                if st.button(f"Update Day {day_num}", key=f"update_{day_num}"):
                    st.session_state.itinerary_data['days'][day_num]['date'] = new_date
                    st.session_state.itinerary_data['days'][day_num]['title'] = new_title
                    st.session_state.itinerary_data['days'][day_num]['location'] = new_location
                    st.success(f"✅ Day {day_num} updated!")
            else:
                # Display mode
                st.markdown(f"**Location:** {day_info['location']}")
                
                # Day-specific content
                if day_num == 1:
                    st.markdown("""
                    **13:20** - Arrive London (Qatar Airways)  
                    **15:00** - Heathrow Express to Central London  
                    **16:00** - Hotel check-in & freshen up  
                    **17:00** - **Lunch/Late Breakfast**  
                    **18:00** - **Tower Bridge** - Walk across, iconic photos  
                    **19:00** - **Tower of London** - Crown Jewels, Beefeaters  
                    **20:30** - **Walk to Westminster** along Thames  
                    **21:00** - **London Eye** - Christmas evening city views  
                    **22:30** - **Christmas Dinner**  
                    """)
                
                elif day_num == 2:
                    st.markdown("""
                    **09:00** - **Breakfast**  
                    **10:00** - **Tube to Green Park** → **Buckingham Palace**  
                    **11:30** - **St. James's Park walk**  
                    **12:30** - **Tube to Hyde Park Corner** → **Winter Wonderland**  
                    **14:00** - **Lunch** at Winter Wonderland  
                    **15:30** - **Tube to Oxford Circus** → **Oxford Street Christmas Lights**  
                    **16:30** - **Walk to Regent Street** → **Christmas Lights**  
                    **17:30** - **Walk to Covent Garden** → **Christmas Market**  
                    **18:30** - **Leicester Square** → **Christmas atmosphere**  
                    **20:00** - **Dinner** in West End  
                    """)
                
                elif day_num == 3:
                    st.markdown("""
                    **09:00** - **Breakfast**  
                    **10:00** - **Tube to London Bridge** → **The Shard**  
                    **11:30** - **Walk to Borough Market** (2 minutes)  
                    **12:30** - **Tube to Russell Square** → **British Museum**  
                    **14:00** - **Lunch** near British Museum  
                    **15:30** - **Tube to Fulham Broadway** → **Chelsea FC Stadium**  
                    **16:30** - **Return to hotel** & checkout  
                    **17:30** - **Train King's Cross → Northallerton** (2 hours)  
                    **20:00** - **Dinner** at host home  
                    """)
                
                elif day_num == 4:
                    st.markdown("""
                    **08:00** - **Breakfast**  
                    **09:00** - **Train Northallerton → Durham** (30 mins)  
                    **10:00** - **Durham Cathedral & Castle** - UNESCO site  
                    **11:30** - **Train Durham → Newcastle** (20 mins)  
                    **12:00** - **Newcastle Quayside & Tyne Bridge**  
                    **13:00** - **Lunch** in Newcastle  
                    **14:30** - **Bus Newcastle → Whitby** (2 hours)  
                    **16:30** - **Whitby Abbey & Harbor**  
                    **18:00** - **Bus Whitby → Northallerton** (1.5 hours)  
                    **20:00** - **Dinner** at host home  
                    """)
                
                elif day_num == 5:
                    st.markdown("""
                    **08:00** - **Breakfast**  
                    **09:00** - **Train Northallerton → Edinburgh** (2.5 hours via York)  
                    **12:00** - **Walk to Edinburgh Castle** (15 mins uphill)  
                    **12:30** - **Edinburgh Castle** - Scottish Crown Jewels  
                    **14:30** - **Walk down Royal Mile**  
                    **15:00** - **St. Giles Cathedral**  
                    **15:30** - **Lunch** on Royal Mile  
                    **16:30** - **Train Edinburgh → Fort William** (4 hours scenic)  
                    **20:30** - Check into Fort William accommodation  
                    **21:00** - **Dinner** in Fort William  
                    """)
                
                elif day_num == 6:
                    st.markdown("""
                    **08:00** - **Breakfast**  
                    **09:00** - **Highland Day Tour** (organized bus tour):  
                    - **Ben Nevis viewpoints**  
                    - **Glenfinnan Viaduct** (Harry Potter bridge)  
                    - **Glenfinnan Monument**  
                    **13:00** - **Lunch** during tour  
                    **14:30** - **Loch Shiel** - Highland loch views  
                    **16:00** - **Glen Coe** - Dramatic valley scenery  
                    **17:30** - **Commando Memorial** - Mountain panorama  
                    **19:00** - Return to Fort William  
                    **20:00** - **Dinner** in Fort William  
                    """)
                
                elif day_num == 7:
                    st.markdown("""
                    **08:00** - **Breakfast**  
                    **09:00** - **Train Fort William → Edinburgh** (4 hours)  
                    **13:00** - **Bus to Holyrood Palace**  
                    **13:30** - **Holyrood Palace** - Royal residence  
                    **15:00** - **Arthur's Seat hike** (if weather permits)  
                    **16:00** - **Lunch** in Edinburgh  
                    **17:00** - **Princes Street** - Shopping & atmosphere  
                    **18:00** - **Edinburgh Christmas Market**  
                    **19:30** - **Dinner** in Old Town  
                    **21:00** - **Edinburgh Hogmanay Street Party**  
                    **00:00** - **Midnight Fireworks** from Castle  
                    **01:00** - **Hotel near airport** (taxi/night bus)  
                    """)
                
                elif day_num == 8:
                    st.markdown("""
                    **07:00** - **Breakfast**  
                    **08:00** - **Airport bus to Edinburgh Airport**  
                    **09:00** - Airport check-in  
                    **10:20** - **Flight departure to Bangalore (British Airways)**  
                    **05:05+1** - **Arrive Bangalore** (next day)  
                    """)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Tab 2: Flight Details
with tab2:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown("# ✈️ Confirmed Flight Information")
    
    # Editable flight details
    if st.checkbox("✏️ Edit Flight Details"):
        st.markdown('<div class="edit-section">', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            outbound_date = st.date_input("Outbound Date", datetime(2024, 12, 25))
            outbound_time = st.time_input("Departure Time", datetime.strptime("03:55", "%H:%M").time())
            arrival_time = st.time_input("Arrival Time", datetime.strptime("13:20", "%H:%M").time())
            outbound_airline = st.text_input("Outbound Airline", "Qatar Airways")
        
        with col2:
            return_date = st.date_input("Return Date", datetime(2025, 1, 1))
            return_time = st.time_input("Return Departure", datetime.strptime("10:20", "%H:%M").time())
            return_arrival = st.time_input("Return Arrival", datetime.strptime("05:05", "%H:%M").time())
            return_airline = st.text_input("Return Airline", "British Airways")
        
        flight_cost = st.number_input("Total Flight Cost per Person (£)", value=700, step=50)
        
        if st.button("💾 Save Flight Details"):
            st.session_state.cost_data['Flights'] = flight_cost
            st.success("✅ Flight details saved!")
        
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        flight_cost = 700
    
    # Display flight information
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("## 🛫 OUTBOUND FLIGHT")
        st.markdown("### Trivandrum (TRV) → London (LHR)")
        st.write("**Date:** December 25, 2024")
        st.write("**Departure:** 03:55 AM IST")
        st.write("**Arrival:** 13:20 PM GMT")
        st.write("**Duration:** 14 hours 55 minutes")
        st.write("**Airline:** Qatar Airways")
    
    with col2:
        st.markdown("## 🛬 RETURN FLIGHT")
        st.markdown("### Edinburgh (EDI) → Bangalore (BLR)")
        st.write("**Date:** January 1, 2025")
        st.write("**Departure:** 10:20 AM GMT")
        st.write("**Arrival:** 05:05 AM IST (next day)")
        st.write("**Duration:** 13 hours 15 minutes")
        st.write("**Airline:** British Airways")
    
    # Cost summary
    st.markdown("## 💰 Flight Cost Summary")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Per Person (Return)", f"£{flight_cost}", "Complete round trip")
    with col2:
        st.metric("Total Group Cost", f"£{flight_cost * 4}", "4 people")
    with col3:
        st.metric("Cost in INR", f"₹{flight_cost * 4 * 105:,}", "Approx @₹105/£")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Tab 3: Cost Calculator
with tab3:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown("# 💰 Interactive Cost Calculator")
    
    # Editable cost categories
    st.markdown("## ✏️ Edit Cost Categories")
    
    # Editable cost inputs
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 💰 Major Expenses")
        for category in ['Flights', 'London Accommodation (3 nights)', 'Edinburgh/Highland Accommodation', 'Transport (all trains/buses)']:
            st.session_state.cost_data[category] = st.number_input(
                category, 
                value=st.session_state.cost_data[category], 
                step=25,
                key=f"cost_{category}"
            )
    
    with col2:
        st.markdown("### 💸 Variable Expenses")
        for category in ['Attractions', 'Food Budget', 'Shopping & Souvenirs', 'Emergency Fund']:
            st.session_state.cost_data[category] = st.number_input(
                category, 
                value=st.session_state.cost_data[category], 
                step=25,
                key=f"cost_{category}_2"
            )
    
    # Calculate and display totals
    total_per_person = sum(st.session_state.cost_data.values())
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Create cost pie chart
        fig = px.pie(
            values=list(st.session_state.cost_data.values()),
            names=list(st.session_state.cost_data.keys()),
            title="Cost Distribution per Person"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #f0f8ff, #e6f3ff); padding: 1.5rem; border-radius: 15px; text-align: center;">
            <h3>💵 Total Cost</h3>
            <h2>£{total_per_person:,.0f}</h2>
            <p><strong>Per Person</strong></p>
            
            <h2>£{total_per_person * 4:,.0f}</h2>
            <p><strong>Group of 4</strong></p>
            
            <hr>
            <h3>₹{total_per_person * 4 * 105:,.0f}</h3>
            <p><strong>Total in INR</strong></p>
            <small>@ ₹105 per £1</small>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Tab 4: Editable Price Tables
with tab4:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown("# 📊 Editable Day-wise Cost Tables")
    
    # Select day to edit
    day_select = st.selectbox("Select Day to Edit/View", 
                             options=list(st.session_state.price_tables.keys()),
                             key="day_select")
    
    st.markdown(f"## Day-wise Costs: {day_select}")
    
    # Edit mode for tables
    table_edit_mode = st.toggle("✏️ Edit Price Table", help="Turn on to edit prices")
    
    if table_edit_mode:
        st.markdown('<div class="edit-section">', unsafe_allow_html=True)
        st.markdown("### ✏️ Edit Activities and Prices")
        
        # Add new activity
        with st.expander("➕ Add New Activity"):
            new_activity = st.text_input("Activity Name")
            col1, col2, col3 = st.columns(3)
            with col1:
                new_individual = st.number_input("Individual Cost", value=0.0, step=0.10)
            with col2:
                new_couple = st.number_input("Couple Cost", value=0.0, step=0.10)
            with col3:
                new_total = st.number_input("Total (4 people)", value=0.0, step=0.10)
            
            if st.button("Add Activity"):
                st.session_state.price_tables[day_select]['activities'].append({
                    'Activity': new_activity,
                    'Individual': new_individual,
                    'Couple': new_couple,
                    'Total_4': new_total
                })
                st.success(f"✅ Added {new_activity}")
        
        # Edit existing activities
        activities = st.session_state.price_tables[day_select]['activities']
        
        for i, activity in enumerate(activities):
            with st.expander(f"✏️ Edit: {activity['Activity']}"):
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    new_name = st.text_input("Activity", activity['Activity'], key=f"name_{day_select}_{i}")
                with col2:
                    new_ind = st.number_input("Individual", activity['Individual'], step=0.10, key=f"ind_{day_select}_{i}")
                with col3:
                    new_coup = st.number_input("Couple", activity['Couple'], step=0.10, key=f"coup_{day_select}_{i}")
                with col4:
                    new_tot = st.number_input("Total 4", activity['Total_4'], step=0.10, key=f"tot_{day_select}_{i}")
                
                col_update, col_delete = st.columns(2)
                with col_update:
                    if st.button(f"Update", key=f"update_{day_select}_{i}"):
                        st.session_state.price_tables[day_select]['activities'][i] = {
                            'Activity': new_name,
                            'Individual': new_ind,
                            'Couple': new_coup,
                            'Total_4': new_tot
                        }
                        st.success(f"✅ Updated {new_name}")
                
                with col_delete:
                    if st.button(f"🗑️ Delete", key=f"delete_{day_select}_{i}"):
                        st.session_state.price_tables[day_select]['activities'].pop(i)
                        st.success("✅ Activity deleted")
                        st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Display price table
    if day_select in st.session_state.price_tables:
        activities_df = pd.DataFrame(st.session_state.price_tables[day_select]['activities'])
        
        if not activities_df.empty:
            # Format the dataframe for better display
            activities_df['Individual'] = activities_df['Individual'].apply(lambda x: f"£{x:.2f}" if x > 0 else "FREE")
            activities_df['Couple'] = activities_df['Couple'].apply(lambda x: f"£{x:.2f}" if x > 0 else "FREE")
            activities_df['Total_4'] = activities_df['Total_4'].apply(lambda x: f"£{x:.2f}" if x > 0 else "FREE")
            
            st.dataframe(activities_df, use_container_width=True, hide_index=True)
            
            # Calculate day total
            raw_activities = st.session_state.price_tables[day_select]['activities']
            day_total = sum(activity['Total_4'] for activity in raw_activities)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(f"{day_select} Total", f"£{day_total:.2f}", "For 4 people")
            with col2:
                st.metric("Per Person", f"£{day_total/4:.2f}", "Average cost")
            with col3:
                st.metric("In INR", f"₹{day_total * 105:,.0f}", "Total group cost")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Tab 5: Interactive Map
with tab5:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown("# 🗺️ Interactive Travel Route Map")
    
    # Create map with travel route
    m = folium.Map(location=[54.5, -2.5], zoom_start=6)
    
    # Add key locations with custom markers
    locations = {
        "London": {"coords": [51.5074, -0.1278], "color": "red", "icon": "star", "popup": "Days 1-3: Christmas & Boxing Day"},
        "Northallerton": {"coords": [54.3394, -1.4324], "color": "green", "icon": "home", "popup": "Host Home Base"},
        "Durham": {"coords": [54.7761, -1.5733], "color": "blue", "icon": "university", "popup": "Day 4: UNESCO Cathedral"},
        "Newcastle": {"coords": [54.9783, -1.6178], "color": "blue", "icon": "building", "popup": "Day 4: Tyne Bridge"},
        "Whitby": {"coords": [54.4858, -0.6206], "color": "purple", "icon": "anchor", "popup": "Day 4: Abbey & Harbor"},
        "Edinburgh": {"coords": [55.9533, -3.1883], "color": "orange", "icon": "castle", "popup": "Days 5&7: Castle & Hogmanay"},
        "Fort William": {"coords": [56.8198, -5.1052], "color": "darkgreen", "icon": "mountain", "popup": "Days 5-6: Highland Base"}
    }
    
    for name, details in locations.items():
        folium.Marker(
            details["coords"],
            popup=f"<b>{name}</b><br>{details['popup']}",
            tooltip=name,
            icon=folium.Icon(color=details["color"], icon=details["icon"])
        ).add_to(m)
    
    # Add travel routes
    routes = [
        {"coords": [[51.5074, -0.1278], [54.3394, -1.4324]], "color": "green", "tooltip": "London → Northallerton"},
        {"coords": [[54.3394, -1.4324], [54.7761, -1.5733]], "color": "blue", "tooltip": "Northallerton → Durham"},
        {"coords": [[54.7761, -1.5733], [54.9783, -1.6178]], "color": "blue", "tooltip": "Durham → Newcastle"},
        {"coords": [[54.9783, -1.6178], [54.4858, -0.6206]], "color": "purple", "tooltip": "Newcastle → Whitby"},
        {"coords": [[54.3394, -1.4324], [55.9533, -3.1883]], "color": "orange", "tooltip": "Northallerton → Edinburgh"},
        {"coords": [[55.9533, -3.1883], [56.8198, -5.1052]], "color": "darkgreen", "tooltip": "Edinburgh → Fort William"},
        {"coords": [[56.8198, -5.1052], [55.9533, -3.1883]], "color": "red", "tooltip": "Fort William → Edinburgh"}
    ]
    
    for route in routes:
        folium.PolyLine(
            locations=route["coords"],
            color=route["color"],
            weight=4,
            tooltip=route["tooltip"]
        ).add_to(m)
    
    st_folium(m, width=700, height=500)
    
    # Map legend
    st.markdown("### 🗺️ Map Legend")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**🔴 London** - Christmas & Boxing Day")
        st.markdown("**🟢 Northallerton** - Host home base")
    with col2:
        st.markdown("**🔵 Durham/Newcastle** - Northern England")
        st.markdown("**🟣 Whitby** - Yorkshire coast")
    with col3:
        st.markdown("**🟠 Edinburgh** - Scottish capital")
        st.markdown("**🟢 Fort William** - Highland adventures")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Sidebar with quick stats
with st.sidebar:
    st.markdown("## 📊 Trip Overview")
    
    try:
        # Load and display the background image in sidebar too
        image = Image.open("1.jpg")
        st.image(image, caption="Your Epic Travel Group!", use_column_width=True)
    except:
        st.info("📸 Upload 1.jpg to see group photo")
    
    st.metric("Days", "8")
    st.metric("Cities", "7")
    st.metric("Countries", "1 (UK)")
    st.metric("Group Size", "4 people")
    st.metric("Flight Cost", f"£{st.session_state.cost_data['Flights']}")
    
    # Quick edit flight cost
    if st.checkbox("💰 Quick Edit Flight Cost"):
        new_flight_cost = st.number_input("New Flight Cost", value=st.session_state.cost_data['Flights'], step=50)
        if st.button("Update Flight Cost"):
            st.session_state.cost_data['Flights'] = new_flight_cost
            st.success("✅ Updated!")
    
    st.markdown("---")
    st.markdown("## 🎯 Quick Actions")
    
    if st.button("🔄 Reset All Data"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.success("✅ All data reset!")
        st.rerun()
    
    if st.button("💾 Export Summary"):
        st.success("📋 Export feature coming soon!")
    
    st.markdown("---")
    st.success("✅ Live editable travel planner")
    st.info("🎄 Epic Christmas adventure awaits!")

# Footer
st.markdown('<div class="content-card">', unsafe_allow_html=True)
footer_text = f"""
# 🎄 Have the Most Epic UK Christmas Adventure! 🎄

**Finally Shine is Leaving the District, State and Country - What an Achievement!**

## 📋 Trip Summary:
- **📅 Duration:** 8 days (Dec 25, 2024 - Jan 1, 2025)
- **👥 Group:** 4 people (Couple + 2 individuals)
- **✈️ Route:** Trivandrum → London → Edinburgh → Bangalore
- **🎯 Highlights:** Christmas in London, Yorkshire coast, Scottish Highlands, Edinburgh Hogmanay

## ✈️ Flight Summary:
- **Outbound:** Dec 25, 03:55 IST (Trivandrum) → 13:20 GMT (London)
- **Return:** Jan 1, 10:20 GMT (Edinburgh) → Jan 2, 05:05 IST (Bangalore)  
- **Total Cost:** £{st.session_state.cost_data['Flights']} per person | £{st.session_state.cost_data['Flights'] * 4} for group

## 🎉 Special Experiences:
- **Christmas Day** in London with Tower Bridge & London Eye
- **Boxing Day** at Hyde Park Winter Wonderland
- **Yorkshire Coast** adventure at Whitby Abbey
- **Scottish Highlands** with Glenfinnan Viaduct (Harry Potter location)
- **Edinburgh Hogmanay** - World's best New Year celebration

## 📞 Emergency Support:
- **UK Emergency:** 999 | **Indian High Commission:** +44 20 7836 8484

---
*Generated on: {datetime.now().strftime("%B %d, %Y at %I:%M %p")}*  
*⚡ Fully editable travel planner - customize as needed!*
"""

st.markdown(footer_text)
st.markdown('</div>', unsafe_allow_html=True)

# Close main container
st.markdown('</div>', unsafe_allow_html=True)
