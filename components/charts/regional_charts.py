import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

def create_regional_distribution_pie(df):
    """
    Create a pie chart showing the distribution of sales across regions
    
    Args:
        df (pd.DataFrame): The video games sales dataframe
    
    Returns:
        dcc.Graph: Plotly pie chart wrapped in a Dash component
    """
    regional_totals = {
        'North America': df['NA_Sales'].sum(),
        'Europe': df['EU_Sales'].sum(),
        'Japan': df['JP_Sales'].sum(),
        'Other Regions': df['Other_Sales'].sum()
    }
    
    fig = go.Figure(data=[
        go.Pie(
            labels=list(regional_totals.keys()),
            values=list(regional_totals.values()),
            hole=0.4,
            textinfo='label+percent',
            hovertemplate="%{label}<br>%{value:.1f}M units<br>%{percent}<extra></extra>"
        )
    ])
    
    fig.update_layout(
        title='Global Sales Distribution by Region',
        template='plotly_white',
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    return dcc.Graph(figure=fig, id='regional-distribution-pie')

def create_top_games_by_region(df, region_col, region_name, n=10):
    """
    Create a bar chart showing top games for a specific region
    
    Args:
        df (pd.DataFrame): The video games sales dataframe
        region_col (str): Column name for regional sales
        region_name (str): Display name for the region
        n (int): Number of top games to display
    
    Returns:
        dcc.Graph: Plotly bar chart wrapped in a Dash component
    """
    top_games = df.nlargest(n, region_col)[['Name', 'Platform', region_col]]
    
    fig = px.bar(
        top_games,
        x=region_col,
        y='Name',
        orientation='h',
        text=region_col,
        custom_data=['Platform'],
        title=f'Top {n} Games in {region_name}'
    )
    
    fig.update_traces(
        texttemplate='%{text:.1f}M',
        textposition='outside',
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Platform: %{customdata[0]}<br>"
            "Sales: %{x:.1f}M units<extra></extra>"
        )
    )
    
    fig.update_layout(
        template='plotly_white',
        xaxis_title='Sales (Millions)',
        yaxis_title=None,
        yaxis={'categoryorder': 'total ascending'},
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    return dcc.Graph(figure=fig, id=f'top-games-{region_name.lower()}')

def create_regional_heatmap(df):
    """
    Create a heatmap showing genre popularity across regions
    
    Args:
        df (pd.DataFrame): The video games sales dataframe
    
    Returns:
        dcc.Graph: Plotly heatmap wrapped in a Dash component
    """
    # Calculate average sales by genre for each region
    genre_regional = df.groupby('Genre').agg({
        'NA_Sales': 'mean',
        'EU_Sales': 'mean',
        'JP_Sales': 'mean',
        'Other_Sales': 'mean'
    }).round(2)
    
    # Create heatmap
    fig = go.Figure(data=go.Heatmap(
        z=genre_regional.values,
        x=['North America', 'Europe', 'Japan', 'Other'],
        y=genre_regional.index,
        colorscale='Blues',
        hoverongaps=False,
        hovertemplate=(
            "Genre: %{y}<br>"
            "Region: %{x}<br>"
            "Avg Sales: %{z:.2f}M units<extra></extra>"
        )
    ))
    
    fig.update_layout(
        title='Average Game Sales by Genre and Region',
        template='plotly_white',
        xaxis_title=None,
        yaxis_title=None,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    return dcc.Graph(figure=fig, id='regional-genre-heatmap')

def create_regional_stats_cards(df):
    """
    Create statistics cards for each region
    
    Args:
        df (pd.DataFrame): The video games sales dataframe
    
    Returns:
        list: List of dbc.Card components with regional statistics
    """
    regions = {
        'NA_Sales': 'North America',
        'EU_Sales': 'Europe',
        'JP_Sales': 'Japan',
        'Other_Sales': 'Other Regions'
    }
    
    cards = []
    for col, name in regions.items():
        total_sales = df[col].sum()
        avg_sales = df[col].mean()
        max_sales = df[col].max()
        top_game = df.loc[df[col].idxmax(), 'Name']
        
        card_content = [
            dbc.CardHeader(name),
            dbc.CardBody([
                html.H5(f"{total_sales:.1f}M", className="card-title"),
                html.P([
                    f"Average: {avg_sales:.2f}M units",
                    html.Br(),
                    f"Best-selling: {top_game} ({max_sales:.1f}M)"
                ])
            ])
        ]
        
        cards.append(dbc.Col(dbc.Card(card_content), width=3))
    
    return cards

def create_regional_layout(df):
    """
    Create the main layout for regional sales analysis
    
    Args:
        df (pd.DataFrame): The video games sales dataframe
    
    Returns:
        html.Div: Main container with all regional analysis components
    """
    return html.Div([
        dbc.Row(create_regional_stats_cards(df), className="mb-4"),
        dbc.Row([
            dbc.Col(create_regional_distribution_pie(df), width=6),
            dbc.Col(create_regional_heatmap(df), width=6)
        ]),
        dbc.Row([
            dbc.Col([
                create_top_games_by_region(df, 'NA_Sales', 'North America'),
                create_top_games_by_region(df, 'JP_Sales', 'Japan')
            ], width=6),
            dbc.Col([
                create_top_games_by_region(df, 'EU_Sales', 'Europe'),
                create_top_games_by_region(df, 'Other_Sales', 'Other Regions')
            ], width=6)
        ])
    ])

def register_callbacks(app):
    """
    Register any callbacks for interactive features
    
    Args:
        app: The Dash app instance
    """
    pass