# src/layouts/competitive.py
from dash import html, dcc
import plotly.graph_objects as go
import plotly.express as px
from .styles import COLORS, GRAPH_THEME, CARD_STYLE, KPI_CARD_STYLE, CHART_CONTAINER_STYLE

def create_competitive_layout(df):
   publisher_data = df.groupby('Publisher').agg({
       'Global_Sales': ['sum', 'mean'],
       'Name': 'count',
       'Genre': 'nunique'
   }).reset_index()
   
   top_publisher = publisher_data.iloc[0]['Publisher']
   market_leader_share = (publisher_data.iloc[0][('Global_Sales', 'sum')] / 
                         publisher_data[('Global_Sales', 'sum')].sum()) * 100

   layout = GRAPH_THEME['layout'].copy()
   layout.pop('title', None)

   return html.Div([
       html.Div([
           html.Div([
               html.H4("Market Leader", style={'color': COLORS['text']}),
               html.H2(f"{top_publisher}", style={'color': COLORS['primary']}),
               html.P(f"{market_leader_share:.1f}% Share", style={'color': COLORS['accent']})
           ], style=KPI_CARD_STYLE)
       ], style={'display': 'grid', 'gridTemplateColumns': 'repeat(auto-fit, minmax(250px, 1fr))', 'gap': '20px'}),

       html.Div([
           html.Div([
               dcc.Graph(
                   id='publisher-market-share',
                   figure=go.Figure(data=[
                       go.Pie(
                           labels=publisher_data['Publisher'].head(10),
                           values=publisher_data[('Global_Sales', 'sum')].head(10),
                           hole=0.4,
                           marker=dict(colors=[COLORS['primary'], COLORS['secondary'], 
                                             COLORS['accent'], COLORS['warning']])
                       )
                   ]).update_layout(
                       **layout,
                       title='Top 10 Publishers Market Share'
                   )
               )
           ], style=CARD_STYLE),

           html.Div([
               dcc.Graph(
                   id='publisher-performance',
                   figure=go.Figure(data=[
                       go.Scatter(
                           x=publisher_data[('Name', 'count')],
                           y=publisher_data[('Global_Sales', 'mean')],
                           mode='markers',
                           marker=dict(
                               size=publisher_data[('Global_Sales', 'sum')] * 50,
                               color=publisher_data['Genre'],
                               colorscale=[[0, COLORS['secondary']], [1, COLORS['primary']]]
                           ),
                           text=publisher_data['Publisher']
                       )
                   ]).update_layout(
                       **layout,
                       title='Publisher Performance Analysis'
                   )
               )
           ], style=CARD_STYLE)
       ], style=CHART_CONTAINER_STYLE)
   ])