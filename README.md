# 🌾 Asia Agriculture Production Dashboard

A comprehensive, interactive dashboard for visualizing and analyzing agricultural production data (crops and livestock) across Asian countries from 1961 to 2023.

![Dashboard](https://img.shields.io/badge/Dashboard-Interactive-brightgreen)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 📊 Features

### Interactive Web Dashboard
- ** Overview Tab**: Key metrics, top producers, and data distribution
- ** Production Trends**: Time-series analysis with customizable filters
- ** Country Comparison**: Multi-country production comparisons
- ** Top Producers**: Ranking analysis with dynamic controls
- ** Geographic Analysis**: Treemap visualization of production distribution
- ** Data Explorer**: Searchable data table with flexible filtering

### Static Visualization Generation
- Production trend charts for multiple countries
- Top producer bar charts
- Production heatmaps over time
- Country production portfolio pie charts
- Growth rate comparison charts
- Comprehensive dashboard overview

### Data Processing Utilities
- Efficient data loading and cleaning
- Time-series extraction
- Growth rate calculations (CAGR)
- Top producer identification
- Missing data analysis

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone or navigate to the project directory:**
```powershell
cd E:\FDS
```

2. **Install required packages:**
```powershell
pip install -r requirements.txt
```

### Running the Dashboard

**Start the interactive web dashboard:**
```powershell
python dashboard.py
```

Then open your browser and navigate to: **http://127.0.0.1:8050**

The dashboard will automatically load the CSV data files and present an interactive interface.

### Generating Static Visualizations

**Create high-quality static charts:**
```powershell
python generate_visuals.py
```

This will generate PNG images in the `visualizations/` folder including:
- Production trends
- Top producer charts
- Heatmaps
- Country portfolios
- Growth comparisons

## 📁 Project Structure

```
E:\FDS\
├── dashboard.py                               # Main interactive dashboard
├── data_processor.py                          # Data processing utilities
├── generate_visuals.py                        # Static visualization generator
├── requirements.txt                           # Python dependencies
├── README.md                                  # This file
│
├── Production_Crops_Livestock_E_Asia_NOFLAG.csv    # Main dataset
├── Production_Crops_Livestock_E_Asia.csv           # Dataset with flags
├── Production_Crops_Livestock_E_AreaCodes.csv      # Country codes
├── Production_Crops_Livestock_E_ItemCodes.csv      # Product codes
├── Production_Crops_Livestock_E_Elements.csv       # Metric definitions
├── Production_Crops_Livestock_E_Flags.csv          # Data quality flags
│
└── visualizations/                            # Generated charts (auto-created)
    ├── rice_production_trends.png
    ├── rice_top_producers.png
    ├── wheat_top_producers.png
    └── ... (more visualizations)
```

## 📊 Data Overview

### Dataset Coverage
- **Geographic Scope**: Asian countries and regions
- **Time Period**: 1961 - 2023 (63 years)
- **Products**: 300+ agricultural items (crops and livestock)
- **Metrics**: Production, Area Harvested, Yield, Stocks, etc.
- **Total Records**: 15,000+ data entries

### Key Metrics Available
- **Production**: Total output (tonnes, heads, etc.)
- **Area Harvested**: Land area used (hectares)
- **Yield**: Productivity per unit area (kg/ha)
- **Stocks**: Livestock populations
- **Producing Animals**: Number of animals slaughtered

## 🎨 Dashboard Features Detail

### 1. Overview Tab
- Total countries and products tracked
- Year coverage information
- Top 5 producing countries
- Top 5 products by production
- Data elements distribution chart

### 2. Production Trends Tab
- Select country, product, and metric
- Interactive time-series line chart
- Zoom, pan, and hover capabilities
- Download chart as PNG

### 3. Country Comparison Tab
- Compare multiple countries simultaneously
- Select any product and year
- Horizontal bar chart visualization
- Sort by production volume

### 4. Top Producers Tab
- Dynamic top N selection (5-20 producers)
- Product-specific rankings
- Production statistics panel
- Market share calculations

### 5. Geographic Analysis Tab
- Treemap visualization
- Size represents production volume
- Color-coded by intensity
- Year slider for temporal analysis

### 6. Data Explorer Tab
- Filterable data table
- Country, product, and metric filters
- Display last 10 years of data
- Responsive table design

## 🔧 Customization

### Modify Color Schemes
Edit the Plotly color palettes in `dashboard.py`:
```python
marker_color='#1f77b4'  # Change to your preferred color
colorscale='Viridis'     # Options: Viridis, Plasma, Inferno, etc.
```

### Add New Visualizations
Extend the `generate_visuals.py` with new chart types:
```python
def create_custom_chart(self, ...):
    fig = go.Figure(...)
    # Your custom visualization
    return fig
```

### Adjust Dashboard Theme
Change the Bootstrap theme in `dashboard.py`:
```python
external_stylesheets=[dbc.themes.DARKLY]  # Try: DARKLY, SLATE, CYBORG
```

## 📈 Usage Examples

### Example 1: Analyze Rice Production Trends
1. Open dashboard
2. Navigate to "Production Trends" tab
3. Select Country: "China"
4. Select Product: "Rice"
5. Select Metric: "Production"
6. View the time-series chart

### Example 2: Compare Wheat Producers
1. Navigate to "Country Comparison" tab
2. Select Product: "Wheat"
3. Select Countries: China, India, Indonesia, Bangladesh
4. Adjust year slider to 2023
5. View comparative bar chart

### Example 3: Generate Report Images
```powershell
python generate_visuals.py
```
Check the `visualizations/` folder for PNG images ready for presentations.

## 🛠️ Troubleshooting

### Issue: Port 8050 already in use
**Solution**: Change the port in `dashboard.py`:
```python
app.run_server(debug=True, host='0.0.0.0', port=8051)
```

### Issue: Module not found errors
**Solution**: Ensure all dependencies are installed:
```powershell
pip install -r requirements.txt --upgrade
```

### Issue: Data files not found
**Solution**: Ensure CSV files are in the same directory as Python scripts.

## 📊 Academic Use Case

This dashboard is designed for **Phase 1** of the FDS project (11-Aug-2025):

### Problem Identification
**Domain**: Agriculture and Food Security in Asia

**Objectives**:
1. **Identify production trends** across Asian countries to understand agricultural development patterns
2. **Compare regional production capabilities** to highlight opportunities for trade and food security

### Justification
- **Real-world relevance**: Food security is critical for Asia's 4.7 billion population
- **Data-driven insights**: Historical data reveals growth patterns and potential challenges
- **Policy implications**: Helps identify countries needing agricultural support or investment

### Study Section Components
✓ **Strengths**: Comprehensive 63-year dataset covering all Asian countries  
✓ **Limitations**: Missing data for certain years/countries, data quality flags  
✓ **Novel observations**: Interactive visualization reveals production shifts and emerging producers  
✓ **Data techniques**: Time-series analysis, CAGR calculations, comparative analysis  

## 📝 License

This project is open source and available under the MIT License.

## 👥 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

## 📧 Contact

For questions or suggestions about this dashboard, please open an issue in the project repository.

---

**Built with ❤️ using Python, Plotly, and Dash**

*Last Updated: November 2025*
