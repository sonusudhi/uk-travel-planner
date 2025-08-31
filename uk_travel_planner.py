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

# Custom CSS with proper background and clean styling
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.4), rgba(0,0,0,0.4)), url('1.jpg');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    .main-header {
        font-size: 3.5rem;
        color: #ffffff;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.9);
        background: linear-gradient(135deg, rgba(31,78,121,0.95), rgba(44,90,160,0.95));
        padding: 2rem;
        border-radius: 20px;
        backdrop-filter: blur(15px);
        border: 2px solid rgba(255,255,255,0.2);
    }
    .content-card {
        background: rgba(255,255,255,0.98);
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.3);
    }
    .edit-section {
        background: linear-gradient(135deg, #f0f8ff, #e6f3ff);
        padding: 1.5rem;
        border-radius: 15px;
        border: 2px dashed #2c5aa0;
        margin: 1rem 0;
    }
    .cost-summary {
        background: linear-gradient(135deg, #e8f5e8, #d4edda);
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        border: 2px solid #28a745;
        margin: 1rem 0;
    }
    .place-image {
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        margin: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('''
<div class="main-header">
    🎄 UK Epic Christmas Trip 🎄<br>
    <h2 style="margin-top: 1rem; font-size: 2rem; text-shadow: 2px 2px 4px rgba(0,0,0,0.8);">Finally Shine is Leaving the District, State and Country Hurray!</h2>
    <p style="font-size: 1.2rem; margin-top: 1rem; text-shadow: 1px 1px 2px rgba(0,0,0,0.8);">Group of 4: Couple + 2 Individuals | Dec 25, 2024 - Jan 1, 2025</p>
</div>
''', unsafe_allow_html=True)

# Initialize session state for editable content
if 'cost_data' not in st.session_state:
    st.session_state.cost_data = {
        'Flights': 600,
        'London Accommodation (3 nights)': 300,
        'Edinburgh/Highland Accommodation': 200,
        'Transport (all trains/buses)': 180,
        'Attractions': 150,
        'Food Budget': 350,
        'Shopping & Souvenirs': 200,
        'Emergency Fund': 100
    }

# Initialize daily cost tables
if 'daily_costs' not in st.session_state:
    st.session_state.daily_costs = {
        'Day 1 - Christmas London': [
            {'Activity': 'Heathrow Express', 'Individual': 25, 'Couple': 50, 'Total_4': 100},
            {'Activity': 'Tower Bridge (walk)', 'Individual': 0, 'Couple': 0, 'Total_4': 0},
            {'Activity': 'Tower of London', 'Individual': 29.90, 'Couple': 59.80, 'Total_4': 119.60},
            {'Activity': 'London Eye', 'Individual': 32, 'Couple': 64, 'Total_4': 128},
            {'Activity': 'London Day Travel Card', 'Individual': 15, 'Couple': 30, 'Total_4': 60}
        ],
        'Day 2 - Boxing Day London': [
            {'Activity': 'Buckingham Palace', 'Individual': 0, 'Couple': 0, 'Total_4': 0},
            {'Activity': 'Hyde Park Winter Wonderland', 'Individual': 0, 'Couple': 0, 'Total_4': 0},
            {'Activity': 'Ice Skating', 'Individual': 17, 'Couple': 34, 'Total_4': 68},
            {'Activity': 'London Day Travel Card', 'Individual': 15, 'Couple': 30, 'Total_4': 60}
        ],
        'Day 3 - Final London': [
            {'Activity': 'The Shard', 'Individual': 32, 'Couple': 64, 'Total_4': 128},
            {'Activity': 'British Museum', 'Individual': 0, 'Couple': 0, 'Total_4': 0},
            {'Activity': 'Chelsea FC Stadium', 'Individual': 0, 'Couple': 0, 'Total_4': 0},
            {'Activity': 'Train to Northallerton', 'Individual': 45, 'Couple': 90, 'Total_4': 180},
            {'Activity': 'London Day Travel Card', 'Individual': 15, 'Couple': 30, 'Total_4': 60}
        ],
        'Day 4 - Northern England': [
            {'Activity': 'Train to Durham', 'Individual': 15, 'Couple': 30, 'Total_4': 60},
            {'Activity': 'Durham Cathedral', 'Individual': 0, 'Couple': 0, 'Total_4': 0},
            {'Activity': 'Train Durham-Newcastle', 'Individual': 8, 'Couple': 16, 'Total_4': 32},
            {'Activity': 'Bus Newcastle-Whitby', 'Individual': 12, 'Couple': 24, 'Total_4': 48},
            {'Activity': 'Whitby Abbey', 'Individual': 7.20, 'Couple': 14.40, 'Total_4': 28.80},
            {'Activity': 'Bus Whitby-Northallerton', 'Individual': 10, 'Couple': 20, 'Total_4': 40}
        ],
        'Day 5 - Edinburgh to Highlands': [
            {'Activity': 'Train to Edinburgh', 'Individual': 35, 'Couple': 70, 'Total_4': 140},
            {'Activity': 'Edinburgh Castle', 'Individual': 19.50, 'Couple': 39, 'Total_4': 78},
            {'Activity': 'Train Edinburgh-Fort William', 'Individual': 45, 'Couple': 90, 'Total_4': 180},
            {'Activity': 'Fort William Accommodation', 'Individual': 40, 'Couple': 80, 'Total_4': 160}
        ],
        'Day 6 - Scottish Highlands': [
            {'Activity': 'Highland Day Tour', 'Individual': 65, 'Couple': 130, 'Total_4': 260},
            {'Activity': 'Ben Nevis Views', 'Individual': 0, 'Couple': 0, 'Total_4': 0},
            {'Activity': 'Glenfinnan Viaduct', 'Individual': 0, 'Couple': 0, 'Total_4': 0},
            {'Activity': 'Glen Coe Views', 'Individual': 0, 'Couple': 0, 'Total_4': 0},
            {'Activity': 'Fort William Accommodation', 'Individual': 40, 'Couple': 80, 'Total_4': 160}
        ],
        'Day 7 - Edinburgh Hogmanay': [
            {'Activity': 'Train Fort William-Edinburgh', 'Individual': 45, 'Couple': 90, 'Total_4': 180},
            {'Activity': 'Holyrood Palace', 'Individual': 17.50, 'Couple': 35, 'Total_4': 70},
            {'Activity': 'Arthur\'s Seat (free)', 'Individual': 0, 'Couple': 0, 'Total_4': 0},
            {'Activity': 'Hogmanay Street Party', 'Individual': 0, 'Couple': 0, 'Total_4': 0},
            {'Activity': 'Edinburgh Airport Hotel', 'Individual': 37.50, 'Couple': 75, 'Total_4': 150}
        ],
        'Day 8 - Departure': [
            {'Activity': 'Airport Bus', 'Individual': 8, 'Couple': 16, 'Total_4': 32}
        ]
    }

# Main content tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📅 Day-by-Day Itinerary", 
    "✈️ Flight Details", 
    "💰 Cost Calculator", 
    "📊 Editable Price Tables",
    "🖼️ Place Images",
    "🗺️ Interactive Map"
])

# Tab 1: Clean Itinerary
with tab1:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown("# 📅 Complete 8-Day Itinerary")
    
    # Day 1
    st.markdown("## 🎄 Day 1: Christmas Day - December 25")
    st.markdown("**Location:** Trivandrum → London")
    st.markdown("### Tower Thames Area (All Walking Distance)")
    
    st.write("**03:55 IST** - Departure from Trivandrum (Qatar Airways)")
    st.write("**13:20 GMT** - Arrive London")
    st.write("**15:00** - Heathrow Express to Central London")
    st.write("**16:00** - Hotel check-in & freshen up")
    st.write("**17:00** - **Lunch/Late Breakfast**")
    st.write("**18:00** - **Tower Bridge** - Walk across, iconic Christmas photos")
    st.write("**19:00** - **Tower of London** - Crown Jewels, Beefeaters (5-min walk)")
    st.write("**20:30** - **Walk along Thames to Westminster** (20 mins riverside)")
    st.write("**21:00** - **London Eye** - Christmas evening panoramic views")
    st.write("**22:30** - **Christmas Dinner**")
    
    st.info("💡 Christmas Day: Limited tube services, but all these attractions walkable along Thames")
    st.markdown("---")
    
    # Day 2
    st.markdown("## 🎁 Day 2: Boxing Day - December 26")
    st.markdown("**Location:** London")
    st.markdown("### Royal London & Christmas Lights Circuit")
    
    st.write("**09:00** - **Breakfast**")
    st.write("**10:00** - **Tube to Green Park** → **Buckingham Palace** - Guard changing, royal atmosphere")
    st.write("**11:30** - **Walk through St. James's Park** - Royal park, lake views")
    st.write("**12:30** - **Tube to Hyde Park Corner** → **Hyde Park Winter Wonderland**")
    st.write("**14:00** - **Lunch** at Winter Wonderland")
    st.write("**15:30** - **Ice skating** and Christmas market exploration")
    st.write("**16:30** - **Tube to Oxford Circus** → **Oxford Street Christmas Lights**")
    st.write("**17:00** - **Walk to Regent Street** → **Regent Street Christmas Lights**")
    st.write("**17:30** - **Walk to Covent Garden** → **Christmas Market, street performers**")
    st.write("**18:30** - **Walk to Leicester Square** → **Christmas decorations and buzz**")
    st.write("**20:00** - **Dinner** in West End area")
    
    st.success("✅ Perfect Boxing Day when everything reopens and Winter Wonderland is fully operational")
    st.markdown("---")
    
    # Day 3
    st.markdown("## 🏛️ Day 3: December 27")
    st.markdown("**Location:** London → Northallerton")
    st.markdown("### Final London Highlights")
    
    st.write("**09:00** - **Breakfast**")
    st.write("**10:00** - **Tube to London Bridge** → **The Shard** - Europe's tallest building views")
    st.write("**11:30** - **Walk to Borough Market** (2-minute walk) - Historic food market")
    st.write("**12:30** - **Tube to Russell Square** → **British Museum** - World artifacts, Egyptian collection")
    st.write("**14:00** - **Lunch** near British Museum")
    st.write("**15:30** - **Tube to Fulham Broadway** → **Chelsea FC Stadium (exterior)** - Quick photos")
    st.write("**16:30** - **Return to hotel** & checkout, collect luggage")
    st.write("**17:30** - **Train King's Cross → Northallerton** (2 hours direct)")
    st.write("**20:00** - **Dinner** at host home")
    
    st.markdown("---")
    
    # Day 4
    st.markdown("## 🏰 Day 4: December 28")
    st.markdown("**Location:** Northern England Triangle")
    st.markdown("### Durham, Newcastle & Whitby Public Transport Tour")
    
    st.write("**08:00** - **Breakfast**")
    st.write("**09:00** - **Train Northallerton → Durham** (30 minutes)")
    st.write("**10:00** - **Durham Cathedral & Castle** - UNESCO World Heritage site, Norman architecture")
    st.write("**11:30** - **Train Durham → Newcastle** (20 minutes)")
    st.write("**12:00** - **Newcastle Quayside & Tyne Bridge** - Walk from Central Station")
    st.write("**13:00** - **Lunch** in Newcastle city center")
    st.write("**14:30** - **Bus Newcastle → Whitby** (2 hours via Middlesbrough)")
    st.write("**16:30** - **Whitby Abbey** - Dramatic clifftop ruins, Dracula connections")
    st.write("**17:30** - **Whitby Harbor** - Picturesque fishing port, Captain Cook heritage")
    st.write("**18:00** - **Bus Whitby → Northallerton** (1.5 hours direct)")
    st.write("**20:00** - **Dinner** at host home")
    
    st.markdown("---")
    
    # Day 5
    st.markdown("## 🏴󠁧󠁢󠁳󠁣󠁴󠁿 Day 5: December 29")
    st.markdown("**Location:** Edinburgh → Scottish Highlands")
    st.markdown("### Edinburgh Castle & Highland Railway Journey")
    
    st.write("**08:00** - **Breakfast**")
    st.write("**09:00** - **Train Northallerton → Edinburgh** (2.5 hours, change at York)")
    st.write("**12:00** - **Walk from Waverley Station to Edinburgh Castle** (15-minute uphill walk)")
    st.write("**12:30** - **Edinburgh Castle** - Scottish Crown Jewels, Stone of Destiny, city views")
    st.write("**14:30** - **Walk down Royal Mile** - Historic street from castle to palace")
    st.write("**15:00** - **St. Giles Cathedral** - Scotland's High Kirk (free entry)")
    st.write("**15:30** - **Lunch** on Royal Mile")
    st.write("**16:30** - **Train Edinburgh → Fort William** (4 hours - scenic West Highland Line)")
    st.write("**20:30** - Check into Fort William Highland accommodation")
    st.write("**21:00** - **Dinner** in Fort William")
    
    st.success("🚂 One of the world's most beautiful train journeys - West Highland Line!")
    st.markdown("---")
    
    # Day 6
    st.markdown("## 🏔️ Day 6: December 30")
    st.markdown("**Location:** Scottish Highlands")
    st.markdown("### Full Highland Adventure Day")
    
    st.write("**08:00** - **Breakfast**")
    st.write("**09:00** - **Highland Day Tour** (organized bus tour from Fort William):")
    st.write("  - **Ben Nevis area** - UK's highest mountain viewpoints")
    st.write("  - **Glenfinnan Viaduct** - Famous Harry Potter filming location")
    st.write("  - **Glenfinnan Monument** - Bonnie Prince Charlie memorial")
    st.write("**13:00** - **Lunch** during tour with Highland scenery")
    st.write("**14:30** - **Loch Shiel** - Beautiful Highland loch, boat trip option")
    st.write("**16:00** - **Glen Coe** - Dramatic valley, 'Scotland in Miniature'")
    st.write("**17:30** - **Commando Memorial** - WWII memorial with mountain panorama")
    st.write("**19:00** - Return to Fort William")
    st.write("**20:00** - **Dinner** in Fort William")
    
    st.info("🎬 Perfect day for Harry Potter fans and Highland scenery lovers!")
    st.markdown("---")
    
    # Day 7
    st.markdown("## 🎆 Day 7: December 31 - New Year's Eve")
    st.markdown("**Location:** Fort William → Edinburgh")
    st.markdown("### Edinburgh Hogmanay Preparation")
    
    st.write("**08:00** - **Breakfast**")
    st.write("**09:00** - **Train Fort William → Edinburgh** (4 hours scenic return journey)")
    st.write("**13:00** - **Bus/walk to Holyrood Palace** from Waverley Station")
    st.write("**13:30** - **Holyrood Palace** - Official royal residence in Scotland")
    st.write("**15:00** - **Arthur's Seat hike** - Ancient volcano, panoramic Edinburgh views (weather permitting)")
    st.write("**16:00** - **Lunch** in Edinburgh city center")
    st.write("**17:00** - **Princes Street** - Main shopping street, New Year atmosphere")
    st.write("**18:00** - **Edinburgh Christmas Market** (if still running)")
    st.write("**19:30** - **Dinner** in Edinburgh Old Town")
    st.write("**21:00** - **Edinburgh Hogmanay Street Party** - World-famous NYE celebration")
    st.write("**00:00** - **Midnight Fireworks from Edinburgh Castle** - Viewed from Royal Mile")
    st.write("**01:00** - **Hotel near Edinburgh Airport** (taxi/night bus)")
    
    st.warning("🎉 Book Hogmanay dinner reservations in advance! Dress very warmly for outdoor celebration!")
    st.markdown("---")
    
    # Day 8
    st.markdown("## ✈️ Day 8: January 1 - New Year's Day Departure")
    st.markdown("**Location:** Edinburgh → Bangalore")
    
    st.write("**07:00** - **Breakfast**")
    st.write("**08:00** - **Airport bus to Edinburgh Airport**")
    st.write("**09:00** - Airport check-in and security")
    st.write("**10:20** - **Flight departure to Bangalore (British Airways)**")
    st.write("**05:05+1** - **Arrive Bangalore** (next day)")
    
    st.success("✅ Perfect New Year's Day departure with comfortable morning timing!")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Tab 2: Flight Details
with tab2:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown("# ✈️ Confirmed Flight Information")
    
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
    
    # Clean cost summary
    st.markdown("## 💰 Flight Cost Summary")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Per Person", "£600", "Return ticket")
    with col2:
        st.metric("Group Total", "£2,800", "4 people")
    with col3:
        st.metric("INR Total", "₹2,94,000", "@₹105/£")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Tab 3: Cost Calculator
with tab3:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown("# 💰 Interactive Cost Calculator")
    
    # Editable cost inputs
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 💰 Major Expenses")
        st.session_state.cost_data['Flights'] = st.number_input("Flights (return per person)", value=600, step=50)
        st.session_state.cost_data['London Accommodation (3 nights)'] = st.number_input("London Hotels", value=300, step=25)
        st.session_state.cost_data['Edinburgh/Highland Accommodation'] = st.number_input("Scotland Hotels", value=200, step=25)
        st.session_state.cost_data['Transport (all trains/buses)'] = st.number_input("All Transport", value=180, step=25)
    
    with col2:
        st.markdown("### 💸 Variable Expenses")
        st.session_state.cost_data['Attractions'] = st.number_input("Attraction Entries", value=150, step=25)
        st.session_state.cost_data['Food Budget'] = st.number_input("Food Budget", value=350, step=25)
        st.session_state.cost_data['Shopping & Souvenirs'] = st.number_input("Shopping", value=200, step=25)
        st.session_state.cost_data['Emergency Fund'] = st.number_input("Emergency Fund", value=100, step=25)
    
    # Calculate totals (clean calculation)
    total_per_person = sum(st.session_state.cost_data.values())
    group_total = total_per_person * 4
    inr_total = group_total * 105
    
    # Clean cost summary display
    st.markdown(f"""
    <div class="cost-summary">
        <h2>💵 Total Cost Summary</h2>
        <h1>£{total_per_person:,.0f}</h1>
        <p><strong>Per Person</strong></p>
        
        <h1>£{group_total:,.0f}</h1>
        <p><strong>Group of 4</strong></p>
        
        <hr style="margin: 1rem 0;">
        <h2>₹{inr_total:,.0f}</h2>
        <p><strong>Total in Indian Rupees</strong></p>
        <small>Exchange Rate: ₹105 per £1</small>
    </div>
    """, unsafe_allow_html=True)
    
    # Cost breakdown chart
    fig = px.pie(
        values=list(st.session_state.cost_data.values()),
        names=list(st.session_state.cost_data.keys()),
        title="Cost Distribution per Person"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Tab 4: Editable Price Tables
with tab4:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown("# 📊 Editable Day-wise Cost Tables")
    
    # Select day to edit
    day_select = st.selectbox("Select Day to Edit/View", 
                             options=list(st.session_state.daily_costs.keys()))
    
    st.markdown(f"## {day_select} - Detailed Costs")
    
    # Edit mode for tables
    table_edit_mode = st.toggle("✏️ Edit Price Table")
    
    if table_edit_mode:
        st.markdown('<div class="edit-section">', unsafe_allow_html=True)
        
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
                st.session_state.daily_costs[day_select].append({
                    'Activity': new_activity,
                    'Individual': new_individual,
                    'Couple': new_couple,
                    'Total_4': new_total
                })
                st.success(f"✅ Added {new_activity}")
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Display current day's table
    if day_select in st.session_state.daily_costs:
        activities = st.session_state.daily_costs[day_select]
        
        if activities:
            # Create clean dataframe
            df = pd.DataFrame(activities)
            
            # Format currency properly
            df_display = df.copy()
            df_display['Individual'] = df_display['Individual'].apply(lambda x: f"£{x:.2f}" if x > 0 else "FREE")
            df_display['Couple'] = df_display['Couple'].apply(lambda x: f"£{x:.2f}" if x > 0 else "FREE")
            df_display['Total_4'] = df_display['Total_4'].apply(lambda x: f"£{x:.2f}" if x > 0 else "FREE")
            
            st.dataframe(df_display, use_container_width=True, hide_index=True)
            
            # Calculate day totals (excluding flights)
            day_total = sum(activity['Total_4'] for activity in activities if 'Flight' not in activity['Activity'])
            day_total_per_person = day_total / 4
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(f"{day_select} Total", f"£{day_total:.2f}", "Group of 4")
            with col2:
                st.metric("Per Person", f"£{day_total_per_person:.2f}", "Daily average")
            with col3:
                st.metric("In INR", f"₹{day_total * 105:,.0f}", "Group total")
    
    # Calculate total for all days (excluding flights)
    all_days_total = 0
    for day_name, activities in st.session_state.daily_costs.items():
        day_total = sum(activity['Total_4'] for activity in activities if 'Flight' not in activity['Activity'])
        all_days_total += day_total
    
    st.markdown("---")
    st.markdown("## 🎯 Complete Trip Total (Excluding Flights)")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total (No Flights)", f"£{all_days_total:.2f}", "Group of 4")
    with col2:
        st.metric("Per Person (No Flights)", f"£{all_days_total/4:.2f}", "Average cost")
    with col3:
        st.metric("INR (No Flights)", f"₹{all_days_total * 105:,.0f}", "Group total")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Tab 5: Place Images
with tab5:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown("# 🖼️ Destination Images & Information")
    
    # Image upload section
    st.markdown("## 📸 Add Images of Places")
    
    places = [
        "Tower of London", "Tower Bridge", "London Eye", "Buckingham Palace",
        "Hyde Park Winter Wonderland", "The Shard", "British Museum", "Chelsea FC",
        "Durham Cathedral", "Newcastle Tyne Bridge", "Whitby Abbey",
        "Edinburgh Castle", "Glenfinnan Viaduct", "Glen Coe", "Fort William"
    ]
    
    selected_place = st.selectbox("Select Place to Add Image", places)
    uploaded_image = st.file_uploader(f"Upload image for {selected_place}", type=['jpg', 'jpeg', 'png'])
    
    if uploaded_image:
        image = Image.open(uploaded_image)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image(image, caption=f"{selected_place}", use_container_width=True)
    
    # Placeholder images section
    st.markdown("## 🏛️ Place Information & Images")
    
    place_info = {
        "Tower of London": {
            "description": "Historic castle housing the Crown Jewels, with 1000 years of history",
            "highlights": ["Crown Jewels", "Beefeater Guards", "Medieval Architecture", "Tower Ravens"],
            "visit_time": "2-3 hours",
            "best_time": "Morning opening to avoid crowds"
        },
        "London Eye": {
            "description": "Giant observation wheel offering 360-degree views of London",
            "highlights": ["Thames Views", "City Panorama", "30-minute rotation", "Christmas atmosphere"],
            "visit_time": "1 hour",
            "best_time": "Late afternoon for sunset views"
        },
        "Edinburgh Castle": {
            "description": "Ancient fortress perched on volcanic rock, Scotland's most famous castle",
            "highlights": ["Scottish Crown Jewels", "Stone of Destiny", "Great Hall", "One O'Clock Gun"],
            "visit_time": "3-4 hours",
            "best_time": "Early morning before crowds"
        },
        "Glenfinnan Viaduct": {
            "description": "Famous railway bridge from Harry Potter films, stunning Highland scenery",
            "highlights": ["Harry Potter Bridge", "Steam Train", "Highland Views", "Photo Opportunities"],
            "visit_time": "1-2 hours",
            "best_time": "When Jacobite Steam Train passes"
        }
    }
    
    # Display place information in grid
    for place, info in place_info.items():
        with st.expander(f"📍 {place}"):
            col1, col2 = st.columns([1, 2])
            with col1:
                st.markdown("**Key Information:**")
                st.write(f"**Visit Time:** {info['visit_time']}")
                st.write(f"**Best Time:** {info['best_time']}")
            with col2:
                st.write(info['description'])
                st.write("**Highlights:**")
                for highlight in info['highlights']:
                    st.write(f"• {highlight}")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Tab 6: Interactive Map
with tab6:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown("# 🗺️ Complete Travel Route Map")
    
    # Create comprehensive map
    m = folium.Map(location=[54.5, -2.5], zoom_start=6)
    
    # Add all key locations
    locations = {
        "London": {"coords": [51.5074, -0.1278], "color": "red", "icon": "star", 
                  "popup": "Days 1-3: Christmas, Boxing Day & Final London"},
        "Northallerton": {"coords": [54.3394, -1.4324], "color": "green", "icon": "home", 
                          "popup": "Host Home Base - Dec 27, 30"},
        "Durham": {"coords": [54.7761, -1.5733], "color": "blue", "icon": "university", 
                   "popup": "Day 4: UNESCO Cathedral & Castle"},
        "Newcastle": {"coords": [54.9783, -1.6178], "color": "blue", "icon": "building", 
                     "popup": "Day 4: Tyne Bridge & Quayside"},
        "Whitby": {"coords": [54.4858, -0.6206], "color": "purple", "icon": "anchor", 
                   "popup": "Day 4: Abbey Ruins & Harbor"},
        "Edinburgh": {"coords": [55.9533, -3.1883], "color": "orange", "icon": "castle", 
                     "popup": "Days 5&7: Castle & Hogmanay"},
        "Fort William": {"coords": [56.8198, -5.1052], "color": "darkgreen", "icon": "mountain", 
                        "popup": "Days 5-6: Highland Base & Tours"}
    }
    
    for name, details in locations.items():
        folium.Marker(
            details["coords"],
            popup=f"<b>{name}</b><br>{details['popup']}",
            tooltip=name,
            icon=folium.Icon(color=details["color"], icon=details["icon"])
        ).add_to(m)
    
    # Add travel routes with different colors
    routes = [
        {"coords": [[51.5074, -0.1278], [54.3394, -1.4324]], "color": "green", "weight": 4, "tooltip": "Dec 27: London → Northallerton (Train)"},
        {"coords": [[54.3394, -1.4324], [54.7761, -1.5733]], "color": "blue", "weight": 3, "tooltip": "Dec 28: Northallerton → Durham (Train)"},
        {"coords": [[54.7761, -1.5733], [54.9783, -1.6178]], "color": "blue", "weight": 3, "tooltip": "Dec 28: Durham → Newcastle (Train)"},
        {"coords": [[54.9783, -1.6178], [54.4858, -0.6206]], "color": "purple", "weight": 3, "tooltip": "Dec 28: Newcastle → Whitby (Bus)"},
        {"coords": [[54.3394, -1.4324], [55.9533, -3.1883]], "color": "orange", "weight": 4, "tooltip": "Dec 29: Northallerton → Edinburgh (Train)"},
        {"coords": [[55.9533, -3.1883], [56.8198, -5.1052]], "color": "darkgreen", "weight": 5, "tooltip": "Dec 29: Edinburgh → Fort William (Scenic Train)"},
        {"coords": [[56.8198, -5.1052], [55.9533, -3.1883]], "color": "red", "weight": 4, "tooltip": "Dec 31: Fort William → Edinburgh (Train)"}
    ]
    
    for route in routes:
        folium.PolyLine(
            locations=route["coords"],
            color=route["color"],
            weight=route["weight"],
            tooltip=route["tooltip"]
        ).add_to(m)
    
    st_folium(m, width=600, height=500)
    
    # Clean map legend
    st.markdown("### 🗺️ Travel Route Legend")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("🔴 **London** - Christmas base")
        st.write("🟢 **Northallerton** - Host home")
        st.write("🔵 **Durham/Newcastle** - Day trip")
    with col2:
        st.write("🟣 **Whitby** - Yorkshire coast")
        st.write("🟠 **Edinburgh** - Scottish capital")
        st.write("🌲 **Fort William** - Highland adventures")
    with col3:
        st.write("**Route Colors:**")
        st.write("• Green: Main journeys")
        st.write("• Blue: Northern England")
        st.write("• Red: Final return")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Sidebar with clean summary
with st.sidebar:
    st.markdown("## 🎄 Trip Overview")
    
    # Try to display group photo in sidebar
    try:
        image = Image.open("1.jpg")
        st.image(image, caption="Epic Travel Group!", use_container_width=True)
    except:
        st.info("📸 Upload 1.jpg to see group photo")
    
    # Clean metrics
    st.metric("Duration", "8 days")
    st.metric("Cities Visited", "7")
    st.metric("Group Size", "4 people")
    st.metric("Flight Cost", f"£{st.session_state.cost_data['Flights']}")
    
    # Calculate total daily costs (excluding flights)
    total_daily_costs = 0
    for day_activities in st.session_state.daily_costs.values():
        daily_total = sum(activity['Total_4'] for activity in day_activities if 'Flight' not in activity['Activity'])
        total_daily_costs += daily_total
    
    st.metric("Daily Costs Total", f"£{total_daily_costs:.0f}")
    st.metric("Grand Total", f"£{total_daily_costs + (st.session_state.cost_data['Flights'] * 4):.0f}")
    
    st.markdown("---")
    st.markdown("## 🎯 Quick Actions")
    
    if st.button("📧 Email Summary"):
        st.info("📧 Email feature coming soon!")
    
    if st.button("📱 Export to PDF"):
        st.info("📄 PDF export in development!")
    
    if st.button("🔄 Reset All"):
        if st.checkbox("Confirm reset"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.success("✅ All data reset!")
            st.rerun()
    
    st.markdown("---")
    st.success("✅ Fully editable travel planner")
    st.info("🎄 Epic adventure awaits!")

# Clean footer
st.markdown('<div class="content-card">', unsafe_allow_html=True)

# Calculate final totals properly
flight_total = st.session_state.cost_data['Flights'] * 4
daily_total = sum(
    sum(activity['Total_4'] for activity in day_activities if 'Flight' not in activity['Activity'])
    for day_activities in st.session_state.daily_costs.values()
)
grand_total = flight_total + daily_total
inr_grand_total = grand_total * 105

footer_content = f"""
# 🎄 Epic UK Christmas Adventure Complete! 🎄

## 🎉 Finally Shine is Leaving the District, State and Country - What an Achievement!

### 📋 Complete Trip Summary:
- **📅 Duration:** 8 amazing days (Dec 25, 2024 - Jan 1, 2025)
- **👥 Group:** 4 adventurers (Couple + 2 individuals)
- **✈️ Route:** Trivandrum → London → Scottish Highlands → Edinburgh → Bangalore
- **🎯 Highlights:** Christmas in London, Yorkshire coast, Highland railway, Edinburgh Hogmanay

### 💰 Final Cost Breakdown:
- **✈️ Flights:** £{flight_total:,.0f} (£600 × 4 people)
- **🏨 Daily Expenses:** £{daily_total:.0f} (all accommodation, transport, attractions)
- **💵 Grand Total:** £{grand_total:.0f} for entire group
- **💱 INR Total:** ₹{inr_grand_total:,.0f} (@ ₹105 per £1)

### 🎉 Epic Experiences Included:
- **🎄 Christmas Day** arrival in London with Tower Bridge & London Eye
- **🎁 Boxing Day** at Hyde Park Winter Wonderland with Christmas lights
- **🏰 Durham Cathedral** - UNESCO World Heritage medieval masterpiece
- **⚓ Whitby Abbey** - Dramatic coastal ruins with Dracula connections
- **🚂 West Highland Line** - One of world's most beautiful train journeys
- **🏔️ Scottish Highlands** - Glenfinnan Viaduct (Harry Potter bridge)
- **🎆 Edinburgh Hogmanay** - World's most famous New Year celebration

### 📞 Emergency & Support:
- **🚨 UK Emergency:** 999 or 112
- **🇮🇳 Indian High Commission London:** +44 20 7836 8484
- **📱 Host Contact:** Available throughout trip

---
**Generated:** {datetime.now().strftime("%B %d, %Y at %I:%M %p")}  
**⚡ Fully customizable travel planner - edit anything you need!**  
**🎄 Wishing you the most epic Christmas adventure ever! 🎄**
"""

st.markdown(footer_content)
st.markdown('</div>', unsafe_allow_html=True)

