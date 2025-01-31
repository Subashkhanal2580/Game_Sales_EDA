
from dash import html, dcc
import dash_bootstrap_components as dbc
from typing import List, Dict, Optional

def create_sidebar(is_open: bool = True) -> html.Div:
    """
    Creates the sidebar navigation component for the dashboard.
    
    Args:
        is_open (bool): Initial state of the sidebar
        
    Returns:
        dash.html.Div: A div containing the sidebar elements
    """
    sidebar = html.Div(
        [
            # Sidebar Header with Toggle
            html.Div(
                [
                    html.Button(
                        html.I(className="fas fa-bars"),
                        id="sidebar-toggle",
                        className="btn btn-link text-dark p-0 border-0"
                    ),
                    html.H5("Navigation", className="mb-0 ms-3")
                ],
                className="d-flex align-items-center py-3"
            ),
            
            html.Hr(className="my-3"),
            
            # Main Navigation
            dbc.Nav(
                [
                    # Dashboard Overview
                    dbc.NavItem(
                        dbc.NavLink(
                            [
                                html.I(className="fas fa-home"),
                                html.Span("Dashboard Overview", className="ms-2")
                            ],
                            href="/",
                            active="exact",
                            className="d-flex align-items-center"
                        ),
                        className="mb-2"
                    ),
                    
                    # Sales Analysis Section
                    html.Div(
                        [
                            html.P(
                                [
                                    html.I(className="fas fa-chart-line"),
                                    html.Span("Sales Analysis", className="ms-2")
                                ],
                                className="fw-bold mb-2 text-muted d-flex align-items-center"
                            ),
                            dbc.Nav(
                                [
                                    dbc.NavLink(
                                        "Global Sales",
                                        href="/sales/global",
                                        active="exact",
                                        className="rounded-1"
                                    ),
                                    dbc.NavLink(
                                        "Regional Analysis",
                                        href="/sales/regional",
                                        active="exact",
                                        className="rounded-1"
                                    ),
                                    dbc.NavLink(
                                        "Yearly Trends",
                                        href="/sales/trends",
                                        active="exact",
                                        className="rounded-1"
                                    ),
                                ],
                                vertical=True,
                                pills=True,
                                className="flex-column ps-3 nav-section"
                            ),
                        ],
                        className="mb-3"
                    ),
                    
                    # Genre Analysis Section
                    html.Div(
                        [
                            html.P(
                                [
                                    html.I(className="fas fa-gamepad"),
                                    html.Span("Genre Analysis", className="ms-2")
                                ],
                                className="fw-bold mb-2 text-muted d-flex align-items-center"
                            ),
                            dbc.Nav(
                                [
                                    dbc.NavLink(
                                        "Genre Distribution",
                                        href="/genre/distribution",
                                        active="exact",
                                        className="rounded-1"
                                    ),
                                    dbc.NavLink(
                                        "Top Genres",
                                        href="/genre/top",
                                        active="exact",
                                        className="rounded-1"
                                    ),
                                    dbc.NavLink(
                                        "Genre Trends",
                                        href="/genre/trends",
                                        active="exact",
                                        className="rounded-1"
                                    ),
                                ],
                                vertical=True,
                                pills=True,
                                className="flex-column ps-3 nav-section"
                            ),
                        ],
                        className="mb-3"
                    ),
                    
                    # Publisher Analysis Section
                    html.Div(
                        [
                            html.P(
                                [
                                    html.I(className="fas fa-building"),
                                    html.Span("Publisher Analysis", className="ms-2")
                                ],
                                className="fw-bold mb-2 text-muted d-flex align-items-center"
                            ),
                            dbc.Nav(
                                [
                                    dbc.NavLink(
                                        "Top Publishers",
                                        href="/publisher/top",
                                        active="exact",
                                        className="rounded-1"
                                    ),
                                    dbc.NavLink(
                                        "Publisher Comparison",
                                        href="/publisher/comparison",
                                        active="exact",
                                        className="rounded-1"
                                    ),
                                ],
                                vertical=True,
                                pills=True,
                                className="flex-column ps-3 nav-section"
                            ),
                        ],
                        className="mb-3"
                    ),
                ],
                vertical=True,
                className="mb-4"
            ),
            
            html.Hr(className="my-3"),
            
            # Filters Section
            html.Div(
                [
                    html.H6(
                        [
                            html.I(className="fas fa-filter"),
                            html.Span("Filters", className="ms-2")
                        ],
                        className="d-flex align-items-center mb-3"
                    ),
                    
                    # Year Range Filter
                    html.Div(
                        [
                            html.Label(
                                "Year Range:",
                                className="form-label fw-medium mb-2"
                            ),
                            dcc.RangeSlider(
                                id="year-range-slider",
                                min=1980,
                                max=2020,
                                step=1,
                                value=[1980, 2020],
                                marks={
                                    1980: {'label': '1980', 'style': {'transform': 'rotate(-45deg)'}},
                                    1990: {'label': '1990', 'style': {'transform': 'rotate(-45deg)'}},
                                    2000: {'label': '2000', 'style': {'transform': 'rotate(-45deg)'}},
                                    2010: {'label': '2010', 'style': {'transform': 'rotate(-45deg)'}},
                                    2020: {'label': '2020', 'style': {'transform': 'rotate(-45deg)'}}
                                },
                                className="mt-1 mb-4"
                            ),
                        ],
                        className="mb-3"
                    ),
                    
                    # Platform Filter
                    html.Div(
                        [
                            html.Label(
                                "Platform:",
                                className="form-label fw-medium mb-2"
                            ),
                            dcc.Dropdown(
                                id="platform-dropdown",
                                multi=True,
                                placeholder="Select platforms...",
                                className="dash-bootstrap"
                            ),
                        ],
                        className="mb-3"
                    ),
                ],
                className="sidebar-filters"
            ),
        ],
        id="sidebar",
        className=f"sidebar bg-white shadow-sm {'' if is_open else 'collapsed'}"
    )
    
    return sidebar

def get_sidebar_styles() -> Dict:
    """
    Returns custom CSS styles for the sidebar component.
    
    Returns:
        dict: Dictionary containing CSS styles
    """
    return {
        ".sidebar": {
            "width": "280px",
            "height": "100vh",
            "position": "fixed",
            "top": "0",
            "left": "0",
            "padding": "1rem",
            "transition": "transform 0.3s ease-in-out",
            "overflow-y": "auto",
            "z-index": "1030"
        },
        ".sidebar.collapsed": {
            "transform": "translateX(-280px)"
        },
        ".sidebar .nav-link": {
            "color": "#495057",
            "padding": "0.5rem 1rem",
            "transition": "all 0.2s ease-in-out"
        },
        ".sidebar .nav-link:hover": {
            "background-color": "#f8f9fa",
            "color": "#2c3e50"
        },
        ".sidebar .nav-link.active": {
            "background-color": "#e9ecef",
            "color": "#2c3e50",
            "font-weight": "500"
        },
        ".nav-section .nav-link": {
            "font-size": "0.9rem",
            "padding": "0.4rem 1rem"
        },
        ".sidebar-filters": {
            "padding-bottom": "2rem"
        },
        ".dash-bootstrap .Select-control": {
            "border-color": "#dee2e6",
            "border-radius": "0.375rem"
        },
        ".dash-bootstrap .Select-menu-outer": {
            "border-bottom-left-radius": "0.375rem",
            "border-bottom-right-radius": "0.375rem",
            "box-shadow": "0 0.125rem 0.25rem rgba(0, 0, 0, 0.075)"
        },
        "@media (max-width: 768px)": {
            ".sidebar": {
                "transform": "translateX(-280px)"
            },
            ".sidebar.show": {
                "transform": "translateX(0)"
            }
        }
    }

def create_sidebar_callbacks(app):
    """
    Creates the callbacks for the sidebar functionality.
    
    Args:
        app: The Dash app instance
    """
    from dash.dependencies import Input, Output, State
    
    @app.callback(
        Output("sidebar", "className"),
        Input("sidebar-toggle", "n_clicks"),
        State("sidebar", "className"),
        prevent_initial_call=True
    )
    def toggle_sidebar(n_clicks, className):
        if n_clicks:
            if "collapsed" in className:
                return className.replace("collapsed", "").strip()
            else:
                return f"{className} collapsed".strip()
        return className