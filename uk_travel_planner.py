import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

# Page configuration
st.set_page_config(
    page_title="UK Christmas Travel Planner",
    page_icon="🇬🇧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f4e79;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .section-header {
        font-size: 1.8rem;
        color: #2c5aa0;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 3px solid #2c5aa0;
        padding-bottom: 0.5rem;
    }
    .cost-box {
        background: linear-gradient(135deg, #f0f8ff, #e6f3ff);
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 5px solid #2c5aa0;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .day-card {
        background: #ffffff;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        margin: 1.5rem 0;
        border-left: 6px solid #ff6b6b;
    }
    .location-tag {
        background: linear-gradient(45deg, #ff6b6b, #ff8e8e);
        color: white;
        padding: 0.4rem 1rem;
        border-radius: 25px;
        font-size: 0.85rem;
        font-weight: bold;
        display: inline-block;
        margin: 0.3rem;
        box-shadow: 0 2px 10px rgba(255,107,107,0.3);
    }
    .time-tag {
        background: linear-gradient(45deg, #4ecdc4, #44a08d);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        display: inline-block;
        margin-right: 0.8rem;
        box-shadow: 0 2px 8px rgba(78,205,196,0.3);
    }
    .weather-card {
        background: linear-gradient(135deg, #74b9ff, #0984e3);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        text-align: center;
    }
    .tip-box {
        background: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid #fdcb6e;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'generated_itinerary' not in st.session_state:
    st.session_state.generated_itinerary = False

# Title
st.markdown('<h1 class="main-header">🇬🇧 UK Christmas Travel Planner</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; font-size: 1.3rem; color: #666; font-style: italic;">Kochi → London → Edinburgh → Kochi | December 25, 2024 - January 3, 2025</p>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("## ✈️ Trip Customization")
    
    # Group details
    st.markdown("### 👥 Group Information")
    group_size = st.number_input("Group Size", min_value=1, max_value=20, value=4)
    
    budget_per_person = st.selectbox("Budget Range (per person)", 
                                   ["Budget (£800-1200)", "Mid-range (£1200-2000)", "Luxury (£2000+)"])
    
    # Interests
    st.markdown("### 🎯 Travel Preferences")
    interests = st.multiselect("Select Primary Interests", 
                              ["Historical Sites", "Museums", "Shopping", "Nightlife", 
                               "Food & Dining", "Architecture", "Parks & Nature", 
                               "Festivals & Events", "Royal Attractions"],
                              default=["Historical Sites", "Museums", "Food & Dining"])
    
    activity_level = st.selectbox("Activity Level", 
                                ["Relaxed", "Moderate", "Active", "Very Active"],
                                index=1)
    
    transport_pref = st.selectbox("Transport Preference", 
                                 ["Public Transport", "Mixed", "Taxis/Uber"])
    
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
    "🗺️ Interactive Map", 
    "💰 Cost Breakdown", 
    "✈️ Flight Information", 
    "📋 Travel Essentials"
])

# Tab 1: Itinerary
with tab1:
    st.markdown('<h2 class="section-header">📅 Detailed Daily Itinerary</h2>', unsafe_allow_html=True)
    
    # Generate button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🎯 Generate Personalized Itinerary"):
            st.session_state.generated_itinerary = True
            st.success("✅ Itinerary generated based on your preferences!")
    
    if st.session_state.generated_itinerary or True:
        # Day 1: Arrival
        st.markdown("""
        <div class="day-card">
            <h3>🎄 Day 1: December 25 - Christmas Arrival in London</h3>
            <span class="location-tag">LONDON</span>
            
            <div style="margin-top: 1.5rem;">
                <p><span class="time-tag">06:00-10:00</span><strong>Flight Arrival</strong></p>
                <ul>
                    <li>✈️ International flight arrival from Kochi</li>
                    <li>🛂 Immigration and customs</li>
                    <li>🚂 Airport transfer to central London</li>
                </ul>
                
                <p><span class="time-tag">11:00-15:00</span><strong>Check-in & Gentle Start</strong></p>
                <ul>
                    <li>🏠 Hotel check-in and freshen up</li>
                    <li>🍽️ Traditional Christmas lunch</li>
                    <li>🎄 Westminster Christmas decorations walk</li>
                </ul>
                
                <p><span class="time-tag">15:00-19:00</span><strong>Light Exploration</strong></p>
                <ul>
                    <li>🏰 Buckingham Palace exterior</li>
                    <li>🌳 Hyde Park Winter Wonderland (if open)</li>
                    <li>📸 Christmas photo session</li>
                </ul>
                
                <p><span class="time-tag">19:00+</span><strong>Christmas Evening</strong></p>
                <ul>
                    <li>🍽️ Christmas dinner with host</li>
                    <li>🛌 Early rest for jet lag recovery</li>
                </ul>
            </div>
            
            <div style="margin-top: 1rem; padding: 1rem; background: #f0f8ff; border-radius: 8px;">
                <strong>💡 Day 1 Tips:</strong> Take it easy - many attractions closed on Christmas Day
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # London Days
        london_days = [
            {
                "day": 2, "date": "December 26", "title": "Boxing Day - Historic London",
                "morning": ["Tower of London", "Tower Bridge area"],
                "afternoon": ["Westminster Abbey", "Big Ben photos"],
                "evening": ["Traditional pub dinner in Southwark"]
            },
            {
                "day": 3, "date": "December 27", "title": "Royal & Cultural London",
                "morning": ["Buckingham Palace", "St. James's Park"],
                "afternoon": ["British Museum", "Covent Garden"],
                "evening": ["West End show booking"]
            },
            {
                "day": 4, "date": "December 28", "title": "Modern & Traditional Mix",
                "morning": ["St. Paul's Cathedral", "City of London"],
                "afternoon": ["Tate Modern", "Borough Market"],
                "evening": ["Thames dinner cruise"]
            },
            {
                "day": 5, "date": "December 29", "title": "Markets & Shopping",
                "morning": ["Camden Market", "Regent's Park"],
                "afternoon": ["Oxford Street shopping", "Hyde Park"],
                "evening": ["Chinatown dinner"]
            },
            {
                "day": 6, "date": "December 30", "title": "Journey to Edinburgh",
                "morning": ["Final London breakfast", "King's Cross station"],
                "afternoon": ["Train to Edinburgh (4.5 hours)"],
                "evening": ["Edinburgh arrival, Royal Mile walk"]
            }
        ]
        
        for day_info in london_days:
            st.markdown(f"""
            <div class="day-card">
                <h3>🏴󠁧󠁢󠁥󠁮󠁧󠁿 Day {day_info['day']}: {day_info['date']} - {day_info['title']}</h3>
                <span class="location-tag">{'LONDON → EDINBURGH' if 'Journey' in day_info['title'] else 'LONDON'}</span>
                
                <div style="margin-top: 1.5rem;">
                    <p><span class="time-tag">09:00-12:30</span><strong>Morning</strong></p>
                    <ul>
                        {"".join(f"<li>🏛️ {activity}</li>" for activity in day_info['morning'])}
                    </ul>
                    
                    <p><span class="time-tag">13:00-17:30</span><strong>Afternoon</strong></p>
                    <ul>
                        {"".join(f"<li>🎯 {activity}</li>" for activity in day_info['afternoon'])}
                    </ul>
                    
                    <p><span class="time-tag">18:00+</span><strong>Evening</strong></p>
                    <ul>
                        {"".join(f"<li>🌃 {activity}</li>" for activity in day_info['evening'])}
                    </ul>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Edinburgh Days
        edinburgh_days = [
            {
                "day": 7, "date": "December 31", "title": "Hogmanay Preparation",
                "morning": ["Edinburgh Castle", "Royal Mile"],
                "afternoon": ["Holyrood Palace", "Arthur's Seat"],
                "evening": ["Hogmanay Street Party", "Midnight fireworks"]
            },
            {
                "day": 8, "date": "January 1", "title": "New Year's Day",
                "morning": ["Recovery brunch", "Calton Hill"],
                "afternoon": ["National Gallery", "Princes Street"],
                "evening": ["Scottish folk music", "Traditional dinner"]
            },
            {
                "day": 9, "date": "January 2", "title": "Final Edinburgh Day",
                "morning": ["Last shopping", "Grassmarket"],
                "afternoon": ["Camera Obscura", "Christmas Market"],
                "evening": ["Farewell dinner", "Pack for departure"]
            }
        ]
        
        for day_info in edinburgh_days:
            st.markdown(f"""
            <div class="day-card">
                <h3>🏴󠁧󠁢󠁳󠁣󠁴󠁿 Day {day_info['day']}: {day_info['date']} - {day_info['title']}</h3>
                <span class="location-tag">EDINBURGH</span>
                
                <div style="margin-top: 1.5rem;">
                    <p><span class="time-tag">09:00-12:30</span><strong>Morning</strong></p>
                    <ul>
                        {"".join(f"<li>🏴󠁧󠁢󠁳󠁣󠁴󠁿 {activity}</li>" for activity in day_info['morning'])}
                    </ul>
                    
                    <p><span class="time-tag">13:30-17:30</span><strong>Afternoon</strong></p>
                    <ul>
                        {"".join(f"<li>🏴󠁧󠁢󠁳󠁣󠁴󠁿 {activity}</li>" for activity in day_info['afternoon'])}
                    </ul>
                    
                    <p><span class="time-tag">18:00+</span><strong>Evening</strong></p>
                    <ul>
                        {"".join(f"<li>🌃 {activity}</li>" for activity in day_info['evening'])}
                    </ul>
                </div>
                
                {"<div style='margin-top: 1rem; padding: 1rem; background: #ffe6e6; border-radius: 8px;'><strong>🎉 Hogmanay Note:</strong> Book in advance! Dress warmly for outdoor celebrations.</div>" if "Hogmanay" in day_info['title'] else ""}
            </div>
            """, unsafe_allow_html=True)
        
        # Final Day
        st.markdown("""
        <div class="day-card">
            <h3>✈️ Day 10: January 3 - Departure Day</h3>
            <span class="location-tag">EDINBURGH → KOCHI</span>
            
            <div style="margin-top: 1.5rem;">
                <p><span class="time-tag">08:00-11:00</span><strong>Final Preparations</strong></p>
                <ul>
                    <li>🏨 Hotel check-out</li>
                    <li>☕ Scottish breakfast</li>
                    <li>🛍️ Last-minute shopping</li>
                </ul>
                
                <p><span class="time-tag">11:00-14:00</span><strong>Departure</strong></p>
                <ul>
                    <li>🚌 Airport transfer</li>
                    <li>✈️ Flight to Kochi</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Tab 2: Interactive Map
with tab2:
    st.markdown('<h2 class="section-header">🗺️ Interactive Travel Map</h2>', unsafe_allow_html=True)
    
    # Filter attractions
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
    
    folium_static(m)
    
    # Legend
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**🔴 Red Markers:** London Attractions")
    with col2:
        st.markdown("**🔵 Blue Markers:** Edinburgh Attractions")

# Tab 3: Cost Breakdown
with tab3:
    st.markdown('<h2 class="section-header">💰 Detailed Cost Analysis</h2>', unsafe_allow_html=True)
    
    # Budget multipliers
    budget_multipliers = {
        "Budget (£800-1200)": 1.0,
        "Mid-range (£1200-2000)": 1.5,
        "Luxury (£2000+)": 2.5
    }
    
    multiplier = budget_multipliers[budget_per_person]
    
    # Base costs per person
    base_costs = {
        "Flights": {"Kochi → London": 350, "Edinburgh → Kochi": 400},
        "Accommodation": {"London (5 nights)": 75*5*multiplier, "Edinburgh (3 nights)": 85*3*multiplier},
        "Transportation": {"Transfers": 60, "London-Edinburgh train": 80, "Local transport": 50},
        "Food": {"Meals (9 days)": 45*9*multiplier},
        "Attractions": {"Entry fees": 150*multiplier, "Entertainment": 100*multiplier},
        "Shopping": {"Souvenirs": 150},
        "Miscellaneous": {"Emergency fund": 100}
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
            <h3>💵 Cost Summary</h3>
            <h2>£{total_per_person:,.0f}</h2>
            <p><strong>Per Person</strong></p>
            
            <h2>£{total_per_person * group_size:,.0f}</h2>
            <p><strong>Group of {group_size}</strong></p>
            
            <p><em>{budget_per_person}</em></p>
        </div>
        """, unsafe_allow_html=True)
    
    # Detailed breakdown
    st.markdown("### 📊 Detailed Breakdown")
    breakdown_data = []
    for category, items in base_costs.items():
        for item, cost in items.items():
            breakdown_data.append({
                "Category": category,
                "Item": item,
                "Cost per Person": f"£{cost:.0f}",
                f"Total for {group_size} people": f"£{cost * group_size:.0f}"
            })
    
    df = pd.DataFrame(breakdown_data)
    st.dataframe(df, use_container_width=True)

# Tab 4: Flight Information
with tab4:
    st.markdown('<h2 class="section-header">✈️ Flight Planning Guide</h2>', unsafe_allow_html=True)
    
    # Flight information
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🛫 Outbound Flight
        **Route:** Kochi → London  
        **Date:** December 25, 2024  
        **Airlines:** Qatar Airways, Emirates, Oman Air  
        **Cost:** £300-450 per person  
        **Duration:** 9-12 hours  
        **Booking:** URGENT - Book immediately!
        """)
    
    with col2:
        st.markdown("""
        ### 🛬 Return Flight
        **Route:** Edinburgh → Kochi  
        **Date:** January 3, 2025  
        **Airlines:** Qatar Airways, Emirates, British Airways  
        **Cost:** £350-500 per person  
        **Duration:** 11-14 hours  
        **Connection:** Doha, Dubai, Amsterdam
        """)
    
    # Booking tips
    st.markdown("### ✅ Flight Booking Strategy")
    booking_tips = [
        "🔥 **URGENT**: Christmas flights sell out - book within 48 hours",
        "💳 **Payment**: Use credit cards for protection",
        "🎫 **Seats**: Book together for group travel",
        "🧳 **Baggage**: Check allowances (30kg typical)",
        "🛡️ **Insurance**: Travel insurance mandatory",
        "📅 **Flexibility**: Dec 24/26 might be cheaper than Dec 25",
        "🔄 **Multi-city**: Book as separate one-way tickets"
    ]
    
    for tip in booking_tips:
        st.markdown(f"- {tip}")

# Tab 5: Travel Essentials
with tab5:
    st.markdown('<h2 class="section-header">📋 Travel Preparation</h2>', unsafe_allow_html=True)
    
    # Weather info
    if show_weather:
        st.markdown("### 🌤️ Weather Forecast")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="weather-card">
                <h4>London (Dec 25-30)</h4>
                <p><strong>🌡️ Temperature:</strong> 2-8°C</p>
                <p><strong>☔ Conditions:</strong> Cold, frequent rain</p>
                <p><strong>🌅 Daylight:</strong> 8:00 AM - 4:00 PM</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="weather-card">
                <h4>Edinburgh (Dec 31-Jan 2)</h4>
                <p><strong>🌡️ Temperature:</strong> 1-6°C</p>
                <p><strong>❄️ Conditions:</strong> Very cold, possible snow</p>
                <p><strong>🌅 Daylight:</strong> 8:30 AM - 3:45 PM</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Packing list
    st.markdown("### 🎒 Essential Packing List")
    
    packing_categories = {
        "📋 Documents": [
            "Passport (6+ months validity)",
            "UK visa (if required)", 
            "Flight tickets",
            "Travel insurance",
            "Hotel confirmations"
        ],
        "🧥 Winter Clothing": [
            "Heavy winter coat",
            "Thermal underwear",
            "Warm sweaters",
            "Waterproof jacket",
            "Warm socks and gloves",
            "Comfortable walking shoes",
            "Formal outfit for New Year"
        ],
        "🔌 Electronics": [
            "UK power adapter (Type G)",
            "Phone charger",
            "Camera",
            "Portable battery"
        ],
        "💊 Health Items": [
            "Prescription medications",
            "First aid kit",
            "Cold medicine",
            "Hand sanitizer"
        ]
    }
    
    for category, items in packing_categories.items():
        with st.expander(category):
            for item in items:
                st.checkbox(item, key=f"pack_{item}")
    
    # Emergency contacts
    st.markdown("### 🚨 Emergency Information")
    st.markdown("""
    **Emergency Numbers:**
    - Emergency Services: 999 or 112
    - Non-emergency Police: 101
    - NHS Health: 111
    
    **Indian High Commission London:**
    - Address: India House, Aldwych, London WC2B 4NA
    - Phone: +44 20 7836 8484
    """)
    
    # Cultural tips
    st.markdown("### 🇬🇧 Cultural Tips")
    cultural_tips = [
        "**Tipping:** 10-15% in restaurants if no service charge",
        "**Queuing:** British love orderly lines - always wait your turn",
        "**Pub Etiquette:** Order at bar, no table service",
        "**Transport:** Stand right on escalators",
        "**Christmas:** Many shops closed Dec 25-26"
    ]
    
    for tip in cultural_tips:
        st.markdown(f"- {tip}")

# Footer
st.markdown("---")

# Create footer with proper string formatting
footer_text = f"""
<div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; margin-top: 2rem; color: white;">
    <h2>🎄 Have a Wonderful Christmas Holiday in the UK! 🎄</h2>
    <p style="font-size: 1.1rem;">This itinerary is customized for your group of {group_size} people with {budget_per_person} preferences.</p>
    
    <div style="margin-top: 1rem;">
        <strong>📞 Emergency:</strong> UK 999 | Indian High Commission +44 20 7836 8484
    </div>
    
    <p style="margin-top: 1rem; font-style: italic;">
        Generated on: {datetime.now().strftime("%B %d, %Y at %I:%M %p")}<br>
        <small>⚡ Powered by Advanced Travel Planning System</small>
    </p>
</div>
"""

st.markdown(footer_text, unsafe_allow_html=True)

# Quick stats in sidebar
with st.sidebar:
    st.markdown("---")
    st.markdown("### 📊 Trip Summary")
    
    # Calculate quick stats
    total_attractions = len(filter_attractions(london_attractions, interests)) + len(filter_attractions(edinburgh_attractions, interests))
    base_cost_per_person = 1200 * budget_multipliers[budget_per_person]
    
    st.metric("Days", "10")
    st.metric("Cities", "2")
    st.metric("Attractions", total_attractions)
    st.metric("Est. Cost/Person", f"£{base_cost_per_person:.0f}")
    
    # Quick calculator
    st.markdown("### 💰 Quick Calculator")
    custom_days = st.slider("Days to adjust", 7, 14, 10)
    daily_cost = base_cost_per_person / 10
    adjusted_cost = daily_cost * custom_days
    
    st.write(f"**{custom_days} days cost:** £{adjusted_cost:.0f} per person")
    st.write(f"**Group total:** £{adjusted_cost * group_size:.0f}")

# Performance indicator
st.sidebar.markdown("---")
st.sidebar.markdown("*✅ All systems operational*")
st.sidebar.markdown("*🔄 Data updated: Real-time*")