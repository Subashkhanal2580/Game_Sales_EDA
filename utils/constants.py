"""
Constants and configuration values for the video game sales dashboard.
"""

from typing import Dict, List
from pathlib import Path

# File paths
DATA_DIR = Path("data")
ASSETS_DIR = Path("assets")
DEFAULT_DATA_FILE = DATA_DIR / "vgsales.csv"

# Data constants
SALES_COLUMNS = ['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales', 'Global_Sales']
CATEGORICAL_COLUMNS = ['Platform', 'Genre', 'Publisher']
NUMERIC_COLUMNS = ['Year'] + SALES_COLUMNS

# Region mappings
REGIONS = {
    'NA_Sales': 'North America',
    'EU_Sales': 'Europe',
    'JP_Sales': 'Japan',
    'Other_Sales': 'Other Regions',
    'Global_Sales': 'Global'
}

# Color schemes
COLOR_SCHEMES = {
    # Main color palette for general use
    'primary': {
        'main': '#1f77b4',
        'light': '#aec7e8',
        'dark': '#1f77b4',
        'text': '#2c3e50'
    },
    # Color scheme for different regions
    'regions': {
        'NA_Sales': '#1f77b4',     # Blue
        'EU_Sales': '#2ca02c',     # Green
        'JP_Sales': '#ff7f0e',     # Orange
        'Other_Sales': '#9467bd',  # Purple
        'Global_Sales': '#d62728'  # Red
    },
    # Color scheme for genres
    'genres': {
        'Action': '#1f77b4',
        'Sports': '#ff7f0e',
        'Platform': '#2ca02c',
        'Racing': '#d62728',
        'Role-Playing': '#9467bd',
        'Puzzle': '#8c564b',
        'Misc': '#e377c2',
        'Shooter': '#7f7f7f',
        'Simulation': '#bcbd22',
        'Fighting': '#17becf',
        'Adventure': '#aec7e8',
        'Strategy': '#ffbb78'
    },
    # Gradient color schemes for heatmaps
    'heatmap': {
        'sales': ['#f7fbff', '#6baed6', '#08519c'],
        'correlation': ['#f7fbff', '#c6dbef', '#4292c6', '#2171b5', '#084594']
    }
}

# Chart configurations
CHART_CONFIG = {
    # Default chart sizes
    'sizes': {
        'small': {'width': 400, 'height': 300},
        'medium': {'width': 600, 'height': 400},
        'large': {'width': 800, 'height': 500},
        'wide': {'width': 1000, 'height': 400}
    },
    # Default margins
    'margins': {
        'small': {'t': 20, 'r': 20, 'b': 30, 'l': 40},
        'medium': {'t': 20, 'r': 30, 'b': 40, 'l': 50},
        'large': {'t': 30, 'r': 40, 'b': 50, 'l': 60},
        'wide': {'t': 60, 'r': 20, 'b': 50, 'l': 60}
    },
    # Animation defaults
    'animation': {
        'duration': 500,
        'easing': 'cubic-in-out'
    }
}

# Time periods for filtering
TIME_PERIODS = {
    'all_time': 'All Time',
    'last_5_years': 'Last 5 Years',
    'last_10_years': 'Last 10 Years',
    'last_20_years': 'Last 20 Years',
    'by_decade': {
        '1980s': (1980, 1989),
        '1990s': (1990, 1999),
        '2000s': (2000, 2009),
        '2010s': (2010, 2019)
    }
}

# Default values for analysis
ANALYSIS_DEFAULTS = {
    'top_n': 10,
    'min_sales': 0.01,
    'year_range': (1980, 2020),
    'sales_unit': 'millions',
    'significant_threshold': 0.01
}

# Text content
TEXT_CONTENT = {
    'headers': {
        'sales_analysis': 'Sales Analysis',
        'platform_comparison': 'Platform Comparison',
        'genre_distribution': 'Genre Distribution',
        'publisher_analysis': 'Publisher Analysis',
        'regional_breakdown': 'Regional Breakdown',
        'time_trends': 'Time Trends'
    },
    'tooltips': {
        'sales': 'Sales (in millions)',
        'market_share': 'Market Share (%)',
        'year_over_year': 'Year-over-Year Growth (%)',
        'regional_split': 'Regional Sales Distribution'
    }
}

# Layout constants
LAYOUT = {
    'sidebar_width': 250,
    'header_height': 60,
    'footer_height': 40,
    'padding': {
        'small': 8,
        'medium': 16,
        'large': 24
    },
    'grid_breakpoints': {
        'sm': 576,
        'md': 768,
        'lg': 992,
        'xl': 1200
    }
}

# Cache settings
CACHE_CONFIG = {
    'timeout': 3600,  # 1 hour
    'max_entries': 100
}

# Error messages
ERROR_MESSAGES = {
    'data_loading': 'Error loading data: {}',
    'data_processing': 'Error processing data: {}',
    'visualization': 'Error creating visualization: {}',
    'invalid_filter': 'Invalid filter parameters: {}',
    'missing_data': 'Required data not found: {}'
}

# Export settings
EXPORT_CONFIG = {
    'formats': ['csv', 'xlsx', 'json'],
    'chart_formats': ['png', 'svg', 'pdf'],
    'default_format': 'csv'
}

# Simplified color palette for basic usage
COLORS = {
    'primary': '#1f77b4',     # Blue
    'secondary': '#2ca02c',   # Green
    'tertiary': '#ff7f0e',    # Orange
    'quaternary': '#9467bd',  # Purple
    'success': '#2ecc71',     # Green
    'warning': '#f1c40f',     # Yellow
    'danger': '#e74c3c',      # Red
    'info': '#3498db',        # Light Blue
    'light': '#ecf0f1',       # Light Gray
    'dark': '#2c3e50',        # Dark Blue
    'muted': '#95a5a6',       # Gray
    'white': '#ffffff',
    'black': '#000000'
}

# Chart template with consistent styling
CHART_TEMPLATE = {
    'layout': {
        'font': {
            'family': 'Arial, sans-serif',
            'size': 12,
            'color': COLORS['dark']
        },
        'plot_bgcolor': 'white',
        'paper_bgcolor': 'white',
        'titlefont': {
            'size': 16,
            'color': COLORS['dark']
        },
        'margin': {'t': 60, 'r': 30, 'b': 60, 'l': 60},
        'hovermode': 'closest',
        'showlegend': True,
        'legend': {
            'orientation': 'h',
            'yanchor': 'bottom',
            'y': 1.02,
            'xanchor': 'right',
            'x': 1
        },
        'xaxis': {
            'showgrid': True,
            'gridcolor': COLORS['light'],
            'gridwidth': 1,
            'zeroline': False,
            'showline': True,
            'linecolor': COLORS['muted'],
            'linewidth': 1,
            'ticks': 'outside'
        },
        'yaxis': {
            'showgrid': True,
            'gridcolor': COLORS['light'],
            'gridwidth': 1,
            'zeroline': False,
            'showline': True,
            'linecolor': COLORS['muted'],
            'linewidth': 1,
            'ticks': 'outside'
        }
    }
}