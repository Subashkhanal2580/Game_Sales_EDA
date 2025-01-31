from dash import html
import dash_bootstrap_components as dbc
from utils.data_processing import (
    get_top_games,
    get_top_publishers,
    get_top_genres,
    format_sales
)

def create_top_games_card(df, n=5):
    """
    Create a card displaying the top n games by global sales
    
    Parameters:
    -----------
    df : pandas.DataFrame
        The video games sales dataset
    n : int
        Number of top games to display
    """
    top_games = get_top_games(df, n)
    
    game_items = []
    for idx, (name, sales, year, publisher) in enumerate(top_games, 1):
        game_items.append(
            html.Div([
                html.Div([
                    html.Span(f"{idx}.", className="me-2 text-muted"),
                    html.Span(name, className="fw-bold"),
                ], className="d-flex align-items-center"),
                html.Div([
                    html.Small(f"{year}", className="text-muted me-2"),
                    html.Small(publisher, className="text-muted"),
                    html.Span(f"${format_sales(sales)}M", className="ms-auto"),
                ], className="d-flex align-items-center mt-1"),
                html.Hr() if idx < len(top_games) else None
            ], className="mb-3")
        )
    
    return dbc.Card([
        dbc.CardHeader([
            html.H6("Top Games", className="mb-0"),
            html.Small("By Global Sales", className="text-muted"),
        ]),
        dbc.CardBody(game_items),
    ], className="h-100 shadow-sm")

def create_publisher_summary_card(df, n=5):
    """
    Create a card displaying top publishers summary
    
    Parameters:
    -----------
    df : pandas.DataFrame
        The video games sales dataset
    n : int
        Number of top publishers to display
    """
    top_publishers = get_top_publishers(df, n)
    
    publisher_items = []
    for name, sales, game_count in top_publishers:
        publisher_items.append(
            html.Div([
                html.Div([
                    html.Span(name, className="fw-bold"),
                    html.Span(f"${format_sales(sales)}M", className="ms-auto"),
                ]),
                html.Div([
                    html.Small(f"{game_count:,} games", className="text-muted"),
                    html.Small(
                        f"{(sales / df['Global_Sales'].sum() * 100):.1f}% market share",
                        className="text-muted ms-auto"
                    ),
                ], className="d-flex mt-1"),
                html.Hr() if name != top_publishers[-1][0] else None
            ], className="mb-3")
        )
    
    return dbc.Card([
        dbc.CardHeader([
            html.H6("Leading Publishers", className="mb-0"),
            html.Small("Market Share & Game Count", className="text-muted"),
        ]),
        dbc.CardBody(publisher_items),
    ], className="h-100 shadow-sm")

def create_genre_summary_card(df, n=5, title = "Genre Distribution", content = None, trend = None):
    """
    Create a card displaying genre distribution summary
    
    Parameters:
    -----------
    df : pandas.DataFrame
        The video games sales dataset
    n : int
        Number of top genres to display
    """
    top_genres = get_top_genres(df, n)
    
    genre_items = []
    max_sales = max(sales for _, sales, _ in top_genres)
    
    for genre, sales, count in top_genres:
        width_percentage = (sales / max_sales) * 100
        
        genre_items.append(
            html.Div([
                html.Div([
                    html.Span(genre, className="fw-bold"),
                    html.Span(f"${format_sales(sales)}M", className="ms-auto"),
                ]),
                html.Div([
                    dbc.Progress(
                        value=width_percentage,
                        className="my-1",
                        style={"height": "4px"}
                    ),
                ]),
                html.Div([
                    html.Small(f"{count:,} games", className="text-muted"),
                    html.Small(
                        f"{(sales / df['Global_Sales'].sum() * 100):.1f}% of sales",
                        className="text-muted ms-auto"
                    ),
                ], className="d-flex"),
                html.Hr() if genre != top_genres[-1][0] else None
            ], className="mb-3")
        )
    
    return dbc.Card([
        dbc.CardHeader([
            html.H6("Popular Genres", className="mb-0"),
            html.Small("Sales Distribution", className="text-muted"),
        ]),
        dbc.CardBody(genre_items),
    ], className="h-100 shadow-sm")

def create_regional_summary_card(df):
    """
    Create a card displaying regional sales distribution summary
    
    Parameters:
    -----------
    df : pandas.DataFrame
        The video games sales dataset
    """
    regions = {
        'NA_Sales': ('North America', 'primary'),
        'EU_Sales': ('Europe', 'success'),
        'JP_Sales': ('Japan', 'danger'),
        'Other_Sales': ('Other Regions', 'info')
    }
    
    total_sales = df['Global_Sales'].sum()
    region_items = []
    
    for col, (region_name, color) in regions.items():
        sales = df[col].sum()
        percentage = (sales / total_sales) * 100
        
        region_items.append(
            html.Div([
                html.Div([
                    html.Span(region_name, className="fw-bold"),
                    html.Span(f"${format_sales(sales)}M", className="ms-auto"),
                ]),
                dbc.Progress(
                    value=percentage,
                    className="my-1",
                    color=color,
                    style={"height": "4px"}
                ),
                html.Small(
                    f"{percentage:.1f}% of global sales",
                    className="text-muted"
                ),
                html.Hr() if col != 'Other_Sales' else None
            ], className="mb-3")
        )
    
    return dbc.Card([
        dbc.CardHeader([
            html.H6("Regional Distribution", className="mb-0"),
            html.Small("Sales by Region", className="text-muted"),
        ]),
        dbc.CardBody(region_items),
    ], className="h-100 shadow-sm")

def build_summary_section(df):
    """
    Build the complete summary section with all cards
    
    Parameters:
    -----------
    df : pandas.DataFrame
        The video games sales dataset
    """
    return html.Div([
        html.H4("Market Summary", className="mb-4"),
        dbc.Row([
            dbc.Col([create_top_games_card(df)], md=6, lg=6, className="mb-4"),
            dbc.Col([create_publisher_summary_card(df)], md=6, lg=6, className="mb-4"),
        ]),
        dbc.Row([
            dbc.Col([create_genre_summary_card(df)], md=6, lg=6, className="mb-4"),
            dbc.Col([create_regional_summary_card(df)], md=6, lg=6, className="mb-4"),
        ]),
    ])