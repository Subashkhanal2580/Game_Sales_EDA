"""
Data processing utilities for the video game sales dashboard.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Union
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def calculate_total_sales(df: pd.DataFrame) -> Dict[str, float]:
    """
    Calculate total sales figures across different regions.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        The video games dataset
        
    Returns:
    --------
    Dict[str, float]
        Dictionary containing total sales for each region and global
    """
    return {
        'global': df['Global_Sales'].sum(),
        'na': df['NA_Sales'].sum(),
        'eu': df['EU_Sales'].sum(),
        'jp': df['JP_Sales'].sum(),
        'other': df['Other_Sales'].sum()
    }

def get_unique_counts(df: pd.DataFrame) -> Dict[str, int]:
    """
    Get counts of unique values for categorical columns.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        The video games dataset
        
    Returns:
    --------
    Dict[str, int]
        Dictionary containing counts of unique publishers, platforms, and genres
    """
    return {
        'publishers': df['Publisher'].nunique(),
        'platforms': df['Platform'].nunique(),
        'genres': df['Genre'].nunique()
    }

# def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
#     """
#     Clean the video game sales dataset by handling missing values,
#     incorrect years, and sales inconsistencies.
#     """
#     cleaned_df = df.copy()
    
#     # Handle year cleaning
#     current_year = datetime.now().year
#     cleaned_df['Year'] = pd.to_numeric(cleaned_df['Year'], errors='coerce')
    
#     # Replace invalid years (N/A, future years, years before 1980)
#     year_mask = (cleaned_df['Year'].isna()) | \
#                 (cleaned_df['Year'] > current_year) | \
#                 (cleaned_df['Year'] < 1980)
    
#     if year_mask.any():
#         logger.warning(f"Found {year_mask.sum()} rows with invalid years")
#         median_year = cleaned_df.loc[~year_mask, 'Year'].median()
#         cleaned_df.loc[year_mask, 'Year'] = median_year
    
#     # Round year to integer
#     cleaned_df['Year'] = cleaned_df['Year'].round().astype(int)
    
#     # Fix sales inconsistencies
#     sales_columns = ['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales']
#     regional_sum = cleaned_df[sales_columns].sum(axis=1)
    
#     # Update Global_Sales where needed
#     cleaned_df['Global_Sales'] = regional_sum
    
#     return cleaned_df

def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the video game sales dataset by handling missing values,
    incorrect years, and sales inconsistencies.
    """
    cleaned_df = df.copy()
    
    # Handle year cleaning
    current_year = datetime.now().year
    cleaned_df['Year'] = pd.to_numeric(cleaned_df['Year'], errors='coerce')
    
    # Replace invalid years (N/A, future years, years before 1980)
    year_mask = (cleaned_df['Year'].isna()) | \
                (cleaned_df['Year'] > current_year) | \
                (cleaned_df['Year'] < 1980)
    
    if year_mask.any():
        logger.warning(f"Found {year_mask.sum()} rows with invalid years")
        median_year = cleaned_df.loc[~year_mask, 'Year'].median()
        cleaned_df.loc[year_mask, 'Year'] = median_year
    
    # Round year to integer
    cleaned_df['Year'] = cleaned_df['Year'].round().astype(int)
    
    # Handle missing values in categorical columns
    categorical_columns = ['Platform', 'Genre', 'Publisher', 'Name']
    for col in categorical_columns:
        # Count missing values
        missing_count = cleaned_df[col].isna().sum()
        if missing_count > 0:
            logger.warning(f"Found {missing_count} missing values in {col}")
            # Fill missing values with 'Unknown'
            cleaned_df[col] = cleaned_df[col].fillna('Unknown')
        # Ensure string type
        cleaned_df[col] = cleaned_df[col].astype(str)
    
    # Fix sales inconsistencies
    sales_columns = ['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales']
    # Fill missing sales with 0
    for col in sales_columns:
        cleaned_df[col] = cleaned_df[col].fillna(0)
    
    regional_sum = cleaned_df[sales_columns].sum(axis=1)
    
    # Update Global_Sales where needed
    cleaned_df['Global_Sales'] = regional_sum
    
    return cleaned_df

def preprocess_overview_data(df: pd.DataFrame) -> Dict:
    """
    Preprocess data for the overview dashboard.
    """
    stats = {
        'total_sales': df['Global_Sales'].sum(),
        'total_games': len(df),
        'active_publishers': df['Publisher'].nunique(),
        'total_platforms': df['Platform'].nunique(),
        'top_game': df.nlargest(1, 'Global_Sales')['Name'].iloc[0],
        'top_game_sales': df['Global_Sales'].max(),
        'peak_year': df.groupby('Year')['Global_Sales'].sum().idxmax()
    }
    
    peak_year_sales = df[df['Year'] == stats['peak_year']]['Global_Sales'].sum()
    stats['peak_year_sales'] = peak_year_sales
    
    return stats

def preprocess_sales_data(df: pd.DataFrame) -> Dict:
    """
    Preprocess data for the sales analysis dashboard.
    """
    # Get the game with highest global sales
    top_game = df.nlargest(1, 'Global_Sales').iloc[0]
    
    # Calculate peak year by sales
    yearly_sales = df.groupby('Year')['Global_Sales'].sum()
    peak_year = yearly_sales.idxmax()
    
    return {
        'total_sales': df['Global_Sales'].sum(),
        'top_game': top_game['Name'],
        'top_game_sales': top_game['Global_Sales'],
        'peak_year': peak_year,
        'peak_year_sales': yearly_sales[peak_year]
    }

def preprocess_genre_data(df: pd.DataFrame) -> Dict:
    """
    Preprocess data for the genre analysis dashboard.
    """
    # Calculate genre statistics
    genre_sales = df.groupby('Genre')['Global_Sales'].sum()
    top_genre = genre_sales.idxmax()
    
    # Calculate genre growth
    genre_yearly = df.pivot_table(
        values='Global_Sales',
        index='Year',
        columns='Genre',
        aggfunc='sum'
    ).fillna(0)
    
    genre_growth = (genre_yearly.iloc[-1] - genre_yearly.iloc[0]) / genre_yearly.iloc[0] * 100
    fastest_growing = genre_growth.idxmax()
    
    return {
        'unique_genres': list(df['Genre'].unique()),
        'top_genre': top_genre,
        'top_genre_sales': genre_sales[top_genre],
        'fastest_growing': fastest_growing,
        'growth_rate': genre_growth[fastest_growing]
    }

def preprocess_platform_data(df: pd.DataFrame) -> Dict:
    """
    Preprocess data for the platform analysis dashboard.
    """
    # Calculate platform statistics
    platform_sales = df.groupby('Platform')['Global_Sales'].sum()
    top_platform = platform_sales.idxmax()
    
    # Calculate platform with most releases
    platform_releases = df['Platform'].value_counts()
    most_releases = platform_releases.idxmax()
    
    return {
        'unique_platforms': list(df['Platform'].unique()),
        'top_platform': top_platform,
        'top_platform_sales': platform_sales[top_platform],
        'most_releases': most_releases,
        'release_count': platform_releases[most_releases]
    }

def preprocess_publisher_data(df: pd.DataFrame) -> Dict:
    """
    Preprocess data for the publisher analysis dashboard.
    """
    # Calculate publisher statistics
    publisher_sales = df.groupby('Publisher')['Global_Sales'].sum()
    top_publisher = publisher_sales.idxmax()
    
    # Calculate publisher with most games
    publisher_games = df['Publisher'].value_counts()
    most_games = publisher_games.idxmax()
    
    return {
        'unique_publishers': list(df['Publisher'].unique()),
        'top_publisher': top_publisher,
        'top_publisher_sales': publisher_sales[top_publisher],
        'most_games': most_games,
        'game_count': publisher_games[most_games]
    }

def calculate_market_share(df: pd.DataFrame, 
                         groupby_col: str) -> pd.DataFrame:
    """
    Calculate market share by any given column (Platform, Genre, Publisher).
    """
    grouped = df.groupby(groupby_col).agg({
        'Global_Sales': 'sum',
        'Rank': 'count'
    }).reset_index()
    
    total_sales = grouped['Global_Sales'].sum()
    grouped['Market_Share'] = (grouped['Global_Sales'] / total_sales) * 100
    grouped = grouped.sort_values('Global_Sales', ascending=False)
    
    return grouped

def analyze_time_trends(df: pd.DataFrame, 
                       group_by: Union[str, List[str]] = 'Year') -> pd.DataFrame:
    """
    Analyze sales trends over time, optionally grouped by additional categories.
    """
    if isinstance(group_by, str):
        group_by = [group_by]
    
    if 'Year' not in group_by:
        group_by = ['Year'] + group_by
    
    trends = df.groupby(group_by).agg({
        'Global_Sales': 'sum',
        'Rank': 'count',
        'NA_Sales': 'sum',
        'EU_Sales': 'sum',
        'JP_Sales': 'sum',
        'Other_Sales': 'sum'
    }).reset_index()
    
    return trends

def calculate_regional_distribution(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate the distribution of sales across regions for each game.
    """
    regional_cols = ['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales']
    total_sales = df[regional_cols].sum(axis=1)
    
    regional_dist = df[regional_cols].div(total_sales, axis=0) * 100
    regional_dist.columns = [col.replace('Sales', 'Percentage') 
                           for col in regional_dist.columns]
    
    return pd.concat([df, regional_dist], axis=1)

def get_top_performers(df: pd.DataFrame, 
                      category: str,
                      metric: str = 'Global_Sales',
                      top_n: int = 10) -> pd.DataFrame:
    """
    Get top performing games, platforms, genres, or publishers.
    """
    if category == 'Name':
        return df.nlargest(top_n, metric)
    
    grouped = df.groupby(category).agg({
        metric: 'sum',
        'Rank': 'count'
    }).reset_index()
    
    return grouped.nlargest(top_n, metric)

def get_yearly_trends(df: pd.DataFrame) -> pd.DataFrame:
    """
    Get yearly sales trends and game count.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        The video games dataset
        
    Returns:
    --------
    pandas.DataFrame
        DataFrame with yearly trends including sales and game count
    """
    yearly_data = df.groupby('Year').agg({
        'Global_Sales': 'sum',
        'Name': 'count'  # Count of games per year
    }).rename(columns={'Name': 'Game_Count'})
    
    return yearly_data

def get_genre_trends(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate genre market share trends over time.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        The video games dataset
        
    Returns:
    --------
    pandas.DataFrame
        DataFrame with genre market share by year
    """
    # Calculate sales by genre and year
    genre_sales = df.pivot_table(
        values='Global_Sales',
        index='Year',
        columns='Genre',
        aggfunc='sum',
        fill_value=0
    )
    
    # Convert to market share percentages
    yearly_total = genre_sales.sum(axis=1)
    genre_shares = genre_sales.div(yearly_total, axis=0) * 100
    
    return genre_shares

def get_platform_trends(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate platform market share trends over time.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        The video games dataset
        
    Returns:
    --------
    pandas.DataFrame
        DataFrame with platform market share by year
    """
    # Calculate sales by platform and year
    platform_sales = df.pivot_table(
        values='Global_Sales',
        index='Year',
        columns='Platform',
        aggfunc='sum',
        fill_value=0
    )
    
    # Convert to market share percentages
    yearly_total = platform_sales.sum(axis=1)
    platform_shares = platform_sales.div(yearly_total, axis=0) * 100
    
    return platform_shares

def format_sales(value: float) -> str:
    """
    Format sales values for display
    
    Parameters:
    -----------
    value : float
        Sales value in millions
        
    Returns:
    --------
    str
        Formatted sales string
    """
    if value >= 1000:
        return f"{value/1000:.1f}B"
    return f"{value:.1f}"

def get_top_games(df: pd.DataFrame, n: int = 5) -> List[Tuple[str, float, int, str]]:
    """
    Get top n games by global sales
    
    Parameters:
    -----------
    df : pandas.DataFrame
        The video games dataset
    n : int
        Number of top games to return
        
    Returns:
    --------
    List[Tuple[str, float, int, str]]
        List of tuples containing (game_name, sales, year, publisher)
    """
    top_games = df.nlargest(n, 'Global_Sales')
    return [
        (row['Name'], row['Global_Sales'], int(row['Year']), row['Publisher'])
        for _, row in top_games.iterrows()
    ]

def get_top_publishers(df: pd.DataFrame, n: int = 5) -> List[Tuple[str, float, int]]:
    """
    Get top n publishers by global sales
    
    Parameters:
    -----------
    df : pandas.DataFrame
        The video games dataset
    n : int
        Number of top publishers to return
        
    Returns:
    --------
    List[Tuple[str, float, int]]
        List of tuples containing (publisher_name, total_sales, game_count)
    """
    publisher_stats = df.groupby('Publisher').agg({
        'Global_Sales': 'sum',
        'Name': 'count'
    }).reset_index()
    
    top_publishers = publisher_stats.nlargest(n, 'Global_Sales')
    return [
        (row['Publisher'], row['Global_Sales'], row['Name'])
        for _, row in top_publishers.iterrows()
    ]

def get_top_genres(df: pd.DataFrame, n: int = 5) -> List[Tuple[str, float, int]]:
    """
    Get top n genres by global sales
    
    Parameters:
    -----------
    df : pandas.DataFrame
        The video games dataset
    n : int
        Number of top genres to return
        
    Returns:
    --------
    List[Tuple[str, float, int]]
        List of tuples containing (genre_name, total_sales, game_count)
    """
    genre_stats = df.groupby('Genre').agg({
        'Global_Sales': 'sum',
        'Name': 'count'
    }).reset_index()
    
    top_genres = genre_stats.nlargest(n, 'Global_Sales')
    return [
        (row['Genre'], row['Global_Sales'], row['Name'])
        for _, row in top_genres.iterrows()
    ]

def calculate_growth_rates(df: pd.DataFrame) -> Dict[str, Dict[str, float]]:
    """
    Calculate growth rates for different time periods.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        The video games dataset
        
    Returns:
    --------
    Dict[str, Dict[str, float]]
        Dictionary containing growth metrics for different time periods
    """
    yearly_data = get_yearly_trends(df)
    
    # Calculate growth rates for different periods
    growth_rates = {}
    
    # Last year growth
    last_year = yearly_data.index.max()
    prev_year = last_year - 1
    
    if prev_year in yearly_data.index:
        sales_growth = ((yearly_data.loc[last_year, 'Global_Sales'] / 
                        yearly_data.loc[prev_year, 'Global_Sales']) - 1) * 100
        release_growth = ((yearly_data.loc[last_year, 'Game_Count'] / 
                          yearly_data.loc[prev_year, 'Game_Count']) - 1) * 100
        avg_sales_last = yearly_data.loc[last_year, 'Global_Sales'] / yearly_data.loc[last_year, 'Game_Count']
        avg_sales_prev = yearly_data.loc[prev_year, 'Global_Sales'] / yearly_data.loc[prev_year, 'Game_Count']
        avg_sales_growth = ((avg_sales_last / avg_sales_prev) - 1) * 100
        
        growth_rates['Last Year'] = {
            'sales_growth': sales_growth,
            'release_growth': release_growth,
            'avg_sales_growth': avg_sales_growth
        }
    
    # 5-year growth
    five_years_ago = last_year - 5
    if five_years_ago in yearly_data.index:
        sales_growth_5y = ((yearly_data.loc[last_year, 'Global_Sales'] / 
                           yearly_data.loc[five_years_ago, 'Global_Sales']) - 1) * 100
        release_growth_5y = ((yearly_data.loc[last_year, 'Game_Count'] / 
                             yearly_data.loc[five_years_ago, 'Game_Count']) - 1) * 100
        avg_sales_last = yearly_data.loc[last_year, 'Global_Sales'] / yearly_data.loc[last_year, 'Game_Count']
        avg_sales_5y = yearly_data.loc[five_years_ago, 'Global_Sales'] / yearly_data.loc[five_years_ago, 'Game_Count']
        avg_sales_growth_5y = ((avg_sales_last / avg_sales_5y) - 1) * 100
        
        growth_rates['5-Year Trend'] = {
            'sales_growth': sales_growth_5y,
            'release_growth': release_growth_5y,
            'avg_sales_growth': avg_sales_growth_5y
        }
    
    return growth_rates

def calculate_yoy_growth(df: pd.DataFrame) -> Dict[str, float]:
    """
    Calculate year-over-year growth rates for sales and releases.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        The video games dataset
        
    Returns:
    --------
    Dict[str, float]
        Dictionary containing YoY growth rates for different metrics
    """
    yearly_data = get_yearly_trends(df)
    
    # Get the last two years of data
    last_year = yearly_data.index.max()
    prev_year = last_year - 1
    
    if prev_year not in yearly_data.index:
        return None
    
    # Calculate growth rates
    sales_growth = ((yearly_data.loc[last_year, 'Global_Sales'] /
                    yearly_data.loc[prev_year, 'Global_Sales']) - 1) * 100
    
    release_growth = ((yearly_data.loc[last_year, 'Game_Count'] /
                      yearly_data.loc[prev_year, 'Game_Count']) - 1) * 100
    
    return {
        'sales_growth': sales_growth,
        'release_growth': release_growth
    }

def analyze_publisher_performance(df: pd.DataFrame) -> pd.DataFrame:
    """
    Analyze publisher performance including market share and efficiency metrics.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        The video games dataset
        
    Returns:
    --------
    pandas.DataFrame
        DataFrame with publisher performance metrics
    """
    publisher_stats = df.groupby('Publisher').agg({
        'Global_Sales': 'sum',
        'Name': 'count',
        'NA_Sales': 'sum',
        'EU_Sales': 'sum',
        'JP_Sales': 'sum',
        'Other_Sales': 'sum'
    }).reset_index()
    
    total_sales = publisher_stats['Global_Sales'].sum()
    publisher_stats['Market_Share'] = publisher_stats['Global_Sales'] / total_sales * 100
    publisher_stats['Avg_Sales_Per_Game'] = publisher_stats['Global_Sales'] / publisher_stats['Name']
    
    # Calculate regional focus
    regions = ['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales']
    for region in regions:
        publisher_stats[f'{region}_Share'] = publisher_stats[region] / publisher_stats['Global_Sales'] * 100
    
    return publisher_stats.sort_values('Global_Sales', ascending=False)

def analyze_genre_performance(df: pd.DataFrame) -> pd.DataFrame:
    """
    Analyze genre performance including market share and growth trends.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        The video games dataset
        
    Returns:
    --------
    pandas.DataFrame
        DataFrame with genre performance metrics
    """
    genre_stats = df.groupby('Genre').agg({
        'Global_Sales': 'sum',
        'Name': 'count',
        'NA_Sales': 'sum',
        'EU_Sales': 'sum',
        'JP_Sales': 'sum',
        'Other_Sales': 'sum'
    }).reset_index()
    
    total_sales = genre_stats['Global_Sales'].sum()
    genre_stats['Market_Share'] = genre_stats['Global_Sales'] / total_sales * 100
    genre_stats['Avg_Sales_Per_Game'] = genre_stats['Global_Sales'] / genre_stats['Name']
    
    # Calculate regional popularity
    regions = ['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales']
    for region in regions:
        genre_stats[f'{region}_Share'] = genre_stats[region] / genre_stats['Global_Sales'] * 100
    
    return genre_stats.sort_values('Global_Sales', ascending=False)