# src/app.py
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from .layouts.market import create_market_layout
from .layouts.time import create_time_layout
from .layouts.platform import create_platform_layout
from .layouts.geographic import create_geographic_layout
from .layouts.competitive import create_competitive_layout
from .data_processing.preprocessor import DataPreprocessor
from .layouts.styles import COLORS, TAB_STYLE, SELECTED_TAB_STYLE, HEADER_STYLE

def create_app():
   app = Dash(
       __name__,
       external_stylesheets=[
           dbc.themes.CYBORG,
           'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap'
       ],
       meta_tags=[
           {'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0'}
       ]
   )
   
   preprocessor = DataPreprocessor('data/vgsales.csv')
   df = preprocessor.df

   app.layout = html.Div([
       html.Nav([
           html.Div([
               html.Img(src='assets/logo.png', style={'height': '40px'}),
               html.H1('GameSight Analytics', style={'color': COLORS['text'], 'marginLeft': '15px'})
           ], style={'display': 'flex', 'alignItems': 'center'}),
           
           html.Div([
               dbc.Button('Download Report', id='btn-download', color='primary', className='mr-2'),
               dcc.Download(id='download-data')
           ], style={'display': 'flex', 'gap': '10px'})
       ], style={
           'backgroundColor': COLORS['card_background'],
           'padding': '15px 30px',
           'display': 'flex',
           'justifyContent': 'space-between',
           'alignItems': 'center',
           'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'
       }),

       html.Div([
           dcc.Tabs(
               id='tabs',
               value='market',
               children=[
                   dcc.Tab(label='Market Overview', value='market',
                          style=TAB_STYLE, selected_style=SELECTED_TAB_STYLE),
                   dcc.Tab(label='Time Analysis', value='time',
                          style=TAB_STYLE, selected_style=SELECTED_TAB_STYLE),
                   dcc.Tab(label='Platform Analytics', value='platform',
                          style=TAB_STYLE, selected_style=SELECTED_TAB_STYLE),
                   dcc.Tab(label='Geographic Insights', value='geographic',
                          style=TAB_STYLE, selected_style=SELECTED_TAB_STYLE),
                   dcc.Tab(label='Competitive Analysis', value='competitive',
                          style=TAB_STYLE, selected_style=SELECTED_TAB_STYLE)
               ],
               style={'backgroundColor': COLORS['background'],
                      'padding': '20px 20px 0 20px'}
           ),
           
           html.Div(
               id='tab-content',
               style={
                   'backgroundColor': COLORS['background'],
                   'padding': '20px',
                   'minHeight': 'calc(100vh - 180px)'
               }
           )
       ], style={'backgroundColor': COLORS['background']}),

       html.Footer([
           html.P('© 2024 GameSight Analytics', 
                 style={'color': COLORS['text'], 'opacity': '0.7'})
       ], style={
           'backgroundColor': COLORS['card_background'],
           'padding': '20px',
           'textAlign': 'center',
           'marginTop': 'auto'
       })
   ], style={
       'backgroundColor': COLORS['background'],
       'minHeight': '100vh',
       'display': 'flex',
       'flexDirection': 'column'
   })

   @app.callback(
       Output('tab-content', 'children'),
       Input('tabs', 'value')
   )
   def render_content(tab):
       try:
           if tab == 'market':
               return create_market_layout(df=df)
           elif tab == 'time':
               return create_time_layout(df=df)
           elif tab == 'platform':
               return create_platform_layout(df=df)
           elif tab == 'geographic':
               return create_geographic_layout(df=df)
           elif tab == 'competitive':
               return create_competitive_layout(df=df)
       except Exception as e:
           return html.Div(f"Error loading {tab} content: {str(e)}")

   @app.callback(
       Output('download-data', 'data'),
       Input('btn-download', 'n_clicks'),
       prevent_initial_call=True
   )
   def download_report(n_clicks):
       if n_clicks:
           return dict(
               content=df.to_csv(index=False),
               filename='game_sales_analysis.csv'
           )

   return app