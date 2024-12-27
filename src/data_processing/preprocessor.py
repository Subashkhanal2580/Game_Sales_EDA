# src/data_processing/preprocessor.py
import pandas as pd
import numpy as np

class DataPreprocessor:
    def __init__(self, filepath):
        """Initialize the preprocessor with data file."""
        self.df = pd.read_csv(filepath)
        self._clean_data()
        
    def _clean_data(self):
        """Clean and prepare the dataset."""
        # Remove rows with missing values
        self.df = self.df.dropna()
        
        # Convert year to int, handling any errors
        self.df['Year'] = pd.to_numeric(self.df['Year'], errors='coerce')
        self.df = self.df.dropna(subset=['Year'])
        self.df['Year'] = self.df['Year'].astype(int)
        
        # Filter out outlier years
        self.df = self.df[(self.df['Year'] >= 1980) & (self.df['Year'] <= 2020)]
    
    def get_yearly_sales(self):
        """Calculate yearly sales metrics."""
        yearly_sales = self.df.groupby('Year').agg({
            'Global_Sales': 'sum',
            'Name': 'count'
        }).reset_index()
        
        yearly_sales['YoY_Growth'] = yearly_sales['Global_Sales'].pct_change() * 100
        yearly_sales['Market_Size'] = yearly_sales['Name']  # Number of games released
        return yearly_sales
    
    def get_regional_distribution(self):
        """Calculate regional sales distribution."""
        return pd.DataFrame({
            'Region': ['North America', 'Europe', 'Japan', 'Other'],
            'Sales': [
                self.df['NA_Sales'].sum(),
                self.df['EU_Sales'].sum(),
                self.df['JP_Sales'].sum(),
                self.df['Other_Sales'].sum()
            ],
            'Market_Share': [
                (self.df['NA_Sales'].sum() / self.df['Global_Sales'].sum()) * 100,
                (self.df['EU_Sales'].sum() / self.df['Global_Sales'].sum()) * 100,
                (self.df['JP_Sales'].sum() / self.df['Global_Sales'].sum()) * 100,
                (self.df['Other_Sales'].sum() / self.df['Global_Sales'].sum()) * 100
            ]
        })
    
    def get_genre_trends(self):
        """Analyze genre performance over time."""
        return self.df.pivot_table(
            values='Global_Sales',
            index='Year',
            columns='Genre',
            aggfunc='sum'
        ).reset_index()
    
    def get_platform_analysis(self):
        """Analyze platform performance."""
        platform_data = self.df.groupby('Platform').agg({
            'Global_Sales': ['sum', 'mean', 'count'],
            'Name': 'nunique'
        }).reset_index()
        
        platform_data.columns = ['Platform', 'Total_Sales', 'Avg_Sales', 'Game_Count', 'Unique_Games']
        platform_data['Market_Share'] = (platform_data['Total_Sales'] / platform_data['Total_Sales'].sum()) * 100
        
        return platform_data

    def get_publisher_insights(self):
        """Analyze publisher performance."""
        return self.df.groupby('Publisher').agg({
            'Global_Sales': ['sum', 'mean'],
            'Name': 'count',
            'Genre': 'nunique'
        }).reset_index()