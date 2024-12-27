# src/layouts/time.py
from dash import html, dcc
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from .styles import COLORS, GRAPH_THEME, CARD_STYLE, KPI_CARD_STYLE, CHART_CONTAINER_STYLE

def create_time_layout(df):
    yearly_data = df.groupby('Year').agg({
        'Global_Sales': 'sum',
        'Name': 'count'
    }).reset_index()
    
    peak_year = yearly_data.loc[yearly_data['Global_Sales'].idxmax(), 'Year']
    peak_sales = yearly_data['Global_Sales'].max()
    cagr = ((yearly_data.iloc[-1]['Global_Sales'] / yearly_data.iloc[0]['Global_Sales']) 
            ** (1 / (len(yearly_data) - 1)) - 1) * 100

    layout = GRAPH_THEME['layout'].copy()
    layout.pop('title', None)

    return html.Div([
        html.Div([
            html.Div([
                html.H4("Peak Year", style={'color': COLORS['text']}),
                html.H2(f"{int(peak_year)}", style={'color': COLORS['primary']}),
                html.P(f"${peak_sales:.1f}B Sales", style={'color': COLORS['accent']})
            ], style=KPI_CARD_STYLE),
            
            html.Div([
                html.H4("Industry CAGR", style={'color': COLORS['text']}),
                html.H2(f"{cagr:.1f}%", style={'color': COLORS['primary']}),
                html.P("Compound Annual Growth", style={'color': COLORS['accent']})
            ], style=KPI_CARD_STYLE)
        ], style={'display': 'grid', 'gridTemplateColumns': 'repeat(auto-fit, minmax(250px, 1fr))', 'gap': '20px'}),

        html.Div([
            html.Div([
                dcc.Graph(
                    id='sales-growth-combined',
                    figure=make_subplots(specs=[[{"secondary_y": True}]])
                    .add_trace(
                        go.Scatter(
                            x=yearly_data['Year'],
                            y=yearly_data['Global_Sales'],
                            name="Global Sales",
                            line=dict(color=COLORS['primary'], width=3)
                        )
                    )
                    .add_trace(
                        go.Bar(
                            x=yearly_data['Year'],
                            y=yearly_data['Name'],
                            name="Number of Games",
                            marker_color=COLORS['accent']
                        ),
                        secondary_y=True
                    )
                    .update_layout(
                        **layout,
                        title='Industry Growth and Game Releases'
                    )
                )
            ], style=CARD_STYLE),

            html.Div([
                dcc.Graph(
                    id='sales-distribution',
                    figure=go.Figure(
                        data=[go.Violin(
                            y=df['Global_Sales'],
                            x=df['Year'].astype(str),
                            line_color=COLORS['primary'],
                            fillcolor=COLORS['accent'],
                            opacity=0.6
                        )]
                    ).update_layout(
                        **layout,
                        title='Sales Distribution by Year'
                    )
                )
            ], style=CARD_STYLE)
        ], style=CHART_CONTAINER_STYLE)
    ])