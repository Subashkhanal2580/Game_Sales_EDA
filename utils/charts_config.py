"""
Chart configuration utilities for the video game sales dashboard.
Provides consistent styling and configuration for all visualizations.
"""

from typing import Dict, Any, List, Optional, Union
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd

from .constants import COLOR_SCHEMES, CHART_CONFIG, REGIONS

class ChartConfigurator:
    """
    Utility class for managing chart configurations and styling.
    """
    
    @staticmethod
    def get_base_layout(
        title: str,
        size: str = 'medium',
        show_legend: bool = True
    ) -> Dict[str, Any]:
        """
        Get base layout configuration for charts.
        
        Args:
            title (str): Chart title
            size (str): Size preset ('small', 'medium', 'large', 'wide')
            show_legend (bool): Whether to show the legend
            
        Returns:
            Dict[str, Any]: Base layout configuration
        """
        size_config = CHART_CONFIG['sizes'][size]
        margin_config = CHART_CONFIG['margins'][size]
        
        return {
            'title': {
                'text': title,
                'font': {'size': 16, 'color': COLOR_SCHEMES['primary']['text']},
                'x': 0.5,
                'xanchor': 'center'
            },
            'width': size_config['width'],
            'height': size_config['height'],
            'margin': margin_config,
            'showlegend': show_legend,
            'paper_bgcolor': 'rgba(0,0,0,0)',
            'plot_bgcolor': 'rgba(0,0,0,0)',
            'font': {
                'family': 'Arial, sans-serif',
                'color': COLOR_SCHEMES['primary']['text']
            }
        }

    @staticmethod
    def style_axes(
        fig: go.Figure,
        x_title: Optional[str] = None,
        y_title: Optional[str] = None,
        grid: bool = True
    ) -> go.Figure:
        """
        Apply consistent styling to chart axes.
        
        Args:
            fig (go.Figure): Plotly figure object
            x_title (str, optional): X-axis title
            y_title (str, optional): Y-axis title
            grid (bool): Whether to show grid lines
            
        Returns:
            go.Figure: Styled figure
        """
        axis_style = {
            'showgrid': grid,
            'gridcolor': '#E5E5E5',
            'gridwidth': 0.5,
            'zeroline': False,
            'linecolor': '#757575',
            'linewidth': 1,
            'ticks': 'outside',
            'tickfont': {'size': 10},
            'showline': True
        }
        
        fig.update_xaxes(
            title_text=x_title,
            title_font={'size': 12},
            **axis_style
        )
        
        fig.update_yaxes(
            title_text=y_title,
            title_font={'size': 12},
            **axis_style
        )
        
        return fig

    @staticmethod
    def create_sales_bar(
        data: pd.DataFrame,
        x: str,
        y: str = 'Global_Sales',
        title: str = 'Sales Distribution',
        size: str = 'medium',
        orientation: str = 'v'
    ) -> go.Figure:
        """
        Create a styled bar chart for sales data.
        
        Args:
            data (pd.DataFrame): Input data
            x (str): Column name for x-axis
            y (str): Column name for y-axis (default: 'Global_Sales')
            title (str): Chart title
            size (str): Chart size preset
            orientation (str): Bar orientation ('v' or 'h')
            
        Returns:
            go.Figure: Configured bar chart
        """
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=data[x] if orientation == 'v' else data[y],
            y=data[y] if orientation == 'v' else data[x],
            orientation=orientation,
            marker_color=COLOR_SCHEMES['primary']['main'],
            hovertemplate='%{y:.2f}M units<extra></extra>' if orientation == 'v' 
                         else '%{x:.2f}M units<extra></extra>'
        ))
        
        fig.update_layout(
            **ChartConfigurator.get_base_layout(title, size)
        )
        
        x_title = x.replace('_', ' ').title()
        y_title = 'Sales (Millions)' if y == 'Global_Sales' else y.replace('_', ' ').title()
        
        if orientation == 'h':
            x_title, y_title = y_title, x_title
            
        fig = ChartConfigurator.style_axes(fig, x_title, y_title)
        
        return fig

    @staticmethod
    def create_time_series(
        data: pd.DataFrame,
        time_column: str = 'Year',
        value_columns: Union[str, List[str]] = 'Global_Sales',
        title: str = 'Sales Over Time',
        size: str = 'medium'
    ) -> go.Figure:
        """
        Create a styled time series chart.
        
        Args:
            data (pd.DataFrame): Input data
            time_column (str): Column name for time axis
            value_columns (str or List[str]): Column(s) for values
            title (str): Chart title
            size (str): Chart size preset
            
        Returns:
            go.Figure: Configured time series chart
        """
        fig = go.Figure()
        
        if isinstance(value_columns, str):
            value_columns = [value_columns]
        
        # Ensure data is not empty
        if data.empty:
            fig.add_annotation(
                text="No data available",
                xref="paper",
                yref="paper",
                x=0.5,
                y=0.5,
                showarrow=False
            )
            return fig
            
        for col in value_columns:
            if col in data.columns:  # Only add trace if column exists
                color = (COLOR_SCHEMES['regions'].get(col, COLOR_SCHEMES['primary']['main']) 
                        if col in REGIONS else COLOR_SCHEMES['primary']['main'])
                
                fig.add_trace(go.Scatter(
                    x=data[time_column],
                    y=data[col],
                    name=REGIONS.get(col, col.replace('_', ' ')),
                    mode='lines+markers',
                    line={'color': color, 'width': 2},
                    marker={'size': 6},
                    hovertemplate='%{y:.2f}M units<extra></extra>'
                ))
        
        fig.update_layout(
            **ChartConfigurator.get_base_layout(title, size)
        )
        
        fig = ChartConfigurator.style_axes(
            fig,
            x_title=time_column,
            y_title='Sales (Millions)'
        )
        
        return fig

    @staticmethod
    def create_pie_chart(
        data: pd.DataFrame,
        names: str,
        values: str = 'Global_Sales',
        title: str = 'Distribution',
        size: str = 'medium'
    ) -> go.Figure:
        """
        Create a styled pie chart.
        
        Args:
            data (pd.DataFrame): Input data
            names (str): Column name for slice labels
            values (str): Column name for slice values
            title (str): Chart title
            size (str): Chart size preset
            
        Returns:
            go.Figure: Configured pie chart
        """
        fig = go.Figure(data=[go.Pie(
            labels=data[names],
            values=data[values],
            hole=0.4,
            textinfo='label+percent',
            hovertemplate='%{label}<br>%{value:.2f}M units<br>%{percent}<extra></extra>'
        )])
        
        fig.update_layout(
            **ChartConfigurator.get_base_layout(title, size)
        )
        
        fig.update_traces(
            marker=dict(
                colors=px.colors.qualitative.Set3[:len(data)]
            )
        )
        
        return fig

    @staticmethod
    def create_heatmap(
        data: pd.DataFrame,
        title: str = 'Heatmap',
        size: str = 'large',
        colorscale: Optional[List[str]] = None
    ) -> go.Figure:
        """
        Create a styled heatmap.
        
        Args:
            data (pd.DataFrame): Input data matrix
            title (str): Chart title
            size (str): Chart size preset
            colorscale (List[str], optional): Custom color scale
            
        Returns:
            go.Figure: Configured heatmap
        """
        if colorscale is None:
            colorscale = COLOR_SCHEMES['heatmap']['correlation']
            
        fig = go.Figure(data=go.Heatmap(
            z=data.values,
            x=data.columns,
            y=data.index,
            colorscale=colorscale,
            hoverongaps=False,
            hovertemplate='%{y}<br>%{x}<br>Value: %{z:.2f}<extra></extra>'
        ))
        
        layout = ChartConfigurator.get_base_layout(title, size)
        layout.update({
            'xaxis': {
                'side': 'bottom',
                'tickangle': 45
            }
        })
        
        fig.update_layout(**layout)
        
        return fig

    @staticmethod
    def create_regional_comparison(
        data: pd.DataFrame,
        category: str,
        title: str = 'Regional Sales Comparison',
        size: str = 'large'
    ) -> go.Figure:
        """
        Create a multi-region comparison chart.
        
        Args:
            data (pd.DataFrame): Input data
            category (str): Category column for comparison
            title (str): Chart title
            size (str): Chart size preset
            
        Returns:
            go.Figure: Configured comparison chart
        """
        fig = go.Figure()
        
        for region in ['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales']:
            fig.add_trace(go.Bar(
                name=REGIONS[region],
                x=data[category],
                y=data[region],
                marker_color=COLOR_SCHEMES['regions'][region],
                hovertemplate='%{x}<br>%{y:.2f}M units<extra></extra>'
            ))
        
        fig.update_layout(
            barmode='group',
            **ChartConfigurator.get_base_layout(title, size)
        )
        
        fig = ChartConfigurator.style_axes(
            fig,
            x_title=category.replace('_', ' '),
            y_title='Sales (Millions)'
        )
        
        return fig

    @staticmethod
    def apply_dark_theme(fig: go.Figure) -> go.Figure:
        """
        Apply dark theme to a chart.
        
        Args:
            fig (go.Figure): Input figure
            
        Returns:
            go.Figure: Dark themed figure
        """
        dark_layout = {
            'paper_bgcolor': '#2d3436',
            'plot_bgcolor': '#2d3436',
            'font': {'color': '#ffffff'},
        }
        
        fig.update_layout(**dark_layout)
        
        fig.update_xaxes(
            gridcolor='#636e72',
            linecolor='#b2bec3'
        )
        
        fig.update_yaxes(
            gridcolor='#636e72',
            linecolor='#b2bec3'
        )
        
        return fig