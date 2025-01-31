from dash import html
import dash_bootstrap_components as dbc
from utils.data_processing import calculate_total_sales, get_unique_counts
import plotly.graph_objects as go

def create_stat_card(title, value, subtitle=None, icon=None, color="primary"):
    """
    Create a styled card displaying a single statistic
    
    Parameters:
    -----------
    title : str
        The title of the statistic
    value : str or number
        The main value to display
    subtitle : str, optional
        Additional context or information
    icon : str, optional
        Font Awesome icon class
    color : str, optional
        Bootstrap color class (primary, success, warning, danger, info)
    """
    return dbc.Card(
        dbc.CardBody([
            html.Div([
                html.I(className=f"fas {icon}") if icon else None,
                html.H6(title, className="text-muted mb-1"),
            ], className="d-flex justify-content-between align-items-center"),
            html.H4(value, className="mb-1"),
            html.Small(subtitle, className="text-muted") if subtitle else None,
        ]),
        className=f"border-{color} shadow-sm h-100"
    )

def format_number(num):
    """Format numbers for display with K/M/B suffixes"""
    if num >= 1e9:
        return f"{num/1e9:.1f}B"
    elif num >= 1e6:
        return f"{num/1e6:.1f}M"
    elif num >= 1e3:
        return f"{num/1e3:.1f}K"
    return str(num)

def create_stats_row(df):
    """
    Create a row of statistics cards
    
    Parameters:
    -----------
    df : pandas.DataFrame
        The video games sales dataset
    """
    # Calculate statistics
    total_sales = calculate_total_sales(df)
    counts = get_unique_counts(df)
    
    stats_cards = [
        dbc.Col([
            create_stat_card(
                "Total Global Sales",
                f"${format_number(total_sales['global'])}",
                "Lifetime sales across all regions",
                "fa-globe",
                "success"
            )
        ], md=6, lg=3),
        
        dbc.Col([
            create_stat_card(
                "Total Games",
                format_number(len(df)),
                "Number of games in database",
                "fa-gamepad",
                "primary"
            )
        ], md=6, lg=3),
        
        dbc.Col([
            create_stat_card(
                "Publishers",
                format_number(counts['publishers']),
                "Unique game publishers",
                "fa-building",
                "info"
            )
        ], md=6, lg=3),
        
        dbc.Col([
            create_stat_card(
                "Platforms",
                format_number(counts['platforms']),
                f"Across {counts['genres']} genres",
                "fa-laptop",
                "warning"
            )
        ], md=6, lg=3),
    ]
    
    return dbc.Row(stats_cards, className="g-3 mb-4")

def create_regional_stats_cards(df):
    """
    Create cards showing regional sales distribution
    
    Parameters:
    -----------
    df : pandas.DataFrame
        The video games sales dataset
    """
    regional_sales = {
        'NA_Sales': ('North America', 'fa-flag-usa', 'primary'),
        'EU_Sales': ('Europe', 'fa-euro-sign', 'success'),
        'JP_Sales': ('Japan', 'fa-yen-sign', 'danger'),
        'Other_Sales': ('Other Regions', 'fa-globe-americas', 'info')
    }
    
    regional_cards = []
    for col, (region, icon, color) in regional_sales.items():
        total = df[col].sum()
        percentage = (total / df['Global_Sales'].sum()) * 100
        
        regional_cards.append(
            dbc.Col([
                create_stat_card(
                    region,
                    f"${format_number(total)}",
                    f"{percentage:.1f}% of global sales",
                    icon,
                    color
                )
            ], md=6, lg=3)
        )
    
    return dbc.Row(regional_cards, className="g-3")

def create_year_range_card(df):
    """
    Create a card showing the year range of the dataset
    
    Parameters:
    -----------
    df : pandas.DataFrame
        The video games sales dataset
    """
    years = df['Year'].dropna()
    min_year = int(years.min())
    max_year = int(years.max())
    
    return dbc.Card(
        dbc.CardBody([
            html.H6("Data Coverage", className="text-muted mb-3"),
            html.Div([
                html.Span(f"{min_year}", className="h4"),
                html.Span(" - ", className="mx-2 text-muted"),
                html.Span(f"{max_year}", className="h4"),
            ]),
            html.Small(f"Spanning {max_year - min_year + 1} years", className="text-muted"),
        ]),
        className="border-secondary shadow-sm"
    )

def build_stats_section(df):
    """
    Build the complete statistics section
    
    Parameters:
    -----------
    df : pandas.DataFrame
        The video games sales dataset
    """
    return html.Div([
        html.H4("Key Statistics", className="mb-4"),
        create_stats_row(df),
        create_regional_stats_cards(df),
        html.Div(className="my-4"),  # Spacer
        dbc.Row([
            dbc.Col([create_year_range_card(df)], md=6, lg=4)
        ])
    ])