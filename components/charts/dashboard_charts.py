"""
Dashboard-specific chart functions using the ChartConfigurator utility.
These functions create the specific visualizations needed for the video game sales dashboard.
"""

from typing import Dict, List
import pandas as pd
from dash import html
from utils.charts_config import ChartConfigurator

def create_sales_trend_chart(df: pd.DataFrame) -> Dict:
    """
    Create a line chart showing sales trends over time for each region.
    
    Args:
        df (pd.DataFrame): Filtered DataFrame containing video game sales data
    
    Returns:
        Dict: Plotly figure object
    """
    # Filter out rows with null or invalid years
    df_clean = df[df['Year'].notna() & (df['Year'] != 'N/A')].copy()
    
    # Convert Year to numeric if it isn't already
    df_clean['Year'] = pd.to_numeric(df_clean['Year'], errors='coerce')
    
    # Additional filtering for valid years (e.g., between 1980 and 2020)
    df_clean = df_clean[(df_clean['Year'] >= 1980) & (df_clean['Year'] <= 2020)]
    
    if df_clean.empty:
        # Return an empty chart with a message if no valid data
        return ChartConfigurator.create_time_series(
            data=pd.DataFrame({'Year': [2000], 'Value': [0]}),
            time_column='Year',
            value_columns=['Value'],
            title='No valid data available for the selected period',
            size='large'
        )
    
    yearly_sales = df_clean.groupby('Year').agg({
        'NA_Sales': 'sum',
        'EU_Sales': 'sum',
        'JP_Sales': 'sum',
        'Other_Sales': 'sum'
    }).reset_index()
    
    return ChartConfigurator.create_time_series(
        data=yearly_sales,
        time_column='Year',
        value_columns=['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales'],
        title='Sales Trends by Region',
        size='large'
    )

def create_regional_distribution_chart(df: pd.DataFrame) -> Dict:
    """
    Create a pie chart showing the distribution of sales across regions.
    
    Args:
        df (pd.DataFrame): Filtered DataFrame containing video game sales data
    
    Returns:
        Dict: Plotly figure object
    """
    regional_sales = pd.DataFrame({
        'Region': ['North America', 'Europe', 'Japan', 'Other'],
        'Sales': [
            df['NA_Sales'].sum(),
            df['EU_Sales'].sum(),
            df['JP_Sales'].sum(),
            df['Other_Sales'].sum()
        ]
    })
    
    return ChartConfigurator.create_pie_chart(
        data=regional_sales,
        names='Region',
        values='Sales',
        title='Regional Sales Distribution',
        size='medium'
    )

def create_genre_distribution_chart(df: pd.DataFrame) -> Dict:
    """
    Create a bar chart showing the distribution of sales across genres.
    
    Args:
        df (pd.DataFrame): Filtered DataFrame containing video game sales data
    
    Returns:
        Dict: Plotly figure object
    """
    genre_sales = (df.groupby('Genre')['Global_Sales']
                  .sum()
                  .sort_values(ascending=True)
                  .reset_index())
    
    return ChartConfigurator.create_sales_bar(
        data=genre_sales,
        x='Genre',
        y='Global_Sales',
        title='Sales by Genre',
        size='medium',
        orientation='h'
    )

def create_platform_share_chart(df: pd.DataFrame) -> Dict:
    """
    Create a regional comparison chart showing platform performance across regions.
    
    Args:
        df (pd.DataFrame): Filtered DataFrame containing video game sales data
    
    Returns:
        Dict: Plotly figure object
    """
    platform_sales = (df.groupby('Platform')
                     .agg({
                         'NA_Sales': 'sum',
                         'EU_Sales': 'sum',
                         'JP_Sales': 'sum',
                         'Other_Sales': 'sum'
                     })
                     .reset_index()
                     .sort_values('NA_Sales', ascending=False)
                     .head(10))  # Top 10 platforms
    
    return ChartConfigurator.create_regional_comparison(
        data=platform_sales,
        category='Platform',
        title='Platform Performance by Region',
        size='large'
    )

def create_top_games_table(df: pd.DataFrame, n: int = 10) -> List:
    """
    Create an HTML table of top games by global sales.
    
    Args:
        df (pd.DataFrame): Filtered DataFrame containing video game sales data
        n (int): Number of top games to display
    
    Returns:
        List: List of dash table rows
    """
    top_games = df.nlargest(n, 'Global_Sales')[
        ['Name', 'Platform', 'Year', 'Genre', 'Publisher', 'Global_Sales']
    ]
    
    # Create header with consistent styling
    header = html.Thead(html.Tr([
        html.Th(col, style={
            'backgroundColor': '#f8f9fa',
            'padding': '12px',
            'borderBottom': '2px solid #dee2e6',
            'textAlign': 'left',
            'fontSize': '14px',
            'fontWeight': 'bold'
        }) for col in ['Name', 'Platform', 'Year', 'Genre', 'Publisher', 'Global Sales (M)']
    ]))
    
    # Create rows with alternating colors
    rows = []
    for idx, game in top_games.iterrows():
        row = html.Tr([
            html.Td(game['Name']),
            html.Td(game['Platform']),
            html.Td(f"{game['Year']:.0f}"),
            html.Td(game['Genre']),
            html.Td(game['Publisher']),
            html.Td(f"{game['Global_Sales']:.1f}")
        ], style={
            'backgroundColor': '#ffffff' if idx % 2 == 0 else '#f8f9fa',
            'padding': '8px',
            'fontSize': '13px'
        })
        rows.append(row)
    
    body = html.Tbody(rows)
    
    return [header, body]