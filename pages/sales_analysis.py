# import pandas as pd
# import numpy as np
# from dash import html, dcc, callback, Input, Output
# import plotly.express as px
# import plotly.graph_objects as go

# from utils.data_loading import load_vgsales_data
# from utils.data_processing import preprocess_sales_data
# from components.cards.stats_card import create_stat_card
# from components.charts.regional_charts import create_regional_distribution_pie
# from utils.constants import COLORS, CHART_TEMPLATE

# def create_sales_analysis_layout():
#     """Creates the layout for the sales analysis page."""
    
#     # Load and preprocess data
#     df = load_vgsales_data()
#     sales_stats = preprocess_sales_data(df)
    
#     layout = html.Div([
#         # Header Section
#         html.Div([
#             html.H1("Video Game Sales Analysis", 
#                    className="text-3xl font-bold mb-4"),
#             html.P("Comprehensive analysis of video game sales across regions and time periods",
#                   className="text-gray-600 mb-8")
#         ], className="mb-8"),
        
#         # Filters Section
#         html.Div([
#             # Time Period Filter
#             html.Div([
#                 html.Label("Select Time Period:", className="block text-sm font-medium mb-2"),
#                 dcc.RangeSlider(
#                     id='sales-year-range',
#                     min=df['Year'].min(),
#                     max=df['Year'].max(),
#                     value=[df['Year'].min(), df['Year'].max()],
#                     marks={int(year): str(int(year)) 
#                           for year in range(int(df['Year'].min()), int(df['Year'].max()) + 1, 5)},
#                     className="mt-2"
#                 )
#             ], className="w-full md:w-1/2 mb-6"),
            
#             # Sales Threshold Filter
#             html.Div([
#                 html.Label("Minimum Global Sales (M):", className="block text-sm font-medium mb-2"),
#                 dcc.Slider(
#                     id='sales-threshold',
#                     min=0,
#                     max=df['Global_Sales'].max(),
#                     value=0,
#                     marks={i: f'${i}M' for i in range(0, int(df['Global_Sales'].max()) + 1, 5)},
#                     className="mt-2"
#                 )
#             ], className="w-full md:w-1/2 mb-6")
#         ], className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8"),
        
#         # Key Metrics Cards
#         html.Div([
#             create_stat_card(
#                 "Total Sales",
#                 f"${sales_stats['total_sales']:.2f}B",
#                 "Global lifetime sales"
#             ),
#             create_stat_card(
#                 "Best Selling Game",
#                 sales_stats['top_game'],
#                 f"${sales_stats['top_game_sales']:.2f}M in sales"
#             ),
#             create_stat_card(
#                 "Peak Year",
#                 str(int(sales_stats['peak_year'])),
#                 f"${sales_stats['peak_year_sales']:.2f}M in sales"
#             )
#         ], className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8"),
        
#         # Sales Trends Analysis
#         html.Div([
#             html.H2("Global Sales Trends", className="text-xl font-semibold mb-4"),
#             dcc.Graph(
#                 id='sales-trends',
#                 config={'displayModeBar': False}
#             )
#         ], className="mb-8"),
        
#         # Regional Sales Distribution
#         html.Div([
#             html.H2("Regional Sales Distribution", className="text-xl font-semibold mb-4"),
#             dcc.Graph(
#                 id='regional-distribution',
#                 config={'displayModeBar': False}
#             )
#         ], className="mb-8"),
        
#         # Sales Performance Matrix
#         html.Div([
#             html.H2("Sales Performance Analysis", className="text-xl font-semibold mb-4"),
#             html.Div([
#                 # Genre Performance
#                 html.Div([
#                     html.H3("Genre Performance", className="text-lg font-medium mb-3"),
#                     dcc.Graph(
#                         id='genre-sales',
#                         config={'displayModeBar': False}
#                     )
#                 ], className="w-full lg:w-1/2 mb-6"),
                
#                 # Platform Performance
#                 html.Div([
#                     html.H3("Platform Performance", className="text-lg font-medium mb-3"),
#                     dcc.Graph(
#                         id='platform-sales',
#                         config={'displayModeBar': False}
#                     )
#                 ], className="w-full lg:w-1/2 mb-6")
#             ], className="grid grid-cols-1 lg:grid-cols-2 gap-4")
#         ], className="mb-8"),
        
#         # Top Performers Table
#         html.Div([
#             html.H2("Top Performing Games", className="text-xl font-semibold mb-4"),
#             html.Div(id='top-games-table', className="overflow-x-auto")
#         ], className="mb-8")
#     ], className="p-6")
    
#     return layout

# # Callbacks
# @callback(
#     Output('sales-trends', 'figure'),
#     [Input('sales-year-range', 'value'),
#      Input('sales-threshold', 'value')]
# )
# def update_sales_trends(years, threshold):
#     """Updates the sales trends visualization."""
#     df = load_vgsales_data()
    
#     # Filter data
#     mask = (df['Year'] >= years[0]) & (df['Year'] <= years[1]) & (df['Global_Sales'] >= threshold)
#     df_filtered = df[mask]
    
#     # Calculate yearly sales
#     yearly_sales = df_filtered.groupby('Year').agg({
#         'Global_Sales': 'sum',
#         'NA_Sales': 'sum',
#         'EU_Sales': 'sum',
#         'JP_Sales': 'sum',
#         'Other_Sales': 'sum'
#     }).reset_index()
    
#     fig = px.line(yearly_sales,
#                   x='Year',
#                   y=['Global_Sales', 'NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales'],
#                   title='Sales Trends Over Time')
    
#     fig.update_layout(
#         template=CHART_TEMPLATE,
#         xaxis_title="Year",
#         yaxis_title="Sales (Millions)",
#         legend_title="Region"
#     )
    
#     return fig

# @callback(
#     Output('regional-distribution', 'figure'),
#     [Input('sales-year-range', 'value'),
#      Input('sales-threshold', 'value')]
# )
# def update_regional_distribution(years, threshold):
#     """Updates the regional distribution visualization."""
#     df = load_vgsales_data()
    
#     # Filter data
#     mask = (df['Year'] >= years[0]) & (df['Year'] <= years[1]) & (df['Global_Sales'] >= threshold)
#     df_filtered = df[mask]
    
#     # Calculate regional totals
#     regional_totals = pd.DataFrame({
#         'Region': ['North America', 'Europe', 'Japan', 'Other'],
#         'Sales': [
#             df_filtered['NA_Sales'].sum(),
#             df_filtered['EU_Sales'].sum(),
#             df_filtered['JP_Sales'].sum(),
#             df_filtered['Other_Sales'].sum()
#         ]
#     })
    
#     fig = go.Figure(data=[go.Pie(
#         labels=regional_totals['Region'],
#         values=regional_totals['Sales'],
#         hole=.4,
#         textinfo='label+percent',
#         hovertemplate="%{label}<br>$%{value:.1f}M<extra></extra>"
#     )])
    
#     fig.update_layout(
#         template=CHART_TEMPLATE,
#         title="Regional Sales Distribution"
#     )
    
#     return fig

# @callback(
#     Output('genre-sales', 'figure'),
#     [Input('sales-year-range', 'value'),
#      Input('sales-threshold', 'value')]
# )
# def update_genre_sales(years, threshold):
#     """Updates the genre sales visualization."""
#     df = load_vgsales_data()
    
#     # Filter data
#     mask = (df['Year'] >= years[0]) & (df['Year'] <= years[1]) & (df['Global_Sales'] >= threshold)
#     df_filtered = df[mask]
    
#     # Calculate genre performance
#     genre_sales = df_filtered.groupby('Genre')['Global_Sales'].sum().sort_values(ascending=True)
    
#     fig = go.Figure(go.Bar(
#         x=genre_sales.values,
#         y=genre_sales.index,
#         orientation='h',
#         marker_color=COLORS['primary']
#     ))
    
#     fig.update_layout(
#         template=CHART_TEMPLATE,
#         title="Sales by Genre",
#         xaxis_title="Global Sales (Millions)",
#         yaxis_title="Genre",
#         showlegend=False
#     )
    
#     return fig

# @callback(
#     Output('platform-sales', 'figure'),
#     [Input('sales-year-range', 'value'),
#      Input('sales-threshold', 'value')]
# )
# def update_platform_sales(years, threshold):
#     """Updates the platform sales visualization."""
#     df = load_vgsales_data()
    
#     # Filter data
#     mask = (df['Year'] >= years[0]) & (df['Year'] <= years[1]) & (df['Global_Sales'] >= threshold)
#     df_filtered = df[mask]
    
#     # Calculate platform performance
#     platform_sales = df_filtered.groupby('Platform')['Global_Sales'].sum().sort_values(ascending=True)
    
#     fig = go.Figure(go.Bar(
#         x=platform_sales.values,
#         y=platform_sales.index,
#         orientation='h',
#         marker_color=COLORS['secondary']
#     ))
    
#     fig.update_layout(
#         template=CHART_TEMPLATE,
#         title="Sales by Platform",
#         xaxis_title="Global Sales (Millions)",
#         yaxis_title="Platform",
#         showlegend=False
#     )
    
#     return fig

# @callback(
#     Output('top-games-table', 'children'),
#     [Input('sales-year-range', 'value'),
#      Input('sales-threshold', 'value')]
# )
# def update_top_games_table(years, threshold):
#     """Updates the top games table."""
#     df = load_vgsales_data()
    
#     # Filter data
#     mask = (df['Year'] >= years[0]) & (df['Year'] <= years[1]) & (df['Global_Sales'] >= threshold)
#     df_filtered = df[mask]
    
#     # Get top games
#     top_games = get_top_games(df_filtered)
    
#     return create_top_games_table(top_games)

# def get_top_games(df, n=10):
#     """Gets the top n games by global sales."""
#     return df.nlargest(n, 'Global_Sales')[['Name', 'Platform', 'Publisher', 'Global_Sales', 'Year']]

# def create_top_games_table(df):
#     """Creates an HTML table for top games."""
#     return html.Table(
#         # Header
#         [html.Tr([html.Th(col, className="px-4 py-2 bg-gray-100") 
#                  for col in ['Game', 'Platform', 'Publisher', 'Global Sales', 'Year']])] +
#         # Body
#         [html.Tr([
#             html.Td(row['Name'], className="px-4 py-2 border"),
#             html.Td(row['Platform'], className="px-4 py-2 border"),
#             html.Td(row['Publisher'], className="px-4 py-2 border"),
#             html.Td(f"${row['Global_Sales']:.2f}M", className="px-4 py-2 border"),
#             html.Td(int(row['Year']), className="px-4 py-2 border")
#         ]) for _, row in df.iterrows()],
#         className="min-w-full border-collapse border"
#     )

import pandas as pd
import numpy as np
from dash import html, dcc, callback, Input, Output
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

from utils.data_loading import load_vgsales_data
from utils.data_processing import preprocess_sales_data
from components.cards.stats_card import create_stat_card
from components.charts.regional_charts import create_regional_distribution_pie
from utils.constants import COLORS, CHART_TEMPLATE

# Modern theme constants
THEME = {
    'primary': '#4F46E5',
    'secondary': '#818CF8',
    'background': '#F9FAFB',
    'card': '#FFFFFF',
    'text': {
        'primary': '#111827',
        'secondary': '#4B5563',
        'muted': '#6B7280'
    }
}

# Enhanced Plotly theme
CHART_THEME = {
    'layout': {
        'paper_bgcolor': 'rgba(0,0,0,0)',
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'font': {'size': 12, 'family': 'Inter, system-ui, sans-serif'},
        'margin': dict(l=40, r=40, t=40, b=40),
        'hovermode': 'closest',
        'colorway': [THEME['primary'], THEME['secondary']],
        'showlegend': True,
        'legend': {
            'orientation': 'h',
            'yanchor': 'bottom',
            'y': 1.02,
            'xanchor': 'right',
            'x': 1
        }
    }
}

def create_date_options():
    """Creates predefined date range options."""
    return [
        {'label': 'Last 30 Days', 'value': 30},
        {'label': 'Last 6 Months', 'value': 180},
        {'label': 'Last Year', 'value': 365},
        {'label': 'All Time', 'value': 'all'}
    ]

def create_sales_analysis_layout():
    """Creates the modernized layout for the sales analysis page."""
    df = load_vgsales_data()
    sales_stats = preprocess_sales_data(df)
    
    return html.Div([
        # Header Section
        html.Div([
            html.Div([
                html.H1("Video Game Sales Analysis", 
                   className="text-2xl font-bold text-gray-900"),
                html.P("Comprehensive analysis of video game sales across regions and time periods",
                    className="text-sm text-gray-600 mt-2")
            ], className="mb-8"),
        ], className="bg-white rounded-lg shadow-md p-6 mb-8"),
        
        # Filters Section
        html.Div([
            # Time Period Filter
            html.Div([
                html.Div([
                    html.Label("Time Period", 
                            className="block text-sm font-medium text-gray-700 mb-2"),
                    dcc.Dropdown(
                        id='date-range-preset',
                        options=create_date_options(),
                        value='all',
                        className="w-full mb-2"
                    ),
                    dcc.DatePickerRange(
                        id='date-range',
                        min_date_allowed=datetime(int(df['Year'].min()), 1, 1),
                        max_date_allowed=datetime(int(df['Year'].max()), 12, 31),
                        className="w-full"
                    )
                ], className="w-72"),
            ], className="bg-white rounded-lg shadow-md p-6 mb-8"),
            
            # Sales Threshold Filter
            html.Div([
                html.Div([
                    html.Label("Minimum Global Sales (M)", 
                            className="block text-sm font-medium text-gray-700 mb-2"),
                    dcc.Input(
                        id='sales-threshold',
                        type='number',
                        min=0,
                        max=df['Global_Sales'].max(),
                        value=0,
                        className="w-full px-3 py-2 border rounded-md"
                    )
                ], className="w-72 ml-4")
            ], className="bg-white rounded-lg shadow-md p-6 mb-8"),
        ], className="bg-white rounded-lg shadow-md p-6 mb-8"),

        

        html.Div([
            html.Div([
                create_stat_card(
                    "Total Global Sales",
                    f"${sales_stats['total_sales']:.2f}B",
                    "Lifetime sales volume",
                    "bg-green-100"
                ),
                create_stat_card(
                    "Best Selling Title",
                    sales_stats['top_game'],
                    f"${sales_stats['top_game_sales']:.2f}M in sales",
                    "bg-blue-100"
                ),
                create_stat_card(
                    "Peak Performance Year",
                    str(int(sales_stats['peak_year'])),
                    f"${sales_stats['peak_year_sales']:.2f}M in sales",
                    "bg-yellow-100"
                )
            ], className="flex justify-between items-stretch px-3"),
        ], className="bg-white rounded-lg shadow-md p-6 mb-8"),
        
        # Sales Trends Analysis
        html.Div([
            html.H2("Global Sales Trends", 
                   className="text-lg font-semibold mb-4"),
            dcc.Graph(
                id='sales-trends',
                config={'displayModeBar': 'hover'},
                className="h-96"
            )
        ], className="bg-white rounded-lg shadow-md p-6 mb-8"),
        
        # Regional Distribution
        html.Div([
            html.H2("Regional Sales Distribution", 
                   className="text-lg font-semibold mb-4"),
            dcc.Graph(
                id='regional-distribution',
                config={'displayModeBar': 'hover'},
                className="h-96"
            )
        ], className="bg-white rounded-lg shadow-md p-6 mb-8"),
        
        # Performance Matrix
        html.Div([
            html.H2("Sales Performance Analysis", 
                   className="text-lg font-semibold mb-4"),
            html.Div([
                # Genre Performance
                html.Div([
                    html.H3("Genre Performance", 
                           className="text-base font-medium mb-3"),
                    dcc.Graph(
                        id='genre-sales',
                        config={'displayModeBar': 'hover'},
                        className="h-96"
                    )
                ], className="bg-white rounded-lg shadow-md p-6"),
                
                # Platform Performance
                html.Div([
                    html.H3("Platform Performance", 
                           className="text-base font-medium mb-3"),
                    dcc.Graph(
                        id='platform-sales',
                        config={'displayModeBar': 'hover'},
                        className="h-96"
                    )
                ], className="bg-white rounded-lg shadow-md p-6")
            ], className="grid grid-cols-1 lg:grid-cols-2 gap-6")
        ], className="mb-8"),
        
        # Top Games Table
        html.Div([
            html.H2("Top Performing Games", 
                   className="text-lg font-semibold mb-4"),
            html.Div(
                id='top-games-table',
                className="overflow-x-auto"
            )
        ], className="bg-white rounded-lg shadow-md p-6")
    ], className="p-6 bg-gray-50 min-h-screen")

@callback(
    [Output('date-range', 'start_date'),
     Output('date-range', 'end_date')],
    Input('date-range-preset', 'value')
)
def update_date_range(preset):
    """Updates date range based on preset selection."""
    end_date = datetime.now()
    if preset == 'all':
        df = load_vgsales_data()
        return datetime(int(df['Year'].min()), 1, 1), datetime(int(df['Year'].max()), 12, 31)
    
    start_date = end_date - timedelta(days=int(preset))
    return start_date, end_date

@callback(
    Output('sales-trends', 'figure'),
    [Input('date-range', 'start_date'),
     Input('date-range', 'end_date'),
     Input('sales-threshold', 'value')]
)
def update_sales_trends(start_date, end_date, threshold):
    """Updates the sales trends visualization."""
    df = load_vgsales_data()
    
    start_year = int(start_date.split('-')[0]) if start_date else df['Year'].min()
    end_year = int(end_date.split('-')[0]) if end_date else df['Year'].max()
    
    mask = (df['Year'] >= start_year) & (df['Year'] <= end_year) & (df['Global_Sales'] >= threshold)
    df_filtered = df[mask]
    
    yearly_sales = df_filtered.groupby('Year').agg({
        'Global_Sales': 'sum',
        'NA_Sales': 'sum',
        'EU_Sales': 'sum',
        'JP_Sales': 'sum',
        'Other_Sales': 'sum'
    }).reset_index()
    
    fig = px.line(yearly_sales,
                  x='Year',
                  y=['Global_Sales', 'NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales'],
                  labels={
                      'value': 'Sales (Millions)',
                      'variable': 'Region'
                  })
    

    fig.update_layout(
        **CHART_THEME['layout'],
        
        title=None,
        xaxis_title="Year",
        yaxis_title="Sales (Millions)",
    )
    
    return fig

@callback(
    Output('regional-distribution', 'figure'),
    [Input('date-range', 'start_date'),
     Input('date-range', 'end_date'),
     Input('sales-threshold', 'value')]
)
def update_regional_distribution(start_date, end_date, threshold):
    """Updates the regional distribution visualization."""
    df = load_vgsales_data()
    
    start_year = int(start_date.split('-')[0]) if start_date else df['Year'].min()
    end_year = int(end_date.split('-')[0]) if end_date else df['Year'].max()
    
    mask = (df['Year'] >= start_year) & (df['Year'] <= end_year) & (df['Global_Sales'] >= threshold)
    df_filtered = df[mask]
    
    regional_totals = pd.DataFrame({
        'Region': ['North America', 'Europe', 'Japan', 'Other'],
        'Sales': [
            df_filtered['NA_Sales'].sum(),
            df_filtered['EU_Sales'].sum(),
            df_filtered['JP_Sales'].sum(),
            df_filtered['Other_Sales'].sum()
        ]
    })
    
    fig = go.Figure(data=[go.Pie(
        labels=regional_totals['Region'],
        values=regional_totals['Sales'],
        hole=.4,
        textinfo='label+percent',
        hovertemplate="%{label}<br>$%{value:.1f}M<extra></extra>"
    )])
    
    fig.update_layout(
        **CHART_THEME['layout'],
        
        title=None
    )
    
    return fig

@callback(
    Output('genre-sales', 'figure'),
    [Input('date-range', 'start_date'),
     Input('date-range', 'end_date'),
     Input('sales-threshold', 'value')]
)
def update_genre_sales(start_date, end_date, threshold):
    """Updates the genre sales visualization."""
    df = load_vgsales_data()
    
    start_year = int(start_date.split('-')[0]) if start_date else df['Year'].min()
    end_year = int(end_date.split('-')[0]) if end_date else df['Year'].max()
    
    mask = (df['Year'] >= start_year) & (df['Year'] <= end_year) & (df['Global_Sales'] >= threshold)
    df_filtered = df[mask]
    
    genre_sales = df_filtered.groupby('Genre')['Global_Sales'].sum().sort_values(ascending=True)
    
    fig = go.Figure(go.Bar(
        x=genre_sales.values,
        y=genre_sales.index,
        orientation='h',
        marker_color=THEME['primary']
    ))
    
    fig.update_layout(
        **CHART_THEME['layout'],
        
        title=None,
        xaxis_title="Global Sales (Millions)",
        yaxis_title=None,
        
    )
    
    return fig

@callback(
    Output('platform-sales', 'figure'),
    [Input('date-range', 'start_date'),
     Input('date-range', 'end_date'),
     Input('sales-threshold', 'value')]
)
def update_platform_sales(start_date, end_date, threshold):
    """Updates the platform sales visualization."""
    df = load_vgsales_data()
    
    start_year = int(start_date.split('-')[0]) if start_date else df['Year'].min()
    end_year = int(end_date.split('-')[0]) if end_date else df['Year'].max()
    
    mask = (df['Year'] >= start_year) & (df['Year'] <= end_year) & (df['Global_Sales'] >= threshold)
    df_filtered = df[mask]
    
    platform_sales = df_filtered.groupby('Platform')['Global_Sales'].sum().sort_values(ascending=True)
    
    fig = go.Figure(go.Bar(
        x=platform_sales.values,
        y=platform_sales.index,
        orientation='h',
        marker_color=THEME['secondary']
    ))
    
    fig.update_layout(
        **CHART_THEME['layout'],
        title=None,
        xaxis_title="Global Sales (Millions)",
        yaxis_title=None,
        
    )
    
    return fig

@callback(
    Output('top-games-table', 'children'),
    [Input('date-range', 'start_date'),
     Input('date-range', 'end_date'),
     Input('sales-threshold', 'value')]
)
def update_top_games_visualization(start_date, end_date, threshold):
    df = load_vgsales_data()
    
    start_year = int(start_date.split('-')[0]) if start_date else df['Year'].min()
    end_year = int(end_date.split('-')[0]) if end_date else df['Year'].max()
    
    mask = (df['Year'] >= start_year) & (df['Year'] <= end_year) & (df['Global_Sales'] >= threshold)
    df_filtered = df[mask]
    
    top_games = df_filtered.nlargest(10, 'Global_Sales')

    # Create scatter plot for circles
    scatter = go.Scatter(
        x=top_games['Global_Sales'],
        y=top_games['Name'],
        mode='markers+text',
        name='Sales',
        marker=dict(
            symbol='circle',
            size=25,
            color=top_games['Global_Sales'],
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(
                title='Sales (M)',
                thickness=20
            ),
            line=dict(width=2, color='white')
        ),
        text=top_games['Global_Sales'].round(1).astype(str) + 'M',
        textposition='middle right',
        hovertemplate="<b>%{y}</b><br>" +
                     "Sales: $%{x:.1f}M<br>" +
                     "<extra></extra>"
    )

    # Create lines connecting to y-axis
    lines = go.Scatter(
        x=[0] * len(top_games) + top_games['Global_Sales'].tolist(),
        y=top_games['Name'].tolist() * 2,
        mode='lines',
        line=dict(color='rgba(128, 128, 128, 0.5)', width=1),
        hoverinfo='none',
        showlegend=False
    )

    # Create figure and add traces
    fig = go.Figure(data=[lines, scatter])

    # Update layout
    layout = dict(CHART_THEME['layout'])
    layout.update({
        'xaxis': dict(
            title='Global Sales (Millions)',
            zeroline=False,
            gridcolor='rgba(128, 128, 128, 0.2)',
            showline=True,
            linewidth=1,
            linecolor='black'
        ),
        'yaxis': dict(
            title=None,
            zeroline=False,
            gridcolor='rgba(128, 128, 128, 0.2)',
            showline=True,
            linewidth=1,
            linecolor='black'
        ),
        'plot_bgcolor': 'white',
        'showlegend': False,
        'title': {
            'text': 'Best Selling Games',
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 24}
        },
        'margin': dict(l=200, r=50, t=50, b=50),
        'height': 600
    })
    
    fig.update_layout(**layout)

    # Add animations
    fig.update_traces(
        marker={
            'size': 25,
            'line': {'width': 2, 'color': 'white'}
        },
        selector={'mode': 'markers+text'}
    )

    return dcc.Graph(
        figure=fig,
        config={'displayModeBar': False}
    )

def get_top_games(df, n=10):
    """Gets the top n games by global sales."""
    return df.nlargest(n, 'Global_Sales')[['Name', 'Platform', 'Publisher', 'Global_Sales', 'Year']]

def create_top_games_table(df):
    """Creates a modern styled HTML table for top games."""
    return html.Table([
        # Header
        html.Thead(
            html.Tr([
                html.Th(col, className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider")
                for col in ['Game', 'Platform', 'Publisher', 'Global Sales', 'Year']
            ], className="bg-gray-50 border-b border-gray-200"),
            className="bg-gray-50"
        ),
        # Body
        html.Tbody([
            html.Tr([
                html.Td(
                    row['Name'],
                    className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900"
                ),
                html.Td(
                    row['Platform'],
                    className="px-6 py-4 whitespace-nowrap text-sm text-gray-500"
                ),
                html.Td(
                    row['Publisher'],
                    className="px-6 py-4 whitespace-nowrap text-sm text-gray-500"
                ),
                html.Td(
                    f"${row['Global_Sales']:.2f}M",
                    className="px-6 py-4 whitespace-nowrap text-sm text-gray-900"
                ),
                html.Td(
                    int(row['Year']),
                    className="px-6 py-4 whitespace-nowrap text-sm text-gray-500"
                )
            ], className="hover:bg-gray-50 transition-colors duration-200")
            for _, row in df.iterrows()
        ], className="bg-white divide-y divide-gray-200")
    ], className="min-w-full divide-y divide-gray-200 shadow-sm rounded-lg overflow-hidden")