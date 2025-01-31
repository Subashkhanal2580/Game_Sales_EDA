import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

def create_yearly_sales_chart(df):
    """
    Create a line chart showing total global sales trends by year
    
    Args:
        df (pd.DataFrame): The video games sales dataframe
    
    Returns:
        dcc.Graph: Plotly graph object wrapped in a Dash component
    """
    # Group by year and sum global sales
    yearly_sales = df.groupby('Year')['Global_Sales'].sum().reset_index()
    yearly_sales = yearly_sales.dropna()  # Remove any NaN years
    
    fig = px.line(
        yearly_sales,
        x='Year',
        y='Global_Sales',
        title='Global Video Game Sales Trend by Year',
        labels={'Year': 'Release Year', 'Global_Sales': 'Global Sales (Millions)'}
    )
    
    fig.update_layout(
        template='plotly_white',
        xaxis_tickangle=-45,
        margin=dict(l=20, r=20, t=40, b=20),
        hovermode='x unified'
    )
    
    return dcc.Graph(figure=fig, id='yearly-sales-trend')

def create_yearly_regional_sales(df):
    """
    Create a stacked area chart showing regional sales distribution by year
    
    Args:
        df (pd.DataFrame): The video games sales dataframe
    
    Returns:
        dcc.Graph: Plotly graph object wrapped in a Dash component
    """
    # Group by year and sum regional sales
    regional_sales = df.groupby('Year').agg({
        'NA_Sales': 'sum',
        'EU_Sales': 'sum',
        'JP_Sales': 'sum',
        'Other_Sales': 'sum'
    }).reset_index()
    
    regional_sales = regional_sales.dropna()
    
    fig = go.Figure()
    
    # Add areas for each region
    regions = {
        'NA_Sales': 'North America',
        'EU_Sales': 'Europe',
        'JP_Sales': 'Japan',
        'Other_Sales': 'Other Regions'
    }
    
    for column, name in regions.items():
        fig.add_trace(
            go.Scatter(
                x=regional_sales['Year'],
                y=regional_sales[column],
                name=name,
                stackgroup='one',
                hovertemplate="%{y:.1f}M units<extra></extra>"
            )
        )
    
    fig.update_layout(
        title='Regional Sales Distribution by Year',
        xaxis_title='Release Year',
        yaxis_title='Sales (Millions)',
        template='plotly_white',
        hovermode='x unified',
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return dcc.Graph(figure=fig, id='yearly-regional-sales')

def create_top_years_card(df):
    """
    Create a card showing the top 5 years by global sales
    
    Args:
        df (pd.DataFrame): The video games sales dataframe
    
    Returns:
        dbc.Card: Bootstrap card component with top years information
    """
    top_years = df.groupby('Year')['Global_Sales'].sum().sort_values(ascending=False).head()
    
    card_content = [
        dbc.CardHeader("Top Years by Global Sales"),
        dbc.CardBody([
            html.Div([
                html.H5(f"{int(year)}: {sales:.1f}M units")
                for year, sales in top_years.items()
            ])
        ])
    ]
    
    return dbc.Card(card_content, className="mb-4")

def create_yearly_sales_layout(df):
    """
    Create the main layout for yearly sales analysis
    
    Args:
        df (pd.DataFrame): The video games sales dataframe
    
    Returns:
        html.Div: Main container with all yearly sales components
    """
    return html.Div([
        dbc.Row([
            dbc.Col([
                create_top_years_card(df)
            ], width=12)
        ]),
        dbc.Row([
            dbc.Col([
                create_yearly_sales_chart(df)
            ], width=12)
        ]),
        dbc.Row([
            dbc.Col([
                create_yearly_regional_sales(df)
            ], width=12)
        ])
    ])

# Callback functions can be added here if interactive features are needed
def register_callbacks(app):
    """
    Register any callbacks for interactive features
    
    Args:
        app: The Dash app instance
    """
    pass