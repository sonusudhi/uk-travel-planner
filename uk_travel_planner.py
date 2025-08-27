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
    page_title="UK Christmas Travel Planner - Group of 4",
    page_icon="🇬🇧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS (keeping minimal styling)
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f4e79;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .cost-box {
        background: linear-gradient(135deg, #f0f8ff, #e6f3ff);
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 5px solid #2c5aa0;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .weather-card {
        background: linear-gradient(135deg, #74b9ff, #0984e3);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'generated_itinerary' not in st.session_state:
    st.session_state.generated_itinerary = False

# Title
st.markdown('<h1 class="main-header">🇬🇧 UK Christmas Travel Planner</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; font-size: 1.3rem; color: #666; font-style: italic;">Group of 4: Couple + 2 Individuals | Dec 28, 2024 - Jan 4, 2025</p>', unsafe_allow_html=True)

# Group photo section - loads from GitHub
st.markdown("## 👥 Meet Your Travel Group")

try:
    # Load the uploaded photo from GitHub
    image = Image.open("1.jpg")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(image, caption="Your Travel Group of 4", use_column_width=True)
        st.success("🎉 Ready for UK Christmas adventure!")
except:
    # Fallback if image not found
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.info("📸 Upload 1.jpg to your GitHub repository to see your group photo here!")
        st.write("**Group:** 4 people (1 Couple + 2 Individuals)")

# Sidebar
with st.sidebar:
    st.markdown("## ✈️ Trip Details")
    
    # Fixed group information
    st.markdown("### 👥 Group Information")
    st.info("**Fixed Group Size: 4 People**\n- 1 Couple\n- 2 Individuals")
    
    # Travel preferences
    st.markdown("### 🎯 Customize Your Experience")
    budget_per_person = st.selectbox("Budget Range (per person)", 
                                   ["Budget (£800-1200)", "Mid-range (£1200-2000)", "Luxury (£2000+)"],
                                   index=1)
    
    interests = st.multiselect("Select Primary Interests", 
                              ["Historical Sites", "Museums", "Shopping", "Nightlife", 
                               "Food & Dining", "Architecture", "Parks & Nature", 
                               "Festivals & Events", "Royal Attractions"],
                              default=["Historical Sites", "Museums", "Food & Dining"])
    
    activity_level = st.selectbox("Activity Level", 
                                ["Relaxed", "Moderate", "Active", "Very Active"],
                                index=1)
    
    show_weather = st.checkbox("Show Weather Information", value=True)

# Attraction data
london_attractions = {
    "Tower of London": {"coords": [51.5081, -0.0759], "type": "Historical", "duration": 3, "cost": 29.90},
    "British Museum": {"coords": [51.5194, -0.1270], "type": "Museums", "duration": 4, "cost": 0},
    "Westminster Abbey": {"coords": [51.4994, -0.1273], "type": "Historical", "duration": 2, "cost": 27},
    "London Eye": {"coords": [51.5033, -0.1196], "type": "Architecture", "duration": 1, "cost": 32},
    "Covent Garden": {"coords": [51.5118, -0.1226], "type": "Shopping", "duration": 2, "cost": 0},
    "Hyde Park": {"coords": [51.5074, -0.1657], "type": "Parks", "duration": 2, "cost": 0},
    "Buckingham Palace": {"coords": [51.5014, -0.1419], "type": "Royal", "duration": 1, "cost": 0},
    "Camden Market": {"coords": [51.5414, -0.1460], "type": "Shopping", "duration": 3, "cost": 0},
    "Tate Modern": {"coords": [51.5076, -0.0994], "type": "Museums", "duration": 3, "cost": 0},
    "St. Paul's Cathedral": {"coords": [51.5138, -0.0984], "type": "Architecture", "duration": 2, "cost": 25}
}

edinburgh_attractions = {
    "Edinburgh Castle": {"coords": [55.9486, -3.1999], "type": "Historical", "duration": 3, "cost": 19.50},
    "Royal Mile": {"coords": [55.9507, -3.1836], "type": "Historical", "duration": 2, "cost": 0},
    "Arthur's Seat": {"coords": [55.9445, -3.1615], "type": "Parks", "duration": 3, "cost": 0},
    "Holyrood Palace": {"coords": [55.9530, -3.1722], "type": "Royal", "duration": 2, "cost": 17.50},
    "Princes Street": {"coords": [55.9520, -3.1970], "type": "Shopping", "duration": 2, "cost": 0},
    "Christmas Market": {"coords": [55.9533, -3.1883], "type": "Festivals", "duration": 2, "cost": 0},
    "Grassmarket": {"coords": [55.9476, -3.1977], "type": "Nightlife", "duration": 2, "cost": 0},
    "National Gallery": {"coords": [55.9501, -3.1958], "type": "Museums", "duration": 2, "cost": 0},
    "Camera Obscura": {"coords": [55.9496, -3.1947], "type": "Museums", "duration": 1, "cost": 17},
    "Calton Hill": {"coords": [55.9553, -3.1825], "type": "Parks", "duration": 1, "cost": 0}
}

# Filter attractions based on interests
def filter_attractions(attractions_dict, selected_interests):
    if not selected_interests:
        return attractions_dict
    
    filtered = {}
    interest_mapping = {
        "Historical Sites": "Historical",
        "Museums": "Museums", 
        "Shopping": "Shopping",
        "Nightlife": "Nightlife",
        "Parks & Nature": "Parks",
        "Architecture": "Architecture",
        "Festivals & Events": "Festivals",
        "Royal Attractions": "Royal"
    }
    
    mapped_interests = [interest_mapping.get(interest, interest) for interest in selected_interests]
    
    for name, details in attractions_dict.items():
        if any(interest in details["type"] for interest in mapped_interests):
            filtered[name] = details
    
    if len(filtered) < 3:
        return attractions_dict
    
    return filtered

# Main tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📅 Day-by-Day Itinerary", 
    "✈️ Flight Details", 
    "🗺️ Interactive Map", 
    "💰 Cost Breakdown", 
    "📋 Travel Essentials"
])

# Tab 1: Clean Itinerary Format
with tab1:
    st.markdown("# 📅 Your Personalized 8-Day Itinerary")
    
    # Generate button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🎯 Generate Personalized Itinerary"):
            st.session_state.generated_itinerary = True
            st.success("✅ Itinerary generated for your group of 4!")
    
    if st.session_state.generated_itinerary or True:
        
        # Day 1: Arrival
        st.markdown("## ✈️ Day 1: Saturday December 28 - Arrival in London")
        st.markdown("**Location:** Kochi → London")
        
        st.markdown("### 🛫 20:10 IST - Departure from Kochi")
        st.write("- ✈️ Flight departure from Kochi (COK)")
        st.write("- 👫 Group check-in for 4 people")
        st.write("- 🍽️ In-flight meals and entertainment")
        st.write("- 📱 Keep family updated on departure")
        
        st.markdown("### 🛬 09:45 GMT - Sunday Morning Arrival in London")
        st.write("- 🛬 Landing at London airport")
        st.write("- 🛂 Immigration and customs for group")
        st.write("- 💷 Currency exchange and UK SIM cards")
        st.write("- 🚂 Airport transfer to central London")
        
        st.markdown("### 🏨 11:00-15:00 - London Arrival & Settlement")
        st.write("- 🏨 Hotel check-in (rooms for couple + 2 individuals)")
        st.write("- 🚿 Freshen up after long flight")
        st.write("- 🍽️ First British meal together")
        st.write("- 🌆 Gentle walk around local area")
        
        st.markdown("### 🌃 15:00+ - Light Exploration & Rest")
        st.write("- 🏰 Quick visit to nearby attraction")
        st.write("- 📸 First group photos in London")
        st.write("- 🛌 Early rest to combat jet lag")
        st.write("- 📋 Plan next day activities")
        
        st.info("💡 Day 1 Tips: Take it easy after the overnight flight. Focus on rest and gentle exploration.")
        st.markdown("---")
        
        # London Days
        st.markdown("## 🏴󠁧󠁢󠁥󠁮󠁧󠁿 Day 2: December 29 - Historic London Discovery")
        st.markdown("**Location:** London")
        
        st.markdown("### 🌅 09:00-12:30 - Morning Adventures")
        st.write("- 🏛️ Tower of London")
        st.write("- 🏛️ Tower Bridge area")
        st.write("- ☕ Coffee break for the group")
        
        st.markdown("### 🌞 13:00-17:30 - Afternoon Exploration")
        st.write("- 🍽️ Lunch at recommended restaurant")
        st.write("- 🎯 Westminster Abbey")
        st.write("- 🎯 Big Ben & Parliament")
        
        st.markdown("### 🌃 18:00+ - Evening Experience")
        st.write("- 🌃 Traditional pub dinner")
        st.write("- 🌃 Group photos by Thames")
        st.markdown("---")
        
        st.markdown("## 🏴󠁧󠁢󠁥󠁮󠁧󠁿 Day 3: December 30 - Royal & Cultural London")
        st.markdown("**Location:** London")
        
        st.markdown("### 🌅 09:00-12:30 - Morning Adventures")
        st.write("- 🏛️ Buckingham Palace")
        st.write("- 🏛️ St. James's Park")
        st.write("- ☕ Coffee break for the group")
        
        st.markdown("### 🌞 13:00-17:30 - Afternoon Exploration")
        st.write("- 🍽️ Lunch at recommended restaurant")
        st.write("- 🎯 British Museum")
        st.write("- 🎯 Covent Garden")
        
        st.markdown("### 🌃 18:00+ - Evening Experience")
        st.write("- 🌃 West End show booking")
        st.write("- 🌃 Late dinner in Theatreland")
        st.markdown("---")
        
        st.markdown("## 🏴󠁧󠁢󠁥󠁮󠁧󠁿 Day 4: December 31 - New Year's Eve in London")
        st.markdown("**Location:** London")
        
        st.markdown("### 🌅 09:00-12:30 - Morning Adventures")
        st.write("- 🏛️ St. Paul's Cathedral")
        st.write("- 🏛️ City of London")
        st.write("- ☕ Coffee break for the group")
        
        st.markdown("### 🌞 13:00-17:30 - Afternoon Exploration")
        st.write("- 🍽️ Lunch at recommended restaurant")
        st.write("- 🎯 London Eye")
        st.write("- 🎯 South Bank walk")
        
        st.markdown("### 🌃 18:00+ - Evening Experience")
        st.write("- 🌃 New Year's Eve celebration")
        st.write("- 🌃 Fireworks by Thames")
        
        st.warning("🎉 New Year's Eve Special: Book restaurants in advance! Dress warmly for outdoor celebrations. Consider Thames boat party.")
        st.markdown("---")
        
        # Travel to Edinburgh
        st.markdown("## 🚂 Day 5: January 1, 2025 - New Year's Day Travel to Edinburgh")
        st.markdown("**Location:** London → Edinburgh")
        
        st.markdown("### 🌅 09:00-11:00 - New Year's Morning")
        st.write("- 🥳 Recovery breakfast after New Year's celebration")
        st.write("- 🏨 Hotel check-out")
        st.write("- 🚂 King's Cross station departure")
        
        st.markdown("### 🚄 11:30-16:00 - Journey to Scotland")
        st.write("- 🚄 Train journey to Edinburgh (4.5 hours)")
        st.write("- 🥪 Lunch on board")
        st.write("- 🌄 Scenic views of English & Scottish countryside")
        
        st.markdown("### 🏴󠁧󠁢󠁳󠁣󠁴󠁿 16:30+ - Edinburgh Arrival")
        st.write("- 🏴󠁧󠁢󠁳󠁣󠁴󠁿 Arrival at Edinburgh Waverley")
        st.write("- 🏨 Hotel check-in")
        st.write("- 🍽️ First Scottish dinner")
        st.write("- 🌃 Evening Royal Mile stroll")
        st.markdown("---")
        
        # Edinburgh Days
        st.markdown("## 🏴󠁧󠁢󠁳󠁣󠁴󠁿 Day 6: January 2 - Edinburgh Castle & History")
        st.markdown("**Location:** Edinburgh")
        
        st.markdown("### 🌅 09:00-12:30 - Morning")
        st.write("- 🏴󠁧󠁢󠁳󠁣󠁴󠁿 Edinburgh Castle")
        st.write("- 🏴󠁧󠁢󠁳󠁣󠁴󠁿 Royal Mile exploration")
        
        st.markdown("### 🌞 13:30-17:30 - Afternoon")
        st.write("- 🏴󠁧󠁢󠁳󠁣󠁴󠁿 Holyrood Palace")
        st.write("- 🏴󠁧󠁢󠁳󠁣󠁴󠁿 Arthur's Seat hike")
        
        st.markdown("### 🌃 18:00+ - Evening")
        st.write("- 🌃 Traditional Scottish dinner")
        st.write("- 🌃 Folk music session")
        st.markdown("---")
        
        st.markdown("## 🏴󠁧󠁢󠁳󠁣󠁴󠁿 Day 7: January 3 - Final Scottish Experience")
        st.markdown("**Location:** Edinburgh")
        
        st.markdown("### 🌅 09:00-12:30 - Morning")
        st.write("- 🏴󠁧󠁢󠁳󠁣󠁴󠁿 National Gallery")
        st.write("- 🏴󠁧󠁢󠁳󠁣󠁴󠁿 Princes Street shopping")
        
        st.markdown("### 🌞 13:30-17:30 - Afternoon")
        st.write("- 🏴󠁧󠁢󠁳󠁣󠁴󠁿 Camera Obscura")
        st.write("- 🏴󠁧󠁢󠁳󠁣󠁴󠁿 Last-minute shopping")
        
        st.markdown("### 🌃 18:00+ - Evening")
        st.write("- 🌃 Farewell dinner")
        st.write("- 🌃 Pack for early departure")
        st.markdown("---")
        
        # Final Departure Day
        st.markdown("## ✈️ Day 8: January 4, 2025 - Departure Day")
        st.markdown("**Location:** Edinburgh → Bengaluru")
        
        st.markdown("### 🌙 03:00-05:30 - Early Morning Departure")
        st.write("- ⏰ Very early wake-up call")
        st.write("- 🏨 Hotel check-out")
        st.write("- 🚌 Airport transfer (allow extra time)")
        st.write("- ✈️ Flight check-in for group")
        
        st.markdown("### 🛫 06:05 GMT - Flight Departure")
        st.write("- 🛫 Departure from Edinburgh")
        st.write("- 🍽️ In-flight meals")
        st.write("- 📱 Share travel memories")
        
        st.markdown("### 🛬 01:50+1 IST - Arrival in Bengaluru")
        st.write("- 🏠 Safe arrival in India")
        st.write("- 📸 Share photos with family")
        st.write("- 💭 Amazing UK memories created!")
        
        st.success("✅ Departure Tips: Pack souvenirs carefully, keep receipts for customs, arrive at airport 3 hours early for international flight.")

# Tab 2: Flight Details (Clean Format)
with tab2:
    st.markdown("# ✈️ Confirmed Flight Information")
    
    # Outbound Flight
    st.markdown("## 🛫 OUTBOUND FLIGHT")
    st.markdown("### Kochi (COK) → London (LHR/LGW)")
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Date:** Saturday, December 28, 2024")
        st.write("**Departure:** 20:10 IST")
        st.write("**Arrival:** 09:45 GMT (Next Day)")
        st.write("**Flight Duration:** ~13-15 hours (with connections)")
    
    with col2:
        st.metric("Total Return Cost", "£600", "Per person")
        st.write("**Passengers:** 4 People")
        st.write("**Group:** 1 Couple + 2 Individuals")
    
    # Return Flight
    st.markdown("## 🛬 RETURN FLIGHT")
    st.markdown("### Edinburgh (EDI) → Bengaluru (BLR)")
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Date:** Saturday, January 4, 2025")
        st.write("**Departure:** 06:05 GMT")
        st.write("**Arrival:** 01:50+1 IST (Next Day)")
        st.write("**Flight Duration:** ~19-21 hours (with connections)")
    
    with col2:
        st.metric("Return Ticket Included", "£600", "Total per person")
        st.write("**Final Destination:** Bengaluru")
        st.write("**Early departure - 6:05 AM**")
    
    # Total Flight Cost Summary
    st.markdown("## 💰 Flight Cost Summary")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Per Person (Return)", "£600", "Complete round trip")
    with col2:
        st.metric("Total Group Cost", "£2,400", "4 people × £600")
    with col3:
        st.metric("Cost in INR", "₹2,52,000", "Approx @₹105/£")
    
    # Important Flight Notes
    st.markdown("## ⚠️ Important Flight Information")
    
    st.markdown("### 📋 Key Details:")
    st.write("- ✅ **Open-jaw routing:** Kochi → London, Edinburgh → Bengaluru")
    st.write("- ✅ **Group booking:** 4 passengers traveling together")
    st.write("- ✅ **Early departure:** 6:05 AM requires 3:00 AM hotel departure")
    st.write("- ✅ **Return ticket cost:** £600 includes both outbound and return flights")
    st.write("- ✅ **Overnight flight:** Saturday night departure, Sunday morning arrival")
    
    st.markdown("### 🎒 Booking Checklist:")
    st.checkbox("Seat selection for group (couple together, individuals nearby)")
    st.checkbox("Meal preferences specified for all passengers")
    st.checkbox("Baggage allowance confirmed (typically 30kg international)")
    st.checkbox("Travel insurance purchased for all 4 people")
    st.checkbox("Airport transfers booked for group transportation")
    
    st.markdown("### 📱 Pre-Flight Actions:")
    st.write("- **Web check-in:** 24-48 hours before departure")
    st.write("- **Seat assignments:** Ensure couple sits together")
    st.write("- **Special requests:** Meals, assistance, etc.")
    st.write("- **Contact details:** Emergency contacts updated")

# Tab 3: Interactive Map
with tab3:
    st.markdown("# 🗺️ Interactive Travel Map")
    
    filtered_london = filter_attractions(london_attractions, interests)
    filtered_edinburgh = filter_attractions(edinburgh_attractions, interests)
    
    # Create map
    m = folium.Map(location=[54.5, -2.5], zoom_start=6)
    
    # Add London attractions
    for name, details in filtered_london.items():
        folium.Marker(
            details["coords"],
            popup=f"<b>{name}</b><br>Type: {details['type']}<br>Duration: {details['duration']}h<br>Cost: £{details['cost']}",
            tooltip=name,
            icon=folium.Icon(color='red', icon='info-sign')
        ).add_to(m)
    
    # Add Edinburgh attractions
    for name, details in filtered_edinburgh.items():
        folium.Marker(
            details["coords"],
            popup=f"<b>{name}</b><br>Type: {details['type']}<br>Duration: {details['duration']}h<br>Cost: £{details['cost']}",
            tooltip=name,
            icon=folium.Icon(color='blue', icon='info-sign')
        ).add_to(m)
    
    # Add route
    folium.PolyLine(
        locations=[[51.5074, -0.1278], [55.9533, -3.1883]],
        color="green", weight=5,
        tooltip="London → Edinburgh"
    ).add_to(m)
    
    st_folium(m, width=700, height=500)
    
    # Legend
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**🔴 Red Markers:** London Attractions")
    with col2:
        st.markdown("**🔵 Blue Markers:** Edinburgh Attractions")

# Tab 4: Cost Breakdown
with tab4:
    st.markdown("# 💰 Complete Cost Analysis for Group of 4")
    
    # Budget multiplier
    budget_multipliers = {
        "Budget (£800-1200)": 1.0,
        "Mid-range (£1200-2000)": 1.5,
        "Luxury (£2000+)": 2.5
    }
    
    multiplier = budget_multipliers[budget_per_person]
    
    # Updated costs per person with correct flight price (£600 TOTAL return)
    base_costs = {
        "Flights": {"Return flights (COK-LHR-EDI-BLR)": 600},  # Total return cost
        "Accommodation": {
            "London (3 nights)": 85*3*multiplier, 
            "Edinburgh (2 nights)": 90*2*multiplier,
            "Room arrangements": 50  # Extra cost for couple room + 2 individual rooms
        },
        "Transportation": {
            "Airport transfers": 70, 
            "London-Edinburgh train": 85, 
            "Local transport": 40
        },
        "Food": {"Meals (7 days)": 50*7*multiplier},
        "Attractions": {"Entry fees": 120*multiplier, "Entertainment": 80*multiplier},
        "Shopping": {"Souvenirs": 150},
        "Miscellaneous": {"Emergency fund": 100, "Group expenses": 75}
    }
    
    # Calculate totals
    category_totals = {}
    total_per_person = 0
    
    for category, items in base_costs.items():
        category_total = sum(items.values())
        category_totals[category] = category_total
        total_per_person += category_total
    
    # Display cost visualization
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig = px.pie(
            values=list(category_totals.values()), 
            names=list(category_totals.keys()),
            title="Cost Distribution per Person"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown(f"""
        <div class="cost-box">
            <h3>💵 Group Cost Summary</h3>
            <h2>£{total_per_person:,.0f}</h2>
            <p><strong>Per Person</strong></p>
            
            <h2>£{total_per_person * 4:,.0f}</h2>
            <p><strong>Total for Group of 4</strong></p>
            
            <hr>
            <h3>₹{total_per_person * 4 * 105:,.0f}</h3>
            <p><strong>Total in Indian Rupees</strong></p>
            <small>@ ₹105 per £1</small>
        </div>
        """, unsafe_allow_html=True)
    
    # Detailed breakdown for group of 4
    st.markdown("## 📊 Detailed Cost Breakdown (Group of 4)")
    breakdown_data = []
    for category, items in base_costs.items():
        for item, cost in items.items():
            breakdown_data.append({
                "Category": category,
                "Item": item,
                "Per Person": f"£{cost:.0f}",
                "Total (4 people)": f"£{cost * 4:.0f}",
                "INR (Total)": f"₹{cost * 4 * 105:.0f}"
            })
    
    df = pd.DataFrame(breakdown_data)
    st.dataframe(df, use_container_width=True)
    
    # Room arrangement explanation
    st.markdown("## 🏨 Accommodation Arrangements")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**London (3 nights)**")
        st.write("- 1 Double room for couple")
        st.write("- 2 Single rooms for individuals")
        st.write("- Central location preferred")
    
    with col2:
        st.markdown("**Edinburgh (2 nights)**")
        st.write("- 1 Double room for couple")
        st.write("- 2 Single rooms for individuals")
        st.write("- Near Royal Mile")
    
    with col3:
        st.markdown("**Cost Optimization**")
        st.write("- Group booking discounts")
        st.write("- Same hotel for all")
        st.write("- Breakfast included options")

# Tab 5: Travel Essentials
with tab5:
    st.markdown("# 📋 Travel Preparation for Group of 4")
    
    # Weather info
    if show_weather:
        st.markdown("## 🌤️ Weather Forecast (Dec 28 - Jan 4)")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="weather-card">
                <h4>London (Dec 28-Jan 1)</h4>
                <p><strong>🌡️ Temperature:</strong> 3-9°C</p>
                <p><strong>☔ Conditions:</strong> Cold, frequent rain</p>
                <p><strong>🌅 Daylight:</strong> 8:00 AM - 4:00 PM</p>
                <p><strong>🎆 New Year's:</strong> Outdoor celebrations!</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="weather-card">
                <h4>Edinburgh (Jan 1-4)</h4>
                <p><strong>🌡️ Temperature:</strong> 1-7°C</p>
                <p><strong>❄️ Conditions:</strong> Very cold, possible snow</p>
                <p><strong>🌅 Daylight:</strong> 8:30 AM - 3:45 PM</p>
                <p><strong>🧥 Essential:</strong> Heavy winter clothing</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Group-specific packing
    st.markdown("## 🎒 Group Packing Strategy")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**👫 For the Couple:**")
        st.write("- Share heavy items (chargers, toiletries)")
        st.write("- One person carries group first aid")
        st.write("- Coordinate outfit colors for photos")
        st.write("- Shared power bank for both phones")
        
        st.markdown("**📱 Group Communication:**")
        st.write("- WhatsApp group for coordination")
        st.write("- Shared Google Photos album")
        st.write("- One person handles group bookings")
        st.write("- Emergency contact sharing")
    
    with col2:
        st.markdown("**🎯 For Individuals:**")
        st.write("- Personal power banks")
        st.write("- Individual comfort items")
        st.write("- Personal medication copies")
        st.write("- Solo exploration backup plans")
        
        st.markdown("**💡 Group Benefits:**")
        st.write("- Split taxi costs (4-way)")
        st.write("- Group discounts at attractions")
        st.write("- Shared meals for variety")
        st.write("- Safety in numbers")
    
    # Updated packing checklist
    st.markdown("## ✅ Essential Items Checklist")
    
    st.markdown("### 📋 Documents (Each Person)")
    st.checkbox("Passport (6+ months validity)")
    st.checkbox("UK visa (if required)")
    st.checkbox("Flight tickets (Kochi→London, Edinburgh→Bengaluru)")
    st.checkbox("Travel insurance (mandatory)")
    st.checkbox("Hotel confirmations")
    st.checkbox("Emergency contact list")
    st.checkbox("Copy of group itinerary")
    
    st.markdown("### 🧥 Winter Clothing (Per Person)")
    st.checkbox("Heavy winter coat (waterproof)")
    st.checkbox("Thermal underwear (2-3 sets)")
    st.checkbox("Warm sweaters/hoodies (3-4)")
    st.checkbox("Waterproof jacket/umbrella")
    st.checkbox("Warm socks (8+ pairs)")
    st.checkbox("Gloves, hat, scarf set")
    st.checkbox("Comfortable walking boots")
    st.checkbox("Formal outfit for New Year's Eve")
    st.checkbox("Sleepwear for cold nights")
    
    st.markdown("### 🔌 Electronics & Tech")
    st.checkbox("UK power adapter Type G (1 per person)")
    st.checkbox("Portable phone chargers")
    st.checkbox("Camera for group photos")
    st.checkbox("UK SIM cards or roaming plan")
    st.checkbox("Headphones for flights")
    st.checkbox("Universal charging cables")
    st.checkbox("Power bank (fully charged)")
    
    st.markdown("### 💊 Health & Personal")
    st.checkbox("Prescription medications (extra supply)")
    st.checkbox("First aid kit (shared)")
    st.checkbox("Cold/flu medicine")
    st.checkbox("Hand sanitizer")
    st.checkbox("Personal hygiene items")
    st.checkbox("Sunglasses")
    st.checkbox("Lip balm and moisturizer")
    st.checkbox("Travel-sized toiletries")
    
    # Group coordination tips
    st.markdown("## 👥 Group Travel Tips")
    
    group_tips = [
        "**👫 Couple Coordination:** Book seats together, share luggage space efficiently",
        "**🎯 Individual Freedom:** Plan some solo time, respect different interests",
        "**💰 Money Management:** Use group expense tracking app (Splitwise)",
        "**📱 Stay Connected:** Create WhatsApp group, share live locations",
        "**🏨 Room Strategy:** Couple in double room, individuals in singles nearby",
        "**🍽️ Dining:** Mix group meals with individual choices",
        "**📸 Photography:** Designate group photographer, share photos daily",
        "**🚶‍♂️ Walking Pace:** Accommodate different fitness levels",
        "**⏰ Punctuality:** Set group meeting times with 10-minute buffer",
        "**🛍️ Shopping:** Coordinate gift shopping, share souvenir ideas"
    ]
    
    for tip in group_tips:
        st.write(f"- {tip}")
    
    # Emergency contacts
    st.markdown("## 🚨 Emergency Information")
    
    st.markdown("**UK Emergency Numbers:**")
    st.write("- Emergency Services: 999 or 112")
    st.write("- Non-emergency Police: 101")
    st.write("- NHS Health: 111")
    
    st.markdown("**Indian High Commission London:**")
    st.write("- Address: India House, Aldwych, London WC2B 4NA")
    st.write("- Phone: +44 20 7836 8484")
    st.write("- Emergency: +44 20 7632 3149")
    
    st.markdown("**Group Emergency Plan:**")
    st.write("- Keep everyone's phone numbers saved")
    st.write("- Share hotel addresses with all members")
    st.write("- Designate meeting points if separated")
    st.write("- Keep some cash for emergencies")

# Footer
st.markdown("---")

# Clean footer text
footer_text = f"""
# 🎄 Have an Amazing UK Christmas & New Year Holiday! 🎄

**Customized itinerary for your group of 4 people**

## 📋 Trip Summary:
- **📅 Duration:** 8 days (Dec 28, 2024 - Jan 4, 2025)
- **👥 Group:** 4 people (Couple + 2 individuals)
- **✈️ Route:** Kochi → London → Edinburgh → Bengaluru
- **💰 Budget:** {budget_per_person}

## ✈️ Your Flight Details:
- **Outbound:** Dec 28, 20:10 IST (Kochi) → Dec 29, 09:45 GMT (London)
- **Return:** Jan 4, 06:05 GMT (Edinburgh) → Jan 5, 01:50 IST (Bengaluru)
- **Total Cost:** £600 per person | £2,400 for group

## 📞 24/7 Support Information:
- **UK Emergency:** 999
- **Indian High Commission London:** +44 20 7836 8484

Generated on: {datetime.now().strftime("%B %d, %Y at %I:%M %p")}

*⚡ Personalized for your group of 4 travelers*
"""

st.markdown(footer_text)

# Sidebar summary
with st.sidebar:
    st.markdown("---")
    st.markdown("## 📊 Trip Summary")
    
    # Calculate quick stats
    total_attractions = len(filter_attractions(london_attractions, interests)) + len(filter_attractions(edinburgh_attractions, interests))
    base_cost_per_person = 1200 * budget_multipliers[budget_per_person]
    
    st.metric("Days", "8")
    st.metric("Cities", "2") 
    st.metric("Group Size", "4 people")
    st.metric("Flight Cost", "£600 per person")
    st.metric("Total/Person", f"£{base_cost_per_person:.0f}")
    st.metric("Group Total", f"£{base_cost_per_person * 4:.0f}")
    
    # Group photo reminder
    st.markdown("---")
    st.markdown("## 📸 Group Photo")
    st.info("💡 Your group photo (1.jpg) should display above if uploaded to GitHub!")
    
    # Quick reminders
    st.markdown("## ⚠️ Important Reminders")
    st.error("🚨 Early Flight: 6:05 AM departure = 3:00 AM hotel departure!")
    st.info("🎯 New Destination: Return flight goes to Bengaluru, not Kochi")
    st.success("✅ Open-jaw booking saves train cost!")
    
    st.markdown("---")
    st.success("✅ Updated with your specific details")
    st.info("📅 Dates: Dec 28, 2024 - Jan 4, 2025")

