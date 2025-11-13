"""
Agricultural Production Dashboard for Asia
==========================================
An interactive dashboard for visualizing crops and livestock production data across Asian countries.
"""

import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from pathlib import Path

# Initialize the Dash app with a dark theme
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.DARKLY, dbc.icons.FONT_AWESOME],
    suppress_callback_exceptions=True,
    title="Asia Agriculture Dashboard"
)

# Load data
DATA_DIR = Path(__file__).parent

def load_data():
    """Load and prepare the dataset"""
    # Load main data (NOFLAG version for cleaner data)
    df = pd.read_csv(DATA_DIR / 'Production_Crops_Livestock_E_Asia_NOFLAG.csv')
    
    # Load lookup tables
    areas = pd.read_csv(DATA_DIR / 'Production_Crops_Livestock_E_AreaCodes.csv')
    items = pd.read_csv(DATA_DIR / 'Production_Crops_Livestock_E_ItemCodes.csv')
    elements = pd.read_csv(DATA_DIR / 'Production_Crops_Livestock_E_Elements.csv')
    
    # Clean column names
    areas.columns = areas.columns.str.strip()
    items.columns = items.columns.str.strip()
    elements.columns = elements.columns.str.strip()
    
    return df, areas, items, elements

# Load data
print("Loading data...")
df_main, df_areas, df_items, df_elements = load_data()

# Get year columns
year_cols = [col for col in df_main.columns if col.startswith('Y')]
years = [int(col[1:]) for col in year_cols]

# App Layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1([
                html.I(className="fas fa-chart-line me-3"),
                "Asia Agriculture Production Dashboard"
            ], className="text-center my-4 text-info"),
            html.P(
                "Comprehensive analysis of crops and livestock production across Asian countries (1961-2023)",
                className="text-center text-muted mb-4"
            )
        ])
    ]),
    
    dbc.Tabs([
        dbc.Tab(label="Overview", tab_id="overview"),
        dbc.Tab(label="Production Trends", tab_id="trends"),
        dbc.Tab(label="Country Comparison", tab_id="comparison"),
        dbc.Tab(label="Top Producers", tab_id="top_producers"),
        dbc.Tab(label="Geographic Analysis", tab_id="geographic"),
        dbc.Tab(label="Data Explorer", tab_id="explorer"),
    ], id="tabs", active_tab="overview"),
    
    html.Div(id="tab-content", className="mt-4")
], fluid=True, className="min-vh-100 py-3")

@callback(Output("tab-content", "children"), Input("tabs", "active_tab"))
def render_tab_content(active_tab):
    """Render content based on selected tab"""
    if active_tab == "overview":
        return render_overview()
    elif active_tab == "trends":
        return render_trends()
    elif active_tab == "comparison":
        return render_comparison()
    elif active_tab == "top_producers":
        return render_top_producers()
    elif active_tab == "geographic":
        return render_geographic()
    elif active_tab == "explorer":
        return render_explorer()
    return html.Div("Select a tab")

def render_overview():
    """Overview dashboard with key metrics"""
    # Calculate key metrics
    total_countries = df_main['Area'].nunique()
    total_items = df_main['Item'].nunique()
    year_range = f"{min(years)} - {max(years)}"
    
    # Get production data for latest year
    latest_year = f'Y{max(years)}'
    production_data = df_main[df_main['Element'] == 'Production'].copy()
    
    # Top 5 countries by total production
    country_totals = {}
    for country in production_data['Area'].unique():
        country_data = production_data[production_data['Area'] == country]
        total = country_data[latest_year].sum()
        if not pd.isna(total) and total > 0:
            country_totals[country] = total
    
    top_countries = sorted(country_totals.items(), key=lambda x: x[1], reverse=True)[:5]
    
    # Top 5 items by production
    item_totals = {}
    for item in production_data['Item'].unique():
        item_data = production_data[production_data['Item'] == item]
        total = item_data[latest_year].sum()
        if not pd.isna(total) and total > 0:
            item_totals[item] = total
    
    top_items = sorted(item_totals.items(), key=lambda x: x[1], reverse=True)[:5]
    
    # Create visualizations
    # 1. Top countries bar chart
    fig_countries = go.Figure(data=[
        go.Bar(
            x=[c[0] for c in top_countries],
            y=[c[1] for c in top_countries],
            marker_color='#1f77b4',
            text=[f'{c[1]:,.0f}' for c in top_countries],
            textposition='outside'
        )
    ])
    fig_countries.update_layout(
        title=f'Top 5 Producing Countries ({max(years)})',
        xaxis_title='Country',
        yaxis_title='Total Production',
        height=400,
        template='plotly_dark'
    )
    
    # 2. Top items bar chart
    fig_items = go.Figure(data=[
        go.Bar(
            x=[i[0][:30] for i in top_items],  # Truncate long names
            y=[i[1] for i in top_items],
            marker_color='#2ca02c',
            text=[f'{i[1]:,.0f}' for i in top_items],
            textposition='outside'
        )
    ])
    fig_items.update_layout(
        title=f'Top 5 Products by Production ({max(years)})',
        xaxis_title='Product',
        yaxis_title='Total Production',
        height=400,
        template='plotly_dark'
    )
    
    # 3. Production elements distribution
    element_counts = df_main.groupby('Element').size()
    fig_elements = go.Figure(data=[
        go.Pie(
            labels=element_counts.index,
            values=element_counts.values,
            hole=0.4
        )
    ])
    fig_elements.update_layout(
        title='Data Elements Distribution',
        height=400,
        template='plotly_dark'
    )
    
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H3(total_countries, className="text-info"),
                        html.P("Countries/Regions", className="text-muted mb-0")
                    ])
                ], className="text-center shadow-sm bg-dark")
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H3(total_items, className="text-success"),
                        html.P("Products Tracked", className="text-muted mb-0")
                    ])
                ], className="text-center shadow-sm bg-dark")
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H3(year_range, className="text-warning"),
                        html.P("Year Coverage", className="text-muted mb-0")
                    ])
                ], className="text-center shadow-sm bg-dark")
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H3(len(df_main), className="text-danger"),
                        html.P("Total Records", className="text-muted mb-0")
                    ])
                ], className="text-center shadow-sm bg-dark")
            ], width=3),
        ], className="mb-4"),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        dcc.Graph(figure=fig_countries)
                    ])
                ], className="shadow-sm bg-dark")
            ], width=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        dcc.Graph(figure=fig_items)
                    ])
                ], className="shadow-sm bg-dark")
            ], width=6),
        ], className="mb-4"),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        dcc.Graph(figure=fig_elements)
                    ])
                ], className="shadow-sm bg-dark")
            ], width=12),
        ])
    ], fluid=True)

def render_trends():
    """Production trends over time"""
    countries = sorted(df_main['Area'].unique())
    items = sorted(df_main['Item'].unique())
    elements = sorted(df_main['Element'].unique())
    
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Select Filters", className="mb-3"),
                        html.Label("Country:"),
                        dcc.Dropdown(
                            id='trend-country',
                            options=[{'label': c, 'value': c} for c in countries],
                            value=countries[0],
                            className="mb-3"
                        ),
                        html.Label("Product:"),
                        dcc.Dropdown(
                            id='trend-item',
                            options=[{'label': i, 'value': i} for i in items],
                            value=items[0],
                            className="mb-3"
                        ),
                        html.Label("Metric:"),
                        dcc.Dropdown(
                            id='trend-element',
                            options=[{'label': e, 'value': e} for e in elements],
                            value='Production',
                            className="mb-3"
                        ),
                    ])
                ], className="shadow-sm bg-dark")
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        dcc.Graph(id='trend-chart', style={'height': '600px'})
                    ])
                ], className="shadow-sm bg-dark")
            ], width=9),
        ])
    ], fluid=True)

@callback(
    Output('trend-chart', 'figure'),
    [Input('trend-country', 'value'),
     Input('trend-item', 'value'),
     Input('trend-element', 'value')]
)
def update_trend_chart(country, item, element):
    """Update trend chart based on selections"""
    filtered_df = df_main[
        (df_main['Area'] == country) &
        (df_main['Item'] == item) &
        (df_main['Element'] == element)
    ]
    
    if filtered_df.empty:
        return go.Figure().add_annotation(
            text="No data available for this selection",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
    
    # Extract year data
    values = []
    year_labels = []
    for year_col in year_cols:
        val = filtered_df[year_col].values[0]
        if not pd.isna(val) and val > 0:
            values.append(val)
            year_labels.append(int(year_col[1:]))
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=year_labels,
        y=values,
        mode='lines+markers',
        name=element,
        line=dict(width=3),
        marker=dict(size=6)
    ))
    
    unit = filtered_df['Unit'].values[0] if 'Unit' in filtered_df.columns else ''
    
    fig.update_layout(
        title=f'{element} of {item} in {country} Over Time',
        xaxis_title='Year',
        yaxis_title=f'{element} ({unit})',
        hovermode='x unified',
        template='plotly_dark'
    )
    
    return fig

def render_comparison():
    """Compare multiple countries"""
    countries = sorted(df_main['Area'].unique())
    items = sorted(df_main['Item'].unique())
    
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Compare Countries", className="mb-3"),
                        html.Label("Product:"),
                        dcc.Dropdown(
                            id='compare-item',
                            options=[{'label': i, 'value': i} for i in items],
                            value=items[0],
                            className="mb-3"
                        ),
                        html.Label("Countries (select multiple):"),
                        dcc.Dropdown(
                            id='compare-countries',
                            options=[{'label': c, 'value': c} for c in countries],
                            value=countries[:5],
                            multi=True,
                            className="mb-3"
                        ),
                        html.Label("Year:"),
                        dcc.Slider(
                            id='compare-year',
                            min=min(years),
                            max=max(years),
                            value=max(years),
                            marks={year: str(year) for year in range(min(years), max(years)+1, 10)},
                            tooltip={"placement": "bottom", "always_visible": True}
                        ),
                    ])
                ], className="shadow-sm bg-dark")
            ], width=12),
        ], className="mb-4"),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        dcc.Graph(id='compare-chart', style={'height': '500px'})
                    ])
                ], className="shadow-sm bg-dark")
            ], width=12),
        ])
    ], fluid=True)

@callback(
    Output('compare-chart', 'figure'),
    [Input('compare-item', 'value'),
     Input('compare-countries', 'value'),
     Input('compare-year', 'value')]
)
def update_comparison_chart(item, countries_list, year):
    """Update comparison chart"""
    if not countries_list:
        return go.Figure().add_annotation(
            text="Please select at least one country",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
    
    year_col = f'Y{year}'
    
    # Get production data for selected countries
    comparison_data = []
    for country in countries_list:
        filtered_df = df_main[
            (df_main['Area'] == country) &
            (df_main['Item'] == item) &
            (df_main['Element'] == 'Production')
        ]
        
        if not filtered_df.empty and year_col in filtered_df.columns:
            val = filtered_df[year_col].values[0]
            if not pd.isna(val):
                comparison_data.append({'Country': country, 'Production': val})
    
    if not comparison_data:
        return go.Figure().add_annotation(
            text="No data available for this selection",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
    
    df_compare = pd.DataFrame(comparison_data)
    df_compare = df_compare.sort_values('Production', ascending=True)
    
    fig = go.Figure(data=[
        go.Bar(
            y=df_compare['Country'],
            x=df_compare['Production'],
            orientation='h',
            marker_color='#ff7f0e',
            text=df_compare['Production'].apply(lambda x: f'{x:,.0f}'),
            textposition='outside'
        )
    ])
    
    fig.update_layout(
        title=f'Production of {item} by Country ({year})',
        xaxis_title='Production',
        yaxis_title='Country',
        height=max(400, len(df_compare) * 40),
        template='plotly_dark'
    )
    
    return fig

def render_top_producers():
    """Show top producers for different categories"""
    items = sorted(df_main['Item'].unique())
    
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Top Producers Analysis", className="mb-3"),
                        html.Label("Product:"),
                        dcc.Dropdown(
                            id='top-item',
                            options=[{'label': i, 'value': i} for i in items],
                            value=items[0],
                            className="mb-3"
                        ),
                        html.Label("Number of Top Producers:"),
                        dcc.Slider(
                            id='top-n',
                            min=5,
                            max=20,
                            value=10,
                            marks={i: str(i) for i in range(5, 21, 5)},
                            tooltip={"placement": "bottom", "always_visible": True}
                        ),
                    ])
                ], className="shadow-sm bg-dark")
            ], width=12),
        ], className="mb-4"),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        dcc.Graph(id='top-producers-chart', style={'height': '600px'})
                    ])
                ], className="shadow-sm bg-dark")
            ], width=8),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Production Statistics", className="mb-3"),
                        html.Div(id='top-producers-stats')
                    ])
                ], className="shadow-sm bg-dark")
            ], width=4),
        ])
    ], fluid=True)

@callback(
    [Output('top-producers-chart', 'figure'),
     Output('top-producers-stats', 'children')],
    [Input('top-item', 'value'),
     Input('top-n', 'value')]
)
def update_top_producers(item, n):
    """Update top producers visualization"""
    latest_year = f'Y{max(years)}'
    
    filtered_df = df_main[
        (df_main['Item'] == item) &
        (df_main['Element'] == 'Production')
    ]
    
    if filtered_df.empty:
        fig = go.Figure().add_annotation(
            text="No data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
        return fig, "No data available"
    
    # Get production values for latest year
    country_production = []
    for _, row in filtered_df.iterrows():
        val = row[latest_year]
        if not pd.isna(val) and val > 0:
            country_production.append({
                'Country': row['Area'],
                'Production': val
            })
    
    if not country_production:
        fig = go.Figure().add_annotation(
            text="No data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
        return fig, "No data available"
    
    df_top = pd.DataFrame(country_production)
    df_top = df_top.sort_values('Production', ascending=False).head(n)
    
    # Create visualization
    fig = go.Figure(data=[
        go.Bar(
            x=df_top['Country'],
            y=df_top['Production'],
            marker_color=px.colors.qualitative.Set3,
            text=df_top['Production'].apply(lambda x: f'{x:,.0f}'),
            textposition='outside'
        )
    ])
    
    fig.update_layout(
        title=f'Top {n} Producers of {item} ({max(years)})',
        xaxis_title='Country',
        yaxis_title='Production',
        xaxis={'tickangle': -45},
        template='plotly_dark'
    )
    
    # Calculate statistics
    total_production = df_top['Production'].sum()
    avg_production = df_top['Production'].mean()
    top_producer = df_top.iloc[0]
    top_share = (top_producer['Production'] / total_production * 100)
    
    stats = html.Div([
        html.P([html.Strong("Total Production:"), html.Br(), f"{total_production:,.0f}"]),
        html.Hr(),
        html.P([html.Strong("Average Production:"), html.Br(), f"{avg_production:,.0f}"]),
        html.Hr(),
        html.P([html.Strong("Top Producer:"), html.Br(), top_producer['Country']]),
        html.Hr(),
        html.P([html.Strong("Top Producer Share:"), html.Br(), f"{top_share:.1f}%"]),
    ])
    
    return fig, stats

def render_geographic():
    """Geographic distribution analysis"""
    items = sorted(df_main['Item'].unique())
    
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Geographic Analysis", className="mb-3"),
                        html.Label("Product:"),
                        dcc.Dropdown(
                            id='geo-item',
                            options=[{'label': i, 'value': i} for i in items],
                            value=items[0],
                            className="mb-3"
                        ),
                        html.Label("Year:"),
                        dcc.Slider(
                            id='geo-year',
                            min=min(years),
                            max=max(years),
                            value=max(years),
                            marks={year: str(year) for year in range(min(years), max(years)+1, 10)},
                            tooltip={"placement": "bottom", "always_visible": True}
                        ),
                    ])
                ], className="shadow-sm bg-dark")
            ], width=12),
        ], className="mb-4"),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        dcc.Graph(id='geo-chart', style={'height': '600px'})
                    ])
                ], className="shadow-sm bg-dark")
            ], width=12),
        ])
    ], fluid=True)

@callback(
    Output('geo-chart', 'figure'),
    [Input('geo-item', 'value'),
     Input('geo-year', 'value')]
)
def update_geographic_chart(item, year):
    """Update geographic chart"""
    year_col = f'Y{year}'
    
    filtered_df = df_main[
        (df_main['Item'] == item) &
        (df_main['Element'] == 'Production')
    ]
    
    if filtered_df.empty:
        return go.Figure().add_annotation(
            text="No data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
    
    geo_data = []
    for _, row in filtered_df.iterrows():
        val = row[year_col]
        if not pd.isna(val) and val > 0:
            geo_data.append({
                'Country': row['Area'],
                'Production': val
            })
    
    if not geo_data:
        return go.Figure().add_annotation(
            text="No data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
    
    df_geo = pd.DataFrame(geo_data)
    df_geo = df_geo.sort_values('Production', ascending=False)
    
    # Create treemap
    fig = px.treemap(
        df_geo,
        path=['Country'],
        values='Production',
        title=f'Production Distribution of {item} ({year})',
        color='Production',
        color_continuous_scale='Viridis'
    )
    
    fig.update_traces(textinfo="label+value")
    fig.update_layout(template='plotly_dark')
    
    return fig

def render_explorer():
    """Data explorer with detailed table"""
    countries = sorted(df_main['Area'].unique())
    items = sorted(df_main['Item'].unique())
    elements = sorted(df_main['Element'].unique())
    
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Data Explorer", className="mb-3"),
                        dbc.Row([
                            dbc.Col([
                                html.Label("Country:"),
                                dcc.Dropdown(
                                    id='explorer-country',
                                    options=[{'label': 'All', 'value': 'all'}] + 
                                            [{'label': c, 'value': c} for c in countries],
                                    value='all'
                                ),
                            ], width=4),
                            dbc.Col([
                                html.Label("Product:"),
                                dcc.Dropdown(
                                    id='explorer-item',
                                    options=[{'label': 'All', 'value': 'all'}] + 
                                            [{'label': i, 'value': i} for i in items],
                                    value='all'
                                ),
                            ], width=4),
                            dbc.Col([
                                html.Label("Metric:"),
                                dcc.Dropdown(
                                    id='explorer-element',
                                    options=[{'label': 'All', 'value': 'all'}] + 
                                            [{'label': e, 'value': e} for e in elements],
                                    value='Production'
                                ),
                            ], width=4),
                        ])
                    ])
                ], className="shadow-sm mb-4 bg-dark")
            ], width=12),
        ]),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div(id='explorer-table')
                    ])
                ], className="shadow-sm bg-dark")
            ], width=12),
        ])
    ], fluid=True)

@callback(
    Output('explorer-table', 'children'),
    [Input('explorer-country', 'value'),
     Input('explorer-item', 'value'),
     Input('explorer-element', 'value')]
)
def update_explorer_table(country, item, element):
    """Update data explorer table"""
    filtered_df = df_main.copy()
    
    if country != 'all':
        filtered_df = filtered_df[filtered_df['Area'] == country]
    if item != 'all':
        filtered_df = filtered_df[filtered_df['Item'] == item]
    if element != 'all':
        filtered_df = filtered_df[filtered_df['Element'] == element]
    
    # Limit to 100 rows for performance
    filtered_df = filtered_df.head(100)
    
    # Select key columns to display
    display_cols = ['Area', 'Item', 'Element', 'Unit'] + year_cols[-10:]  # Last 10 years
    filtered_df = filtered_df[display_cols]
    
    if filtered_df.empty:
        return html.P("No data available for the selected filters.", className="text-muted")
    
    # Create table
    table = dbc.Table.from_dataframe(
        filtered_df,
        striped=True,
        bordered=True,
        hover=True,
        responsive=True,
        size='sm',
        dark=True
    )
    
    return html.Div([
        html.P(f"Showing {len(filtered_df)} records (limited to 100)", className="text-muted mb-2"),
        table
    ])

if __name__ == '__main__':
    print("Starting dashboard server...")
    print("Open your browser and navigate to: http://127.0.0.1:8050")
    app.run(debug=True, host='0.0.0.0', port=8050)
