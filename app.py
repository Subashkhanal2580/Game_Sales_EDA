# """
# Main application file for the Video Game Sales Dashboard.
# Integrates all components and sets up the dashboard structure.
# """

# import dash
# from dash import html, dcc
# import dash_bootstrap_components as dbc
# from dash.dependencies import Input, Output, State
# import pandas as pd
# import logging
# from pathlib import Path

# # Import our utility modules
# from utils.data_loading import load_vgsales_data, DataLoadingError
# from utils.data_processing import (
#     clean_dataset,
#     calculate_market_share,
#     analyze_time_trends,
#     calculate_regional_distribution,
#     get_top_performers
# )
# from components.charts.dashboard_charts import (
#     create_sales_trend_chart,
#     create_regional_distribution_chart,
#     create_genre_distribution_chart,
#     create_platform_share_chart,
#     create_top_games_table
# )
# from utils.constants import (
#     COLOR_SCHEMES,
#     LAYOUT,
#     TIME_PERIODS,
#     REGIONS,
#     TEXT_CONTENT
# )

# # Configure logging
# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
# )
# logger = logging.getLogger(__name__)

# # Initialize the Dash app
# app = dash.Dash(
#     __name__,
#     external_stylesheets=[dbc.themes.BOOTSTRAP],
#     suppress_callback_exceptions=True
# )
# server = app.server

# # Load and process data
# try:
#     df = load_vgsales_data()
#     df_clean = clean_dataset(df)
#     logger.info("Data loaded and cleaned successfully")
# except DataLoadingError as e:
#     logger.error(f"Error loading data: {e}")
#     df_clean = pd.DataFrame()

# # Create header component
# def create_header():
#     """Create the dashboard header."""
#     return dbc.Navbar(
#         dbc.Container([
#             html.A(
#                 dbc.Row([
#                     dbc.Col(html.Img(src="/assets/logo.png", height="30px")),
#                     dbc.Col(dbc.NavbarBrand("Video Game Sales Dashboard")),
#                 ]),
#                 href="/",
#                 style={"textDecoration": "none"},
#             )
#         ]),
#         color="dark",
#         dark=True,
#         className="mb-4"
#     )

# # Modify the create_sidebar function
# def create_sidebar():
#     """Create the sidebar with filter controls."""
#     return html.Div([
#         html.H4("Filters", className="mb-3"),
        
#         html.H6("Time Period"),
#         dcc.Dropdown(
#             id='time-filter',
#             options=[
#                 {'label': v, 'value': k}
#                 for k, v in TIME_PERIODS.items()
#                 if isinstance(v, str)
#             ],
#             value='all_time',
#             clearable=False,
#             className="mb-3"
#         ),
        
#         html.H6("Platform"),
#         dcc.Dropdown(
#             id='platform-filter',
#             options=[
#                 {'label': platform, 'value': platform}
#                 for platform in sorted(df_clean['Platform'].dropna().unique())
#             ],
#             multi=True,
#             className="mb-3"
#         ),
        
#         html.H6("Genre"),
#         dcc.Dropdown(
#             id='genre-filter',
#             options=[
#                 {'label': genre, 'value': genre}
#                 for genre in sorted(df_clean['Genre'].dropna().unique())
#             ],
#             multi=True,
#             className="mb-3"
#         ),
        
#         html.H6("Publisher"),
#         dcc.Dropdown(
#             id='publisher-filter',
#             options=[
#                 {'label': pub, 'value': pub}
#                 for pub in sorted(df_clean['Publisher'].dropna().unique())
#             ],
#             multi=True,
#             className="mb-3"
#         ),
        
#         html.Hr(),
        
#         dbc.Button(
#             "Reset Filters",
#             id="reset-filters-button",
#             color="secondary",
#             className="w-100"
#         ),
#     ], style={
#         'padding': '20px',
#         'backgroundColor': '#f8f9fa',
#         'borderRadius': '5px'
#     })

# # Create main content layout
# def create_main_content():
#     """Create the main content area with charts and stats."""
#     return html.Div([
#         dbc.Row([
#             dbc.Col([
#                 dbc.Card([
#                     dbc.CardHeader("Total Global Sales"),
#                     dbc.CardBody([
#                         html.H3(id="total-sales-value"),
#                         html.P("Million Units", className="text-muted")
#                     ])
#                 ])
#             ], width=3),
#             dbc.Col([
#                 dbc.Card([
#                     dbc.CardHeader("Top Genre"),
#                     dbc.CardBody([
#                         html.H3(id="top-genre-value"),
#                         html.P("By Sales Volume", className="text-muted")
#                     ])
#                 ])
#             ], width=3),
#             dbc.Col([
#                 dbc.Card([
#                     dbc.CardHeader("Top Platform"),
#                     dbc.CardBody([
#                         html.H3(id="top-platform-value"),
#                         html.P("By Sales Volume", className="text-muted")
#                     ])
#                 ])
#             ], width=3),
#             dbc.Col([
#                 dbc.Card([
#                     dbc.CardHeader("Total Games"),
#                     dbc.CardBody([
#                         html.H3(id="total-games-value"),
#                         html.P("In Selected Period", className="text-muted")
#                     ])
#                 ])
#             ], width=3),
#         ], className="mb-4"),
        
#         dbc.Row([
#             dbc.Col([
#                 dbc.Card([
#                     dbc.CardHeader("Sales Trends Over Time"),
#                     dbc.CardBody([
#                         dcc.Graph(id="sales-trend-chart")
#                     ])
#                 ])
#             ], width=8),
#             dbc.Col([
#                 dbc.Card([
#                     dbc.CardHeader("Regional Distribution"),
#                     dbc.CardBody([
#                         dcc.Graph(id="regional-distribution-chart")
#                     ])
#                 ])
#             ], width=4),
#         ], className="mb-4"),
        
#         dbc.Row([
#             dbc.Col([
#                 dbc.Card([
#                     dbc.CardHeader("Genre Distribution"),
#                     dbc.CardBody([
#                         dcc.Graph(id="genre-distribution-chart")
#                     ])
#                 ])
#             ], width=6),
#             dbc.Col([
#                 dbc.Card([
#                     dbc.CardHeader("Platform Market Share"),
#                     dbc.CardBody([
#                         dcc.Graph(id="platform-share-chart")
#                     ])
#                 ])
#             ], width=6),
#         ], className="mb-4"),
        
#         dbc.Row([
#             dbc.Col([
#                 dbc.Card([
#                     dbc.CardHeader("Top Games"),
#                     dbc.CardBody([
#                         dbc.Table(id="top-games-table")
#                     ])
#                 ])
#             ], width=12),
#         ]),
#     ])

# # Define the main layout
# app.layout = html.Div([
#     create_header(),
#     dbc.Container([
#         dbc.Row([
#             dbc.Col(create_sidebar(), width=3),
#             dbc.Col(create_main_content(), width=9),
#         ]),
#     ], fluid=True)
# ])

# # Callback for resetting filters
# @app.callback(
#     [Output('time-filter', 'value'),
#      Output('platform-filter', 'value'),
#      Output('genre-filter', 'value'),
#      Output('publisher-filter', 'value')],
#     [Input('reset-filters-button', 'n_clicks')]
# )
# def reset_filters(n_clicks):
#     if n_clicks is None:
#         raise dash.exceptions.PreventUpdate
#     return 'all_time', [], [], []

# # Callback for filtering data
# def filter_dashboard_data(df, time_filter, platforms, genres, publishers):
#     """Filter data based on user selections."""
#     filtered_df = df.copy()
    
#     # Apply time filter
#     if time_filter in TIME_PERIODS['by_decade']:
#         start_year, end_year = TIME_PERIODS['by_decade'][time_filter]
#         filtered_df = filtered_df[
#             (filtered_df['Year'] >= start_year) & 
#             (filtered_df['Year'] <= end_year)
#         ]
#     elif time_filter == 'last_5_years':
#         max_year = filtered_df['Year'].max()
#         filtered_df = filtered_df[filtered_df['Year'] >= max_year - 5]
#     elif time_filter == 'last_10_years':
#         max_year = filtered_df['Year'].max()
#         filtered_df = filtered_df[filtered_df['Year'] >= max_year - 10]
#     elif time_filter == 'last_20_years':
#         max_year = filtered_df['Year'].max()
#         filtered_df = filtered_df[filtered_df['Year'] >= max_year - 20]
    
#     # Apply other filters
#     if platforms:
#         filtered_df = filtered_df[filtered_df['Platform'].isin(platforms)]
#     if genres:
#         filtered_df = filtered_df[filtered_df['Genre'].isin(genres)]
#     if publishers:
#         filtered_df = filtered_df[filtered_df['Publisher'].isin(publishers)]
    
#     return filtered_df

# # Callback to update all charts
# @app.callback(
#     [Output('total-sales-value', 'children'),
#      Output('top-genre-value', 'children'),
#      Output('top-platform-value', 'children'),
#      Output('total-games-value', 'children'),
#      Output('sales-trend-chart', 'figure'),
#      Output('regional-distribution-chart', 'figure'),
#      Output('genre-distribution-chart', 'figure'),
#      Output('platform-share-chart', 'figure'),
#      Output('top-games-table', 'children')],
#     [Input('time-filter', 'value'),
#      Input('platform-filter', 'value'),
#      Input('genre-filter', 'value'),
#      Input('publisher-filter', 'value')]
# )
# def update_dashboard(time_filter, platforms, genres, publishers):
#     """Update all dashboard components based on filters."""
#     # Filter data
#     filtered_df = filter_dashboard_data(df_clean, time_filter, platforms, genres, publishers)
    
#     # Calculate metrics
#     total_sales = f"{filtered_df['Global_Sales'].sum():.1f}"
#     top_genre = filtered_df.groupby('Genre')['Global_Sales'].sum().idxmax()
#     top_platform = filtered_df.groupby('Platform')['Global_Sales'].sum().idxmax()
#     total_games = str(len(filtered_df))
    
#     # Create charts (implement these in chart_configs.py)
#     sales_trend = create_sales_trend_chart(filtered_df)
#     regional_dist = create_regional_distribution_chart(filtered_df)
#     genre_dist = create_genre_distribution_chart(filtered_df)
#     platform_share = create_platform_share_chart(filtered_df)
    
#     # Create top games table
#     top_games_table = create_top_games_table(filtered_df)
    
#     return (
#         total_sales,
#         top_genre,
#         top_platform,
#         total_games,
#         sales_trend,
#         regional_dist,
#         genre_dist,
#         platform_share,
#         top_games_table
#     )

# if __name__ == '__main__':
#     app.run_server(debug=True)

# """
# Main application file for the Video Game Sales Dashboard.
# Integrates all components and sets up the dashboard structure.
# """

# import dash
# from dash import html, dcc
# import dash_bootstrap_components as dbc
# from dash.dependencies import Input, Output, State
# import pandas as pd
# import logging
# from pathlib import Path
# from utils.logging_setup import setup_logging

# # Import our utility modules
# from utils.data_loading import load_vgsales_data, DataLoadingError
# from utils.data_processing import (
#     clean_dataset,
#     calculate_market_share,
#     analyze_time_trends,
#     calculate_regional_distribution,
#     get_top_performers
# )

# # Import page modules
# from pages import (
#     overview,
#     sales_analysis,
#     genre_analysis,
#     platform_analysis,
#     publisher_analysis,
#     log_viewer
# )

# # Configure logging
# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
# )
# logger = setup_logging()

# # Initialize the Dash app
# app = dash.Dash(
#     __name__,
#     external_stylesheets=[
#         dbc.themes.BOOTSTRAP,
#         'https://use.fontawesome.com/releases/v5.15.4/css/all.css'
#     ],
#     suppress_callback_exceptions=True
# )
# server = app.server

# # Load and process data
# try:
#     df = load_vgsales_data()
#     df_clean = clean_dataset(df)
#     logger.info("Data loaded and cleaned successfully")
# except DataLoadingError as e:
#     logger.error(f"Error loading data: {e}")
#     df_clean = pd.DataFrame()

# # Create header component
# def create_header():
#     """Create the dashboard header."""
#     return dbc.Navbar(
#         dbc.Container([
#             # Logo and Brand
#             dbc.Row([
#                 dbc.Col(html.I(className="fas fa-gamepad fa-2x text-white"), width="auto"),
#                 dbc.Col(dbc.NavbarBrand("Video Game Sales Dashboard", className="ms-2")),
#             ], align="center"),
            
#             # Navigation Links
#             dbc.Nav([
#                 dbc.NavItem(dbc.NavLink("Overview", href="/", active="exact")),
#                 dbc.NavItem(dbc.NavLink("Sales Analysis", href="/sales", active="exact")),
#                 dbc.NavItem(dbc.NavLink("Genre Analysis", href="/genre", active="exact")),
#                 dbc.NavItem(dbc.NavLink("Platform Analysis", href="/platform", active="exact")),
#                 dbc.NavItem(dbc.NavLink("Publisher Analysis", href="/publisher", active="exact")),
#                 dbc.NavItem(dbc.NavLink("Logs", href="/logs", active="exact")),
#             ], navbar=True),
#         ]),
#         color="dark",
#         dark=True,
#         className="mb-4"
#     )

# # Create sidebar component
# def create_sidebar():
#     """Create the sidebar with filter controls."""
#     return html.Div([
#         html.H4("Filters", className="mb-3"),
        
#         # Year Range Selector
#         html.Div([
#             html.H6("Time Period", className="mb-2"),
#             dcc.RangeSlider(
#                 id='year-range-slider',
#                 min=int(df_clean['Year'].min()),
#                 max=int(df_clean['Year'].max()),
#                 value=[int(df_clean['Year'].min()), int(df_clean['Year'].max())],
#                 marks={str(year): str(year) 
#                        for year in range(int(df_clean['Year'].min()), 
#                                       int(df_clean['Year'].max()) + 1, 5)},
#                 className="mb-4"
#             ),
#         ]),
        
#         # Platform Filter
#         html.Div([
#             html.H6("Platform", className="mb-2"),
#             dcc.Dropdown(
#                 id='platform-filter',
#                 options=[
#                     {'label': platform, 'value': platform}
#                     for platform in sorted(df_clean['Platform'].unique())
#                 ],
#                 multi=True,
#                 placeholder="Select platforms...",
#                 className="mb-4"
#             ),
#         ]),
        
#         # Genre Filter
#         html.Div([
#             html.H6("Genre", className="mb-2"),
#             dcc.Dropdown(
#                 id='genre-filter',
#                 options=[
#                     {'label': genre, 'value': genre}
#                     for genre in sorted(df_clean['Genre'].unique())
#                 ],
#                 multi=True,
#                 placeholder="Select genres...",
#                 className="mb-4"
#             ),
#         ]),
        
#         # Publisher Filter
#         html.Div([
#             html.H6("Publisher", className="mb-2"),
#             dcc.Dropdown(
#                 id='publisher-filter',
#                 options=[
#                     {'label': pub, 'value': pub}
#                     for pub in sorted(df_clean['Publisher'].unique())
#                 ],
#                 multi=True,
#                 placeholder="Select publishers...",
#                 className="mb-4"
#             ),
#         ]),
        
#         # Reset Filters Button
#         dbc.Button(
#             "Reset Filters",
#             id="reset-filters-button",
#             color="secondary",
#             className="w-100 mt-3"
#         ),
#     ], className="bg-light p-4 h-100")

# # Define the main layout
# app.layout = html.Div([
#     # Store components for sharing data between callbacks
#     dcc.Store(id='filtered-data-store'),
#     dcc.Location(id='url', refresh=False),
    
#     # Header
#     create_header(),
    
#     # Main content area
#     dbc.Container([
#         dbc.Row([
#             # Sidebar
#             dbc.Col(create_sidebar(), width=3, className="mb-4"),
            
#             # Main content
#             dbc.Col([
#                 html.Div(id='page-content')
#             ], width=9)
#         ])
#     ], fluid=True)
# ])

# # Callback for page routing
# @app.callback(
#     Output('page-content', 'children'),
#     Input('url', 'pathname')
# )
# def display_page(pathname):
#     """Route to the appropriate page based on URL pathname."""
#     if pathname == '/' or pathname == '/overview':
#         return overview.create_overview_layout()
#     elif pathname == '/sales':
#         return sales_analysis.create_sales_analysis_layout()
#     elif pathname == '/genre':
#         return genre_analysis.create_genre_analysis_layout()
#     elif pathname == '/platform':
#         return platform_analysis.create_platform_analysis_layout()
#     elif pathname == '/publisher':
#         return publisher_analysis.create_publisher_analysis_layout()
#     elif pathname == '/logs':  # Add this case
#         return log_viewer.create_log_viewer_layout()
#     else:
#         return overview.create_overview_layout()  # Default to overview

# # Callback for resetting filters
# @app.callback(
#     [Output('year-range-slider', 'value'),
#      Output('platform-filter', 'value'),
#      Output('genre-filter', 'value'),
#      Output('publisher-filter', 'value')],
#     Input('reset-filters-button', 'n_clicks'),
#     prevent_initial_call=True
# )
# def reset_filters(n_clicks):
#     """Reset all filters to their default values."""
#     return (
#         [int(df_clean['Year'].min()), int(df_clean['Year'].max())],
#         [],  # Reset platform filter
#         [],  # Reset genre filter
#         []   # Reset publisher filter
#     )

# # Callback for updating filtered data
# @app.callback(
#     Output('filtered-data-store', 'data'),
#     [Input('year-range-slider', 'value'),
#      Input('platform-filter', 'value'),
#      Input('genre-filter', 'value'),
#      Input('publisher-filter', 'value')]
# )
# def update_filtered_data(years, platforms, genres, publishers):
#     """Update the filtered dataset based on selected filters."""
#     filtered_df = df_clean.copy()
    
#     # Apply year filter
#     if years:
#         filtered_df = filtered_df[
#             (filtered_df['Year'] >= years[0]) & 
#             (filtered_df['Year'] <= years[1])
#         ]
    
#     # Apply platform filter
#     if platforms:
#         filtered_df = filtered_df[filtered_df['Platform'].isin(platforms)]
    
#     # Apply genre filter
#     if genres:
#         filtered_df = filtered_df[filtered_df['Genre'].isin(genres)]
    
#     # Apply publisher filter
#     if publishers:
#         filtered_df = filtered_df[filtered_df['Publisher'].isin(publishers)]
    
#     return filtered_df.to_dict('records')

# if __name__ == '__main__':
#     app.run_server(debug=True)

"""
Main application file for the Video Game Sales Dashboard.
Integrates all components and sets up the dashboard structure.
"""

import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import pandas as pd
import logging
from pathlib import Path
from utils.logging_setup import setup_logging

# Import our utility modules
from utils.data_loading import load_vgsales_data, DataLoadingError
from utils.data_processing import (
    clean_dataset,
    calculate_market_share,
    analyze_time_trends,
    calculate_regional_distribution,
    get_top_performers
)

# Import page modules
from pages import (
    overview,
    sales_analysis,
    genre_analysis,
    platform_analysis,
    publisher_analysis,
    log_viewer
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = setup_logging()

# Initialize the Dash app
app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        'https://use.fontawesome.com/releases/v5.15.4/css/all.css'
    ],
    suppress_callback_exceptions=True
)
server = app.server

# Load and process data
try:
    df = load_vgsales_data()
    print("Raw data shape:", df.shape)
    df_clean = clean_dataset(df)
    print("Cleaned data shape:", df_clean.shape)
    print("Sample data:", df_clean.head())
    logger.info("Data loaded and cleaned successfully")
except DataLoadingError as e:
    logger.error(f"Error loading data: {e}")
    print("Error occurred while loading data:", str(e))
    df_clean = pd.DataFrame()

def create_header():
    """Create the dashboard header."""
    return dbc.Navbar(
        dbc.Container([
            # Logo and Brand
            dbc.Row([
                dbc.Col(html.I(className="fas fa-gamepad fa-2x text-white"), width="auto"),
                dbc.Col(dbc.NavbarBrand("Video Game Sales Dashboard", className="ms-2")),
            ], align="center"),
            
            # Navigation Links
            dbc.Nav([
                dbc.NavItem(dbc.NavLink("Overview", href="/", active="exact")),
                dbc.NavItem(dbc.NavLink("Sales Analysis", href="/sales", active="exact")),
                dbc.NavItem(dbc.NavLink("Genre Analysis", href="/genre", active="exact")),
                dbc.NavItem(dbc.NavLink("Platform Analysis", href="/platform", active="exact")),
                dbc.NavItem(dbc.NavLink("Publisher Analysis", href="/publisher", active="exact")),
                dbc.NavItem(dbc.NavLink("Logs", href="/logs", active="exact")),
            ], navbar=True),
        ]),
        color="dark",
        dark=True,
        className="mb-4"
    )

# def create_sidebar():
#     """Create the sidebar with filter controls."""
#     return html.Div([
#         html.H4("Filters", className="mb-3"),
        
#         # Modern Year Range Selector
#         html.Div([
#             html.H6("Time Period", className="mb-2"),
#             dbc.Row([
#                 dbc.Col([
#                     html.Label("From", className="text-muted small"),
#                     dcc.Dropdown(
#                         id='year-start',
#                         options=[{'label': str(int(year)), 'value': int(year)} 
#                                 for year in sorted(df_clean['Year'].unique())],
#                         value=int(df_clean['Year'].min()),
#                         clearable=False,
#                         className="mb-2"
#                     )
#                 ], width=6),
#                 dbc.Col([
#                     html.Label("To", className="text-muted small"),
#                     dcc.Dropdown(
#                         id='year-end',
#                         options=[{'label': str(int(year)), 'value': int(year)} 
#                                 for year in sorted(df_clean['Year'].unique())],
#                         value=int(df_clean['Year'].max()),
#                         clearable=False,
#                         className="mb-2"
#                     )
#                 ], width=6)
#             ])
#         ], className="mb-4"),
        
#         # Platform Filter
#         html.Div([
#             html.H6("Platform", className="mb-2"),
#             dcc.Dropdown(
#                 id='platform-filter',
#                 options=[
#                     {'label': platform, 'value': platform}
#                     for platform in sorted(df_clean['Platform'].unique())
#                 ],
#                 multi=True,
#                 placeholder="Select platforms...",
#                 className="mb-4"
#             ),
#         ]),
        
#         # Genre Filter
#         html.Div([
#             html.H6("Genre", className="mb-2"),
#             dcc.Dropdown(
#                 id='genre-filter',
#                 options=[
#                     {'label': genre, 'value': genre}
#                     for genre in sorted(df_clean['Genre'].unique())
#                 ],
#                 multi=True,
#                 placeholder="Select genres...",
#                 className="mb-4"
#             ),
#         ]),
        
#         # Publisher Filter
#         html.Div([
#             html.H6("Publisher", className="mb-2"),
#             dcc.Dropdown(
#                 id='publisher-filter',
#                 options=[
#                     {'label': pub, 'value': pub}
#                     for pub in sorted(df_clean['Publisher'].unique())
#                 ],
#                 multi=True,
#                 placeholder="Select publishers...",
#                 className="mb-4"
#             ),
#         ]),
        
#         # Reset Filters Button
#         dbc.Button(
#             "Reset Filters",
#             id="reset-filters-button",
#             color="secondary",
#             className="w-100 mt-3"
#         ),
#     ], className="bg-light p-4 h-100")

# Define the main layout
app.layout = html.Div([
    # Store components for sharing data between callbacks
    dcc.Store(id='filtered-data-store'),
    dcc.Location(id='url', refresh=False),
    
    # Header
    create_header(),
    
    # Main content area
    dbc.Container([
        dbc.Row([
            # # Sidebar
            # dbc.Col(create_sidebar(), width=3, className="mb-4"),
            
            # Main content
            dbc.Col([
                html.Div(id='page-content')
            ], width=12)
        ])
    ], fluid=True)
])

# Callback for page routing
@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    """Route to the appropriate page based on URL pathname."""
    if pathname == '/' or pathname == '/overview':
        return overview.create_overview_layout()
    elif pathname == '/sales':
        return sales_analysis.create_sales_analysis_layout()
    elif pathname == '/genre':
        return genre_analysis.create_genre_analysis_layout()
    elif pathname == '/platform':
        return platform_analysis.create_platform_analysis_layout()
    elif pathname == '/publisher':
        return publisher_analysis.create_publisher_analysis_layout()
    elif pathname == '/logs':
        return log_viewer.create_log_viewer_layout()
    else:
        return overview.create_overview_layout()

# # Callback for resetting filters
# @app.callback(
#     [Output('year-start', 'value'),
#      Output('year-end', 'value'),
#      Output('platform-filter', 'value'),
#      Output('genre-filter', 'value'),
#      Output('publisher-filter', 'value')],
#     Input('reset-filters-button', 'n_clicks'),
#     prevent_initial_call=True
# )
# def reset_filters(n_clicks):
#     """Reset all filters to their default values."""
#     if n_clicks is None:
#         raise dash.exceptions.PreventUpdate
        
#     logger.debug("Resetting filters")
#     return (
#         int(df_clean['Year'].min()),
#         int(df_clean['Year'].max()),
#         [],
#         [],
#         []
#     )

# # Callback for updating filtered data
# @app.callback(
#     Output('filtered-data-store', 'data'),
#     [Input('year-start', 'value'),
#      Input('year-end', 'value'),
#      Input('platform-filter', 'value'),
#      Input('genre-filter', 'value'),
#      Input('publisher-filter', 'value')]
# )
# def update_filtered_data(year_start, year_end, platforms, genres, publishers):
#     """Update the filtered dataset based on selected filters."""
#     filtered_df = df_clean.copy()
    
#     logger.debug(f"Filtering with: years={year_start}-{year_end}, platforms={platforms}, genres={genres}, publishers={publishers}")
    
#     # Apply filters
#     if year_start and year_end:
#         filtered_df = filtered_df[
#             (filtered_df['Year'] >= year_start) & 
#             (filtered_df['Year'] <= year_end)
#         ]
    
#     if platforms:
#         filtered_df = filtered_df[filtered_df['Platform'].isin(platforms)]
    
#     if genres:
#         filtered_df = filtered_df[filtered_df['Genre'].isin(genres)]
    
#     if publishers:
#         filtered_df = filtered_df[filtered_df['Publisher'].isin(publishers)]
    
#     logger.debug(f"Filtered data shape: {filtered_df.shape}")
#     return filtered_df.to_dict('records')

if __name__ == '__main__':
    app.run_server(debug=True)