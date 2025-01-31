"""
Log viewer page for the Video Game Sales Dashboard.
"""

from dash import html, dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc
from pathlib import Path
import logging
from utils.logging_setup import list_logs, read_log_file

def create_log_viewer_layout():
    """Create the layout for the log viewer page."""
    available_logs = list_logs()
    
    return html.Div([
        html.H2("Log Viewer", className="mb-4"),
        
        # Log file selector
        dbc.Row([
            dbc.Col([
                html.Label("Select Log File:", className="mb-2"),
                dcc.Dropdown(
                    id='log-file-selector',
                    options=[{'label': log, 'value': log} for log in available_logs],
                    value=available_logs[0] if available_logs else None,
                    clearable=False,
                    className="mb-3"
                ),
            ], width=6),
            dbc.Col([
                html.Div([
                    dbc.Button(
                        "Refresh Logs",
                        id="refresh-logs-button",
                        color="primary",
                        className="me-2"
                    ),
                    dbc.Button(
                        "Clear Display",
                        id="clear-logs-button",
                        color="secondary"
                    ),
                ], className="d-flex align-items-end h-100 mb-3")
            ], width=6),
        ]),
        
        # Log display area
        dbc.Card([
            dbc.CardBody([
                html.Pre(
                    id="log-content",
                    className="mb-0",
                    style={
                        'maxHeight': '600px',
                        'overflowY': 'auto',
                        'whiteSpace': 'pre-wrap',
                        'fontFamily': 'monospace',
                        'fontSize': '12px'
                    }
                )
            ])
        ]),
        
        # Auto-refresh toggle
        dbc.Row([
            dbc.Col([
                dbc.Checkbox(
                    id="auto-refresh-toggle",
                    label="Auto-refresh logs (every 10 seconds)",
                    value=False,
                    className="mt-3"
                ),
                dcc.Interval(
                    id='log-refresh-interval',
                    interval=10*1000,  # 10 seconds
                    disabled=True
                )
            ])
        ])
    ], className="p-4")

@callback(
    Output('log-content', 'children'),
    [Input('log-file-selector', 'value'),
     Input('refresh-logs-button', 'n_clicks'),
     Input('log-refresh-interval', 'n_intervals')],
    prevent_initial_call=False
)
def update_log_content(selected_file, n_clicks, n_intervals):
    """Update the log content display."""
    if not selected_file:
        return "No log file selected"
    
    return read_log_file(selected_file)

@callback(
    Output('log-file-selector', 'options'),
    Output('log-file-selector', 'value'),
    Input('refresh-logs-button', 'n_clicks'),
    State('log-file-selector', 'value'),
    prevent_initial_call=False
)
def refresh_log_files(n_clicks, current_value):
    """Refresh the list of available log files."""
    available_logs = list_logs()
    options = [{'label': log, 'value': log} for log in available_logs]
    
    # Keep current selection if it still exists
    if current_value in [opt['value'] for opt in options]:
        new_value = current_value
    else:
        new_value = available_logs[0] if available_logs else None
        
    return options, new_value

@callback(
    Output('log-refresh-interval', 'disabled'),
    Input('auto-refresh-toggle', 'value')
)
def toggle_auto_refresh(enabled):
    """Toggle the auto-refresh interval."""
    return not enabled

@callback(
    Output('log-content', 'children', allow_duplicate=True),
    Input('clear-logs-button', 'n_clicks'),
    prevent_initial_call=True
)
def clear_log_display(n_clicks):
    """Clear the log display area."""
    return ""