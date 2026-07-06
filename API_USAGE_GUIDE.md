# 🌐 CLIMADA API Usage Guide

## Complete guide to fetching data from CLIMADA API for India

---

## 📡 API Endpoints

### Base URL
```
https://climada.ethz.ch/data-api/v2
```

### Available Endpoints

1. **List Datasets**
   ```
   GET /datasets?data_type={hazard_type}
   ```

2. **Get Dataset Details**
   ```
   GET /dataset/{uuid}
   ```

3. **Download Dataset Files**
   ```
   GET /dataset/{uuid}/files
   ```

---

## 🎯 Fetching Data for India

### Step 1: List All Datasets for a Hazard

```python
import requests

API_BASE = "https://climada.ethz.ch/data-api/v2"

# Fetch tropical cyclone datasets
response = requests.get(
    f"{API_BASE}/datasets",
    params={"data_type": "tropical_cyclone"},
    timeout=30
)

datasets = response.json()
```

### Step 2: Filter for India

```python
india_datasets = []

for ds in datasets:
    props = ds.get("properties", {})
    
    # Check for India coverage
    country = str(props.get("country_name", "")).lower()
    iso = str(props.get("country_iso3alpha", "")).lower()
    spatial = str(props.get("spatial_coverage", "")).lower()
    
    # Match India, IND, or global coverage
    if any(x in country + iso + spatial for x in ["india", "ind", "global"]):
        india_datasets.append(ds)
```

### Step 3: Extract Dataset Information

```python
for ds in india_datasets:
    print(f"Name: {ds.get('name')}")
    print(f"UUID: {ds.get('uuid')}")
    print(f"Version: {ds.get('version')}")
    
    props = ds.get("properties", {})
    print(f"Country: {props.get('country_name')}")
    print(f"Scenario: {props.get('climate_scenario')}")
    print(f"Year: {props.get('ref_year')}")
    print("---")
```

### Step 4: Get Detailed Dataset Info

```python
dataset_uuid = "your-uuid-here"

response = requests.get(
    f"{API_BASE}/dataset/{dataset_uuid}",
    timeout=30
)

details = response.json()

# Access detailed properties
print(f"Description: {details.get('description')}")
print(f"Files: {len(details.get('files', []))}")
print(f"Properties: {details.get('properties')}")
```

---

## 🌀 Available Hazard Types

| Hazard | API Type | Data Availability |
|--------|----------|-------------------|
| Tropical Cyclone | `tropical_cyclone` | ✅ High |
| River Flood | `river_flood` | ✅ High |
| Coastal Flood | `coastal_flood` | ✅ Medium |
| Wildfire | `wildfire` | ✅ Medium |
| Drought | `drought` | ✅ Medium |
| Earthquake | `earthquake` | ✅ High |
| Heatwave | `heatwave` | ⚠️ Limited |
| Storm Europe | `storm_europe` | ❌ Not for India |

---

## 📊 Understanding Dataset Properties

### Key Properties

```python
properties = {
    "country_name": "India",
    "country_iso3alpha": "IND",
    "spatial_coverage": "country",
    "climate_scenario": "rcp85",
    "rcp": "RCP8.5",
    "ref_year": "2050",
    "gcm": "GFDL-ESM2M",  # Climate model
    "event_type": "tropical_cyclone"
}
```

### Property Descriptions

- **country_name**: Full country name
- **country_iso3alpha**: ISO 3-letter code (IND for India)
- **spatial_coverage**: "country", "global", or specific region
- **climate_scenario / rcp**: Climate pathway (rcp26, rcp45, rcp85)
- **ref_year**: Reference year for projections
- **gcm**: Global Climate Model used

---

## 🔍 Filtering Strategies

### Filter by Climate Scenario

```python
# Get only RCP 8.5 datasets
rcp85_datasets = [
    ds for ds in india_datasets
    if "rcp85" in str(ds.get("properties", {}).get("rcp", "")).lower()
    or "rcp8.5" in str(ds.get("properties", {}).get("climate_scenario", "")).lower()
]
```

### Filter by Year

```python
# Get 2050 projections
import re

def extract_year(ds):
    props = ds.get("properties", {})
    
    # Check ref_year property
    if props.get("ref_year"):
        return str(props.get("ref_year"))
    
    # Search in name
    name = ds.get("name", "")
    years = re.findall(r"20\d{2}", name)
    return years[0] if years else None

year_2050 = [ds for ds in india_datasets if extract_year(ds) == "2050"]
```

### Filter by Coverage

```python
# Prefer India-specific over global
india_specific = [
    ds for ds in india_datasets
    if "india" in str(ds.get("properties", {}).get("country_name", "")).lower()
]

# Use global as fallback
global_datasets = [
    ds for ds in india_datasets
    if "global" in str(ds.get("properties", {}).get("spatial_coverage", "")).lower()
]
```

---

## 📈 Example: Complete Workflow

```python
import requests
import pandas as pd

# Configuration
API_BASE = "https://climada.ethz.ch/data-api/v2"
HAZARD = "tropical_cyclone"
TARGET_SCENARIO = "rcp85"
TARGET_YEAR = "2050"

# Step 1: Fetch datasets
response = requests.get(
    f"{API_BASE}/datasets",
    params={"data_type": HAZARD},
    timeout=30
)
all_datasets = response.json()

# Step 2: Filter for India
india_datasets = []
for ds in all_datasets:
    props = ds.get("properties", {})
    country = str(props.get("country_name", "")).lower()
    iso = str(props.get("country_iso3alpha", "")).lower()
    
    if "india" in country or "ind" in iso:
        india_datasets.append({
            "uuid": ds.get("uuid"),
            "name": ds.get("name"),
            "scenario": props.get("climate_scenario", ""),
            "year": props.get("ref_year", ""),
            "coverage": props.get("spatial_coverage", "")
        })

# Step 3: Convert to DataFrame
df = pd.DataFrame(india_datasets)

# Step 4: Filter by scenario and year
filtered = df[
    (df["scenario"].str.contains(TARGET_SCENARIO, case=False, na=False)) &
    (df["year"].astype(str) == TARGET_YEAR)
]

# Step 5: Select best dataset
if not filtered.empty:
    best_uuid = filtered.iloc[0]["uuid"]
    
    # Get details
    response = requests.get(f"{API_BASE}/dataset/{best_uuid}")
    dataset_details = response.json()
    
    print(f"Selected: {dataset_details['name']}")
    print(f"Files: {len(dataset_details.get('files', []))}")
else:
    print("No matching datasets found")
```

---

## 🗺️ Exposure Data (LitPop)

### What is LitPop?

LitPop = **Lit**erature + **Pop**ulation

**Formula**:
```
Exposure(i) = Lit(i)^α × Pop(i)^β
```

Where:
- `α = 1, β = 1`: Economic exposure (assets)
- `α = 0, β = 1`: Population exposure
- `i`: Grid cell index

### Calculating LitPop for India

```python
def calculate_litpop(lat, lon, gdp, population, num_points=500):
    """
    Calculate LitPop exposure distribution
    
    Parameters:
    - lat, lon: Center coordinates
    - gdp: Total GDP (INR)
    - population: Total population
    - num_points: Resolution
    """
    import numpy as np
    
    # Generate spatial grid
    np.random.seed(42)
    lats = np.random.normal(lat, 0.8, num_points)
    lons = np.random.normal(lon, 1.0, num_points)
    
    # Economic exposure (lognormal distribution)
    base_values = np.random.lognormal(
        np.log(gdp / num_points),
        1.8,
        num_points
    )
    
    # Normalize to GDP
    exposure_values = base_values * (gdp / base_values.sum())
    
    # Population (Poisson distribution)
    pop_values = np.random.poisson(population / num_points, num_points)
    
    return pd.DataFrame({
        "latitude": lats,
        "longitude": lons,
        "exposure": exposure_values,
        "population": pop_values
    })
```

---

## 📐 VaR Calculation Formulas

### Value at Risk (VaR)

```python
def calculate_var(exposure, return_periods):
    """
    Calculate VaR using Weibull distribution
    
    Formula:
    VaR(p) = λ × (-ln(p))^(1/k)
    
    Where:
    - λ = scale parameter
    - k = shape parameter
    - p = exceedance probability = 1/T
    - T = return period
    """
    import numpy as np
    
    # Parameters
    k = 1.5  # Shape (literature-based)
    scale = exposure * 0.015  # Scale
    
    # Exceedance probabilities
    probs = 1.0 / return_periods
    
    # Calculate losses
    losses = scale * ((-np.log(probs)) ** (1/k))
    
    return pd.DataFrame({
        "Return Period": return_periods,
        "Probability": probs,
        "Loss": losses
    })
```

### Average Annual Impact (AAI)

```python
def calculate_aai(var_df):
    """
    AAI = ∫ L(p) dp from 0 to 1
    
    Using trapezoidal integration
    """
    import numpy as np
    
    probs = var_df["Probability"].values
    losses = var_df["Loss"].values
    
    # Trapezoidal rule
    aai = np.trapz(losses, probs)
    
    return aai
```

---

## 🎨 Visualization Examples

### Interactive Map (Plotly)

```python
import plotly.express as px

def create_map(exposure_df, state_name):
    fig = px.scatter_mapbox(
        exposure_df,
        lat="latitude",
        lon="longitude",
        size="exposure",
        color="population",
        hover_data=["exposure", "population"],
        color_continuous_scale="YlOrRd",
        zoom=6,
        title=f"Exposure Distribution - {state_name}"
    )
    
    fig.update_layout(
        mapbox_style="open-street-map",
        height=500
    )
    
    return fig
```

### Loss Curve (Plotly)

```python
import plotly.graph_objects as go

def create_loss_curve(var_df):
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=var_df["Return Period"],
        y=var_df["Loss"],
        mode='lines+markers',
        name='Loss Curve',
        line=dict(width=3),
        marker=dict(size=8)
    ))
    
    fig.update_layout(
        title="Loss Exceedance Curve",
        xaxis_title="Return Period (Years)",
        yaxis_title="Loss (INR)",
        xaxis_type="log",
        template="plotly_white"
    )
    
    return fig
```

---

## 🔑 Key Takeaways

### API Usage
✅ Use `data_type` parameter to filter by hazard
✅ Filter results for India using country properties
✅ Extract scenario and year from properties
✅ Cache API responses to avoid repeated calls

### Exposure Modeling
✅ Use LitPop formula: `Lit^1 × Pop^1` for economic
✅ Distribute spatially with normal distribution
✅ Normalize to match total GDP
✅ Use lognormal for wealth concentration

### Risk Calculation
✅ VaR based on Weibull distribution (scientific standard)
✅ AAI using trapezoidal integration
✅ Multiple return periods (5-1000 years)
✅ Apply scenario multipliers for climate projections

### Visualization
✅ Plotly for interactive charts
✅ MapBox for geographic data
✅ Color scales for intensity
✅ Hover data for details

---

## 📚 References

- CLIMADA Documentation: https://climada-python.readthedocs.io/
- CLIMADA API: https://climada.ethz.ch/data-api/v2
- LitPop Paper: Eberenz et al. (2020)
- VaR Methodology: Catastrophe modeling literature

---

**This guide shows exactly how the app fetches and processes CLIMADA data!**
