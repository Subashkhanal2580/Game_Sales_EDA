# src/layouts/geographic.py
from dash import html, dcc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from .styles import COLORS, GRAPH_THEME, CARD_STYLE, KPI_CARD_STYLE, CHART_CONTAINER_STYLE

def create_geographic_layout(df):
   # Regional sales data
   regional_dist = pd.DataFrame({
       'Region': ['North America', 'Europe', 'Japan', 'Other'],
       'Sales': [df['NA_Sales'].sum(), df['EU_Sales'].sum(), 
                df['JP_Sales'].sum(), df['Other_Sales'].sum()]
   })

   # Map data
   map_data = pd.DataFrame([
       {'Country': 'USA', 'Region': 'North America', 'Sales': df['NA_Sales'].sum()},
       {'Country': 'Canada', 'Region': 'North America', 'Sales': df['NA_Sales'].sum() * 0.1},
       {'Country': 'United Kingdom', 'Region': 'Europe', 'Sales': df['EU_Sales'].sum() * 0.2},
       {'Country': 'Germany', 'Region': 'Europe', 'Sales': df['EU_Sales'].sum() * 0.2},
       {'Country': 'France', 'Region': 'Europe', 'Sales': df['EU_Sales'].sum() * 0.15},
       {'Country': 'Japan', 'Region': 'Japan', 'Sales': df['JP_Sales'].sum()},
       # Add more countries as needed
   ])

   layout = GRAPH_THEME['layout'].copy()
   layout.pop('title', None)

   return html.Div([
       # Filters
       html.Div([
           html.Div([
               html.Label('Select Region', style={'color': COLORS['text']}),
               dcc.Dropdown(
                   id='region-filter',
                   options=[{'label': r, 'value': r} for r in regional_dist['Region']],
                   value='All',
                   style={'backgroundColor': COLORS['card_background']}
               )
           ], style={'width': '30%', 'marginRight': '20px'}),
           
           html.Div([
               html.Label('Select Country', style={'color': COLORS['text']}),
               dcc.Dropdown(
                   id='country-filter',
                   options=[{'label': c, 'value': c} for c in map_data['Country']],
                   value='All',
                   style={'backgroundColor': COLORS['card_background']}
               )
           ], style={'width': '30%'})
       ], style={'display': 'flex', 'marginBottom': '20px', 'padding': '20px'}),

       # World Map
       html.Div([
           dcc.Graph(
               id='world-map',
               figure=go.Figure(data=[
                   go.Choropleth(
                       locations=[
                           'USA', 'CAN', 'GBR', 'DEU', 'FRA', 'JPN'
                       ],  # ISO-3 country codes
                       z=map_data['Sales'],
                       text=map_data['Country'],
                       colorscale=[[0, COLORS['background']], [1, COLORS['primary']]],
                       marker_line_color='darkgray',
                       marker_line_width=0.5,
                       colorbar_title='Sales ($B)'
                   )
               ]).update_layout(
                   **layout,
                   title='Global Sales Distribution',
                   geo=dict(
                       showframe=False,
                       showcoastlines=True,
                       projection_type='equirectangular'
                   )
               )
           )
       ], style=CARD_STYLE),

       # Regional Charts
       html.Div([
           html.Div([
               dcc.Graph(
                   id='regional-trends',
                   figure=go.Figure(data=[
                       go.Bar(
                           x=df.groupby('Year')['NA_Sales'].sum().index,
                           y=df.groupby('Year')['NA_Sales'].sum().values,
                           name='North America'
                       ),
                       go.Bar(
                           x=df.groupby('Year')['EU_Sales'].sum().index,
                           y=df.groupby('Year')['EU_Sales'].sum().values,
                           name='Europe'
                       ),
                       go.Bar(
                           x=df.groupby('Year')['JP_Sales'].sum().index,
                           y=df.groupby('Year')['JP_Sales'].sum().values,
                           name='Japan'
                       )
                   ]).update_layout(
                       **layout,
                       title='Regional Sales Trends',
                       barmode='group'
                   )
               )
           ], style=CARD_STYLE)
       ], style=CHART_CONTAINER_STYLE)
   ])

   # Add callbacks for filters
   @app.callback(
       Output('country-filter', 'options'),
       [Input('region-filter', 'value')]
   )
   def update_country_options(selected_region):
       if selected_region == 'All':
           return [{'label': c, 'value': c} for c in map_data['Country']]
       filtered_countries = map_data[map_data['Region'] == selected_region]['Country']
       return [{'label': c, 'value': c} for c in filtered_countries]

   @app.callback(
       [Output('world-map', 'figure'),
        Output('regional-trends', 'figure')],
       [Input('region-filter', 'value'),
        Input('country-filter', 'value')]
   )
   def update_charts(selected_region, selected_country):
       # Update map and charts based on selections
       filtered_data = map_data
       if selected_region != 'All':
           filtered_data = filtered_data[filtered_data['Region'] == selected_region]
       if selected_country != 'All':
           filtered_data = filtered_data[filtered_data['Country'] == selected_country]
       
       # Update map figure
       map_fig = go.Figure(data=[
           go.Choropleth(
               locations=filtered_data.index,
               z=filtered_data['Sales'],
               text=filtered_data['Country'],
               colorscale=[[0, COLORS['background']], [1, COLORS['primary']]]
           )
       ]).update_layout(**layout, title='Global Sales Distribution')
       
       # Update trends figure
       trends_fig = create_trends_figure(df, selected_region, selected_country)
       
       return map_fig, trends_fig