# Application Settings
APP_TITLE = "Video Game Sales Dashboard"
APP_DESCRIPTION = "Interactive dashboard analyzing video game sales data across platforms, genres, and regions"

# Data Settings
DATA_PATH = "data/vgsales.csv"
DATE_FORMAT = "%Y"  # Year format in the dataset

# Layout Settings
LAYOUT_SETTINGS = {
    "fluid": True,  # Makes the layout responsive
    "padding": 20,  # Default padding for layout components
}

# Chart Theme Settings
CHART_THEME = "plotly_white"  # Default chart theme
CHART_COLORS = {
    "primary": "#636EFA",     # Primary color for single-color charts
    "secondary": "#EF553B",   # Secondary color for contrasts
    "success": "#00CC96",     # Success/positive indicators
    "warning": "#FFA15A",     # Warning/caution indicators
    "danger": "#EF553B",      # Danger/negative indicators
    # Color palette for multi-color charts
    "palette": [
        "#636EFA",  # blue
        "#EF553B",  # red
        "#00CC96",  # green
        "#AB63FA",  # purple
        "#FFA15A",  # orange
        "#19D3F3",  # cyan
        "#FF6692",  # pink
        "#B6E880",  # light green
        "#FF97FF",  # magenta
        "#FECB52"   # yellow
    ]
}

# Regional Settings
REGIONS = {
    "NA_Sales": "North America",
    "EU_Sales": "Europe",
    "JP_Sales": "Japan",
    "Other_Sales": "Other Regions"
}

# Chart Default Settings
CHART_DEFAULTS = {
    "margin": dict(l=20, r=20, t=40, b=20),
    "template": CHART_THEME,
    "font_size": 12,
    "title_font_size": 16,
    "legend_title_font_size": 14,
    "hoverlabel": dict(font_size=12),
}

# Card Style Settings
CARD_STYLE = {
    "margin-bottom": "20px",
    "box-shadow": "0 4px 6px rgba(0, 0, 0, 0.1)",
}

# Header Style Settings
HEADER_STYLE = {
    "background-color": "#f8f9fa",
    "padding": "1rem",
    "margin-bottom": "2rem",
    "border-bottom": "1px solid #dee2e6",
}

# Footer Style Settings
FOOTER_STYLE = {
    "background-color": "#f8f9fa",
    "padding": "1rem",
    "margin-top": "2rem",
    "border-top": "1px solid #dee2e6",
}

# Sidebar Settings
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# Content Style Settings
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

# Navigation Settings
NAV_ITEMS = [
    {"name": "Overview", "path": "/"},
    {"name": "Sales Analysis", "path": "/sales"},
    {"name": "Genre Analysis", "path": "/genre"},
    {"name": "Publisher Analysis", "path": "/publisher"},
    {"name": "Platform Analysis", "path": "/platform"}
]

# Chart Animation Settings
ANIMATION_SETTINGS = {
    "transition": dict(duration=500),
    "frame": dict(duration=500)
}

# Data Processing Settings
PROCESSING_SETTINGS = {
    "min_year": 1980,          # Minimum year to consider in analysis
    "max_games_display": 10,   # Maximum number of games to display in top lists
    "sales_threshold": 0.1,    # Minimum sales threshold (in millions)
    "top_n": {
        "publishers": 15,      # Number of top publishers to display
        "platforms": 10,       # Number of top platforms to display
        "genres": 10,         # Number of top genres to display
        "games": 10           # Number of top games to display
    }
}

# Error Messages
ERROR_MESSAGES = {
    "data_load": "Error loading data: {}",
    "processing": "Error processing data: {}",
    "visualization": "Error creating visualization: {}"
}

# Cache Settings
CACHE_CONFIG = {
    "CACHE_TYPE": "filesystem",
    "CACHE_DIR": "cache",
    "CACHE_DEFAULT_TIMEOUT": 300
}

# Debug Settings
DEBUG = True  # Set to False in production

# Server Settings
SERVER_CONFIG = {
    "host": "0.0.0.0",
    "port": 8050,
    "debug": DEBUG
}