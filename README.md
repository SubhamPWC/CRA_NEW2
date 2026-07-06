# 🌍 India Climate Risk Portal

A comprehensive climate risk assessment application for Indian states using CLIMADA data.

## 🚀 Features

- **22+ Indian States** - Complete coverage of major states and UTs
- **Multiple Hazards** - Tropical Cyclones, River Floods, Droughts
- **Climate Scenarios** - RCP 2.6, 4.5, 8.5 projections
- **Value at Risk** - Calculate potential economic losses
- **Interactive Maps** - Geographic visualization of exposure
- **Real CLIMADA Data** - Direct API integration with ETH Zurich

## 📊 What You Get

- State-level climate risk analysis
- Exposure calculations (assets and population)
- VaR estimates for different return periods
- Risk level indicators
- Downloadable reports
- Beautiful visualizations

## 🛠️ Technology

- **Framework**: Streamlit
- **Data Source**: CLIMADA Data API (ETH Zurich)
- **Language**: Python 3.8+
- **Dependencies**: Minimal (streamlit, pandas, numpy, requests)

## 🚀 Quick Start

### Local Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/india-climate-portal-new.git
cd india-climate-portal-new

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

### Deploy to Streamlit Cloud

1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repository
4. Select `app.py` as main file
5. Deploy!

### Deploy to Hugging Face Spaces

1. Create a new Space on Hugging Face
2. Select "Streamlit" as SDK
3. Upload files or connect GitHub
4. Your app will be live!

## 📁 File Structure

```
india-climate-portal-new/
├── app.py                 # Main application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── .gitignore            # Git ignore rules
└── packages.txt          # System dependencies (empty for this app)
```

## 🌟 Key Features Explained

### State Selection
Choose from 22+ Indian states including:
- Kerala, Maharashtra, Tamil Nadu
- Gujarat, West Bengal, Odisha
- Uttar Pradesh, Rajasthan, Karnataka
- And many more!

### Climate Hazards
- **🌀 Tropical Cyclones** - Wind and storm surge damage
- **🌊 River Floods** - Monsoon flooding impacts
- **🏜️ Droughts** - Water scarcity and agricultural effects

### Climate Scenarios
- **RCP 2.6** (🟢) - Strong climate action, warming limited to 1.5-2°C
- **RCP 4.5** (🟡) - Moderate action, warming around 2-3°C
- **RCP 8.5** (🔴) - Business as usual, warming >4°C

### Value at Risk Analysis
Calculate potential losses for:
- 5, 10, 25, 50, 100, 250-year return periods
- Average Annual Impact (AAI)
- Scenario-specific projections

## 🔧 API Integration

This app uses the **CLIMADA Data API**:

```
Base URL: https://climada.ethz.ch/data-api/v2
```

**Endpoints used**:
- `/datasets` - List available climate datasets
- `/dataset/{uuid}` - Get specific dataset details

**No API key required** - Public access

## 📈 Use Cases

- **Government Planning** - Infrastructure and disaster preparedness
- **Insurance Sector** - Risk assessment and pricing
- **Research** - Climate impact studies
- **Policy Making** - Evidence-based climate policy
- **Education** - Teaching climate science

## 🎯 Data Sources

- **CLIMADA** - Climate Adaptation Platform (ETH Zurich)
- **Methodology** - Scientific peer-reviewed models
- **Coverage** - India-specific and global datasets
- **Updates** - Regularly maintained by ETH Zurich

## ⚙️ Configuration

The app requires no configuration! Just:
1. Install dependencies
2. Run the app
3. Start analyzing

## 🐛 Troubleshooting

### App won't start locally
```bash
# Make sure you have Python 3.8+
python --version

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### CLIMADA API errors
- Check your internet connection
- CLIMADA API may be temporarily unavailable
- Try again in a few minutes

### Slow loading
- First run downloads data (takes 1-2 minutes)
- Subsequent runs are cached and fast
- Try selecting smaller states first

## 📝 License

MIT License - Free to use, modify, and distribute

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## 📧 Contact

- **Issues**: Open a GitHub issue
- **Questions**: Create a discussion
- **Feedback**: Submit a pull request

## 🙏 Acknowledgments

- **CLIMADA** - ETH Zurich Weather and Climate Risks
- **Streamlit** - Amazing web framework
- **Hugging Face** - Excellent deployment platform

## 🔗 Links

- [CLIMADA Documentation](https://climada-python.readthedocs.io/)
- [Streamlit Docs](https://docs.streamlit.io/)
- [Hugging Face Spaces](https://huggingface.co/spaces)

---

**Built with ❤️ for climate resilience in India**
