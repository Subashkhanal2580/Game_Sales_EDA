# src/callbacks/tab_callbacks.py
from dash.dependencies import Input, Output
from dash import html
from ..layouts.market import create_market_layout
from ..layouts.time import create_time_layout
from ..layouts.platform import create_platform_layout
from ..layouts.geographic import create_geographic_layout
from ..layouts.competitive import create_competitive_layout

def register_callbacks(app, df, preprocessor):
   """Register all callbacks for the dashboard."""
   
   @app.callback(
       Output('tab-content', 'children'),
       Input('tabs', 'value')
   )
   def render_content(tab):
       """Render content based on selected tab."""
       try:
           if tab == 'market':
               return create_market_layout(df, preprocessor)
           elif tab == 'time':
               return create_time_layout(df, preprocessor)
           elif tab == 'platform':
               return create_platform_layout(df, preprocessor)
           elif tab == 'geographic':
               return create_geographic_layout(df, preprocessor)
           elif tab == 'competitive':
               return create_competitive_layout(df, preprocessor)
           return html.Div(f"Unknown tab value: {tab}")
       except Exception as e:
           print(f"Error rendering {tab} tab:", str(e))
           return html.Div(
               html.P(f"Error loading {tab} content: {str(e)}", 
                     style={'color': 'red', 'padding': '20px'})
           )

   @app.callback(
       Output('download-data', 'data'),
       Input('btn-download', 'n_clicks'),
       prevent_initial_call=True
   )
   def download_report(n_clicks):
       """Generate downloadable report."""
       if n_clicks:
           try:
               data = df.to_csv(index=False)
               return dict(
                   content=data,
                   filename='game_sales_analysis.csv'
               )
           except Exception as e:
               print("Error generating report:", str(e))
               return None