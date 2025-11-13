"""
Quick Test Script
=================
Tests data loading and creates a sample visualization.
"""

import pandas as pd
import plotly.graph_objects as go
from pathlib import Path

print("🧪 Testing Agriculture Dashboard Components\n")
print("=" * 50)

# Test 1: Data Loading
print("\n1. Testing data loading...")
try:
    df = pd.read_csv('Production_Crops_Livestock_E_Asia_NOFLAG.csv')
    print(f"   ✓ Main dataset loaded: {len(df)} records")
    
    areas = pd.read_csv('Production_Crops_Livestock_E_AreaCodes.csv')
    print(f"   ✓ Area codes loaded: {len(areas)} areas")
    
    items = pd.read_csv('Production_Crops_Livestock_E_ItemCodes.csv')
    print(f"   ✓ Item codes loaded: {len(items)} items")
    
    elements = pd.read_csv('Production_Crops_Livestock_E_Elements.csv')
    print(f"   ✓ Elements loaded: {len(elements)} elements")
except Exception as e:
    print(f"   ✗ Error loading data: {e}")
    exit(1)

# Test 2: Data Analysis
print("\n2. Analyzing data structure...")
year_cols = [col for col in df.columns if col.startswith('Y')]
years = [int(col[1:]) for col in year_cols]
print(f"   ✓ Year range: {min(years)} - {max(years)}")
print(f"   ✓ Countries: {df['Area'].nunique()}")
print(f"   ✓ Products: {df['Item'].nunique()}")

# Test 3: Create Sample Visualization
print("\n3. Creating sample visualization...")
try:
    # Get Afghanistan apple production data
    sample_data = df[
        (df['Area'] == 'Afghanistan') & 
        (df['Item'] == 'Apples') & 
        (df['Element'] == 'Production')
    ]
    
    if not sample_data.empty:
        row = sample_data.iloc[0]
        
        # Extract values
        values = []
        year_labels = []
        for year_col in year_cols:
            val = row[year_col]
            if not pd.isna(val) and val > 0:
                values.append(val)
                year_labels.append(int(year_col[1:]))
        
        # Create chart
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=year_labels,
            y=values,
            mode='lines+markers',
            name='Production',
            line=dict(color='#2ca02c', width=3),
            marker=dict(size=6)
        ))
        
        fig.update_layout(
            title='Apple Production in Afghanistan (Sample)',
            xaxis_title='Year',
            yaxis_title='Production (tonnes)',
            template='plotly_white',
            width=1000,
            height=500
        )
        
        # Save chart
        output_dir = Path('visualizations')
        output_dir.mkdir(exist_ok=True)
        
        fig.write_html(output_dir / 'test_chart.html')
        print(f"   ✓ Sample chart created: visualizations/test_chart.html")
        
        # Try to save as image
        try:
            fig.write_image(output_dir / 'test_chart.png')
            print(f"   ✓ Sample chart saved: visualizations/test_chart.png")
        except Exception as e:
            print(f"   ⚠ Could not save PNG (kaleido may need configuration): {e}")
    else:
        print("   ⚠ No sample data found for visualization")
        
except Exception as e:
    print(f"   ✗ Error creating visualization: {e}")

# Test 4: Summary Statistics
print("\n4. Data Summary:")
print(f"   • Latest year data availability: {df[f'Y{max(years)}'].notna().sum()} records")
production_df = df[df['Element'] == 'Production']
print(f"   • Production records: {len(production_df)}")
print(f"   • Top 5 countries by record count:")

country_counts = df['Area'].value_counts().head(5)
for country, count in country_counts.items():
    print(f"     - {country}: {count} records")

print("\n" + "=" * 50)
print("✓ All tests completed successfully!")
print("\n📊 Next steps:")
print("   1. Run: python dashboard.py (for interactive dashboard)")
print("   2. Run: python generate_visuals.py (for static charts)")
print("   3. Or use: .\\start_dashboard.ps1 (quick start)")
print("\nOpen your browser at: http://127.0.0.1:8050")
