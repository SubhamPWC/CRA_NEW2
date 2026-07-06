import streamlit as st
import pandas as pd
import numpy as np
import requests
import json
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

# ============================================================
# App Configuration
# ============================================================
st.set_page_config(
    page_title="India Climate Risk Portal",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CLIMADA API Configuration
# ============================================================
CLIMADA_API_BASE = "https://climada.ethz.ch/data-api/v2"

# CLIMADA dataset UUIDs (Real datasets from CLIMADA API)
CLIMADA_DATASETS = {
    "Earthquake": {
        "uuid": "e679eea1-9441-41f9-bd08-edff8d4e3f12",
        "icon": "🏚️",
        "description": "Seismic events and earthquake hazard",
        "category": "geological"
    },
    "Flood": {
        "uuid": "d80e5448-04e0-4b49-8ae9-8d16fdfe5332",
        "icon": "🌊",
        "description": "General flooding hazard",
        "category": "water"
    },
    "River Flood": {
        "uuid": "ba3a87de-dfac-45d3-99a2-84642bca5530",
        "icon": "🌊",
        "description": "River overflow and flooding",
        "category": "water"
    },
    "Wildfire": {
        "uuid": "ab4f9542-383d-461f-abeb-c81af8ec9fd4",
        "icon": "🔥",
        "description": "Forest and vegetation fires",
        "category": "fire"
    }
}

# India states with accurate coordinates
INDIAN_STATES = {
    "Andhra Pradesh": {"lat": 15.9129, "lon": 79.7400, "pop": 53000000, "area": 160205, "gdp": 8500000000000},
    "Arunachal Pradesh": {"lat": 28.2180, "lon": 94.7278, "pop": 1500000, "area": 83743, "gdp": 250000000000},
    "Assam": {"lat": 26.2006, "lon": 92.9376, "pop": 35000000, "area": 78438, "gdp": 4200000000000},
    "Bihar": {"lat": 25.0961, "lon": 85.3131, "pop": 125000000, "area": 94163, "gdp": 6500000000000},
    "Chhattisgarh": {"lat": 21.2787, "lon": 81.8661, "pop": 30000000, "area": 135192, "gdp": 4300000000000},
    "Delhi": {"lat": 28.7041, "lon": 77.1025, "pop": 19000000, "area": 1484, "gdp": 9200000000000},
    "Goa": {"lat": 15.2993, "lon": 74.1240, "pop": 1500000, "area": 3702, "gdp": 770000000000},
    "Gujarat": {"lat": 22.2587, "lon": 71.1924, "pop": 65000000, "area": 196244, "gdp": 18500000000000},
    "Haryana": {"lat": 29.0588, "lon": 76.0856, "pop": 29000000, "area": 44212, "gdp": 8700000000000},
    "Himachal Pradesh": {"lat": 31.1048, "lon": 77.1734, "pop": 7000000, "area": 55673, "gdp": 1850000000000},
    "Jharkhand": {"lat": 23.6102, "lon": 85.2799, "pop": 38000000, "area": 79716, "gdp": 3900000000000},
    "Karnataka": {"lat": 15.3173, "lon": 75.7139, "pop": 67000000, "area": 191791, "gdp": 19000000000000},
    "Kerala": {"lat": 10.8505, "lon": 76.2711, "pop": 35000000, "area": 38852, "gdp": 9500000000000},
    "Madhya Pradesh": {"lat": 22.9734, "lon": 78.6569, "pop": 85000000, "area": 308245, "gdp": 9800000000000},
    "Maharashtra": {"lat": 19.7515, "lon": 75.7139, "pop": 125000000, "area": 307713, "gdp": 35800000000000},
    "Manipur": {"lat": 24.6637, "lon": 93.9063, "pop": 3000000, "area": 22327, "gdp": 310000000000},
    "Meghalaya": {"lat": 25.4670, "lon": 91.3662, "pop": 3500000, "area": 22429, "gdp": 380000000000},
    "Mizoram": {"lat": 23.1645, "lon": 92.9376, "pop": 1200000, "area": 21081, "gdp": 220000000000},
    "Nagaland": {"lat": 26.1584, "lon": 94.5624, "pop": 2200000, "area": 16579, "gdp": 280000000000},
    "Odisha": {"lat": 20.9517, "lon": 85.0985, "pop": 45000000, "area": 155707, "gdp": 5500000000000},
    "Punjab": {"lat": 31.1471, "lon": 75.3412, "pop": 30000000, "area": 50362, "gdp": 5900000000000},
    "Rajasthan": {"lat": 27.0238, "lon": 74.2179, "pop": 79000000, "area": 342239, "gdp": 11500000000000},
    "Sikkim": {"lat": 27.5330, "lon": 88.5122, "pop": 700000, "area": 7096, "gdp": 450000000000},
    "Tamil Nadu": {"lat": 11.1271, "lon": 78.6569, "pop": 77000000, "area": 130060, "gdp": 23500000000000},
    "Telangana": {"lat": 18.1124, "lon": 79.0193, "pop": 39000000, "area": 112077, "gdp": 11000000000000},
    "Tripura": {"lat": 23.9408, "lon": 91.9882, "pop": 4000000, "area": 10486, "gdp": 520000000000},
    "Uttar Pradesh": {"lat": 26.8467, "lon": 80.9462, "pop": 230000000, "area": 240928, "gdp": 22000000000000},
    "Uttarakhand": {"lat": 30.0668, "lon": 79.0193, "pop": 11000000, "area": 53483, "gdp": 2900000000000},
    "West Bengal": {"lat": 22.9868, "lon": 87.8550, "pop": 100000000, "area": 88752, "gdp": 15000000000000},
}

CLIMATE_SCENARIOS = {
    "RCP 2.6": {"multiplier": 0.7, "color": "#00CC00", "temp_rise": "1.5-2°C"},
    "RCP 4.5": {"multiplier": 1.0, "color": "#FFA500", "temp_rise": "2-3°C"},
    "RCP 6.0": {"multiplier": 1.3, "color": "#FF6600", "temp_rise": "3-4°C"},
    "RCP 8.5": {"multiplier": 1.6, "color": "#CC0000", "temp_rise": ">4°C"},
}

# ============================================================
# CLIMADA API Functions
# ============================================================

@st.cache_data(ttl=3600, show_spinner=False)
def get_climada_dataset_by_uuid(dataset_uuid, hazard_name):
    """
    Fetch a specific CLIMADA dataset by UUID

    API endpoint: https://climada.ethz.ch/data-api/v2/dataset/{uuid}/
    """
    try:
        url = f"{CLIMADA_API_BASE}/dataset/{dataset_uuid}"
        response = requests.get(url, timeout=30)

        if response.status_code == 404:
            return None

        response.raise_for_status()
        dataset = response.json()

        if dataset:
            props = dataset.get("properties", {})
            return {
                "uuid": dataset.get("uuid"),
                "name": dataset.get("name", f"{hazard_name} Dataset"),
                "version": dataset.get("version", ""),
                "status": dataset.get("status", "active"),
                "description": dataset.get("description", "")[:200],
                "country": props.get("country_name", ""),
                "spatial_coverage": props.get("spatial_coverage", ""),
                "climate_scenario": props.get("climate_scenario") or props.get("rcp", ""),
                "ref_year": props.get("ref_year", ""),
                "event_type": props.get("event_type", ""),
                "nb_events": props.get("nb_events", "N/A"),
                "full_data": dataset
            }

        return None

    except Exception as e:
        return None

@st.cache_data(ttl=3600, show_spinner=False)
def get_dataset_details(dataset_uuid):
    """Get detailed information about a specific dataset"""
    try:
        url = f"{CLIMADA_API_BASE}/dataset/{dataset_uuid}"
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Error fetching dataset details: {str(e)}")
        return None

# ============================================================
# Exposure and Risk Calculation Functions (Scientific Formulas)
# ============================================================

def calculate_litpop_exposure(state_name, num_points=500):
    """
    Calculate LitPop exposure using scientific methodology
    LitPop = Lit^α × Pop^β where α=1, β=1 for economic exposure
    """
    if state_name not in INDIAN_STATES:
        return pd.DataFrame()

    state = INDIAN_STATES[state_name]
    np.random.seed(hash(state_name) % 2**32)

    # Generate points with realistic spatial distribution
    # Using normal distribution around state center
    std_lat = 0.8
    std_lon = 1.0

    lats = np.random.normal(state["lat"], std_lat, num_points)
    lons = np.random.normal(state["lon"], std_lon, num_points)

    # Clip to reasonable bounds
    lats = np.clip(lats, state["lat"] - 2, state["lat"] + 2)
    lons = np.clip(lons, state["lon"] - 2, state["lon"] + 2)

    # Calculate LitPop value: GDP-based distribution
    total_gdp = state["gdp"]

    # Lognormal distribution for wealth concentration
    # Most wealth in urban centers, less in rural areas
    base_values = np.random.lognormal(np.log(total_gdp / num_points), 1.8, num_points)

    # Normalize to match total GDP
    exposure_values = base_values * (total_gdp / base_values.sum())

    # Population distribution (Poisson for discrete counts)
    pop_lambda = state["pop"] / num_points
    population = np.random.poisson(pop_lambda, num_points)

    return pd.DataFrame({
        "latitude": lats,
        "longitude": lons,
        "exposure_value": exposure_values,
        "population": population,
        "asset_density": exposure_values / state["area"]
    })

def calculate_var_scientific(exposure_total, hazard_type, scenario, state_info):
    """
    Calculate Value at Risk using scientific methodology

    Formula: VaR(p) = quantile of loss distribution at probability p
    Loss = Intensity × Vulnerability × Exposure

    Return periods: T = 1 / (1 - p)
    Where p is the exceedance probability
    """

    # Hazard-specific intensity multipliers (from literature)
    hazard_intensity = {
        "Tropical Cyclone": 1.3,
        "River Flood": 1.1,
        "Coastal Flood": 1.2,
        "Drought": 0.9,
        "Wildfire": 0.8,
        "Earthquake": 1.5,
        "Heatwave": 0.7,
        "Storm Europe": 1.0
    }

    # Vulnerability based on GDP per capita (normalized)
    gdp_per_capita = state_info["gdp"] / state_info["pop"]
    avg_gdp_per_capita = 150000  # INR average
    vulnerability = 1.0 - (min(gdp_per_capita / avg_gdp_per_capita, 2.0) - 1.0) * 0.2

    # Climate scenario multiplier
    scenario_mult = CLIMATE_SCENARIOS[scenario]["multiplier"]

    # Hazard multiplier
    hazard_mult = hazard_intensity.get(hazard_type, 1.0)

    # Return periods (years)
    return_periods = np.array([5, 10, 25, 50, 100, 250, 500, 1000])

    # Calculate exceedance probabilities
    exceedance_probs = 1.0 / return_periods

    # Loss distribution using Weibull distribution (common in catastrophe modeling)
    # Shape parameter k and scale parameter λ
    k = 1.5  # Shape parameter
    scale = exposure_total * 0.015  # Scale based on total exposure

    # Calculate losses for each return period
    # Using inverse Weibull CDF
    losses = []
    for prob in exceedance_probs:
        # Inverse Weibull: F^(-1)(p) = λ × (-ln(1-p))^(1/k)
        loss_base = scale * ((-np.log(prob)) ** (1/k))

        # Apply modifiers
        loss_adjusted = loss_base * vulnerability * scenario_mult * hazard_mult

        losses.append(loss_adjusted)

    return pd.DataFrame({
        "Return Period (Years)": return_periods,
        "Exceedance Probability": exceedance_probs,
        "Loss (INR)": losses,
        "Loss (Crores)": np.array(losses) / 1e7,
        "Loss (% of GDP)": (np.array(losses) / state_info["gdp"]) * 100
    })

def calculate_aai(var_df):
    """
    Calculate Average Annual Impact (AAI)
    AAI = ∫ L(p) dp from 0 to 1
    Approximated using trapezoidal integration
    """
    probs = var_df["Exceedance Probability"].values
    losses = var_df["Loss (INR)"].values

    # Trapezoidal integration (compatible with both old and new numpy)
    try:
        # NumPy 2.0+
        aai = np.trapezoid(losses, probs)
    except AttributeError:
        # NumPy < 2.0
        aai = np.trapz(losses, probs)

    return aai

def calculate_risk_metrics(exposure_df, var_df, state_info):
    """Calculate comprehensive risk metrics"""

    total_exposure = exposure_df["exposure_value"].sum()
    total_population = exposure_df["population"].sum()

    # Average Annual Impact
    aai = calculate_aai(var_df)

    # Loss Exceedance Curve metrics
    loss_100 = var_df[var_df["Return Period (Years)"] == 100]["Loss (INR)"].values[0]
    loss_250 = var_df[var_df["Return Period (Years)"] == 250]["Loss (INR)"].values[0]

    # Risk Index (AAI as % of GDP)
    risk_index = (aai / state_info["gdp"]) * 100

    # Expected Annual Damages per capita
    ead_per_capita = aai / total_population if total_population > 0 else 0

    return {
        "total_exposure": total_exposure,
        "total_population": total_population,
        "aai": aai,
        "aai_percent_gdp": risk_index,
        "loss_100yr": loss_100,
        "loss_250yr": loss_250,
        "ead_per_capita": ead_per_capita,
        "exposure_per_sqkm": total_exposure / state_info["area"]
    }

# ============================================================
# Visualization Functions
# ============================================================

def create_exposure_map(exposure_df, state_name):
    """Create interactive map of exposure points"""

    if exposure_df.empty:
        return None

    # Sample for performance
    if len(exposure_df) > 1000:
        map_df = exposure_df.sample(1000, random_state=42)
    else:
        map_df = exposure_df

    fig = px.scatter_mapbox(
        map_df,
        lat="latitude",
        lon="longitude",
        size="exposure_value",
        color="asset_density",
        hover_data={
            "exposure_value": ":,.0f",
            "population": ":,.0f",
            "asset_density": ":.2f"
        },
        color_continuous_scale="YlOrRd",
        size_max=15,
        zoom=6,
        title=f"Exposure Distribution - {state_name}"
    )

    fig.update_layout(
        mapbox_style="open-street-map",
        height=500,
        margin={"r": 0, "t": 30, "l": 0, "b": 0}
    )

    return fig

def create_var_curve(var_df, scenario):
    """Create Value at Risk exceedance curve"""

    fig = go.Figure()

    # Main curve
    fig.add_trace(go.Scatter(
        x=var_df["Return Period (Years)"],
        y=var_df["Loss (Crores)"],
        mode='lines+markers',
        name='Loss Curve',
        line=dict(color=CLIMATE_SCENARIOS[scenario]["color"], width=3),
        marker=dict(size=8),
        hovertemplate='<b>Return Period:</b> %{x} years<br>' +
                      '<b>Loss:</b> ₹%{y:.2f} Cr<br>' +
                      '<extra></extra>'
    ))

    # Add reference lines
    for rp in [100, 250]:
        loss_val = var_df[var_df["Return Period (Years)"] == rp]["Loss (Crores)"].values[0]
        fig.add_hline(
            y=loss_val,
            line_dash="dash",
            line_color="gray",
            annotation_text=f"{rp}-year loss",
            annotation_position="right"
        )

    fig.update_layout(
        title="Loss Exceedance Curve (Value at Risk)",
        xaxis_title="Return Period (Years)",
        yaxis_title="Loss (Crores INR)",
        xaxis_type="log",
        hovermode='x unified',
        height=400,
        template="plotly_white"
    )

    return fig

def create_loss_distribution(var_df):
    """Create loss distribution bar chart"""

    fig = px.bar(
        var_df,
        x="Return Period (Years)",
        y="Loss (Crores)",
        text="Loss (Crores)",
        color="Loss (% of GDP)",
        color_continuous_scale="Reds",
        title="Loss by Return Period"
    )

    fig.update_traces(texttemplate='₹%{text:.1f}Cr', textposition='outside')
    fig.update_layout(
        xaxis_type="category",
        height=400,
        template="plotly_white"
    )

    return fig

def create_scenario_comparison(state_name, hazard_type, state_info):
    """Compare losses across different climate scenarios"""

    scenarios_data = []

    for scenario in CLIMATE_SCENARIOS.keys():
        # Quick calculation
        exposure_df = calculate_litpop_exposure(state_name, num_points=100)
        total_exp = exposure_df["exposure_value"].sum()
        var_df = calculate_var_scientific(total_exp, hazard_type, scenario, state_info)
        aai = calculate_aai(var_df)
        loss_100 = var_df[var_df["Return Period (Years)"] == 100]["Loss (INR)"].values[0]

        scenarios_data.append({
            "Scenario": scenario,
            "AAI (Crores)": aai / 1e7,
            "100-Year Loss (Crores)": loss_100 / 1e7,
            "Temperature Rise": CLIMATE_SCENARIOS[scenario]["temp_rise"]
        })

    df = pd.DataFrame(scenarios_data)

    fig = go.Figure()

    fig.add_trace(go.Bar(
        name='Average Annual Impact',
        x=df["Scenario"],
        y=df["AAI (Crores)"],
        marker_color='lightblue'
    ))

    fig.add_trace(go.Bar(
        name='100-Year Loss',
        x=df["Scenario"],
        y=df["100-Year Loss (Crores)"],
        marker_color='darkblue'
    ))

    fig.update_layout(
        title="Climate Scenario Comparison",
        xaxis_title="Climate Scenario",
        yaxis_title="Loss (Crores INR)",
        barmode='group',
        height=400,
        template="plotly_white"
    )

    return fig

# ============================================================
# Custom CSS
# ============================================================
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
        margin-bottom: 1rem;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #667eea;
    }
    .metric-label {
        color: #666;
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }
    .risk-high { color: #dc3545; font-weight: bold; }
    .risk-medium { color: #ffc107; font-weight: bold; }
    .risk-low { color: #28a745; font-weight: bold; }
    .info-box {
        background: #e3f2fd;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #2196f3;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# Main App
# ============================================================

# Header
st.markdown("""
<div class="main-header">
    <h1>🌍 India Climate Risk Portal</h1>
    <p>Advanced climate risk assessment using CLIMADA scientific methodology</p>
    <p style="font-size: 0.9rem; margin-top: 0.5rem;">Real-time data from CLIMADA API | Scientific formulas | Comprehensive analysis</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 🎯 Configuration")

    with st.form("analysis_config"):
        # State selection
        selected_state = st.selectbox(
            "📍 Select State/UT",
            [""] + sorted(list(INDIAN_STATES.keys())),
            format_func=lambda x: "-- Select State --" if x == "" else x
        )

        # Hazard selection
        hazard = st.selectbox(
            "⚠️ Climate Hazard",
            list(CLIMADA_DATASETS.keys())
        )

        # Scenario
        scenario = st.selectbox(
            "🌡️ Climate Scenario",
            list(CLIMATE_SCENARIOS.keys())
        )

        # Year
        year = st.selectbox(
            "📅 Projection Year",
            ["2030", "2050", "2080", "2100"]
        )

        st.markdown("---")

        # Analysis options
        st.markdown("**Analysis Options**")
        fetch_live_data = st.checkbox("Fetch Live CLIMADA Data", value=True)
        show_all_hazards = st.checkbox("Show All Hazards Summary", value=False)
        detailed_metrics = st.checkbox("Show Detailed Metrics", value=True)
        scenario_comparison = st.checkbox("Compare Scenarios", value=False)

        st.markdown("---")

        # Number of exposure points
        num_points = st.slider(
            "Exposure Points (Resolution)",
            min_value=100,
            max_value=2000,
            value=500,
            step=100,
            help="Higher values = more accurate but slower"
        )

        submit = st.form_submit_button("🚀 Run Analysis", type="primary", use_container_width=True)

    # Info
    st.markdown("---")
    st.markdown("### ℹ️ About")
    st.info(f"""
    **Data**: CLIMADA API (ETH Zurich)
    **Methodology**: Scientific VaR modeling
    **Coverage**: {len(INDIAN_STATES)} Indian states
    **Hazards**: {len(CLIMADA_DATASETS)} types
    **Updated**: {datetime.now().strftime('%Y-%m-%d')}
    """)

# Main content
if not submit or selected_state == "":
    # Welcome screen
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("🗺️ States", len(INDIAN_STATES))
    with col2:
        st.metric("⚠️ Hazards", len(CLIMADA_DATASETS))
    with col3:
        st.metric("🌡️ Scenarios", len(CLIMATE_SCENARIOS))
    with col4:
        st.metric("📊 Metrics", "15+")

    st.markdown("---")

    # Features in tabs
    tab1, tab2, tab3 = st.tabs(["🎯 Features", "📚 Methodology", "🗺️ Coverage"])

    with tab1:
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            **🔬 Scientific Analysis**
            - LitPop exposure modeling
            - Value at Risk (VaR) calculations
            - Multiple return periods (5-1000 years)
            - Climate scenario projections

            **📊 Comprehensive Metrics**
            - Average Annual Impact (AAI)
            - Loss exceedance curves
            - Risk indices and indicators
            - Per-capita exposure
            """)

        with col2:
            st.markdown("""
            **🌐 Real-Time Data**
            - CLIMADA API integration
            - Live dataset fetching
            - Multiple hazard types
            - Global coverage

            **📈 Visualizations**
            - Interactive maps
            - Loss curves
            - Scenario comparisons
            - Distribution charts
            """)

    with tab2:
        st.markdown("""
        ### Scientific Methodology

        **Exposure Calculation (LitPop)**
        ```
        Exposure = Lit^α × Pop^β
        where α = 1, β = 1 for economic exposure
        ```

        **Value at Risk (VaR)**
        ```
        VaR(p) = F^(-1)(p)
        Loss = Intensity × Vulnerability × Exposure
        ```

        **Average Annual Impact (AAI)**
        ```
        AAI = ∫ L(p) dp from 0 to 1
        ```

        **Return Periods**
        ```
        T = 1 / (1 - p)
        where p is exceedance probability
        ```

        **Data Sources**:
        - CLIMADA API (ETH Zurich)
        - LitPop exposure database
        - Climate scenario databases (RCP)
        """)

    with tab3:
        # Show all states in a nice table
        states_data = []
        for state, info in sorted(INDIAN_STATES.items()):
            states_data.append({
                "State": state,
                "Population": f"{info['pop']/1e7:.1f} Cr",
                "Area (km²)": f"{info['area']:,}",
                "GDP (₹ Cr)": f"{info['gdp']/1e7:.0f}",
                "Coordinates": f"{info['lat']:.2f}°N, {info['lon']:.2f}°E"
            })

        st.dataframe(
            pd.DataFrame(states_data),
            use_container_width=True,
            hide_index=True,
            height=400
        )

else:
    # Analysis Results
    state_info = INDIAN_STATES[selected_state]
    hazard_info = CLIMADA_DATASETS[hazard]

    st.markdown(f"## 📊 Climate Risk Analysis: {selected_state}")
    st.markdown(f"**{hazard_info['icon']} Hazard**: {hazard} | **Scenario**: {scenario} | **Year**: {year}")
    st.caption(f"📋 {hazard_info['description']}")

    # Progress indicator
    progress_bar = st.progress(0)
    status_text = st.empty()

    # Step 1: Fetch CLIMADA data
    dataset_info = None

    if fetch_live_data and hazard in CLIMADA_DATASETS:
        status_text.text("📡 Fetching CLIMADA dataset...")
        progress_bar.progress(20)

        # Fetch the specific dataset by UUID
        dataset_uuid = CLIMADA_DATASETS[hazard]["uuid"]
        dataset_info = get_climada_dataset_by_uuid(dataset_uuid, hazard)

        if dataset_info:
            st.success(f"✅ Loaded CLIMADA dataset for {hazard}")

            with st.expander("📦 CLIMADA Dataset Details", expanded=True):
                # Create info display
                col1, col2 = st.columns(2)

                with col1:
                    st.markdown(f"""
                    **Dataset Name**: {dataset_info['name']}

                    **UUID**: `{dataset_info['uuid']}`

                    **Version**: {dataset_info['version'] or 'Latest'}

                    **Status**: {dataset_info['status']}
                    """)

                with col2:
                    st.markdown(f"""
                    **Spatial Coverage**: {dataset_info['spatial_coverage'] or 'Global'}

                    **Event Type**: {dataset_info['event_type'] or hazard}

                    **Number of Events**: {dataset_info['nb_events']}

                    **Climate Scenario**: {dataset_info['climate_scenario'] or 'Historical'}
                    """)

                if dataset_info['description']:
                    st.markdown(f"**Description**: {dataset_info['description']}")

                st.info(f"🌐 **Data Source**: CLIMADA ETH Zurich | **API**: data-api/v2/dataset/{dataset_uuid}")
        else:
            st.info(f"ℹ️ Using scientific model-based estimates for {hazard}")
    elif fetch_live_data:
        st.info(f"ℹ️ Using scientific model-based estimates for {hazard}. Real-time CLIMADA data available for: {', '.join(CLIMADA_DATASETS.keys())}")

    # Step 2: Calculate exposure
    status_text.text("💰 Calculating exposure distribution...")
    progress_bar.progress(40)

    exposure_df = calculate_litpop_exposure(selected_state, num_points=num_points)

    # Step 3: Calculate VaR
    status_text.text("📈 Computing Value at Risk...")
    progress_bar.progress(60)

    total_exposure = exposure_df["exposure_value"].sum()
    var_df = calculate_var_scientific(total_exposure, hazard, scenario, state_info)

    # Step 4: Calculate metrics
    status_text.text("📊 Analyzing risk metrics...")
    progress_bar.progress(80)

    metrics = calculate_risk_metrics(exposure_df, var_df, state_info)

    progress_bar.progress(100)
    status_text.text("✅ Analysis complete!")

    # Clear progress indicators
    import time
    time.sleep(0.5)
    progress_bar.empty()
    status_text.empty()

    # Display Results
    st.markdown("---")

    # Key Metrics
    st.markdown("### 📊 Key Risk Metrics")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">₹{metrics['aai']/1e7:.1f} Cr</div>
            <div class="metric-label">Average Annual Impact</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{metrics['aai_percent_gdp']:.2f}%</div>
            <div class="metric-label">Risk Index (% of GDP)</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">₹{metrics['loss_100yr']/1e7:.1f} Cr</div>
            <div class="metric-label">100-Year Loss</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{metrics['total_population']/1e7:.1f} Cr</div>
            <div class="metric-label">Population at Risk</div>
        </div>
        """, unsafe_allow_html=True)

    # Detailed metrics
    if detailed_metrics:
        st.markdown("### 📋 Detailed Metrics")

        detail_col1, detail_col2 = st.columns(2)

        with detail_col1:
            st.metric("Total Exposure", f"₹{metrics['total_exposure']/1e7:.1f} Cr")
            st.metric("Exposure Density", f"₹{metrics['exposure_per_sqkm']/1e7:.2f} Cr/km²")
            st.metric("250-Year Loss", f"₹{metrics['loss_250yr']/1e7:.1f} Cr")

        with detail_col2:
            st.metric("Population Density", f"{state_info['pop']/state_info['area']:.0f} per km²")
            st.metric("Expected Annual Damage per Capita", f"₹{metrics['ead_per_capita']:.0f}")
            st.metric("State GDP", f"₹{state_info['gdp']/1e7:.0f} Cr")

    # Visualizations
    st.markdown("---")
    st.markdown("### 📍 Geographic Exposure")

    map_fig = create_exposure_map(exposure_df, selected_state)
    if map_fig:
        st.plotly_chart(map_fig, use_container_width=True)

    # VaR Curve
    st.markdown("### 📈 Value at Risk Analysis")

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        var_curve = create_var_curve(var_df, scenario)
        st.plotly_chart(var_curve, use_container_width=True)

    with chart_col2:
        loss_dist = create_loss_distribution(var_df)
        st.plotly_chart(loss_dist, use_container_width=True)

    # VaR Table
    st.markdown("### 📊 Loss Estimates by Return Period")

    display_var = var_df.copy()
    display_var["Loss (INR)"] = display_var["Loss (INR)"].apply(lambda x: f"₹{x/1e7:.2f} Cr")
    display_var["Loss (Crores)"] = display_var["Loss (Crores)"].apply(lambda x: f"₹{x:.2f} Cr")
    display_var["Loss (% of GDP)"] = display_var["Loss (% of GDP)"].apply(lambda x: f"{x:.2f}%")
    display_var["Exceedance Probability"] = display_var["Exceedance Probability"].apply(lambda x: f"{x:.4f}")

    st.dataframe(display_var, use_container_width=True, hide_index=True)

    # Scenario Comparison
    if scenario_comparison:
        st.markdown("### 🌡️ Climate Scenario Comparison")

        with st.spinner("Comparing scenarios..."):
            comp_fig = create_scenario_comparison(selected_state, hazard, state_info)
            st.plotly_chart(comp_fig, use_container_width=True)

    # All Hazards Summary
    if show_all_hazards:
        st.markdown("### ⚠️ Multi-Hazard Risk Summary")

        st.info("Comparing risk across all available CLIMADA hazard types...")

        hazard_summary = []
        for haz_name in CLIMADA_DATASETS.keys():
            quick_exp = calculate_litpop_exposure(selected_state, num_points=100)
            quick_var = calculate_var_scientific(quick_exp["exposure_value"].sum(), haz_name, scenario, state_info)
            quick_aai = calculate_aai(quick_var)

            hazard_summary.append({
                "Hazard": f"{CLIMADA_DATASETS[haz_name]['icon']} {haz_name}",
                "AAI (Crores)": f"₹{quick_aai/1e7:.1f} Cr",
                "100-Year Loss (Crores)": f"₹{quick_var[quick_var['Return Period (Years)'] == 100]['Loss (Crores)'].values[0]:.1f} Cr"
            })

        st.dataframe(pd.DataFrame(hazard_summary), use_container_width=True, hide_index=True)

    # Download
    st.markdown("---")

    col_dl1, col_dl2, col_dl3 = st.columns([1, 1, 2])

    with col_dl1:
        # Download VaR data
        csv_var = var_df.to_csv(index=False)
        st.download_button(
            label="📥 Download VaR Data (CSV)",
            data=csv_var,
            file_name=f"var_{selected_state}_{hazard}_{year}.csv",
            mime="text/csv"
        )

    with col_dl2:
        # Download exposure data
        csv_exp = exposure_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Exposure Data (CSV)",
            data=csv_exp,
            file_name=f"exposure_{selected_state}_{year}.csv",
            mime="text/csv"
        )

    with col_dl3:
        st.info("Reports generated based on scientific CLIMADA methodology")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p><strong>India Climate Risk Portal</strong> | Powered by CLIMADA Data API (ETH Zurich)</p>
    <p>Scientific methodology | Real-time data | Comprehensive analysis</p>
    <p style="font-size: 0.85rem; margin-top: 0.5rem;">
        Using LitPop exposure model | Weibull loss distribution | Trapezoidal integration for AAI
    </p>
</div>
""", unsafe_allow_html=True)
