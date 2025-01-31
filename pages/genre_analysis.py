
import pandas as pd
from dash import html, dcc, callback, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc

from utils.data_loading import load_vgsales_data
from utils.data_processing import preprocess_genre_data
from components.cards.stats_card import create_stat_card
from utils.constants import COLORS, CHART_TEMPLATE
from components.charts.genre_charts import (
    create_genre_sales_chart,
    create_genre_platform_distribution,
    create_genre_regional_analysis,
    create_genre_timeline,
    create_genre_publisher_affinity,
    create_top_games_by_genre
)

def create_genre_analysis_layout():
    """Creates the layout for the genre analysis page."""
    df = load_vgsales_data()
    genre_stats = preprocess_genre_data(df)
    
    layout = html.Div([
        # Header Section
        html.Div([
            html.H1("Video Game Sales Analysis by Genre", className="text-3xl font-bold mb-4"),
            html.P("Analyze sales trends and distribution across different gaming genres", className="text-gray-600 mb-8")
        ], className="mb-8"),
        
        # Filters Section
        html.Div([
            html.Div([
                html.Label("Time Period", className="text-sm text-gray-600"),
                html.Div([
                    dcc.Dropdown(
                        id='year-start',
                        options=[{'label': str(int(year)), 'value': year} 
                                for year in sorted(df['Year'].dropna().unique())],
                        value=df['Year'].dropna().min(),
                        clearable=False,
                        className="w-40",
                        placeholder="Start Year"
                    ),
                    html.Span("to", className="mx-4 text-gray-400"),
                    dcc.Dropdown(
                        id='year-end',
                        options=[{'label': str(int(year)), 'value': year}
                                for year in sorted(df['Year'].dropna().unique())],
                        value=df['Year'].dropna().max(),
                        clearable=False,
                        className="w-40",
                        placeholder="End Year"
                    )
                ], className="flex items-center mt-2 bg-white rounded-lg shadow-sm")
            ], className="w-full lg:w-1/2 mb-6"),
            
            html.Div([
                html.Label("Select Regions", className="text-sm text-gray-600"),
                dcc.Dropdown(
                    id='region-selector',
                    options=[
                        {'label': 'North America', 'value': 'NA_Sales'},
                        {'label': 'Europe', 'value': 'EU_Sales'},
                        {'label': 'Japan', 'value': 'JP_Sales'},
                        {'label': 'Other Regions', 'value': 'Other_Sales'},
                        {'label': 'Global', 'value': 'Global_Sales'}
                    ],
                    value='Global_Sales',
                    multi=True,
                    className="mt-2"
                )
            ], className="w-full md:w-1/2 lg:w-1/3")
        ], className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8"),
        
        # Stats Cards Section
        dbc.Row([
            dbc.Col(create_stat_card(
                "Total Genres",
                str(len(genre_stats['unique_genres'])),
                "Number of unique gaming genres"
            ), width=4),
            dbc.Col(create_stat_card(
                "Top Genre",
                genre_stats['top_genre'],
                f"${genre_stats['top_genre_sales']:.2f}M in sales"
            ), width=4),
            dbc.Col(create_stat_card(
                "Fastest Growing",
                genre_stats['fastest_growing'],
                f"{genre_stats['growth_rate']:.1f}% YoY growth"
            ), width=4)
        ], className="mb-4"),
        
        # Charts Section
        dbc.Row([
            dbc.Col(dcc.Graph(id='genre-sales-chart'), width=12)
        ], className="mb-4"),
        
        dbc.Row([
            dbc.Col(dcc.Graph(id='genre-platform-heatmap'), width=6),
            dbc.Col(dcc.Graph(id='genre-regional-share'), width=6)
        ], className="mb-4"),
        
        dbc.Row([
            dbc.Col(dcc.Graph(id='genre-timeline'), width=12)
        ], className="mb-4"),
        
        dbc.Row([
            dbc.Col(dcc.Graph(id='genre-publisher-heatmap'), width=12)
        ], className="mb-4"),
        
        dbc.Row([
            dbc.Col(dcc.Graph(id='top-games-by-genre'), width=12)
        ], className="mb-4")
    ], className="p-6 bg-gray-50")
    
    return layout

@callback(
    [Output('genre-sales-chart', 'figure'),
     Output('genre-platform-heatmap', 'figure'),
     Output('genre-regional-share', 'figure'),
     Output('genre-timeline', 'figure'),
     Output('genre-publisher-heatmap', 'figure'),
     Output('top-games-by-genre', 'figure')],
    [Input('year-start', 'value'),
     Input('year-end', 'value'),
     Input('region-selector', 'value')]
)
def update_charts(start_year, end_year, regions):
    """Updates all charts based on selected filters."""
    df = load_vgsales_data()
    df_filtered = df[(df['Year'] >= start_year) & (df['Year'] <= end_year)]
    
    # Get top genre for the filtered data
    top_genre = df_filtered.groupby('Genre')['Global_Sales'].sum().idxmax()
    
    # Extract just the figures from the graph components
    sales_chart = create_genre_sales_chart(df_filtered).figure
    platform_dist = create_genre_platform_distribution(df_filtered, regions).figure
    regional_share = create_genre_regional_analysis(df_filtered).figure
    timeline = create_genre_timeline(df_filtered).figure
    publisher_affinity = create_genre_publisher_affinity(df_filtered).figure
    top_games = create_top_games_by_genre(df_filtered, top_genre).figure
    
    return sales_chart, platform_dist, regional_share, timeline, publisher_affinity, top_games