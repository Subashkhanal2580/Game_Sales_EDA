# import pandas as pd
# import plotly.express as px
# import plotly.graph_objects as go
# from dash import Dash, html, dcc
# from dash.dependencies import Input, Output

# app = Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

# # Load and preprocess data
# df = pd.read_csv('vgsales.csv')

# # Precompute common aggregations
# yearly_sales = df.groupby('Year')['Global_Sales'].sum().reset_index()
# yearly_sales['YoY_Growth'] = yearly_sales['Global_Sales'].pct_change() * 100

# regional_dist = pd.DataFrame({
#     'Region': ['North America', 'Europe', 'Japan', 'Other'],
#     'Sales': [df['NA_Sales'].sum(), df['EU_Sales'].sum(), 
#               df['JP_Sales'].sum(), df['Other_Sales'].sum()]
# })

# genre_data = df.groupby('Genre').agg({
#     'Global_Sales': 'sum',
#     'Name': 'count'
# }).reset_index()

# app.layout = html.Div([
#     html.H1('Video Game Sales Analytics Dashboard', 
#             style={'textAlign': 'center', 'padding': '20px'}),
    
#     dcc.Tabs(id='tabs', value='market', children=[
#         dcc.Tab(label='Market Overview', value='market'),
#         dcc.Tab(label='Time Analysis', value='time'),
#         dcc.Tab(label='Cross-Platform', value='platform'),
#         dcc.Tab(label='Geographic', value='geographic'),
#         dcc.Tab(label='Competitive', value='competitive')
#     ]),
    
#     html.Div(id='tab-content')
# ])

# @app.callback(
#     Output('tab-content', 'children'),
#     Input('tabs', 'value')
# )
# def render_content(tab):
#     if tab == 'market':
#         market_concentration = df.groupby('Publisher')['Global_Sales'].sum()\
#             .sort_values(ascending=False).head(10)
            
#         return html.Div([
#             html.Div([
#                 dcc.Graph(figure=px.line(yearly_sales, x='Year', y='Global_Sales',
#                                        title='Global Sales Trends')),
#                 dcc.Graph(figure=px.pie(regional_dist, values='Sales', names='Region',
#                                       title='Regional Distribution'))
#             ], className='row'),
#             html.Div([
#                 dcc.Graph(figure=px.bar(yearly_sales, x='Year', y='YoY_Growth',
#                                       title='Year-over-Year Growth')),
#                 dcc.Graph(figure=px.bar(x=market_concentration.index, 
#                                       y=market_concentration.values,
#                                       title='Market Concentration'))
#             ], className='row')
#         ])
    
#     elif tab == 'time':
#         genre_evolution = df.pivot_table(
#             values='Global_Sales', 
#             index='Year',
#             columns='Genre',
#             aggfunc='sum'
#         ).reset_index()
        
#         platform_lifecycle = df.pivot_table(
#             values='Global_Sales',
#             index='Year',
#             columns='Platform',
#             aggfunc='sum'
#         ).reset_index()
        
#         return html.Div([
#             html.Div([
#                 dcc.Graph(figure=px.line(genre_evolution, x='Year', 
#                                        y=genre_evolution.columns[1:],
#                                        title='Genre Evolution')),
#                 dcc.Graph(figure=px.line(platform_lifecycle, x='Year',
#                                        y=platform_lifecycle.columns[1:],
#                                        title='Platform Lifecycle'))
#             ], className='row'),
#             html.Div([
#                 dcc.Graph(figure=px.scatter(df.groupby(['Genre', 'Year'])
#                                           ['Global_Sales'].sum().reset_index()
#                                           .sort_values('Global_Sales', ascending=False)
#                                           .groupby('Genre').head(1),
#                                           x='Year', y='Global_Sales', color='Genre',
#                                           title='Peak Years by Genre')),
#                 dcc.Graph(figure=px.scatter(df.groupby(['Platform', 'Year'])
#                                           ['Global_Sales'].sum().reset_index(),
#                                           x='Year', y='Global_Sales', color='Platform',
#                                           title='Platform Performance Timeline'))
#             ], className='row')
#         ])
    
#     elif tab == 'platform':
#         platform_genre = df.pivot_table(
#             values='Global_Sales',
#             index='Platform',
#             columns='Genre',
#             aggfunc='sum'
#         )
        
#         multi_platform = df.groupby('Name').agg({
#             'Platform': 'nunique',
#             'Global_Sales': 'sum'
#         }).reset_index().sort_values('Global_Sales', ascending=False).head(20)
        
#         return html.Div([
#             html.Div([
#                 dcc.Graph(figure=px.imshow(platform_genre,
#                                          title='Platform-Genre Performance')),
#                 dcc.Graph(figure=px.scatter(multi_platform, x='Platform',
#                                           y='Global_Sales', title='Multi-Platform Success',
#                                           text='Name'))
#             ], className='row'),
#             html.Div([
#                 dcc.Graph(figure=px.bar(df.groupby('Platform')['Global_Sales'].sum()
#                                       .sort_values(ascending=False).reset_index(),
#                                       x='Platform', y='Global_Sales',
#                                       title='Platform Market Share')),
#                 dcc.Graph(figure=px.scatter(df.groupby('Platform').agg({
#                     'Global_Sales': 'mean',
#                     'Name': 'count'
#                 }).reset_index(), x='Name', y='Global_Sales',
#                 title='Platform Success Metrics'))
#             ], className='row')
#         ])
    
#     elif tab == 'geographic':
#         regional_genre = df.groupby('Genre').agg({
#             'NA_Sales': 'sum',
#             'EU_Sales': 'sum',
#             'JP_Sales': 'sum'
#         }).reset_index()
        
#         market_growth = df.groupby('Year').agg({
#             'NA_Sales': 'sum',
#             'EU_Sales': 'sum',
#             'JP_Sales': 'sum',
#             'Other_Sales': 'sum'
#         }).reset_index()
        
#         return html.Div([
#             html.Div([
#                 dcc.Graph(figure=px.bar(regional_genre, x='Genre',
#                                       y=['NA_Sales', 'EU_Sales', 'JP_Sales'],
#                                       title='Regional Genre Preferences')),
#                 dcc.Graph(figure=px.line(market_growth, x='Year',
#                                        y=['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales'],
#                                        title='Market Growth by Region'))
#             ], className='row'),
#             html.Div([
#                 dcc.Graph(figure=px.scatter(df.groupby(['Genre', 'Platform']).agg({
#                     'NA_Sales': 'sum',
#                     'JP_Sales': 'sum'
#                 }).reset_index(), x='NA_Sales', y='JP_Sales',
#                 color='Genre', title='Cultural Market Differences')),
#                 dcc.Graph(figure=px.scatter(market_growth, x='Year',
#                                           y=['NA_Sales', 'EU_Sales', 'JP_Sales'],
#                                           title='Regional Growth Correlation'))
#             ], className='row')
#         ])
    
#     elif tab == 'competitive':
#         publisher_share = df.groupby('Publisher')['Global_Sales'].sum()\
#             .sort_values(ascending=False).head(10)
        
#         genre_saturation = df.groupby('Genre').agg({
#             'Name': 'count',
#             'Global_Sales': 'mean'
#         }).reset_index()
        
#         return html.Div([
#             html.Div([
#                 dcc.Graph(figure=px.pie(values=publisher_share.values,
#                                       names=publisher_share.index,
#                                       title='Publisher Market Share')),
#                 dcc.Graph(figure=px.scatter(genre_saturation, x='Name',
#                                           y='Global_Sales', text='Genre',
#                                           title='Genre Market Saturation'))
#             ], className='row'),
#             html.Div([
#                 dcc.Graph(figure=px.scatter(df.groupby(['Platform', 'Year']).agg({
#                     'Publisher': 'nunique',
#                     'Global_Sales': 'sum'
#                 }).reset_index(), x='Year', y='Publisher',
#                 color='Platform', title='Platform Competition')),
#                 dcc.Graph(figure=px.scatter(df.groupby('Publisher').agg({
#                     'Name': 'count',
#                     'Global_Sales': 'mean'
#                 }).reset_index().sort_values('Global_Sales', ascending=False).head(20),
#                 x='Name', y='Global_Sales', title='Publisher Success Metrics'))
#             ], className='row')
#         ])

# if __name__ == '__main__':
#     app.run_server(debug=True, port=8050)

# run.py
from src.app import create_app

if __name__ == '__main__':
    app = create_app()
    app.run_server(
        debug=True,        # Set to False in production
        port=8050,         # Default port
        host='localhost'   
    )