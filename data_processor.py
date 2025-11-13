"""
Data Processing Utilities for Agriculture Dashboard
==================================================
Helper functions for loading, cleaning, and processing agricultural data.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple

class DataProcessor:
    """Process and transform agricultural production data"""
    
    def __init__(self, data_dir: Path):
        self.data_dir = Path(data_dir)
        self.df_main = None
        self.df_areas = None
        self.df_items = None
        self.df_elements = None
        
    def load_all_data(self) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """Load all CSV files"""
        print("Loading main dataset from normalized folder...")
        self.df_main = pd.read_csv(
            self.data_dir / 'Production_Crops_Livestock_E_All_Data_(Normalized)' / 'Production_Crops_Livestock_E_All_Data_(Normalized).csv',
            encoding='latin1',
            low_memory=False
        )
        
        print("Loading lookup tables...")
        self.df_areas = pd.read_csv(self.data_dir / 'Production_Crops_Livestock_E_All_Data_(Normalized)' / 'Production_Crops_Livestock_E_AreaCodes.csv')
        self.df_items = pd.read_csv(self.data_dir / 'Production_Crops_Livestock_E_All_Data_(Normalized)' / 'Production_Crops_Livestock_E_ItemCodes.csv')
        self.df_elements = pd.read_csv(self.data_dir / 'Production_Crops_Livestock_E_All_Data_(Normalized)' / 'Production_Crops_Livestock_E_Elements.csv')
        
        # Clean column names
        self.df_areas.columns = self.df_areas.columns.str.strip()
        self.df_items.columns = self.df_items.columns.str.strip()
        self.df_elements.columns = self.df_elements.columns.str.strip()
        
        print(f"Loaded {len(self.df_main)} records from main dataset")
        print(f"Loaded {len(self.df_areas)} areas, {len(self.df_items)} items, {len(self.df_elements)} elements")
        
        return self.df_main, self.df_areas, self.df_items, self.df_elements
    
    def get_year_columns(self) -> List[str]:
        """Extract year columns from main dataset - for normalized format, returns Year column"""
        if 'Year' in self.df_main.columns:
            return ['Year']  # Normalized format
        return [col for col in self.df_main.columns if col.startswith('Y')]  # Wide format
    
    def get_years(self) -> List[int]:
        """Get list of years in dataset"""
        if 'Year' in self.df_main.columns:
            return sorted(self.df_main['Year'].unique())
        year_cols = self.get_year_columns()
        return [int(col[1:]) for col in year_cols]
    
    def filter_data(self, country: str = None, item: str = None, 
                   element: str = None) -> pd.DataFrame:
        """Filter data based on criteria"""
        df = self.df_main.copy()
        
        if country:
            df = df[df['Area'] == country]
        if item:
            df = df[df['Item'] == item]
        if element:
            df = df[df['Element'] == element]
            
        return df
    
    def get_time_series(self, country: str, item: str, element: str) -> pd.DataFrame:
        """Get time series data for specific filters"""
        filtered = self.filter_data(country, item, element)
        
        if filtered.empty:
            return pd.DataFrame()
        
        # For normalized format, data is already in Year/Value format
        if 'Year' in filtered.columns and 'Value' in filtered.columns:
            result = filtered[['Year', 'Value', 'Unit']].copy() if 'Unit' in filtered.columns else filtered[['Year', 'Value']].copy()
            return result.sort_values('Year')
        
        # For wide format (legacy)
        year_cols = self.get_year_columns()
        row = filtered.iloc[0]
        
        data = []
        for year_col in year_cols:
            value = row[year_col]
            if not pd.isna(value):
                data.append({
                    'Year': int(year_col[1:]),
                    'Value': value,
                    'Unit': row.get('Unit', '')
                })
        
        return pd.DataFrame(data)
    
    def get_top_producers(self, item: str, year: int, n: int = 10) -> pd.DataFrame:
        """Get top N producers for a specific item and year"""
        filtered = self.filter_data(item=item, element='Production')
        
        if filtered.empty:
            return pd.DataFrame()
        
        # For normalized format
        if 'Year' in filtered.columns and 'Value' in filtered.columns:
            year_data = filtered[filtered['Year'] == year].copy()
            if year_data.empty:
                return pd.DataFrame()
            
            production_data = []
            for _, row in year_data.iterrows():
                value = row['Value']
                if not pd.isna(value) and value > 0:
                    production_data.append({
                        'Country': row['Area'],
                        'Production': value,
                        'Unit': row.get('Unit', '')
                    })
            
            df = pd.DataFrame(production_data)
            return df.sort_values('Production', ascending=False).head(n)
        
        # For wide format (legacy)
        year_col = f'Y{year}'
        if year_col not in filtered.columns:
            return pd.DataFrame()
        
        # Extract production values
        production_data = []
        for _, row in filtered.iterrows():
            value = row[year_col]
            if not pd.isna(value) and value > 0:
                production_data.append({
                    'Country': row['Area'],
                    'Production': value,
                    'Unit': row.get('Unit', '')
                })
        
        df = pd.DataFrame(production_data)
        return df.sort_values('Production', ascending=False).head(n)
    
    def calculate_growth_rate(self, country: str, item: str, 
                             start_year: int, end_year: int) -> float:
        """Calculate compound annual growth rate (CAGR)"""
        ts = self.get_time_series(country, item, 'Production')
        
        if ts.empty:
            return None
        
        start_val = ts[ts['Year'] == start_year]['Value'].values
        end_val = ts[ts['Year'] == end_year]['Value'].values
        
        if len(start_val) == 0 or len(end_val) == 0:
            return None
        
        start_val = start_val[0]
        end_val = end_val[0]
        
        if start_val <= 0 or end_val <= 0:
            return None
        
        n_years = end_year - start_year
        cagr = ((end_val / start_val) ** (1 / n_years) - 1) * 100
        
        return cagr
    
    def get_production_summary(self, year: int) -> pd.DataFrame:
        """Get production summary for all items in a specific year"""
        year_col = f'Y{year}'
        
        production_df = self.filter_data(element='Production')
        
        if production_df.empty or year_col not in production_df.columns:
            return pd.DataFrame()
        
        summary = production_df.groupby(['Item', 'Unit'])[year_col].sum().reset_index()
        summary.columns = ['Item', 'Unit', 'Total_Production']
        summary = summary[summary['Total_Production'] > 0]
        summary = summary.sort_values('Total_Production', ascending=False)
        
        return summary
    
    def get_country_portfolio(self, country: str, year: int, top_n: int = 20) -> pd.DataFrame:
        """Get top products for a specific country"""
        year_col = f'Y{year}'
        
        country_df = self.filter_data(country=country, element='Production')
        
        if country_df.empty or year_col not in country_df.columns:
            return pd.DataFrame()
        
        portfolio = []
        for _, row in country_df.iterrows():
            value = row[year_col]
            if not pd.isna(value) and value > 0:
                portfolio.append({
                    'Item': row['Item'],
                    'Production': value,
                    'Unit': row.get('Unit', '')
                })
        
        df = pd.DataFrame(portfolio)
        return df.sort_values('Production', ascending=False).head(top_n)
    
    def get_regional_comparison(self, item: str, year: int) -> pd.DataFrame:
        """Compare production across all countries for an item"""
        year_col = f'Y{year}'
        
        filtered = self.filter_data(item=item, element='Production')
        
        if filtered.empty or year_col not in filtered.columns:
            return pd.DataFrame()
        
        comparison = []
        for _, row in filtered.iterrows():
            value = row[year_col]
            if not pd.isna(value):
                comparison.append({
                    'Country': row['Area'],
                    'Production': value,
                    'Unit': row.get('Unit', '')
                })
        
        return pd.DataFrame(comparison).sort_values('Production', ascending=False)
    
    def detect_missing_data(self) -> Dict:
        """Analyze missing data patterns"""
        year_cols = self.get_year_columns()
        
        missing_stats = {
            'total_cells': len(self.df_main) * len(year_cols),
            'missing_cells': 0,
            'missing_by_country': {},
            'missing_by_item': {},
            'missing_by_year': {}
        }
        
        # Count missing values
        for col in year_cols:
            missing_count = self.df_main[col].isna().sum()
            missing_stats['missing_cells'] += missing_count
            year = int(col[1:])
            missing_stats['missing_by_year'][year] = missing_count
        
        missing_stats['missing_percentage'] = (
            missing_stats['missing_cells'] / missing_stats['total_cells'] * 100
        )
        
        return missing_stats
    
    def export_processed_data(self, output_dir: Path):
        """Export processed datasets for easier analysis"""
        output_dir = Path(output_dir)
        output_dir.mkdir(exist_ok=True)
        
        print("Exporting processed data...")
        
        # Export latest year data
        latest_year = max(self.get_years())
        year_col = f'Y{latest_year}'
        
        latest_data = self.df_main[['Area', 'Item', 'Element', 'Unit', year_col]].copy()
        latest_data.columns = ['Country', 'Item', 'Element', 'Unit', 'Value']
        latest_data.to_csv(output_dir / f'latest_year_{latest_year}.csv', index=False)
        
        # Export production summary
        production_summary = self.get_production_summary(latest_year)
        production_summary.to_csv(output_dir / f'production_summary_{latest_year}.csv', index=False)
        
        print(f"Exported processed data to {output_dir}")

def main():
    """Example usage"""
    processor = DataProcessor(Path(__file__).parent)
    processor.load_all_data()
    
    # Example: Get top rice producers in 2023
    print("\n=== Top 10 Rice Producers in 2023 ===")
    top_rice = processor.get_top_producers('Rice', 2023, 10)
    if not top_rice.empty:
        print(top_rice)
    
    # Example: Calculate growth rate
    print("\n=== China Wheat Production Growth (2000-2023) ===")
    growth = processor.calculate_growth_rate('China', 'Wheat', 2000, 2023)
    if growth:
        print(f"CAGR: {growth:.2f}%")
    
    # Example: Missing data analysis
    print("\n=== Missing Data Analysis ===")
    missing = processor.detect_missing_data()
    print(f"Missing percentage: {missing['missing_percentage']:.2f}%")

if __name__ == '__main__':
    main()
