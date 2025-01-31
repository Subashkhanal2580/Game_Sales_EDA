from dash import html
import dash_bootstrap_components as dbc
from datetime import datetime

def create_footer():
    """
    Creates the footer component for the dashboard.
    Returns:
        dash.html.Div: A div containing the footer elements
    """
    current_year = datetime.now().year
    
    footer = html.Footer(
        dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Div(
                                    [
                                        html.Span(
                                            [
                                                "Video Game Sales Dashboard ",
                                                html.I(className="fas fa-gamepad ms-1")
                                            ],
                                            className="footer-brand"
                                        ),
                                        html.Small(
                                            f"© {current_year} All Rights Reserved",
                                            className="copyright-text ms-2"
                                        )
                                    ],
                                    className="d-flex align-items-center"
                                )
                            ],
                            xs=12,
                            md=6,
                            className="mb-3 mb-md-0"
                        ),
                        dbc.Col(
                            [
                                html.Div(
                                    [
                                        html.Span("Data Sources:", className="me-2"),
                                        html.A(
                                            "Video Games Sales Dataset",
                                            href="https://www.kaggle.com/datasets/gregorut/videogamesales",
                                            target="_blank",
                                            className="footer-link me-3"
                                        ),
                                        html.Span("•", className="mx-2"),
                                        html.A(
                                            [
                                                html.I(className="fab fa-github me-1"),
                                                "Source Code"
                                            ],
                                            href="#",
                                            target="_blank",
                                            className="footer-link"
                                        )
                                    ],
                                    className="d-flex align-items-center justify-content-md-end"
                                )
                            ],
                            xs=12,
                            md=6
                        )
                    ],
                    className="py-3"
                ),
                dbc.Row(
                    dbc.Col(
                        html.Div(
                            [
                                html.Small(
                                    "Built with ",
                                    className="tech-stack-text"
                                ),
                                html.I(
                                    className="fab fa-python mx-1",
                                    title="Python"
                                ),
                                html.Small(" Python "),
                                html.Small("•"),
                                html.I(
                                    className="fas fa-chart-bar mx-1",
                                    title="Plotly Dash"
                                ),
                                html.Small(" Plotly Dash "),
                                html.Small("•"),
                                html.I(
                                    className="fab fa-bootstrap mx-1",
                                    title="Bootstrap"
                                ),
                                html.Small(" Bootstrap")
                            ],
                            className="text-center tech-stack"
                        )
                    ),
                    className="border-top pt-3"
                )
            ],
            fluid=True,
            className="footer-container"
        ),
        className="dashboard-footer mt-auto"
    )
    
    return footer

def get_footer_styles():
    """
    Returns custom CSS styles for the footer component.
    Returns:
        dict: Dictionary containing CSS styles
    """
    styles = {
        ".dashboard-footer": {
            "background-color": "#f8f9fa",
            "border-top": "1px solid #eaeaea",
            "color": "#6c757d",
            "padding": "1rem 0",
            "margin-top": "2rem"
        },
        ".footer-brand": {
            "color": "#2c3e50",
            "font-weight": "600",
            "font-size": "1rem"
        },
        ".footer-link": {
            "color": "#3498db",
            "text-decoration": "none",
            "transition": "color 0.2s ease-in-out"
        },
        ".footer-link:hover": {
            "color": "#2980b9",
            "text-decoration": "underline"
        },
        ".copyright-text": {
            "color": "#858585"
        },
        ".tech-stack": {
            "color": "#858585",
            "font-size": "0.9rem"
        },
        ".tech-stack i": {
            "color": "#6c757d"
        }
    }
    
    return styles