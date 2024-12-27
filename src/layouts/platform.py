# src/layouts/platform.py
from dash import html, dcc
import plotly.graph_objects as go
import plotly.express as px
from .styles import COLORS, GRAPH_THEME, CARD_STYLE, KPI_CARD_STYLE, CHART_CONTAINER_STYLE

def create_platform_layout(df):
   platform_data = df.groupby('Platform').agg({
       'Global_Sales': ['sum', 'mean'],
       'Name': 'count'
   }).reset_index()
   
   top_platform = platform_data.iloc[platform_data[('Global_Sales', 'sum')].idxmax()]['Platform']
   top_sales = platform_data[('Global_Sales', 'sum')].max()
   platform_count = len(platform_data)

   layout = GRAPH_THEME['layout'].copy()
   layout.pop('title', None)

   return html.Div([
       html.Div([
           html.Div([
               html.H4("Top Platform", style={'color': COLORS['text']}),
               html.H2(f"{top_platform}", style={'color': COLORS['primary']}),
               html.P(f"${top_sales:.1f}B Sales", style={'color': COLORS['accent']})
           ], style=KPI_CARD_STYLE),
           
           html.Div([
               html.H4("Total Platforms", style={'color': COLORS['text']}),
               html.H2(f"{platform_count}", style={'color': COLORS['primary']})
           ], style=KPI_CARD_STYLE)
       ], style={'display': 'grid', 'gridTemplateColumns': 'repeat(auto-fit, minmax(250px, 1fr))', 'gap': '20px'}),

       html.Div([
           html.Div([
               dcc.Graph(
                   id='platform-share',
                   figure=go.Figure(data=[
                       go.Bar(
                           x=platform_data['Platform'],
                           y=platform_data[('Global_Sales', 'sum')],
                           marker_color=COLORS['primary']
                       )
                   ]).update_layout(
                       **layout,
                       title='Platform Market Share'
                   )
               )
           ], style=CARD_STYLE),

           html.Div([
               dcc.Graph(
                   id='platform-performance',
                   figure=go.Figure(data=[
                       go.Scatter(
                           x=platform_data[('Name', 'count')],
                           y=platform_data[('Global_Sales', 'mean')],
                           mode='markers+text',
                           text=platform_data['Platform'],
                           textposition='top center',
                           marker=dict(
                               size=platform_data[('Global_Sales', 'sum')] * 20,
                               color=platform_data[('Global_Sales', 'sum')],
                               colorscale=[[0, COLORS['secondary']], [1, COLORS['primary']]]
                           )
                       )
                   ]).update_layout(
                       **layout,
                       title='Platform Performance Matrix'
                   )
               )
           ], style=CARD_STYLE)
       ], style=CHART_CONTAINER_STYLE)
   ])