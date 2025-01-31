"""
Data loading utilities for the video game sales dashboard.
Handles loading and basic validation of the video game sales dataset.
"""

import pandas as pd
import numpy as np
from typing import Tuple, Dict, Optional
import logging
from pathlib import Path
from functools import lru_cache

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DataLoadingError(Exception):
    """Custom exception for data loading errors."""
    pass

def validate_dataset(df: pd.DataFrame) -> bool:
    """
    Validate the loaded dataset has the expected structure and data types.
    
    Args:
        df (pd.DataFrame): The loaded DataFrame to validate
        
    Returns:
        bool: True if validation passes, raises DataLoadingError otherwise
    """
    expected_columns = {
        'Rank': np.integer,
        'Name': object,
        'Platform': object,
        'Year': np.float64,
        'Genre': object,
        'Publisher': object,
        'NA_Sales': np.float64,
        'EU_Sales': np.float64,
        'JP_Sales': np.float64,
        'Other_Sales': np.float64,
        'Global_Sales': np.float64
    }
    
    # Check for missing columns
    missing_cols = set(expected_columns.keys()) - set(df.columns)
    if missing_cols:
        raise DataLoadingError(f"Missing required columns: {missing_cols}")
    
    # Check for missing values
    if df.isnull().any().any():
        logger.warning("Dataset contains missing values")
        
    # Validate data types
    for col, dtype in expected_columns.items():
        if not np.issubdtype(df[col].dtype, dtype):
            try:
                df[col] = df[col].astype(dtype)
                logger.warning(f"Column {col} was converted to {dtype}")
            except Exception as e:
                raise DataLoadingError(f"Invalid data type for column {col}: {str(e)}")
    
    return True

def load_vgsales_data(file_path: str = "data/vgsales.csv") -> pd.DataFrame:
    """
    Load the video game sales dataset from CSV.
    
    Args:
        file_path (str): Path to the CSV file
        
    Returns:
        pd.DataFrame: Loaded and validated DataFrame
    """
    try:
        df = pd.read_csv(file_path)
        validate_dataset(df)
        logger.info(f"Successfully loaded dataset with {len(df)} records")
        return df
    except FileNotFoundError:
        raise DataLoadingError(f"Data file not found at {file_path}")
    except Exception as e:
        raise DataLoadingError(f"Error loading data: {str(e)}")

def get_unique_values(df: pd.DataFrame) -> Dict[str, list]:
    """
    Get unique values for categorical columns.
    
    Args:
        df (pd.DataFrame): The loaded DataFrame
        
    Returns:
        Dict[str, list]: Dictionary with column names as keys and lists of unique values
    """
    categorical_columns = ['Platform', 'Genre', 'Publisher']
    return {col: sorted(df[col].unique().tolist()) for col in categorical_columns}

def get_year_range(df: pd.DataFrame) -> Tuple[int, int]:
    """
    Get the range of years in the dataset.
    
    Args:
        df (pd.DataFrame): The loaded DataFrame
        
    Returns:
        Tuple[int, int]: Minimum and maximum years in the dataset
    """
    return int(df['Year'].min()), int(df['Year'].max())

def get_sales_summary(df: pd.DataFrame) -> Dict[str, float]:
    """
    Get summary statistics for sales columns.
    
    Args:
        df (pd.DataFrame): The loaded DataFrame
        
    Returns:
        Dict[str, float]: Dictionary with sales statistics
    """
    sales_columns = ['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales', 'Global_Sales']
    return {
        'total_global_sales': df['Global_Sales'].sum(),
        'avg_global_sales': df['Global_Sales'].mean(),
        'max_global_sales': df['Global_Sales'].max(),
        'regional_totals': {col: df[col].sum() for col in sales_columns[:-1]}
    }

def filter_data(
    df: pd.DataFrame,
    year_range: Optional[Tuple[int, int]] = None,
    platforms: Optional[list] = None,
    genres: Optional[list] = None,
    publishers: Optional[list] = None
) -> pd.DataFrame:
    """
    Filter the dataset based on various criteria.
    
    Args:
        df (pd.DataFrame): The input DataFrame
        year_range (Tuple[int, int], optional): Range of years to include
        platforms (list, optional): List of platforms to include
        genres (list, optional): List of genres to include
        publishers (list, optional): List of publishers to include
        
    Returns:
        pd.DataFrame: Filtered DataFrame
    """
    filtered_df = df.copy()
    
    if year_range:
        filtered_df = filtered_df[
            (filtered_df['Year'] >= year_range[0]) & 
            (filtered_df['Year'] <= year_range[1])
        ]
    
    if platforms:
        filtered_df = filtered_df[filtered_df['Platform'].isin(platforms)]
        
    if genres:
        filtered_df = filtered_df[filtered_df['Genre'].isin(genres)]
        
    if publishers:
        filtered_df = filtered_df[filtered_df['Publisher'].isin(publishers)]
    
    return filtered_df

if __name__ == "__main__":
    # Example usage and testing
    try:
        df = load_vgsales_data()
        print(f"Loaded {len(df)} records")
        print("\nSales Summary:")
        print(get_sales_summary(df))
        print("\nYear Range:")
        print(get_year_range(df))
        print("\nUnique Values Sample:")
        unique_vals = get_unique_values(df)
        for key, values in unique_vals.items():
            print(f"{key}: {len(values)} unique values")
    except DataLoadingError as e:
        logger.error(f"Failed to load data: {str(e)}")

@lru_cache(maxsize=1)
def _load_vgsales_data_cached(file_path: str = "data/vgsales.csv") -> pd.DataFrame:
    """
    Internal cached function to load the video game sales dataset.
    """
    return pd.read_csv(file_path)

def load_vgsales_data(file_path: str = "data/vgsales.csv") -> pd.DataFrame:
    """
    Load the video game sales dataset from CSV.
    
    Args:
        file_path (str): Path to the CSV file
        
    Returns:
        pd.DataFrame: Loaded and validated DataFrame
    """
    try:
        # Use cached data loading
        df = _load_vgsales_data_cached(file_path)
        validate_dataset(df)
        logger.info(f"Successfully loaded dataset with {len(df)} records")
        return df
    except FileNotFoundError:
        raise DataLoadingError(f"Data file not found at {file_path}")
    except Exception as e:
        raise DataLoadingError(f"Error loading data: {str(e)}")

def clear_data_cache():
    """Clear the data loading cache."""
    _load_vgsales_data_cached.cache_clear()
    logger.info("Data cache cleared")