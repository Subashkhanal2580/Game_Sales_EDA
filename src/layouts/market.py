# src/layouts/market.py
from dash import html, dcc
import plotly.graph_objects as go
import pandas as pd
from .styles import COLORS, GRAPH_THEME, CARD_STYLE, KPI_CARD_STYLE, CHART_CONTAINER_STYLE

def create_market_layout(df):
   yearly_sales = df.groupby('Year')['Global_Sales'].sum().reset_index()
   yearly_sales['YoY_Growth'] = yearly_sales['Global_Sales'].pct_change() * 100
   
   latest_year = yearly_sales['Year'].max()
   current_sales = yearly_sales[yearly_sales['Year'] == latest_year]['Global_Sales'].values[0]
   yoy_growth = yearly_sales[yearly_sales['Year'] == latest_year]['YoY_Growth'].values[0]
   total_publishers = df['Publisher'].nunique()
   
   regional_dist = pd.DataFrame({
       'Region': ['North America', 'Europe', 'Japan', 'Other'],
       'Sales': [df['NA_Sales'].sum(), df['EU_Sales'].sum(), 
                df['JP_Sales'].sum(), df['Other_Sales'].sum()]
   })

   market_concentration = df.groupby('Publisher')['Global_Sales'].sum().sort_values(ascending=False)
   top_5_share = (market_concentration.head(5).sum() / market_concentration.sum()) * 100

   layout = GRAPH_THEME['layout'].copy()
   layout.pop('title', None)  # Remove title from base layout

   return html.Div([
       html.Div([
           html.Div([
               html.H4("Annual Sales", style={'color': COLORS['text']}),
               html.H2(f"${current_sales:.1f}B", style={'color': COLORS['primary']}),
               html.P(f"{yoy_growth:.1f}% YoY", 
                     style={'color': COLORS['success'] if yoy_growth > 0 else COLORS['danger']})
           ], style=KPI_CARD_STYLE),
           
           html.Div([
               html.H4("Active Publishers", style={'color': COLORS['text']}),
               html.H2(f"{total_publishers:,}", style={'color': COLORS['primary']})
           ], style=KPI_CARD_STYLE),
           
           html.Div([
               html.H4("Market Concentration", style={'color': COLORS['text']}),
               html.H2(f"{top_5_share:.1f}%", style={'color': COLORS['primary']}),
               html.P("Top 5 Publishers Share", style={'color': COLORS['accent']})
           ], style=KPI_CARD_STYLE)
       ], style={'display': 'grid', 'gridTemplateColumns': 'repeat(auto-fit, minmax(250px, 1fr))', 'gap': '20px'}),

       html.Div([
           html.Div([
               dcc.Graph(
                   id='sales-trend-graph',
                   figure=go.Figure(data=[
                       go.Scatter(
                           x=yearly_sales['Year'],
                           y=yearly_sales['Global_Sales'],
                           mode='lines+markers',
                           name='Global Sales',
                           line=dict(color=COLORS['primary'], width=3)
                       )
                   ]).update_layout(
                       **layout,
                       title='Global Sales Trends'
                   )
               )
           ], style=CARD_STYLE),

           html.Div([
               dcc.Graph(
                   id='regional-dist-graph',
                   figure=go.Figure(data=[
                       go.Pie(
                           labels=regional_dist['Region'],
                           values=regional_dist['Sales'],
                           hole=0.4,
                           marker=dict(colors=[COLORS['primary'], COLORS['secondary'], 
                                             COLORS['accent'], COLORS['warning']])
                       )
                   ]).update_layout(
                       **layout,
                       title='Regional Distribution'
                   )
               )
           ], style=CARD_STYLE)
       ], style=CHART_CONTAINER_STYLE),

       html.Div([
           html.Div([
               dcc.Graph(
                   id='publisher-share-graph',
                   figure=go.Figure(data=[
                       go.Bar(
                           x=market_concentration.head(10).index,
                           y=market_concentration.head(10).values,
                           marker_color=COLORS['primary']
                       )
                   ]).update_layout(
                       **layout,
                       title='Top 10 Publishers Market Share',
                       xaxis_tickangle=-45
                   )
               )
           ], style=CARD_STYLE),

           html.Div([
               dcc.Graph(
                   id='growth-trend-graph',
                   figure=go.Figure(data=[
                       go.Bar(
                           x=yearly_sales['Year'],
                           y=yearly_sales['YoY_Growth'],
                           marker_color=yearly_sales['YoY_Growth'].apply(
                               lambda x: COLORS['success'] if x > 0 else COLORS['danger']
                           )
                       )
                   ]).update_layout(
                       **layout,
                       title='Year-over-Year Growth Rate'
                   )
               )
           ], style=CARD_STYLE)
       ], style=CHART_CONTAINER_STYLE)
   ])