# src/layouts/styles.py

# Color schemes
COLORS = {
    'background': '#1a1a1a',
    'card_background': '#2b2b2b',
    'text': '#ffffff',
    'primary': '#00b4d8',
    'secondary': '#0077be',
    'accent': '#48cae4',
    'success': '#2ecc71',
    'warning': '#f1c40f',
    'danger': '#e74c3c'
}

# Graph themes
GRAPH_THEME = {
    'template': 'plotly_dark',
    'layout': {
        'plot_bgcolor': COLORS['card_background'],
        'paper_bgcolor': COLORS['card_background'],
        'font': {
            'color': COLORS['text'],
            'family': 'Inter, sans-serif'
        },
        'title': {
            'font': {
                'size': 20,
                'color': COLORS['text']
            }
        },
        'legend': {
            'font': {
                'color': COLORS['text']
            }
        },
        'xaxis': {
            'gridcolor': '#404040',
            'zerolinecolor': '#404040'
        },
        'yaxis': {
            'gridcolor': '#404040',
            'zerolinecolor': '#404040'
        }
    }
}

# Common card styles
CARD_STYLE = {
    'backgroundColor': COLORS['card_background'],
    'borderRadius': '10px',
    'padding': '15px',
    'marginBottom': '20px',
    'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)'
}

# Header styles
HEADER_STYLE = {
    'color': COLORS['text'],
    'padding': '20px',
    'textAlign': 'center',
    'fontSize': '2.5rem',
    'fontWeight': 'bold',
    'fontFamily': 'Inter, sans-serif',
    'marginBottom': '30px'
}

# Tab styles
TAB_STYLE = {
    'backgroundColor': COLORS['background'],
    'color': COLORS['text'],
    'padding': '10px 15px',
    'borderRadius': '5px 5px 0 0',
    'border': f'1px solid {COLORS["card_background"]}',
    'marginRight': '2px'
}

SELECTED_TAB_STYLE = {
    **TAB_STYLE,
    'backgroundColor': COLORS['primary'],
    'borderBottom': 'none'
}

# KPI card styles
KPI_CARD_STYLE = {
    **CARD_STYLE,
    'textAlign': 'center',
    'minHeight': '120px'
}

# Chart container styles
CHART_CONTAINER_STYLE = {
    'display': 'grid',
    'gridTemplateColumns': 'repeat(auto-fit, minmax(500px, 1fr))',
    'gap': '20px',
    'padding': '20px'
}