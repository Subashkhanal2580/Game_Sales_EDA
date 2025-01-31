from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from utils.data_processing import (
    get_yearly_trends,
    get_genre_trends,
    get_platform_trends,
    calculate_growth_rates
)

def create_sales_trend_card(df):
    """
    Create a card showing sales trends over time
    
    Parameters:
    -----------
    df : pandas.DataFrame
        The video games sales dataset
    """
    yearly_data = get_yearly_trends(df)
    
    fig = go.Figure()
    
    # Add total sales line
    fig.add_trace(go.Scatter(
        x=yearly_data.index,
        y=yearly_data['Global_Sales'],
        name='Global Sales',
        line=dict(color='#2E86C1', width=3),
        hovertemplate='Year: %{x}<br>Sales: $%{y:.1f}M<extra></extra>'
    ))
    
    # Add game count bar
    fig.add_trace(go.Bar(
        x=yearly_data.index,
        y=yearly_data['Game_Count'],
        name='Number of Games',
        yaxis='y2',
        marker_color='rgba(189, 195, 199, 0.5)',
        hovertemplate='Year: %{x}<br>Games: %{y}<extra></extra>'
    ))
    
    fig.update_layout(
        title=None,
        height=400,
        margin=dict(l=0, r=0, t=20, b=0),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        yaxis=dict(
            title='Global Sales (millions)',
            titlefont=dict(color='#2E86C1'),
            tickfont=dict(color='#2E86C1')
        ),
        yaxis2=dict(
            title='Number of Games',
            titlefont=dict(color='#7F8C8D'),
            tickfont=dict(color='#7F8C8D'),
            overlaying='y',
            side='right'
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        hovermode='x unified'
    )
    
    fig.update_xaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='rgba(189, 195, 199, 0.2)'
    )
    
    fig.update_yaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='rgba(189, 195, 199, 0.2)'
    )
    
    return dbc.Card([
        dbc.CardHeader([
            html.H6("Sales Trends", className="mb-0"),
            html.Small("Global Sales and Game Releases Over Time", className="text-muted"),
        ]),
        dbc.CardBody([
            dcc.Graph(figure=fig, config={'displayModeBar': False}),
        ]),
    ], className="h-100 shadow-sm")

def create_genre_trend_card(df):
    """
    Create a card showing genre popularity trends
    
    Parameters:
    -----------
    df : pandas.DataFrame
        The video games sales dataset
    """
    genre_trends = get_genre_trends(df)
    
    fig = px.area(
        genre_trends,
        x=genre_trends.index,
        y=genre_trends.columns,
        title=None,
        height=400
    )
    
    fig.update_layout(
        margin=dict(l=0, r=0, t=20, b=0),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        yaxis_title="Market Share (%)",
        plot_bgcolor='white',
        paper_bgcolor='white',
        hovermode='x unified'
    )
    
    fig.update_xaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='rgba(189, 195, 199, 0.2)'
    )
    
    fig.update_yaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='rgba(189, 195, 199, 0.2)'
    )
    
    return dbc.Card([
        dbc.CardHeader([
            html.H6("Genre Evolution", className="mb-0"),
            html.Small("Market Share by Genre Over Time", className="text-muted"),
        ]),
        dbc.CardBody([
            dcc.Graph(figure=fig, config={'displayModeBar': False}),
        ]),
    ], className="h-100 shadow-sm")

def create_platform_trend_card(df):
    """
    Create a card showing platform market share trends
    
    Parameters:
    -----------
    df : pandas.DataFrame
        The video games sales dataset
    """
    platform_trends = get_platform_trends(df)
    
    fig = px.line(
        platform_trends,
        x=platform_trends.index,
        y=platform_trends.columns,
        title=None,
        height=400,
        line_shape='spline'
    )
    
    fig.update_layout(
        margin=dict(l=0, r=0, t=20, b=0),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        yaxis_title="Market Share (%)",
        plot_bgcolor='white',
        paper_bgcolor='white',
        hovermode='x unified'
    )
    
    fig.update_xaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='rgba(189, 195, 199, 0.2)'
    )
    
    fig.update_yaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='rgba(189, 195, 199, 0.2)'
    )
    
    return dbc.Card([
        dbc.CardHeader([
            html.H6("Platform Trends", className="mb-0"),
            html.Small("Market Share by Platform Over Time", className="text-muted"),
        ]),
        dbc.CardBody([
            dcc.Graph(figure=fig, config={'displayModeBar': False}),
        ]),
    ], className="h-100 shadow-sm")

def create_growth_card(df):
    """
    Create a card showing growth rates and trends
    
    Parameters:
    -----------
    df : pandas.DataFrame
        The video games sales dataset
    """
    growth_data = calculate_growth_rates(df)
    
    growth_items = []
    for period, metrics in growth_data.items():
        growth_items.append(
            html.Div([
                html.H6(period, className="mb-2"),
                html.Div([
                    dbc.Row([
                        dbc.Col([
                            html.Small("Sales Growth", className="text-muted d-block"),
                            html.Span(
                                f"{metrics['sales_growth']:+.1f}%",
                                className=f"{'text-success' if metrics['sales_growth'] > 0 else 'text-danger'}"
                            )
                        ], width=4),
                        dbc.Col([
                            html.Small("Game Releases", className="text-muted d-block"),
                            html.Span(
                                f"{metrics['release_growth']:+.1f}%",
                                className=f"{'text-success' if metrics['release_growth'] > 0 else 'text-danger'}"
                            )
                        ], width=4),
                        dbc.Col([
                            html.Small("Avg. Sales/Game", className="text-muted d-block"),
                            html.Span(
                                f"{metrics['avg_sales_growth']:+.1f}%",
                                className=f"{'text-success' if metrics['avg_sales_growth'] > 0 else 'text-danger'}"
                            )
                        ], width=4),
                    ]),
                ], className="mb-3"),
                html.Hr() if period != list(growth_data.keys())[-1] else None
            ])
        )
    
    return dbc.Card([
        dbc.CardHeader([
            html.H6("Growth Metrics", className="mb-0"),
            html.Small("Year-over-Year Changes", className="text-muted"),
        ]),
        dbc.CardBody(growth_items),
    ], className="h-100 shadow-sm")

def build_trends_section(df):
    """
    Build the complete trends section with all cards
    
    Parameters:
    -----------
    df : pandas.DataFrame
        The video games sales dataset
    """
    return html.Div([
        html.H4("Market Trends", className="mb-4"),
        dbc.Row([
            dbc.Col([create_sales_trend_card(df)], md=12, lg=8, className="mb-4"),
            dbc.Col([create_growth_card(df)], md=12, lg=4, className="mb-4"),
        ]),
        dbc.Row([
            dbc.Col([create_genre_trend_card(df)], md=12, lg=6, className="mb-4"),
            dbc.Col([create_platform_trend_card(df)], md=12, lg=6, className="mb-4"),
        ]),
    ])