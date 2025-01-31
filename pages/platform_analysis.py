# import pandas as pd
# from dash import html, dcc, callback, Input, Output
# import plotly.express as px
# import plotly.graph_objects as go

# from utils.data_loading import load_vgsales_data
# from utils.data_processing import preprocess_platform_data
# from components.cards.stats_card import create_stat_card
# from components.charts.platform_charts import create_platform_timeline, create_platform_timeline
# from utils.constants import COLORS, CHART_TEMPLATE

# def create_platform_analysis_layout():
#     """Creates the layout for the platform analysis page."""
    
#     # Load and preprocess data
#     df = load_vgsales_data()
#     platform_stats = preprocess_platform_data(df)
    
#     layout = html.Div([
#         # Header Section
#         html.Div([
#             html.H1("Gaming Platform Sales Analysis", 
#                    className="text-3xl font-bold mb-4"),
#             html.P("Explore sales performance across different gaming platforms",
#                   className="text-gray-600 mb-8")
#         ], className="mb-8"),
        
#         # Filters and Controls Section
#         html.Div([
#             # Time Period Filter
#             html.Div([
#                 html.Label("Select Time Period:", className="block text-sm font-medium mb-2"),
#                 dcc.RangeSlider(
#                     id='platform-year-range',
#                     min=df['Year'].min(),
#                     max=df['Year'].max(),
#                     value=[df['Year'].min(), df['Year'].max()],
#                     marks={int(year): str(int(year)) 
#                           for year in range(int(df['Year'].min()), int(df['Year'].max()) + 1, 5)},
#                     className="mt-2"
#                 )
#             ], className="w-full md:w-1/2 lg:w-1/3 mb-6"),
            
#             # Platform Selection
#             html.Div([
#                 html.Label("Select Platforms:", className="block text-sm font-medium mb-2"),
#                 dcc.Dropdown(
#                     id='platform-selector',
#                     options=[{'label': platform, 'value': platform} 
#                             for platform in sorted(df['Platform'].unique())],
#                     value=df['Platform'].value_counts().nlargest(5).index.tolist(),
#                     multi=True,
#                     className="mt-2"
#                 )
#             ], className="w-full md:w-1/2 lg:w-1/3 mb-6")
#         ], className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8"),
        
#         # Key Statistics Cards
#         html.Div([
#             create_stat_card(
#                 "Total Platforms",
#                 str(len(platform_stats['unique_platforms'])),
#                 "Number of gaming platforms"
#             ),
#             create_stat_card(
#                 "Best-Selling Platform",
#                 platform_stats['top_platform'],
#                 f"${platform_stats['top_platform_sales']:.2f}M in sales"
#             ),
#             create_stat_card(
#                 "Most Game Releases",
#                 platform_stats['most_releases'],
#                 f"{platform_stats['release_count']} games"
#             )
#         ], className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8"),
        
#         # Platform Performance Charts
#         html.Div([
#             # Market Share Chart
#             html.Div([
#                 html.H2("Platform Market Share", className="text-xl font-semibold mb-4"),
#                 dcc.Graph(
#                     id='platform-market-share',
#                     config={'displayModeBar': False}
#                 )
#             ], className="w-full lg:w-1/2 mb-6"),
            
#             # Sales Timeline
#             html.Div([
#                 html.H2("Platform Sales Timeline", className="text-xl font-semibold mb-4"),
#                 dcc.Graph(
#                     id='platform-sales-timeline',
#                     config={'displayModeBar': False}
#                 )
#             ], className="w-full lg:w-1/2 mb-6")
#         ], className="grid grid-cols-1 lg:grid-cols-2 gap-4 mb-8"),
        
#         # Regional Performance Analysis
#         html.Div([
#             html.H2("Regional Platform Performance", className="text-xl font-semibold mb-4"),
#             html.Div([
#                 dcc.Graph(
#                     id='platform-regional-comparison',
#                     config={'displayModeBar': False}
#                 )
#             ], className="mb-6")
#         ], className="mb-8"),
        
#         # Platform Success Metrics Table
#         html.Div([
#             html.H2("Platform Success Metrics", className="text-xl font-semibold mb-4"),
#             html.Div(id='platform-metrics-table', className="overflow-x-auto")
#         ], className="mb-8")
#     ], className="p-6")
    
#     return layout

# # Callbacks
# @callback(
#     Output('platform-market-share', 'figure'),
#     [Input('platform-year-range', 'value'),
#      Input('platform-selector', 'value')]
# )
# def update_market_share(years, platforms):
#     """Updates the platform market share chart."""
#     df = load_vgsales_data()
    
#     # Filter data
#     mask = (df['Year'] >= years[0]) & (df['Year'] <= years[1])
#     if platforms:
#         mask &= df['Platform'].isin(platforms)
#     df_filtered = df[mask]
    
#     # Calculate market share
#     platform_sales = df_filtered.groupby('Platform')['Global_Sales'].sum().sort_values(ascending=True)
    
#     fig = go.Figure(go.Bar(
#         x=platform_sales.values,
#         y=platform_sales.index,
#         orientation='h',
#         marker_color=COLORS['primary']
#     ))
    
#     fig.update_layout(
#         template=CHART_TEMPLATE,
#         title="Platform Market Share by Global Sales",
#         xaxis_title="Global Sales (Millions)",
#         yaxis_title="Platform",
#         showlegend=False
#     )
    
#     return fig

# @callback(
#     Output('platform-sales-timeline', 'figure'),
#     [Input('platform-year-range', 'value'),
#      Input('platform-selector', 'value')]
# )
# def update_sales_timeline(years, platforms):
#     """Updates the platform sales timeline chart."""
#     df = load_vgsales_data()
    
#     # Filter data
#     mask = (df['Year'] >= years[0]) & (df['Year'] <= years[1])
#     if platforms:
#         mask &= df['Platform'].isin(platforms)
#     df_filtered = df[mask]
    
#     # Calculate yearly sales by platform
#     yearly_sales = df_filtered.groupby(['Year', 'Platform'])['Global_Sales'].sum().reset_index()
    
#     fig = px.line(yearly_sales, 
#                   x='Year', 
#                   y='Global_Sales', 
#                   color='Platform',
#                   title='Yearly Sales Trends by Platform')
    
#     fig.update_layout(
#         template=CHART_TEMPLATE,
#         xaxis_title="Year",
#         yaxis_title="Global Sales (Millions)",
#     )
    
#     return fig

# @callback(
#     Output('platform-regional-comparison', 'figure'),
#     [Input('platform-year-range', 'value'),
#      Input('platform-selector', 'value')]
# )
# def update_regional_comparison(years, platforms):
#     """Updates the regional platform performance chart."""
#     df = load_vgsales_data()
    
#     # Filter data
#     mask = (df['Year'] >= years[0]) & (df['Year'] <= years[1])
#     if platforms:
#         mask &= df['Platform'].isin(platforms)
#     df_filtered = df[mask]
    
#     # Calculate regional sales
#     regions = ['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales']
#     regional_sales = df_filtered.groupby('Platform')[regions].sum()
    
#     # Create stacked bar chart
#     fig = go.Figure()
#     for region in regions:
#         fig.add_trace(go.Bar(
#             name=region.replace('_Sales', ''),
#             x=regional_sales.index,
#             y=regional_sales[region],
#             hovertemplate="%{y:.1f}M"
#         ))
    
#     fig.update_layout(
#         template=CHART_TEMPLATE,
#         title="Regional Sales Distribution by Platform",
#         xaxis_title="Platform",
#         yaxis_title="Sales (Millions)",
#         barmode='stack'
#     )
    
#     return fig

# @callback(
#     Output('platform-metrics-table', 'children'),
#     [Input('platform-year-range', 'value'),
#      Input('platform-selector', 'value')]
# )
# def update_metrics_table(years, platforms):
#     """Updates the platform metrics table."""
#     df = load_vgsales_data()
    
#     # Filter data
#     mask = (df['Year'] >= years[0]) & (df['Year'] <= years[1])
#     if platforms:
#         mask &= df['Platform'].isin(platforms)
#     df_filtered = df[mask]
    
#     # Calculate metrics
#     metrics = calculate_platform_metrics(df_filtered)
    
#     return create_metrics_table(metrics)

# def calculate_platform_metrics(df):
#     """Calculates various success metrics for each platform."""
#     metrics = []
#     for platform in df['Platform'].unique():
#         platform_data = df[df['Platform'] == platform]
        
#         metric = {
#             'Platform': platform,
#             'Total Games': len(platform_data),
#             'Global Sales': f"${platform_data['Global_Sales'].sum():.2f}M",
#             'Avg Sales/Game': f"${platform_data['Global_Sales'].mean():.2f}M",
#             'Top Publisher': platform_data['Publisher'].mode().iloc[0],
#             'Top Genre': platform_data['Genre'].mode().iloc[0],
#             'Peak Year': int(platform_data.groupby('Year')['Global_Sales'].sum().idxmax())
#         }
#         metrics.append(metric)
    
#     return pd.DataFrame(metrics)

# def create_metrics_table(df_metrics):
#     """Creates an HTML table for platform metrics."""
#     return html.Table(
#         # Header
#         [html.Tr([html.Th(col, className="px-4 py-2 bg-gray-100") 
#                  for col in df_metrics.columns])] +
#         # Body
#         [html.Tr([
#             html.Td(df_metrics.iloc[i][col], className="px-4 py-2 border")
#             for col in df_metrics.columns
#         ]) for i in range(len(df_metrics))],
#         className="min-w-full border-collapse border"
#     )

import pandas as pd
from dash import html, dcc, callback, Input, Output
import plotly.express as px
import plotly.graph_objects as go
from components.charts.platform_charts import (
    create_platform_sales_chart,
    create_platform_timeline,
    create_platform_genre_distribution,
    create_platform_regional_share,
    create_top_games_by_platform,
    create_platform_stats_card
)
from utils.data_loading import load_vgsales_data
from utils.data_processing import preprocess_platform_data
from utils.constants import COLORS, CHART_TEMPLATE

def create_modern_year_range(df):
    min_year = int(df['Year'].min())
    max_year = int(df['Year'].max())
    years = list(range(min_year, max_year + 1))
    
    return html.Div([
        html.Div([
            html.H3("Time Period", className="text-lg font-medium text-gray-900"),
            html.Div(id='selected-years', className="text-sm font-medium text-blue-600")
        ], className="flex justify-between items-center mb-3"),
        html.Div([
            html.Div([
                dcc.Dropdown(
                    id='year-start',
                    options=[{'label': str(year), 'value': year} for year in years],
                    value=min_year,
                    clearable=False,
                    placeholder="Start Year",
                    style={
                        'borderRadius': '8px', 
                        'border': '1px solid #E5E7EB',
                        'width': '120px'
                    }
                )
            ], className="w-1/3"),
            html.Span("to", className="mx-2 text-gray-500"),
            html.Div([
                dcc.Dropdown(
                    id='year-end',
                    options=[{'label': str(year), 'value': year} for year in years],
                    value=max_year,
                    clearable=False,
                    placeholder="End Year",
                    style={
                        'borderRadius': '8px', 
                        'border': '1px solid #E5E7EB',
                        'width': '120px'
                    }
                )
            ], className="w-1/3")
        ], className="flex items-center")
    ], className="bg-white rounded-xl shadow-sm p-4 border border-gray-100")

def create_platform_analysis_layout():
    df = load_vgsales_data()
    platform_stats = preprocess_platform_data(df)
    
    return html.Div([
        # Header with reduced spacing
        html.Div([
            html.H1("Gaming Platform Analysis", 
                    className="text-2xl font-bold text-gray-900"),
            html.P("Comprehensive analysis of gaming platform performance and trends",
                  className="mt-1 text-sm text-gray-600")
        ], className="mb-4"),

        # Filters with compact layout
        html.Div([
            html.Div(create_modern_year_range(df), className="col-span-1"),
            html.Div([
                html.H3("Select Platforms", className="text-lg font-medium text-gray-900 mb-2"),
                dcc.Dropdown(
                    id='platform-selector',
                    options=[{'label': p, 'value': p} for p in sorted(df['Platform'].unique())],
                    value=df['Platform'].value_counts().nlargest(5).index.tolist(),
                    multi=True,
                    placeholder="Choose platforms...",
                    className="basic-multi-select",
                    style={
                        'borderRadius': '8px', 
                        'border': '1px solid #E5E7EB',
                        'minWidth': '200px'
                    }
                )
            ], className="bg-white rounded-xl shadow-sm p-4 border border-gray-100")
        ], className="grid grid-cols-2 gap-4 mb-4"),

        # Statistics Card with reduced padding
        html.Div(
            create_platform_stats_card(df),
            className="bg-white rounded-xl shadow-sm p-4 border border-gray-100 mb-4"
        ),

        # Charts Grid with consistent spacing
        html.Div([
            html.Div([
                html.H3("Global Sales by Platform", 
                        className="text-lg font-medium text-gray-900 mb-2"),
                html.Div(id='platform-sales-chart')
            ], className="bg-white rounded-xl shadow-sm p-4 border border-gray-100 mb-4"),

            html.Div([
                html.H3("Historical Sales Trends", 
                        className="text-lg font-medium text-gray-900 mb-2"),
                html.Div(id='platform-timeline')
            ], className="bg-white rounded-xl shadow-sm p-4 border border-gray-100 mb-4"),

            html.Div([
                html.Div([
                    html.H3("Genre Distribution", 
                            className="text-lg font-medium text-gray-900 mb-2"),
                    html.Div(id='genre-distribution')
                ], className="bg-white rounded-xl shadow-sm p-4 border border-gray-100"),
                html.Div([
                    html.H3("Regional Performance", 
                            className="text-lg font-medium text-gray-900 mb-2"),
                    html.Div(id='regional-share')
                ], className="bg-white rounded-xl shadow-sm p-4 border border-gray-100")
            ], className="grid grid-cols-2 gap-4 mb-4"),

            html.Div([
                html.H3("Top Performing Games", 
                        className="text-lg font-medium text-gray-900 mb-2"),
                html.Div(id='top-games-container')
            ], className="bg-white rounded-xl shadow-sm p-4 border border-gray-100")
        ])
    ], className="min-h-screen bg-gray-50 p-4")

@callback(
    Output('selected-years', 'children'),
    [Input('year-start', 'value'),
     Input('year-end', 'value')]
)
def update_selected_years(start_year, end_year):
    if start_year and end_year:
        return f"{start_year} - {end_year}"
    return ""

@callback(
    Output('year-end', 'options'),
    [Input('year-start', 'value')]
)
def update_end_year_options(start_year):
    df = load_vgsales_data()
    max_year = int(df['Year'].max())
    if start_year:
        return [{'label': str(year), 'value': year} 
                for year in range(start_year, max_year + 1)]
    return []

@callback(
    [Output('platform-sales-chart', 'children'),
     Output('platform-timeline', 'children'),
     Output('genre-distribution', 'children'),
     Output('regional-share', 'children')],
    [Input('year-start', 'value'),
     Input('year-end', 'value'),
     Input('platform-selector', 'value')]
)
def update_charts(start_year, end_year, selected_platforms):
    df = load_vgsales_data()
    
    # Filter data based on selection
    mask = (df['Year'] >= start_year) & (df['Year'] <= end_year)
    if selected_platforms:
        mask &= df['Platform'].isin(selected_platforms)
    filtered_df = df[mask]
    
    return [
        create_platform_sales_chart(filtered_df),
        create_platform_timeline(filtered_df),
        create_platform_genre_distribution(filtered_df),
        create_platform_regional_share(filtered_df)
    ]

@callback(
    Output('top-games-container', 'children'),
    [Input('platform-selector', 'value'),
     Input('year-start', 'value'),
     Input('year-end', 'value')]
)
def update_top_games(selected_platforms, start_year, end_year):
    if not selected_platforms:
        return html.Div("Select platforms to view their top games", 
                       className="text-gray-600 text-center py-4")
    
    df = load_vgsales_data()
    mask = (df['Year'] >= start_year) & (df['Year'] <= end_year)
    filtered_df = df[mask]
    
    return html.Div([
        create_top_games_by_platform(filtered_df, platform)
        for platform in selected_platforms[:3]
    ], className="grid grid-cols-1 gap-6")