import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

def create_genre_sales_chart(df):
    """
    Create a bar chart showing total sales by genre
    
    Args:
        df (pd.DataFrame): The video games sales dataframe
    
    Returns:
        dcc.Graph: Plotly bar chart wrapped in a Dash component
    """
    genre_sales = df.groupby('Genre')['Global_Sales'].sum().sort_values(ascending=True)
    
    fig = go.Figure(go.Bar(
        x=genre_sales.values,
        y=genre_sales.index,
        orientation='h',
        text=genre_sales.values.round(1),
        textposition='outside',
        hovertemplate="<b>%{y}</b><br>Global Sales: %{x:.1f}M units<extra></extra>"
    ))
    
    fig.update_layout(
        title='Global Sales by Genre',
        xaxis_title='Global Sales (Millions)',
        yaxis_title=None,
        template='plotly_white',
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    return dcc.Graph(figure=fig, id='genre-sales-chart')

def create_genre_timeline(df):
    """
    Create a line chart showing genre popularity trends over time
    
    Args:
        df (pd.DataFrame): The video games sales dataframe
    
    Returns:
        dcc.Graph: Plotly line chart wrapped in a Dash component
    """
    timeline_data = df.groupby(['Year', 'Genre'])['Global_Sales'].sum().reset_index()
    
    fig = px.line(
        timeline_data,
        x='Year',
        y='Global_Sales',
        color='Genre',
        title='Genre Popularity Trends Over Time',
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
    
    return dcc.Graph(figure=fig, id='genre-timeline')

def create_genre_platform_distribution(df, regions):
    """
    Create a heatmap showing genre success across different platforms
    
    Args:
        df (pd.DataFrame): The video games sales dataframe
    
    Returns:
        dcc.Graph: Plotly heatmap wrapped in a Dash component
    """
    # Get top 10 platforms by total sales
    top_platforms = df.groupby('Platform')['Global_Sales'].sum().nlargest(10).index
    
    # Calculate average sales for each genre-platform combination
    platform_genre = df[df['Platform'].isin(top_platforms)].pivot_table(
        values='Global_Sales',
        index='Genre',
        columns='Platform',
        aggfunc='mean'
    ).fillna(0)
    
    fig = go.Figure(data=go.Heatmap(
        z=platform_genre.values,
        x=platform_genre.columns,
        y=platform_genre.index,
        colorscale='Viridis',
        hoverongaps=False,
        hovertemplate=(
            "Genre: %{y}<br>"
            "Platform: %{x}<br>"
            "Avg Sales: %{z:.2f}M units<extra></extra>"
        )
    ))
    
    fig.update_layout(
        title='Average Game Sales by Genre and Platform',
        template='plotly_white',
        xaxis_title=None,
        yaxis_title=None,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    return dcc.Graph(figure=fig, id='genre-platform-heatmap')

def create_genre_regional_analysis(df):
    """
    Create a stacked bar chart showing regional sales distribution for each genre
    
    Args:
        df (pd.DataFrame): The video games sales dataframe
    
    Returns:
        dcc.Graph: Plotly stacked bar chart wrapped in a Dash component
    """
    # Calculate regional sales for each genre
    genre_regional = df.groupby('Genre').agg({
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
            x=genre_regional.index,
            y=genre_regional[col],
            hovertemplate="%{x}<br>%{y:.1f}M units<extra></extra>"
        ))
    
    fig.update_layout(
        title='Regional Sales Distribution by Genre',
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
    
    return dcc.Graph(figure=fig, id='genre-regional-share')

def create_top_games_by_genre(df, genre):
    """
    Create a bar chart showing top games for a specific genre
    
    Args:
        df (pd.DataFrame): The video games sales dataframe
        genre (str): Genre to analyze
    
    Returns:
        dcc.Graph: Plotly bar chart wrapped in a Dash component
    """
    genre_games = df[df['Genre'] == genre].nlargest(10, 'Global_Sales')
    
    fig = px.bar(
        genre_games,
        x='Global_Sales',
        y='Name',
        orientation='h',
        title=f'Top 10 {genre} Games',
        labels={'Global_Sales': 'Global Sales (Millions)', 'Name': 'Game Title'}
    )
    
    fig.update_traces(
        texttemplate='%{x:.1f}M',
        textposition='outside',
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Platform: %{customdata[0]}<br>"
            "Sales: %{x:.1f}M units<extra></extra>"
        ),
        customdata=genre_games[['Platform']]
    )
    
    fig.update_layout(
        template='plotly_white',
        showlegend=False,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    return dcc.Graph(figure=fig, id=f'top-games-{genre.lower()}')

def create_genre_publisher_affinity(df):
    """
    Create a heatmap showing publisher affinity for different genres
    
    Args:
        df (pd.DataFrame): The video games sales dataframe
    
    Returns:
        dcc.Graph: Plotly heatmap wrapped in a Dash component
    """
    # Get top 10 publishers by total sales
    top_publishers = df.groupby('Publisher')['Global_Sales'].sum().nlargest(10).index
    
    # Calculate the percentage of each publisher's games in each genre
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
        title='Publisher Genre Affinity (Top 10 Publishers)',
        template='plotly_white',
        xaxis_title=None,
        yaxis_title=None,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    return dcc.Graph(figure=fig, id='genre-publisher-heatmap')

def create_genre_stats_card(df):
    """
    Create a card showing key genre statistics
    
    Args:
        df (pd.DataFrame): The video games sales dataframe
    
    Returns:
        dbc.Card: Bootstrap card component with genre statistics
    """
    total_genres = df['Genre'].nunique()
    avg_sales_per_genre = df['Global_Sales'].sum() / total_genres
    top_genre = df.groupby('Genre')['Global_Sales'].sum().idxmax()
    top_genre_sales = df.groupby('Genre')['Global_Sales'].sum().max()
    
    card_content = [
        dbc.CardHeader("Genre Statistics"),
        dbc.CardBody([
            html.P(f"Total Genres: {total_genres}"),
            html.P(f"Average Sales per Genre: {avg_sales_per_genre:.1f}M"),
            html.P(f"Top Genre: {top_genre} ({top_genre_sales:.1f}M sales)")
        ])
    ]
    
    return dbc.Card(card_content)

def create_genre_layout(df):
    """
    Create the main layout for genre analysis
    
    Args:
        df (pd.DataFrame): The video games sales dataframe
    
    Returns:
        html.Div: Main container with all genre analysis components
    """
    # Get the top genre for detailed game analysis
    top_genre = df.groupby('Genre')['Global_Sales'].sum().idxmax()
    
    return html.Div([
        dbc.Row([
            dbc.Col(create_genre_stats_card(df), width=12)
        ], className="mb-4"),
        dbc.Row([
            dbc.Col(create_genre_sales_chart(df), width=12)
        ], className="mb-4"),
        dbc.Row([
            dbc.Col(create_genre_platform_distribution(df), width=6),
            dbc.Col(create_genre_regional_analysis(df), width=6)
        ], className="mb-4"),
        dbc.Row([
            dbc.Col(create_genre_timeline(df), width=12)
        ], className="mb-4"),
        dbc.Row([
            dbc.Col(create_genre_publisher_affinity(df), width=12)
        ], className="mb-4"),
        dbc.Row([
            dbc.Col(create_top_games_by_genre(df, top_genre), width=12)
        ])
    ])

def register_callbacks(app):
    """
    Register any callbacks for interactive features
    
    Args:
        app: The Dash app instance
    """
    pass