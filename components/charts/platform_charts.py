import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

def create_platform_sales_chart(df):
    """
    Create a bar chart showing total sales by platform
    
    Args:
        df (pd.DataFrame): The video games sales dataframe
    
    Returns:
        dcc.Graph: Plotly bar chart wrapped in a Dash component
    """
    platform_sales = df.groupby('Platform')['Global_Sales'].sum().sort_values(ascending=True)
    
    fig = go.Figure(go.Bar(
        x=platform_sales.values,
        y=platform_sales.index,
        orientation='h',
        text=platform_sales.values.round(1),
        textposition='outside',
        hovertemplate="<b>%{y}</b><br>Global Sales: %{x:.1f}M units<extra></extra>"
    ))
    
    fig.update_layout(
        title='Global Sales by Platform',
        xaxis_title='Global Sales (Millions)',
        yaxis_title=None,
        template='plotly_white',
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    return dcc.Graph(figure=fig, id='platform-sales-chart')

def create_platform_timeline(df):
    """
    Create a line chart showing platform performance over time
    
    Args:
        df (pd.DataFrame): The video games sales dataframe
    
    Returns:
        dcc.Graph: Plotly line chart wrapped in a Dash component
    """
    # Get top 10 platforms by total sales
    top_platforms = df.groupby('Platform')['Global_Sales'].sum().nlargest(10).index
    
    # Create yearly sales data for top platforms
    timeline_data = df[df['Platform'].isin(top_platforms)].groupby(['Year', 'Platform'])['Global_Sales'].sum().reset_index()
    
    fig = px.line(
        timeline_data,
        x='Year',
        y='Global_Sales',
        color='Platform',
        title='Sales Trends by Platform Over Time',
        labels={'Global_Sales': 'Global Sales (Millions)', 'Year': 'Release Year'}
    )
    
    fig.update_layout(
        template='plotly_white',
        hovermode='x unified',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return dcc.Graph(figure=fig, id='platform-timeline')

def create_platform_genre_distribution(df):
    """
    Create a heatmap showing genre distribution across platforms
    
    Args:
        df (pd.DataFrame): The video games sales dataframe
    
    Returns:
        dcc.Graph: Plotly heatmap wrapped in a Dash component
    """
    # Get top 15 platforms by total sales
    top_platforms = df.groupby('Platform')['Global_Sales'].sum().nlargest(15).index
    
    # Calculate genre distribution for each platform
    platform_genre = df[df['Platform'].isin(top_platforms)].pivot_table(
        values='Global_Sales',
        index='Platform',
        columns='Genre',
        aggfunc='sum'
    ).fillna(0)
    
    # Convert to percentages
    platform_genre_pct = platform_genre.div(platform_genre.sum(axis=1), axis=0) * 100
    
    fig = go.Figure(data=go.Heatmap(
        z=platform_genre_pct.values,
        x=platform_genre_pct.columns,
        y=platform_genre_pct.index,
        colorscale='Viridis',
        hoverongaps=False,
        hovertemplate=(
            "Platform: %{y}<br>"
            "Genre: %{x}<br>"
            "Percentage: %{z:.1f}%<extra></extra>"
        )
    ))
    
    fig.update_layout(
        title='Genre Distribution by Platform',
        template='plotly_white',
        xaxis_title=None,
        yaxis_title=None,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    return dcc.Graph(figure=fig, id='platform-genre-heatmap')

def create_platform_regional_share(df):
    """
    Create a stacked bar chart showing regional sales distribution for each platform
    
    Args:
        df (pd.DataFrame): The video games sales dataframe
    
    Returns:
        dcc.Graph: Plotly stacked bar chart wrapped in a Dash component
    """
    # Get top 15 platforms
    top_platforms = df.groupby('Platform')['Global_Sales'].sum().nlargest(15).index
    
    # Calculate regional sales for each platform
    platform_regional = df[df['Platform'].isin(top_platforms)].groupby('Platform').agg({
        'NA_Sales': 'sum',
        'EU_Sales': 'sum',
        'JP_Sales': 'sum',
        'Other_Sales': 'sum'
    })
    
    # Create stacked bar chart
    fig = go.Figure()
    regions = {
        'NA_Sales': 'North America',
        'EU_Sales': 'Europe',
        'JP_Sales': 'Japan',
        'Other_Sales': 'Other'
    }
    
    for col, name in regions.items():
        fig.add_trace(go.Bar(
            name=name,
            x=platform_regional.index,
            y=platform_regional[col],
            hovertemplate="%{x}<br>%{y:.1f}M units<extra></extra>"
        ))
    
    fig.update_layout(
        title='Regional Sales Distribution by Platform',
        xaxis_title=None,
        yaxis_title='Sales (Millions)',
        template='plotly_white',
        barmode='stack',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return dcc.Graph(figure=fig, id='platform-regional-share')

def create_top_games_by_platform(df, platform):
    """
    Create a bar chart showing top games for a specific platform
    
    Args:
        df (pd.DataFrame): The video games sales dataframe
        platform (str): Platform name to analyze
    
    Returns:
        dcc.Graph: Plotly bar chart wrapped in a Dash component
    """
    platform_games = df[df['Platform'] == platform].nlargest(10, 'Global_Sales')
    
    fig = px.bar(
        platform_games,
        x='Global_Sales',
        y='Name',
        orientation='h',
        title=f'Top 10 Games on {platform}',
        labels={'Global_Sales': 'Global Sales (Millions)', 'Name': 'Game Title'}
    )
    
    fig.update_traces(
        texttemplate='%{x:.1f}M',
        textposition='outside',
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Sales: %{x:.1f}M units<extra></extra>"
        )
    )
    
    fig.update_layout(
        template='plotly_white',
        showlegend=False,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    return dcc.Graph(figure=fig, id=f'top-games-{platform}')

def create_platform_stats_card(df):
    """
    Create a card showing key platform statistics
    
    Args:
        df (pd.DataFrame): The video games sales dataframe
    
    Returns:
        dbc.Card: Bootstrap card component with platform statistics
    """
    total_platforms = df['Platform'].nunique()
    avg_sales_per_platform = df['Global_Sales'].sum() / total_platforms
    top_platform = df.groupby('Platform')['Global_Sales'].sum().idxmax()
    top_platform_sales = df.groupby('Platform')['Global_Sales'].sum().max()
    
    card_content = [
        dbc.CardHeader("Platform Statistics"),
        dbc.CardBody([
            html.P(f"Total Platforms: {total_platforms}"),
            html.P(f"Average Sales per Platform: {avg_sales_per_platform:.1f}M"),
            html.P(f"Top Platform: {top_platform} ({top_platform_sales:.1f}M sales)")
        ])
    ]
    
    return dbc.Card(card_content)

def create_platform_layout(df):
    """
    Create the main layout for platform analysis
    
    Args:
        df (pd.DataFrame): The video games sales dataframe
    
    Returns:
        html.Div: Main container with all platform analysis components
    """
    # Get the top platform for detailed game analysis
    top_platform = df.groupby('Platform')['Global_Sales'].sum().idxmax()
    
    return html.Div([
        dbc.Row([
            dbc.Col(create_platform_stats_card(df), width=12)
        ], className="mb-4"),
        dbc.Row([
            dbc.Col(create_platform_sales_chart(df), width=12)
        ], className="mb-4"),
        dbc.Row([
            dbc.Col(create_platform_genre_distribution(df), width=6),
            dbc.Col(create_platform_regional_share(df), width=6)
        ], className="mb-4"),
        dbc.Row([
            dbc.Col(create_platform_timeline(df), width=12)
        ], className="mb-4"),
        dbc.Row([
            dbc.Col(create_top_games_by_platform(df, top_platform), width=12)
        ])
    ])

def register_callbacks(app):
    """
    Register any callbacks for interactive features
    
    Args:
        app: The Dash app instance
    """
    pass