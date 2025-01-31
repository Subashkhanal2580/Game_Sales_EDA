import pandas as pd
from dash import html, dcc, callback, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc

from utils.data_loading import load_vgsales_data
from utils.data_processing import preprocess_overview_data
from components.cards.stats_card import create_stat_card
from components.cards.summary_card import (
    create_genre_summary_card, 
    create_publisher_summary_card, 
    create_regional_summary_card, 
    create_top_games_card
)
from utils.constants import COLORS, CHART_TEMPLATE

def create_overview_layout():
    """Creates the layout for the overview dashboard page."""
    df = load_vgsales_data()
    overview_stats = preprocess_overview_data(df)
    
    years = sorted([int(year) for year in df['Year'].dropna().unique() 
                   if 1980 <= year <= 2020 and df[df['Year'] == year]['Global_Sales'].sum() > 0])
    
    min_year = min(years)
    max_year = max(years)
    
    layout = html.Div([
        # Hero Section
        html.Div([
            html.Div([
                html.Div([
                    html.I(className="fas fa-chart-line text-blue-600 text-3xl mr-3"),
                    html.H1("Video Game Sales Dashboard", 
                           className="text-4xl font-extrabold tracking-tight text-gray-900")
                ], className="flex items-center mb-2"),
                html.P("Comprehensive analysis of global gaming industry trends",
                      className="text-xl text-gray-600 font-medium ml-10")
            ], className="container mx-auto px-6 py-8")
        ], className="bg-white border-b"),
        
        # Main Content Container
        html.Div([
            # Year Range Selection
            html.Div([
                html.Div([
                    html.I(className="fas fa-calendar text-blue-600 mr-2"),
                    html.H2("Time Period Analysis", className="text-lg font-semibold")
                ], className="flex items-center mb-4"),
                html.Div([
                    html.Div([
                        html.Label("Start Year", className="block text-sm font-medium text-gray-700 mb-2"),
                        dcc.Dropdown(
                            id='start-year-dropdown',
                            options=[{'label': str(year), 'value': year} for year in years],
                            value=min_year,
                            className="w-20",
                            clearable=False,
                            style={
            'fontSize': '14px',
            'minWidth': '200px',
            'maxWidth': '200px'
        }
                        )
                    ], className="pr-2"),
                    html.Div([
                        html.Label("End Year", className="block text-sm font-medium text-gray-700 mb-2"),
                        dcc.Dropdown(
                            id='end-year-dropdown',
                            options=[{'label': str(year), 'value': year} for year in years],
                            value=max_year,
                            className="w-20",
                            clearable=False,
                            style={
            'fontSize': '14px',
            'minWidth': '200px',
            'maxWidth': '200px'
        }
                        )
                    ], className="w-1/2 pl-2")
                ], className="flex")
            ], className="card shadow-lg rounded-lg p-4 mb-4 bg-white"),
            
        
            # # KPI Cards
            # html.Div([
            #     create_stat_card(
            #         "Total Global Sales",
            #         f"${overview_stats['total_sales']:.2f}B",
            #         "Lifetime sales volume",
            #         "fas fa-globe",
            #         "bg-blue-50"
            #     ),
            #     create_stat_card(
            #         "Total Games",
            #         f"{overview_stats['total_games']:,}",
            #         "Games released",
            #         "fas fa-gamepad",
            #         "bg-green-50"
            #     ),
            #     create_stat_card(
            #         "Active Publishers",
            #         str(overview_stats['active_publishers']),
            #         "Publishing companies",
            #         "fas fa-building",
            #         "bg-yellow-50"
            #     ),
            #     create_stat_card(
            #         "Platforms",
            #         str(overview_stats['total_platforms']),
            #         "Gaming platforms",
            #         "fas fa-tv",
            #         "bg-purple-50"
            #     )
            # ], className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6"),
            html.Div([  # Card container
                html.Div([  # Row container
                    html.Div([
                        html.I(className="fas fa-globe fa-2x text-blue-600"),
                        html.H3("Total Global Sales", className="text-sm text-gray-600"),
                        html.Div(f"${overview_stats['total_sales']:.2f}B", className="text-4xl font-bold text-gray-800 my-3"),
                        html.Div("Lifetime sales volume", className="text-xs text-gray-500")
                    ], className="col-2 p-6 mx-3 rounded", style={'backgroundColor': '#EBF8FF'}),
                    
                    html.Div([
                        html.I(className="fas fa-gamepad fa-2x text-green-600"),
                        html.H3("Total Games", className="text-sm text-gray-600"),
                        html.Div(f"{overview_stats['total_games']:,}", className="text-4xl font-bold text-gray-800 my-3"),
                        html.Div("Games released", className="text-xs text-gray-500")
                    ], className="col-2 p-6 mx-3 rounded", style={'backgroundColor': '#F0FFF4'}),
                    
                    html.Div([
                        html.I(className="fas fa-building fa-2x text-yellow-600"),
                        html.H3("Active Publishers", className="text-sm text-gray-600"),
                        html.Div(str(overview_stats['active_publishers']), className="text-4xl font-bold text-gray-800 my-3"),
                        html.Div("Publishing companies", className="text-xs text-gray-500")
                    ], className="col-2 p-6 mx-3 rounded", style={'backgroundColor': '#FFFFF0'}),
                    
                    html.Div([
                        html.I(className="fas fa-tv fa-2x text-purple-600"),
                        html.H3("Platforms", className="text-sm text-gray-600"),
                        html.Div(str(overview_stats['total_platforms']), className="text-4xl font-bold text-gray-800 my-3"),
                        html.Div("Gaming platforms", className="text-xs text-gray-500")
                    ], className="col-2 p-6 mx-3 rounded", style={'backgroundColor': '#FAF5FF'})
                ], className="row d-flex justify-content-between px-3")
                ], className="card shadow-lg rounded-lg p-4 mb-4 bg-white"),
            
            # Charts Grid
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([
                            html.I(className="fas fa-chart-line text-blue-600 mr-2"),
                            html.H2("Sales Trends by Region", className="text-xl font-semibold")
                        ], className="flex items-center mb-4"),
                        dcc.Graph(
                            id='overview-sales-trend',
                            className="h-96",
                            config={'displayModeBar': False}
                        )
                    ], className="bg-white p-6 rounded-lg shadow-sm"),
                ], className="bg-white p-6 rounded-lg shadow-sm"),
                
                
                html.Div([
                    html.Div([
                        html.Div([
                            html.I(className="fas fa-globe text-blue-600 mr-2"),
                            html.H2("Regional Market Share", className="text-xl font-semibold")
                        ], className="flex items-center mb-4"),
                        dcc.Graph(
                            id='overview-regional-share',
                            className="h-96",
                            config={'displayModeBar': False}
                        )
                    ], className="bg-white p-6 rounded-lg shadow-sm")
                ], className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6"),
            ], className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6"),

            
            # Market Analysis Section
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([
                            html.I(className="fas fa-award text-blue-600 mr-2"),
                            html.H2("Market Analysis", className="text-2xl font-bold text-gray-900")
                        ], className="flex items-center mb-6"),
                    ], className="bg-white p-6 rounded-lg shadow-sm"),
                ], className="bg-white p-6 rounded-lg shadow-sm"),
                
                html.Div([
                    html.Div([
                        html.Div([
                            html.I(className="fas fa-chart-pie text-blue-600 mr-2"),
                            html.H3("Genre Distribution", className="text-xl font-semibold")
                        ], className="flex items-center mb-4"),
                        dcc.Graph(
                            id='overview-genre-dist',
                            className="h-96",
                            config={'displayModeBar': False}
                        ),
                        html.Div(id='genre-summary-container', className="mt-4")
                    ], className="card shadow-lg rounded-lg p-4 mb-4 bg-white"),
                    
                    html.Div([
                        html.Div([
                            html.I(className="fas fa-microchip text-blue-600 mr-2"),
                            html.H3("Platform Performance", className="text-xl font-semibold")
                        ], className="flex items-center mb-4"),
                        dcc.Graph(
                            id='overview-platform-perf',
                            className="h-96",
                            config={'displayModeBar': False}
                        ),
                        html.Div(id='publisher-summary-container', className="mt-4")
                    ], className="card shadow-lg rounded-lg p-4 mb-4 bg-white")
                ], className="grid grid-cols-1 lg:grid-cols-2 gap-6")
            ], className="mb-6"),
            
            # Key Insights Section
            html.Div([
                html.Div([
                    html.I(className="fas fa-lightbulb text-blue-600 mr-2"),
                    html.H2("Key Insights", className="text-2xl font-bold text-gray-900")
                ], className="flex items-center mb-6"),
                html.Div(
                    id='overview-insights',
                    className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
                )
            ])
        ], className="card shadow-lg rounded-lg p-4 mb-4 bg-white")
    ], className="min-h-screen bg-gray-50")
    
    return layout

def create_stat_card(title, value, description, icon, bg_color):
    """Creates a styled stat card with icon."""
    return html.Div([
        html.Div([
            html.Div([
                html.I(className=f"{icon} text-blue-600", style={"fontSize": "1.5rem"})
            ], className=f"p-3 {bg_color.replace('50', '100')} rounded-lg"),
            html.Div([
                html.P(title, className="text-sm font-medium text-gray-600"),
                html.H3(value, className="text-2xl font-bold text-gray-900"),
                html.P(description, className="text-xs text-gray-500")
            ])
        ], className="flex items-center gap-4")
    ], className=f"bg-white p-6 rounded-lg shadow-sm {bg_color}")

# @callback(
#     [Output('overview-sales-trend', 'figure'),
#      Output('overview-regional-share', 'figure'),
#      Output('overview-genre-dist', 'figure'),
#      Output('overview-platform-perf', 'figure'),
#      Output('overview-insights', 'children'),
#      Output('genre-summary-container', 'children'),
#      Output('publisher-summary-container', 'children')],
#     [Input('start-year-dropdown', 'value'),
#      Input('end-year-dropdown', 'value')]
# )
# def update_dashboard(start_year, end_year):
#     """Updates all dashboard components based on selected year range."""
#     df = load_vgsales_data()
    
#     # Ensure valid year range
#     if start_year > end_year:
#         start_year, end_year = end_year, start_year
    
#     # Filter data
#     mask = (df['Year'] >= start_year) & (df['Year'] <= end_year)
#     df_filtered = df[mask]
    
#     # Generate all visualizations and insights
#     sales_trend = create_sales_trend(df_filtered)
#     regional_share = create_regional_share(df_filtered)
#     genre_dist = create_genre_distribution(df_filtered)
#     platform_perf = create_platform_performance(df_filtered)
#     insights = generate_insights(df_filtered)
    
#     # Create summary cards
#     genre_summary = create_genre_summary_card(df_filtered)
#     publisher_summary = create_publisher_summary_card(df_filtered)
    
#     return sales_trend, regional_share, genre_dist, platform_perf, insights, genre_summary, publisher_summary

@callback(
    [Output('overview-sales-trend', 'figure'),
     Output('overview-regional-share', 'figure'),
     Output('overview-genre-dist', 'figure'),
     Output('overview-platform-perf', 'figure'),
     Output('overview-insights', 'children'),
     Output('genre-summary-container', 'children'),
     Output('publisher-summary-container', 'children')],
    [Input('start-year-dropdown', 'value'),
     Input('end-year-dropdown', 'value')]
)
def update_dashboard(start_year, end_year):
    """Updates all dashboard components based on selected year range."""
    df = load_vgsales_data()
    
    # Handle None values
    if start_year is None or end_year is None:
        start_year = int(df['Year'].min())
        end_year = int(df['Year'].max())
    
    # Ensure valid year range
    if start_year > end_year:
        start_year, end_year = end_year, start_year
    
    # Filter data
    mask = (df['Year'] >= start_year) & (df['Year'] <= end_year)
    df_filtered = df[mask]
    
    # Generate visualizations and insights
    sales_trend = create_sales_trend(df_filtered)
    regional_share = create_regional_share(df_filtered)
    genre_dist = create_genre_distribution(df_filtered)
    platform_perf = create_platform_performance(df_filtered)
    insights = generate_insights(df_filtered)
    genre_summary = create_genre_summary_card(df_filtered)
    publisher_summary = create_publisher_summary_card(df_filtered)
    
    return sales_trend, regional_share, genre_dist, platform_perf, insights, genre_summary, publisher_summary

def create_sales_trend(df):
    """Creates the sales trend visualization with improved styling."""
    yearly_sales = df.groupby('Year').agg({
        'Global_Sales': 'sum',
        'NA_Sales': 'sum',
        'EU_Sales': 'sum',
        'JP_Sales': 'sum'
    }).reset_index()
    
    fig = px.area(yearly_sales,
                  x='Year',
                  y=['NA_Sales', 'EU_Sales', 'JP_Sales'],
                  labels={'value': 'Sales (Millions)', 
                         'variable': 'Region',
                         'NA_Sales': 'North America',
                         'EU_Sales': 'Europe',
                         'JP_Sales': 'Japan'},
                  template=CHART_TEMPLATE)
    
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(l=40, r=40, t=40, b=40),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        hovermode='x unified'
    )
    
    return fig

def create_regional_share(df):
    """Creates the regional market share visualization."""
    totals = {
        'North America': df['NA_Sales'].sum(),
        'Europe': df['EU_Sales'].sum(),
        'Japan': df['JP_Sales'].sum(),
        'Other': df['Other_Sales'].sum()
    }
    
    fig = go.Figure(data=[go.Pie(
        labels=list(totals.keys()),
        values=list(totals.values()),
        hole=.4,
        textinfo='label+percent',
        marker=dict(colors=[COLORS['primary'], COLORS['secondary'], 
                          COLORS['tertiary'], COLORS['quaternary']])
    )])
    
    fig.update_layout(
        showlegend=False,
        margin=dict(l=20, r=20, t=40, b=20),
        annotations=[dict(text=f'${sum(totals.values()):.1f}M',
                        x=0.5, y=0.5, showarrow=False,
                        font=dict(size=20))]
    )
    
    return fig

def create_genre_distribution(df):
    """Creates the genre distribution visualization."""
    genre_sales = df.groupby('Genre')['Global_Sales'].sum().sort_values(ascending=True)
    
    fig = go.Figure(go.Bar(
        x=genre_sales.values,
        y=genre_sales.index,
        orientation='h',
        marker_color=COLORS['primary'],
        text=genre_sales.values.round(1),
        texttemplate='$%{text}M',
        textposition='auto',
    ))
    
    fig.update_layout(
        xaxis_title="Global Sales (Millions)",
        yaxis_title=None,
        margin=dict(l=20, r=20, t=40, b=20),
        xaxis=dict(showgrid=True)
    )
    
    return fig

def create_platform_performance(df):
    """Creates the platform performance visualization."""
    platform_sales = df.groupby('Platform')['Global_Sales'].sum().nlargest(10)
    
    fig = go.Figure(go.Bar(
        x=platform_sales.values,
        y=platform_sales.index,
        orientation='h',
        marker_color=COLORS['secondary'],
        text=platform_sales.values.round(1),
        texttemplate='$%{text}M',
        textposition='auto',
    ))
    
    fig.update_layout(
        xaxis_title="Global Sales (Millions)",
        yaxis_title=None,
        margin=dict(l=20, r=20, t=40, b=20),
        xaxis=dict(showgrid=True)
    )
    
    return fig

# def generate_insights(df):
#     """Generates key insights cards from the data."""
#     insights = []
    
#     # Sales Growth Insight
#     growth = calculate_yoy_growth(df)
#     if growth is not None:
#         trend = 'positive' if growth > 0 else 'negative'
#         insights.append(create_trend_card(
#             "Sales Growth",
#             f"{abs(growth):.1f}%",
#             f"Year-over-year {'increase' if trend == 'positive' else 'decrease'}",
#             trend
#         ))
    
#     # Market Leaders
#     publisher_sales = df.groupby('Publisher')['Global_Sales'].sum()
#     top_publisher = publisher_sales.nlargest(1)
#     publisher_share = (top_publisher.values[0] / publisher_sales.sum()) * 100
    
#     insights.append(create_stat_card(
#         "Market Leader",
#         top_publisher.index[0],
#         f"{publisher_share:.1f}% market share",
#         "bg-blue-50"
#     ))
    
#     # Genre Diversity
#     genre_count = df['Genre'].nunique()
#     avg_sales_per_genre = df['Global_Sales'].sum() / genre_count
    
#     insights.append(create_stat_card(
#         "Genre Diversity",
#         f"{genre_count} genres",
#         f"${avg_sales_per_genre:.1f}M avg. sales per genre",
#         "bg-green-50"
#     ))
    
#     return html.Div(insights, className="grid grid-cols-1 md:grid-cols-3 gap-4")
def generate_insights(df):
    """Generates key insights cards from the data."""
    insights = []
    
    growth = calculate_yoy_growth(df)
    if growth is not None:
        trend = 'positive' if growth > 0 else 'negative'
        insights.append(create_stat_card(
            "Sales Growth",
            f"{abs(growth):.1f}%",
            f"Year-over-year {'increase' if trend == 'positive' else 'decrease'}",
            "fas fa-chart-line",
            "bg-blue-50"
        ))
    
    publisher_sales = df.groupby('Publisher')['Global_Sales'].sum()
    top_publisher = publisher_sales.nlargest(1)
    publisher_share = (top_publisher.values[0] / publisher_sales.sum()) * 100
    
    insights.append(create_stat_card(
        "Market Leader",
        top_publisher.index[0],
        f"{publisher_share:.1f}% market share",
        "fas fa-crown",
        "bg-yellow-50"
    ))
    
    genre_count = df['Genre'].nunique()
    avg_sales_per_genre = df['Global_Sales'].sum() / genre_count
    
    insights.append(create_stat_card(
        "Genre Diversity",
        f"{genre_count} genres",
        f"${avg_sales_per_genre:.1f}M avg. sales per genre",
        "fas fa-layer-group",
        "bg-green-50"
    ))
    
    return html.Div(insights, className="grid grid-cols-1 md:grid-cols-3 gap-4")

def calculate_yoy_growth(df):
    """Calculates year-over-year growth rate."""
    if len(df) < 2:
        return None
        
    yearly_sales = df.groupby('Year')['Global_Sales'].sum()
    if len(yearly_sales) < 2:
        return None
    
    latest_years = sorted(yearly_sales.index)[-2:]
    previous = yearly_sales[latest_years[0]]
    current = yearly_sales[latest_years[1]]
    
    if previous > 0:
        return ((current - previous) / previous) * 100
    return None

def create_trend_card(title, value, description, trend):
    """Creates a card with trend indicator."""
    icon_class = {
        'positive': 'fas fa-arrow-up text-green-500',
        'negative': 'fas fa-arrow-down text-red-500',
        'neutral': 'fas fa-minus text-gray-500'
    }
    
    return dbc.Card([
        dbc.CardHeader(title, className="font-semibold"),
        dbc.CardBody([
            html.H3(value, className="text-2xl font-bold mb-2"),
            html.Div([
                html.I(className=icon_class[trend]),
                html.Span(description, className="ml-2 text-sm text-gray-600")
            ], className="flex items-center")
        ])
    ], className="h-full")

# Updated color constants
COLORS.update({
    'primary': '#4A90E2',    # Blue
    'secondary': '#50C878',  # Green
    'tertiary': '#FF6B6B',   # Red
    'quaternary': '#FFB347', # Orange
    'background': '#F8FAFC', # Light gray
    'text': '#2D3748',       # Dark gray
})

# Updated chart template
CHART_TEMPLATE.update({
    'layout': {
        'font': {'family': 'Inter, system-ui, sans-serif', 'size': 12},
        'plot_bgcolor': 'white',
        'paper_bgcolor': 'white',
        'colorway': [COLORS['primary'], COLORS['secondary'], 
                    COLORS['tertiary'], COLORS['quaternary']],
        'xaxis': {
            'showgrid': True,
            'gridwidth': 1,
            'gridcolor': '#E2E8F0',
            'showline': True,
            'linewidth': 1,
            'linecolor': '#CBD5E0'
        },
        'yaxis': {
            'showgrid': True,
            'gridwidth': 1,
            'gridcolor': '#E2E8F0',
            'showline': True,
            'linewidth': 1,
            'linecolor': '#CBD5E0'
        }
    }
})

def preprocess_overview_data(df):
    """Preprocesses data for overview statistics."""
    return {
        'total_sales': df['Global_Sales'].sum(),
        'total_games': len(df),
        'active_publishers': df['Publisher'].nunique(),
        'total_platforms': df['Platform'].nunique(),
        'avg_rating': df.get('Rating', 0),  # Fallback if column doesn't exist
        'top_genre': df.groupby('Genre')['Global_Sales'].sum().idxmax()
    }

def format_sales(value):
    """Formats sales values with proper units."""
    if value >= 1000:
        return f'{value/1000:.1f}B'
    return f'{value:.1f}M'

def get_top_games(df, n=5):
    """Returns top n games by global sales."""
    return df.nlargest(n, 'Global_Sales')[
        ['Name', 'Global_Sales', 'Year', 'Publisher']
    ].values.tolist()

def get_top_publishers(df, n=5):
    """Returns top n publishers by global sales."""
    publisher_stats = df.groupby('Publisher').agg({
        'Global_Sales': 'sum',
        'Name': 'count'
    }).reset_index()
    
    return publisher_stats.nlargest(n, 'Global_Sales')[
        ['Publisher', 'Global_Sales', 'Name']
    ].values.tolist()

def get_top_genres(df, n=5):
    """Returns top n genres by global sales."""
    genre_stats = df.groupby('Genre').agg({
        'Global_Sales': 'sum',
        'Name': 'count'
    }).reset_index()
    
    return genre_stats.nlargest(n, 'Global_Sales')[
        ['Genre', 'Global_Sales', 'Name']
    ].values.tolist()

def validate_year_range(start_year, end_year, available_years):
    """Validates and adjusts year range if necessary."""
    if not available_years:
        return None, None
        
    min_year, max_year = min(available_years), max(available_years)
    
    start_year = max(min_year, min(start_year, max_year))
    end_year = max(min_year, min(end_year, max_year))
    
    if start_year > end_year:
        start_year, end_year = end_year, start_year
        
    return start_year, end_year