# from dash import html
# import dash_bootstrap_components as dbc
# from typing import Dict, Optional

# from .header import create_header, get_custom_styles as get_header_styles
# from .footer import create_footer, get_footer_styles
# from .sidebar import create_sidebar, get_sidebar_styles

# def create_main_layout(app) -> html.Div:
#     """
#     Creates the main layout structure for the dashboard.
    
#     Args:
#         app: The Dash app instance
        
#     Returns:
#         dash.html.Div: The main layout container
#     """
    
#     layout = html.Div(
#         [
#             # Loading spinner for page transitions
#             dbc.Spinner(
#                 html.Div(id="page-loading-spinner"),
#                 color="primary",
#                 type="border",
#                 fullscreen=True,
#                 show_initially=False,
#             ),
            
#             # Sidebar
#             create_sidebar(is_open=True),
            
#             # Main content area
#             html.Div(
#                 [
#                     # Header
#                     create_header(),
                    
#                     # Main content container
#                     dbc.Container(
#                         [
#                             # Breadcrumb
#                             html.Nav(
#                                 dbc.Breadcrumb(
#                                     items=[],
#                                     id="page-breadcrumb",
#                                 ),
#                                 className="mt-3 mb-4"
#                             ),
                            
#                             # Page content
#                             html.Div(
#                                 id="page-content",
#                                 className="dashboard-content"
#                             ),
                            
#                             # Error message container
#                             dbc.Alert(
#                                 id="error-message",
#                                 dismissable=True,
#                                 is_open=False,
#                                 duration=4000,
#                                 style={"position": "fixed", "bottom": "20px", "right": "20px", "zIndex": 1050}
#                             ),
#                         ],
#                         fluid=True,
#                         className="px-4 py-3"
#                     ),
                    
#                     # Footer
#                     create_footer(),
#                 ],
#                 id="main-content",
#                 className="main-content"
#             ),
#         ],
#         className="dashboard-container",
#     )
    
#     return layout

# def get_all_styles() -> Dict:
#     """
#     Combines all component styles and adds main layout styles.
    
#     Returns:
#         dict: Combined CSS styles for all components
#     """
#     # Combine styles from all components
#     all_styles = {
#         **get_header_styles(),
#         **get_footer_styles(),
#         **get_sidebar_styles(),
#         **get_main_layout_styles()
#     }
    
#     return all_styles

# def get_main_layout_styles() -> Dict:
#     """
#     Returns custom CSS styles for the main layout.
    
#     Returns:
#         dict: Dictionary containing CSS styles
#     """
#     return {
#         ".dashboard-container": {
#             "display": "flex",
#             "min-height": "100vh",
#             "background-color": "#f8f9fa"
#         },
#         ".main-content": {
#             "flex": "1 1 auto",
#             "margin-left": "280px",  # Width of sidebar
#             "transition": "margin-left 0.3s ease-in-out",
#             "min-height": "100vh",
#             "display": "flex",
#             "flexDirection": "column"
#         },
#         ".main-content.sidebar-hidden": {
#             "margin-left": "0"
#         },
#         ".dashboard-content": {
#             "flex": "1 0 auto",
#             "background-color": "#ffffff",
#             "border-radius": "0.5rem",
#             "box-shadow": "0 0.125rem 0.25rem rgba(0, 0, 0, 0.075)",
#             "padding": "1.5rem",
#             "margin-bottom": "2rem"
#         }
#     }

# def create_main_layout_callbacks(app):
#     """
#     Creates callbacks for the main layout functionality.
    
#     Args:
#         app: The Dash app instance
#     """
#     from dash.dependencies import Input, Output, State
    
#     # Callback to update main content margin when sidebar is toggled
#     @app.callback(
#         Output("main-content", "className"),
#         Input("sidebar-container", "className")
#     )
#     def update_main_content_margin(sidebar_className):
#         if "hide" in sidebar_className:
#             return "main-content sidebar-hidden"
#         return "main-content"
    
#     # Callback to update page breadcrumb
#     @app.callback(
#         Output("page-breadcrumb", "items"),
#         Input("url", "pathname")
#     )
#     def update_breadcrumb(pathname):
#         paths = [p for p in pathname.split("/") if p]
#         items = [{"label": "Home", "href": "/"}]
        
#         current_path = ""
#         for path in paths:
#             current_path += f"/{path}"
#             items.append({
#                 "label": path.capitalize(),
#                 "href": current_path,
#                 "active": current_path == pathname
#             })
        
#         return items

# def init_layout(app):
#     """
#     Initializes the complete dashboard layout.
    
#     Args:
#         app: The Dash app instance
        
#     Returns:
#         dash.html.Div: The initialized layout
#     """
#     # Create the layout
#     app.layout = create_main_layout(app)
    
#     # Initialize all callbacks
#     create_main_layout_callbacks(app)
    
#     return app.layout

from dash import html
import dash_bootstrap_components as dbc
from typing import Dict

from .header import create_header, get_custom_styles as get_header_styles
from .footer import create_footer, get_footer_styles
from .sidebar import create_sidebar, get_sidebar_styles

def create_main_layout(app) -> html.Div:
    """
    Creates the main layout structure for the dashboard.
    
    Args:
        app: The Dash app instance
        
    Returns:
        dash.html.Div: The main layout container
    """
    
    layout = html.Div(
        [
            # Global loading spinner
            dbc.Spinner(
                html.Div(id="page-loading-spinner"),
                color="primary",
                spinner_style={
                    "position": "fixed",
                    "top": "50%",
                    "left": "50%",
                    "transform": "translate(-50%, -50%)"
                },
                fullscreen=True,
                show_initially=False,
            ),
            
            # Header
            create_header(),
            
            # Main container with sidebar and content
            html.Div(
                [
                    # Sidebar
                    create_sidebar(is_open=True),
                    
                    # Main content area
                    html.Div(
                        [
                            # Breadcrumb navigation
                            html.Nav(
                                dbc.Breadcrumb(
                                    items=[],
                                    id="page-breadcrumb",
                                ),
                                className="px-4 py-3 bg-light rounded-3 mb-3"
                            ),
                            
                            # Main content container
                            dbc.Container(
                                [
                                    # Page content
                                    html.Div(
                                        id="page-content",
                                        className="bg-white rounded-3 shadow-sm p-4"
                                    ),
                                ],
                                fluid=True,
                                className="mb-4"
                            ),
                            
                            # Error message toast
                            dbc.Toast(
                                id="error-message",
                                header="Error",
                                is_open=False,
                                dismissable=True,
                                duration=4000,
                                icon="danger",
                                style={
                                    "position": "fixed",
                                    "bottom": "20px",
                                    "right": "20px",
                                    "zIndex": 1050
                                }
                            ),
                            
                            # Footer
                            create_footer(),
                        ],
                        id="main-content",
                        className="main-content bg-light"
                    ),
                ],
                className="d-flex"
            ),
        ],
        className="min-vh-100 bg-light"
    )
    
    return layout

def get_main_layout_styles() -> Dict:
    """
    Returns custom CSS styles for the main layout.
    
    Returns:
        dict: Dictionary containing CSS styles
    """
    return {
        "body": {
            "background-color": "#f8f9fa",
            "min-height": "100vh"
        },
        ".main-content": {
            "margin-left": "280px",
            "min-height": "100vh",
            "width": "calc(100% - 280px)",
            "transition": "margin-left 0.3s ease-in-out, width 0.3s ease-in-out",
            "padding": "1.5rem"
        },
        ".main-content.sidebar-collapsed": {
            "margin-left": "0",
            "width": "100%"
        },
        ".page-breadcrumb": {
            "background-color": "transparent",
            "padding": "0.75rem 0"
        },
        ".toast": {
            "min-width": "300px"
        },
        "@media (max-width: 768px)": {
            ".main-content": {
                "margin-left": "0",
                "width": "100%",
                "padding": "1rem"
            }
        }
    }

def get_all_styles() -> Dict:
    """
    Combines all component styles.
    
    Returns:
        dict: Combined CSS styles for all components
    """
    return {
        **get_header_styles(),
        **get_footer_styles(),
        **get_sidebar_styles(),
        **get_main_layout_styles()
    }

def init_layout(app):
    """
    Initializes the complete dashboard layout.
    
    Args:
        app: The Dash app instance
    """
    # Set app layout
    app.layout = create_main_layout(app)
    
    # Register callbacks
    create_main_layout_callbacks(app)

def create_main_layout_callbacks(app):
    """
    Creates callbacks for the main layout functionality.
    
    Args:
        app: The Dash app instance
    """
    from dash.dependencies import Input, Output, State
    
    # Update main content margin when sidebar is toggled
    @app.callback(
        Output("main-content", "className"),
        Input("sidebar", "className"),
        prevent_initial_call=True
    )
    def update_main_content_margin(sidebar_className):
        if "collapsed" in sidebar_className:
            return "main-content bg-light sidebar-collapsed"
        return "main-content bg-light"
    
    # Update breadcrumb based on current path
    @app.callback(
        Output("page-breadcrumb", "items"),
        Input("url", "pathname")
    )
    def update_breadcrumb(pathname):
        if not pathname:
            return [{"label": "Home", "href": "/"}]
            
        paths = [p for p in pathname.split("/") if p]
        items = [{"label": "Home", "href": "/"}]
        
        current_path = ""
        for path in paths:
            current_path += f"/{path}"
            items.append({
                "label": path.replace("-", " ").title(),
                "href": current_path,
                "active": current_path == pathname
            })
        
        return items
    
    # Update page title based on current path
    @app.callback(
        Output("page-title", "children"),
        Input("url", "pathname")
    )
    def update_page_title(pathname):
        if not pathname or pathname == "/":
            return "Dashboard Overview"
            
        paths = [p for p in pathname.split("/") if p]
        return paths[-1].replace("-", " ").title()
        
    # Error message handling
    @app.callback(
        [Output("error-message", "is_open"),
         Output("error-message", "children")],
        [Input("error-trigger", "data")],
        prevent_initial_call=True
    )
    def show_error_message(error_data):
        if error_data:
            return True, error_data.get("message", "An error occurred")
        return False, ""