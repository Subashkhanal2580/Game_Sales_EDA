import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

def create_top_publishers_chart(df, n=15):
    """
    Create a bar chart showing top publishers by global sales
    
    Args:
        df (pd.DataFrame): The video games sales dataframe
        n (int): Number of top publishers to display
    
    Returns:
        dcc.Graph: Plotly bar chart wrapped in a Dash component
    """
    publisher_sales = df.groupby('Publisher')['Global_Sales'].sum().sort_values(ascending=True)
    top_publishers = publisher_sales.tail(n)
    
    fig = go.Figure(go.Bar(
        x=top_publishers.values,
        y=top_publishers.index,
        orientation='h',
        text=top_publishers.values.round(1),
        textposition='outside',
        hovertemplate="<b>%{y}</b><br>Global Sales: %{x:.1f}M units<extra></extra>"
    ))
    
    fig.update_layout(
        title=f'Top {n} Publishers by Global Sales',
        xaxis_title='Global Sales (Millions)',
        yaxis_title=None,
        template='plotly_white',
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    return dcc.Graph(figure=fig, id='top-publishers-chart')

def create_publisher_genre_analysis(df):
    """
    Create a heatmap showing publisher specialization by genre
    
    Args:
        df (pd.DataFrame): The video games sales dataframe
    
    Returns:
        dcc.Graph: Plotly heatmap wrapped in a Dash component
    """
    # Get top 10 publishers by total sales
    top_publishers = df.groupby('Publisher')['Global_Sales'].sum().nlargest(10).index
    
    # Calculate the percentage of sales by genre for each publisher
    publisher_genre = df[df['Publisher'].isin(top_publishers)].pivot_table(
        values='Global_Sales',
        index='Publisher',
        columns='Genre',
        aggfunc='sum'
    ).fillna(0)
    
    # Convert to percentages
    publisher_genre_pct = publisher_genre.div(publisher_genre.sum(axis=1), axis=0) * 100
    
    fig = go.Figure(data=go.Heatmap(
        z=publisher_genre_pct.values,
        x=publisher_genre_pct.columns,
        y=publisher_genre_pct.index,
        colorscale='Viridis',
        hoverongaps=False,
        hovertemplate=(
            "Publisher: %{y}<br>"
            "Genre: %{x}<br>"
            "Percentage: %{z:.1f}%<extra></extra>"
        )
    ))
    
    fig.update_layout(
        title='Publisher Genre Specialization (Top 10 Publishers)',
        template='plotly_white',
        xaxis_title=None,
        yaxis_title=None,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    return dcc.Graph(figure=fig, id='publisher-genre-heatmap')

def create_publisher_timeline(df):
    """
    Create a line chart showing publisher market share over time
    
    Args:
        df (pd.DataFrame): The video games sales dataframe
    
    Returns:
        dcc.Graph: Plotly line chart wrapped in a Dash component
    """
    # Get top 5 publishers
    top_publishers = df.groupby('Publisher')['Global_Sales'].sum().nlargest(5).index
    
    # Create yearly sales data for top publishers
    timeline_data = df[df['Publisher'].isin(top_publishers)].groupby(['Year', 'Publisher'])['Global_Sales'].sum().reset_index()
    
    fig = px.line(
        timeline_data,
        x='Year',
        y='Global_Sales',
        color='Publisher',
        title='Sales Trends of Top 5 Publishers Over Time',
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
    
    return dcc.Graph(figure=fig, id='publisher-timeline')

def create_publisher_regional_performance(df):
    """
    Create a grouped bar chart showing regional performance of top publishers
    
    Args:
        df (pd.DataFrame): The video games sales dataframe
    
    Returns:
        dcc.Graph: Plotly grouped bar chart wrapped in a Dash component
    """
    # Get top 8 publishers
    top_publishers = df.groupby('Publisher')['Global_Sales'].sum().nlargest(8).index
    
    # Calculate regional sales for top publishers
    regional_data = df[df['Publisher'].isin(top_publishers)].groupby('Publisher').agg({
        'NA_Sales': 'sum',
        'EU_Sales': 'sum',
        'JP_Sales': 'sum',
        'Other_Sales': 'sum'
    }).round(2)
    
    # Create grouped bar chart
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
            x=regional_data.index,
            y=regional_data[col],
            hovertemplate="%{x}<br>%{y:.1f}M units<extra></extra>"
        ))
    
    fig.update_layout(
        title='Regional Performance of Top Publishers',
        xaxis_title=None,
        yaxis_title='Sales (Millions)',
        template='plotly_white',
        barmode='group',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return dcc.Graph(figure=fig, id='publisher-regional-performance')

def create_publisher_stats_card(df):
    """
    Create a card showing key publisher statistics
    
    Args:
        df (pd.DataFrame): The video games sales dataframe
    
    Returns:
        dbc.Card: Bootstrap card component with publisher statistics
    """
    total_publishers = df['Publisher'].nunique()
    avg_games_per_publisher = len(df) / total_publishers
    avg_sales_per_publisher = df['Global_Sales'].sum() / total_publishers
    top_publisher = df.groupby('Publisher')['Global_Sales'].sum().idxmax()
    
    card_content = [
        dbc.CardHeader("Publisher Statistics"),
        dbc.CardBody([
            html.P(f"Total Publishers: {total_publishers}"),
            html.P(f"Average Games per Publisher: {avg_games_per_publisher:.1f}"),
            html.P(f"Average Sales per Publisher: {avg_sales_per_publisher:.1f}M"),
            html.P(f"Top Publisher: {top_publisher}")
        ])
    ]
    
    return dbc.Card(card_content)

def create_publisher_layout(df):
    """
    Create the main layout for publisher analysis
    
    Args:
        df (pd.DataFrame): The video games sales dataframe
    
    Returns:
        html.Div: Main container with all publisher analysis components
    """
    return html.Div([
        dbc.Row([
            dbc.Col(create_publisher_stats_card(df), width=12)
        ], className="mb-4"),
        dbc.Row([
            dbc.Col(create_top_publishers_chart(df), width=12)
        ], className="mb-4"),
        dbc.Row([
            dbc.Col(create_publisher_genre_analysis(df), width=6),
            dbc.Col(create_publisher_regional_performance(df), width=6)
        ], className="mb-4"),
        dbc.Row([
            dbc.Col(create_publisher_timeline(df), width=12)
        ])
    ])

def register_callbacks(app):
    """
    Register any callbacks for interactive features
    
    Args:
        app: The Dash app instance
    """
    pass