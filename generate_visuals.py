"""
Static Visualizations Generator
================================
Generate high-quality static charts and save them as images.
"""

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from pathlib import Path
from data_processor import DataProcessor

class VisualizationGenerator:
    """Generate static visualizations from agricultural data"""
    
    def __init__(self, data_dir: Path):
        self.processor = DataProcessor(data_dir)
        self.processor.load_all_data()
        self.output_dir = Path(data_dir) / 'visualizations'
        self.output_dir.mkdir(exist_ok=True)
        
    def create_production_trends(self, countries: list, item: str, save_path: str = None):
        """Create multi-country production trends"""
        fig = go.Figure()
        
        year_cols = self.processor.get_year_columns()
        years = self.processor.get_years()
        
        for country in countries:
            ts = self.processor.get_time_series(country, item, 'Production')
            if not ts.empty:
                fig.add_trace(go.Scatter(
                    x=ts['Year'],
                    y=ts['Value'],
                    mode='lines+markers',
                    name=country,
                    line=dict(width=2),
                    marker=dict(size=4)
                ))
        
        fig.update_layout(
            title=f'Production Trends: {item}',
            xaxis_title='Year',
            yaxis_title='Production',
            hovermode='x unified',
            template='plotly_white',
            width=1200,
            height=600,
            legend=dict(
                orientation="v",
                yanchor="top",
                y=1,
                xanchor="left",
                x=1.02
            )
        )
        
        if save_path:
            fig.write_image(save_path)
            print(f"Saved: {save_path}")
        
        return fig
    
    def create_top_producers_bar(self, item: str, year: int, n: int = 15, save_path: str = None):
        """Create bar chart of top producers"""
        df = self.processor.get_top_producers(item, year, n)
        
        if df.empty:
            print(f"No data available for {item} in {year}")
            return None
        
        fig = go.Figure(data=[
            go.Bar(
                x=df['Country'],
                y=df['Production'],
                text=df['Production'].apply(lambda x: f'{x:,.0f}'),
                textposition='outside',
                marker=dict(
                    color=df['Production'],
                    colorscale='Viridis',
                    showscale=True
                )
            )
        ])
        
        fig.update_layout(
            title=f'Top {n} Producers of {item} ({year})',
            xaxis_title='Country',
            yaxis_title=f'Production ({df["Unit"].iloc[0]})',
            template='plotly_white',
            width=1200,
            height=600,
            xaxis={'tickangle': -45}
        )
        
        if save_path:
            fig.write_image(save_path)
            print(f"Saved: {save_path}")
        
        return fig
    
    def create_production_heatmap(self, item: str, countries: list = None, save_path: str = None):
        """Create heatmap of production over time"""
        if countries is None:
            # Get top 15 producers from latest year
            latest_year = max(self.processor.get_years())
            top_df = self.processor.get_top_producers(item, latest_year, 15)
            if not top_df.empty:
                countries = top_df['Country'].tolist()
            else:
                return None
        
        year_cols = self.processor.get_year_columns()
        years = self.processor.get_years()
        
        # Build matrix
        matrix = []
        country_labels = []
        
        for country in countries:
            filtered = self.processor.filter_data(country=country, item=item, element='Production')
            if not filtered.empty:
                row = filtered.iloc[0]
                values = [row[col] if not pd.isna(row[col]) else 0 for col in year_cols]
                matrix.append(values)
                country_labels.append(country)
        
        if not matrix:
            print(f"No data available for {item}")
            return None
        
        fig = go.Figure(data=go.Heatmap(
            z=matrix,
            x=years,
            y=country_labels,
            colorscale='YlOrRd',
            hoverongaps=False
        ))
        
        fig.update_layout(
            title=f'Production Heatmap: {item} (1961-2023)',
            xaxis_title='Year',
            yaxis_title='Country',
            template='plotly_white',
            width=1400,
            height=800
        )
        
        if save_path:
            fig.write_image(save_path)
            print(f"Saved: {save_path}")
        
        return fig
    
    def create_country_portfolio(self, country: str, year: int, n: int = 20, save_path: str = None):
        """Create pie chart of country's production portfolio"""
        df = self.processor.get_country_portfolio(country, year, n)
        
        if df.empty:
            print(f"No data available for {country} in {year}")
            return None
        
        fig = go.Figure(data=[
            go.Pie(
                labels=df['Item'],
                values=df['Production'],
                hole=0.4,
                textposition='auto',
                textinfo='label+percent'
            )
        ])
        
        fig.update_layout(
            title=f'Production Portfolio: {country} ({year})',
            template='plotly_white',
            width=1000,
            height=800
        )
        
        if save_path:
            fig.write_image(save_path)
            print(f"Saved: {save_path}")
        
        return fig
    
    def create_growth_comparison(self, item: str, countries: list, 
                                start_year: int, end_year: int, save_path: str = None):
        """Create bar chart comparing growth rates"""
        growth_data = []
        
        for country in countries:
            cagr = self.processor.calculate_growth_rate(country, item, start_year, end_year)
            if cagr is not None:
                growth_data.append({'Country': country, 'CAGR': cagr})
        
        if not growth_data:
            print(f"No growth data available")
            return None
        
        df = pd.DataFrame(growth_data)
        df = df.sort_values('CAGR', ascending=True)
        
        # Color bars based on positive/negative growth
        colors = ['green' if x > 0 else 'red' for x in df['CAGR']]
        
        fig = go.Figure(data=[
            go.Bar(
                y=df['Country'],
                x=df['CAGR'],
                orientation='h',
                marker_color=colors,
                text=df['CAGR'].apply(lambda x: f'{x:.1f}%'),
                textposition='outside'
            )
        ])
        
        fig.update_layout(
            title=f'Production Growth Rate: {item} ({start_year}-{end_year})',
            xaxis_title='CAGR (%)',
            yaxis_title='Country',
            template='plotly_white',
            width=1000,
            height=600
        )
        
        if save_path:
            fig.write_image(save_path)
            print(f"Saved: {save_path}")
        
        return fig
    
    def create_dashboard_overview(self, year: int, save_path: str = None):
        """Create comprehensive dashboard with multiple charts"""
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=(
                f'Top 10 Products by Production ({year})',
                f'Top 10 Producing Countries ({year})',
                'Production Elements Distribution',
                'Year Coverage'
            ),
            specs=[[{'type': 'bar'}, {'type': 'bar'}],
                   [{'type': 'pie'}, {'type': 'scatter'}]]
        )
        
        # 1. Top products
        summary = self.processor.get_production_summary(year)
        if not summary.empty:
            top_products = summary.head(10)
            fig.add_trace(
                go.Bar(
                    x=top_products['Item'],
                    y=top_products['Total_Production'],
                    name='Products',
                    showlegend=False
                ),
                row=1, col=1
            )
        
        # 2. Top countries (using wheat as example)
        top_countries = self.processor.get_top_producers('Wheat', year, 10)
        if not top_countries.empty:
            fig.add_trace(
                go.Bar(
                    x=top_countries['Country'],
                    y=top_countries['Production'],
                    name='Countries',
                    showlegend=False,
                    marker_color='orange'
                ),
                row=1, col=2
            )
        
        # 3. Elements distribution
        element_counts = self.processor.df_main.groupby('Element').size()
        fig.add_trace(
            go.Pie(
                labels=element_counts.index,
                values=element_counts.values,
                name='Elements'
            ),
            row=2, col=1
        )
        
        # 4. Data coverage by year
        year_cols = self.processor.get_year_columns()
        years = self.processor.get_years()
        coverage = []
        for year_col in year_cols:
            non_null = self.processor.df_main[year_col].notna().sum()
            coverage.append(non_null)
        
        fig.add_trace(
            go.Scatter(
                x=years,
                y=coverage,
                mode='lines+markers',
                name='Coverage',
                showlegend=False,
                line=dict(color='green')
            ),
            row=2, col=2
        )
        
        fig.update_layout(
            title_text=f'Asia Agriculture Dashboard Overview ({year})',
            showlegend=False,
            template='plotly_white',
            width=1600,
            height=1000
        )
        
        if save_path:
            fig.write_image(save_path)
            print(f"Saved: {save_path}")
        
        return fig
    
    def generate_all_visualizations(self):
        """Generate a comprehensive set of visualizations"""
        print("Generating visualizations...")
        
        latest_year = max(self.processor.get_years())
        
        # 1. Production trends for major crops
        print("\n1. Creating production trends...")
        major_countries = ['China', 'India', 'Indonesia', 'Bangladesh', 'Viet Nam']
        self.create_production_trends(
            major_countries, 
            'Rice',
            self.output_dir / 'rice_production_trends.png'
        )
        
        # 2. Top producers
        print("\n2. Creating top producers charts...")
        for item in ['Rice', 'Wheat', 'Maize (corn)']:
            self.create_top_producers_bar(
                item,
                latest_year,
                15,
                self.output_dir / f'{item.lower().replace(" ", "_")}_top_producers.png'
            )
        
        # 3. Production heatmap
        print("\n3. Creating heatmaps...")
        self.create_production_heatmap(
            'Rice',
            save_path=self.output_dir / 'rice_heatmap.png'
        )
        
        # 4. Country portfolios
        print("\n4. Creating country portfolios...")
        for country in ['China', 'India', 'Indonesia']:
            self.create_country_portfolio(
                country,
                latest_year,
                20,
                self.output_dir / f'{country.lower()}_portfolio.png'
            )
        
        # 5. Growth comparison
        print("\n5. Creating growth comparisons...")
        self.create_growth_comparison(
            'Rice',
            major_countries,
            2000,
            latest_year,
            self.output_dir / 'rice_growth_comparison.png'
        )
        
        # 6. Dashboard overview
        print("\n6. Creating dashboard overview...")
        self.create_dashboard_overview(
            latest_year,
            self.output_dir / 'dashboard_overview.png'
        )
        
        print(f"\n✓ All visualizations saved to: {self.output_dir}")

def main():
    """Generate all visualizations"""
    generator = VisualizationGenerator(Path(__file__).parent)
    generator.generate_all_visualizations()

if __name__ == '__main__':
    main()
