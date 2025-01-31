from dash import html
import dash_bootstrap_components as dbc

def create_header():
    """
    Creates the header component for the dashboard.
    Returns:
        dash.html.Div: A div containing the header elements
    """
    header = html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.H1(
                                [
                                    html.I(className="fas fa-gamepad me-2"),  # Gaming icon
                                    "Video Game Sales Dashboard"
                                ],
                                className="header-title",
                            )
                        ],
                        width={"size": 6, "order": 1},
                    ),
                    dbc.Col(
                        [
                            dbc.Nav(
                                [
                                    dbc.NavItem(
                                        dbc.NavLink(
                                            [
                                                html.I(className="fas fa-home me-1"),
                                                "Overview"
                                            ],
                                            href="/",
                                            active="exact",
                                        )
                                    ),
                                    dbc.NavItem(
                                        dbc.NavLink(
                                            [
                                                html.I(className="fas fa-chart-line me-1"),
                                                "Sales Analysis"
                                            ],
                                            href="/sales",
                                            active="exact",
                                        )
                                    ),
                                    dbc.NavItem(
                                        dbc.NavLink(
                                            [
                                                html.I(className="fas fa-gamepad me-1"),
                                                "Platforms"
                                            ],
                                            href="/platforms",
                                            active="exact",
                                        )
                                    ),
                                ],
                                className="header-nav",
                                navbar=True,
                            )
                        ],
                        width={"size": 6, "order": 2},
                        className="d-flex justify-content-end",
                    ),
                ],
                className="header-row g-0",
                align="center",
            ),
            html.Hr(),  # Horizontal line separator
        ],
        className="dashboard-header py-3 px-4 shadow-sm",
        style={
            "background-color": "#ffffff",
            "position": "sticky",
            "top": 0,
            "zIndex": 1000,
        },
    )
    
    return header

def get_custom_styles():
    """
    Returns custom CSS styles for the header component.
    Returns:
        dict: Dictionary containing CSS styles
    """
    styles = {
        ".dashboard-header": {
            "border-bottom": "1px solid #eaeaea",
        },
        ".header-title": {
            "color": "#2c3e50",
            "font-size": "1.8rem",
            "font-weight": "600",
            "margin-bottom": "0",
        },
        ".header-nav .nav-link": {
            "color": "#576574",
            "font-weight": "500",
            "padding": "0.5rem 1rem",
            "transition": "color 0.2s ease-in-out",
        },
        ".header-nav .nav-link:hover": {
            "color": "#2c3e50",
        },
        ".header-nav .nav-link.active": {
            "color": "#3498db",
            "background-color": "transparent",
        },
    }
    
    return styles