# import pandas as pd
# from dash import html, dcc, callback, Input, Output
# import plotly.express as px
# import plotly.graph_objects as go

# from utils.data_loading import load_vgsales_data
# from utils.data_processing import preprocess_publisher_data
# from components.cards.stats_card import create_stat_card
# from components.charts.publisher_charts import  create_publisher_timeline
# from utils.constants import COLORS, CHART_TEMPLATE

# def create_publisher_analysis_layout():
#     """Creates the layout for the publisher analysis page."""
    
#     # Load and preprocess data
#     df = load_vgsales_data()
#     publisher_stats = preprocess_publisher_data(df)
    
#     layout = html.Div([
#         # Header Section
#         html.Div([
#             html.H1("Game Publisher Performance Analysis", 
#                    className="text-3xl font-bold mb-4"),
#             html.P("Analyze sales performance and market presence of game publishers",
#                   className="text-gray-600 mb-8")
#         ], className="mb-8"),
        
#         # Filters Section
#         html.Div([
#             # Time Period Filter
#             html.Div([
#                 html.Label("Time Period:", className="block text-sm font-medium mb-2"),
#                 dcc.RangeSlider(
#                     id='publisher-year-range',
#                     min=df['Year'].min(),
#                     max=df['Year'].max(),
#                     value=[df['Year'].min(), df['Year'].max()],
#                     marks={int(year): str(int(year)) 
#                           for year in range(int(df['Year'].min()), int(df['Year'].max()) + 1, 5)},
#                     className="mt-2"
#                 )
#             ], className="w-full md:w-1/2 mb-6"),
            
#             # Publisher Selection
#             html.Div([
#                 html.Label("Select Publishers:", className="block text-sm font-medium mb-2"),
#                 dcc.Dropdown(
#                     id='publisher-selector',
#                     options=[{'label': pub, 'value': pub} 
#                             for pub in sorted(df['Publisher'].unique())],
#                     value=df['Publisher'].value_counts().nlargest(10).index.tolist(),
#                     multi=True,
#                     className="mt-2"
#                 )
#             ], className="w-full md:w-1/2 mb-6")
#         ], className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8"),
        
#         # Key Metrics Cards
#         html.Div([
#             create_stat_card(
#                 "Total Publishers",
#                 str(len(publisher_stats['unique_publishers'])),
#                 "Active game publishers"
#             ),
#             create_stat_card(
#                 "Market Leader",
#                 publisher_stats['top_publisher'],
#                 f"${publisher_stats['top_publisher_sales']:.2f}M in sales"
#             ),
#             create_stat_card(
#                 "Most Prolific",
#                 publisher_stats['most_games'],
#                 f"{publisher_stats['game_count']} games released"
#             )
#         ], className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8"),
        
#         # Market Share Analysis
#         html.Div([
#             html.H2("Publisher Market Share Analysis", className="text-xl font-semibold mb-4"),
#             dcc.Graph(
#                 id='publisher-market-share',
#                 config={'displayModeBar': False}
#             )
#         ], className="mb-8"),
        
#         # Publisher Performance Over Time
#         html.Div([
#             html.H2("Sales Performance Timeline", className="text-xl font-semibold mb-4"),
#             dcc.Graph(
#                 id='publisher-timeline',
#                 config={'displayModeBar': False}
#             )
#         ], className="mb-8"),
        
#         # Genre Focus Analysis
#         html.Div([
#             html.H2("Genre Focus by Publisher", className="text-xl font-semibold mb-4"),
#             dcc.Graph(
#                 id='publisher-genre-focus',
#                 config={'displayModeBar': False}
#             )
#         ], className="mb-8"),
        
#         # Regional Success Analysis
#         html.Div([
#             html.H2("Regional Market Presence", className="text-xl font-semibold mb-4"),
#             dcc.Graph(
#                 id='publisher-regional-presence',
#                 config={'displayModeBar': False}
#             )
#         ], className="mb-8"),
        
#         # Detailed Metrics Table
#         html.Div([
#             html.H2("Publisher Performance Metrics", className="text-xl font-semibold mb-4"),
#             html.Div(id='publisher-metrics-table', className="overflow-x-auto")
#         ], className="mb-8")
#     ], className="p-6")
    
#     return layout

# # Callbacks
# @callback(
#     Output('publisher-market-share', 'figure'),
#     [Input('publisher-year-range', 'value'),
#      Input('publisher-selector', 'value')]
# )
# def update_market_share(years, publishers):
#     """Updates the publisher market share visualization."""
#     df = load_vgsales_data()
    
#     # Filter data
#     mask = (df['Year'] >= years[0]) & (df['Year'] <= years[1])
#     if publishers:
#         mask &= df['Publisher'].isin(publishers)
#     df_filtered = df[mask]
    
#     # Calculate market share
#     publisher_sales = df_filtered.groupby('Publisher')['Global_Sales'].sum().sort_values(ascending=True)
    
#     fig = go.Figure(go.Bar(
#         x=publisher_sales.values,
#         y=publisher_sales.index,
#         orientation='h',
#         marker_color=COLORS['primary']
#     ))
    
#     fig.update_layout(
#         template=CHART_TEMPLATE,
#         title="Publisher Market Share by Global Sales",
#         xaxis_title="Global Sales (Millions)",
#         yaxis_title="Publisher",
#         height=max(400, len(publisher_sales) * 30),
#         showlegend=False
#     )
    
#     return fig

# @callback(
#     Output('publisher-timeline', 'figure'),
#     [Input('publisher-year-range', 'value'),
#      Input('publisher-selector', 'value')]
# )
# def update_timeline(years, publishers):
#     """Updates the publisher sales timeline visualization."""
#     df = load_vgsales_data()
    
#     # Filter data
#     mask = (df['Year'] >= years[0]) & (df['Year'] <= years[1])
#     if publishers:
#         mask &= df['Publisher'].isin(publishers)
#     df_filtered = df[mask]
    
#     # Calculate yearly sales
#     yearly_sales = df_filtered.groupby(['Year', 'Publisher'])['Global_Sales'].sum().reset_index()
    
#     fig = px.line(yearly_sales,
#                   x='Year',
#                   y='Global_Sales',
#                   color='Publisher',
#                   title='Publisher Sales Performance Over Time')
    
#     fig.update_layout(
#         template=CHART_TEMPLATE,
#         xaxis_title="Year",
#         yaxis_title="Global Sales (Millions)"
#     )
    
#     return fig

# @callback(
#     Output('publisher-genre-focus', 'figure'),
#     [Input('publisher-year-range', 'value'),
#      Input('publisher-selector', 'value')]
# )
# def update_genre_focus(years, publishers):
#     """Updates the publisher genre focus visualization."""
#     df = load_vgsales_data()
    
#     # Filter data
#     mask = (df['Year'] >= years[0]) & (df['Year'] <= years[1])
#     if publishers:
#         mask &= df['Publisher'].isin(publishers)
#     df_filtered = df[mask]
    
#     # Calculate genre distribution
#     genre_dist = df_filtered.groupby(['Publisher', 'Genre'])['Global_Sales'].sum().reset_index()
    
#     fig = px.treemap(genre_dist,
#                      path=['Publisher', 'Genre'],
#                      values='Global_Sales',
#                      title='Genre Focus by Publisher')
    
#     fig.update_layout(template=CHART_TEMPLATE)
    
#     return fig

# @callback(
#     Output('publisher-regional-presence', 'figure'),
#     [Input('publisher-year-range', 'value'),
#      Input('publisher-selector', 'value')]
# )
# def update_regional_presence(years, publishers):
#     """Updates the publisher regional presence visualization."""
#     df = load_vgsales_data()
    
#     # Filter data
#     mask = (df['Year'] >= years[0]) & (df['Year'] <= years[1])
#     if publishers:
#         mask &= df['Publisher'].isin(publishers)
#     df_filtered = df[mask]
    
#     # Calculate regional sales
#     regions = ['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales']
#     regional_sales = df_filtered.groupby('Publisher')[regions].sum()
    
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
#         title="Regional Sales Distribution by Publisher",
#         xaxis_title="Publisher",
#         yaxis_title="Sales (Millions)",
#         barmode='stack'
#     )
    
#     return fig

# @callback(
#     Output('publisher-metrics-table', 'children'),
#     [Input('publisher-year-range', 'value'),
#      Input('publisher-selector', 'value')]
# )
# def update_metrics_table(years, publishers):
#     """Updates the publisher metrics table."""
#     df = load_vgsales_data()
    
#     # Filter data
#     mask = (df['Year'] >= years[0]) & (df['Year'] <= years[1])
#     if publishers:
#         mask &= df['Publisher'].isin(publishers)
#     df_filtered = df[mask]
    
#     # Calculate metrics
#     metrics = calculate_publisher_metrics(df_filtered)
    
#     return create_metrics_table(metrics)

# def calculate_publisher_metrics(df):
#     """Calculates various performance metrics for each publisher."""
#     metrics = []
#     for publisher in df['Publisher'].unique():
#         pub_data = df[df['Publisher'] == publisher]
        
#         metric = {
#             'Publisher': publisher,
#             'Total Games': len(pub_data),
#             'Global Sales': f"${pub_data['Global_Sales'].sum():.2f}M",
#             'Avg Sales/Game': f"${pub_data['Global_Sales'].mean():.2f}M",
#             'Top Genre': pub_data['Genre'].mode().iloc[0],
#             'Top Platform': pub_data['Platform'].mode().iloc[0],
#             'Peak Year': int(pub_data.groupby('Year')['Global_Sales'].sum().idxmax())
#         }
#         metrics.append(metric)
    
#     return pd.DataFrame(metrics)

# def create_metrics_table(df_metrics):
#     """Creates an HTML table for publisher metrics."""
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
from utils.data_loading import load_vgsales_data
from utils.data_processing import preprocess_publisher_data
from components.cards.stats_card import create_stat_card
from components.charts.publisher_charts import create_publisher_timeline
from utils.constants import COLORS, CHART_TEMPLATE

def create_publisher_analysis_layout():
    df = load_vgsales_data()
    publisher_stats = preprocess_publisher_data(df)
    
    layout = html.Div([
        # Header
        html.Div([
            html.H1("Publisher Analysis Dashboard", className="text-3xl font-bold mb-4"),
            html.P("Comprehensive analysis of video game publisher performance", className="text-gray-600 mb-8")
        ], className="mb-8"),
        
        # Modern Date Range and Publisher Selector
        html.Div([
            html.Div([
                html.Label("Time Period", className="block text-sm font-medium mb-2"),
                html.Div([
                    dcc.Input(
                        id='year-start',
                        type='number',
                        min=int(df['Year'].min()),
                        max=int(df['Year'].max()),
                        value=int(df['Year'].min()),
                        className="w-1/2 p-2 border rounded-l"
                    ),
                    dcc.Input(
                        id='year-end',
                        type='number',
                        min=int(df['Year'].min()),
                        max=int(df['Year'].max()),
                        value=int(df['Year'].max()),
                        className="w-1/2 p-2 border rounded-r"
                    )
                ], className="flex")
            ], className="w-full md:w-1/2 mb-6"),
            
            html.Div([
                html.Label("Publishers", className="block text-sm font-medium mb-2"),
                dcc.Dropdown(
                    id='publisher-selector',
                    options=[{'label': str(pub), 'value': str(pub)} 
                            for pub in df['Publisher'].unique()],
                    value=df['Publisher'].value_counts().nlargest(10).index.tolist(),
                    multi=True,
                    className="w-full"
                )
            ], className="w-full md:w-1/2 mb-6")
        ], className="bg-white p-6 rounded-lg shadow-lg mb-8"),
        
        # Stats Cards
        html.Div([
            create_stat_card(
                "Total Publishers",
                len(publisher_stats['unique_publishers']),
                "Active game publishers"
            ),
            create_stat_card(
                "Market Leader",
                publisher_stats['top_publisher'],
                f"${publisher_stats['top_publisher_sales']:.1f}M in sales"
            ),
            create_stat_card(
                "Most Prolific",
                publisher_stats['most_games'],
                f"{publisher_stats['game_count']} games published"
            )
        ], className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8"),
        
        # Charts Section
        html.Div([
            # Market Share
            html.Div([
                html.H2("Market Share Analysis", className="text-xl font-semibold mb-4"),
                dcc.Graph(id='publisher-market-share')
            ], className="bg-white p-6 rounded-lg shadow-lg mb-8"),
            
            # Timeline
            html.Div([
                html.H2("Sales Timeline", className="text-xl font-semibold mb-4"),
                dcc.Graph(id='publisher-timeline')
            ], className="bg-white p-6 rounded-lg shadow-lg mb-8"),
            
            # Genre Focus
            html.Div([
                html.H2("Genre Distribution", className="text-xl font-semibold mb-4"),
                dcc.Graph(id='publisher-genre-focus')
            ], className="bg-white p-6 rounded-lg shadow-lg mb-8"),
            
            # Regional Performance
            html.Div([
                html.H2("Regional Performance", className="text-xl font-semibold mb-4"),
                dcc.Graph(id='publisher-regional-performance')
            ], className="bg-white p-6 rounded-lg shadow-lg mb-8")
        ])
    ], className="p-8 bg-gray-100")
    
    return layout

@callback(
    [Output('publisher-market-share', 'figure'),
     Output('publisher-timeline', 'figure'),
     Output('publisher-genre-focus', 'figure'),
     Output('publisher-regional-performance', 'figure')],
    [Input('year-start', 'value'),
     Input('year-end', 'value'),
     Input('publisher-selector', 'value')]
)
def update_charts(start_year, end_year, publishers):
    df = load_vgsales_data()
    
    # Filter data
    mask = (df['Year'] >= start_year) & (df['Year'] <= end_year)
    if publishers:
        mask &= df['Publisher'].isin(publishers)
    df_filtered = df[mask]
    
    # Market Share Chart
    publisher_sales = df_filtered.groupby('Publisher')['Global_Sales'].sum().sort_values(ascending=True)
    market_share_fig = go.Figure(go.Bar(
        x=publisher_sales.values,
        y=publisher_sales.index,
        orientation='h',
        text=publisher_sales.values.round(1),
        textposition='outside',
        marker_color=COLORS['primary']
    ))
    market_share_fig.update_layout(
        template=CHART_TEMPLATE,
        title="Publisher Market Share",
        xaxis_title="Global Sales (Millions)",
        yaxis_title=None,
        height=max(400, len(publisher_sales) * 25)
    )
    
    # Timeline Chart
    timeline_data = df_filtered.groupby(['Year', 'Publisher'])['Global_Sales'].sum().reset_index()
    timeline_fig = px.line(
        timeline_data,
        x='Year',
        y='Global_Sales',
        color='Publisher',
        title='Publisher Sales Timeline'
    )
    timeline_fig.update_layout(template=CHART_TEMPLATE)
    
    # Genre Focus Chart
    genre_data = df_filtered.groupby(['Publisher', 'Genre'])['Global_Sales'].sum().reset_index()
    genre_fig = px.treemap(
        genre_data,
        path=['Publisher', 'Genre'],
        values='Global_Sales',
        title='Genre Distribution by Publisher'
    )
    genre_fig.update_layout(template=CHART_TEMPLATE)
    
    # Regional Performance Chart
    regions = ['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales']
    regional_data = df_filtered.groupby('Publisher')[regions].sum()
    
    regional_fig = go.Figure()
    for region in regions:
        regional_fig.add_trace(go.Bar(
            name=region.replace('_Sales', ''),
            x=regional_data.index,
            y=regional_data[region],
            hovertemplate="%{y:.1f}M"
        ))
    
    regional_fig.update_layout(
        template=CHART_TEMPLATE,
        title="Regional Sales Distribution",
        xaxis_title="Publisher",
        yaxis_title="Sales (Millions)",
        barmode='group'
    )
    
    return market_share_fig, timeline_fig, genre_fig, regional_fig