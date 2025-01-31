"""
Logging configuration for the Video Game Sales Dashboard.
This module sets up logging to both file and console.
"""

import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
import os
from datetime import datetime

def setup_logging(log_dir: str = "logs") -> logging.Logger:
    """
    Set up logging configuration to write logs to both file and console.
    
    Parameters:
    -----------
    log_dir : str
        Directory where log files will be stored
        
    Returns:
    --------
    logging.Logger
        Configured logger instance
    """
    # Create logs directory if it doesn't exist
    Path(log_dir).mkdir(exist_ok=True)
    
    # Create logger
    logger = logging.getLogger('vgsales_dashboard')
    logger.setLevel(logging.DEBUG)
    
    # Create formatters
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
    )
    console_formatter = logging.Formatter(
        '%(levelname)s - %(message)s'
    )
    
    # Create and configure file handler with rotation
    log_file = f"{datetime.now().strftime('%Y%m%d')}_vgsales.log"
    file_handler = RotatingFileHandler(
        os.path.join(log_dir, log_file),
        maxBytes=10485760,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(file_formatter)
    
    # Create and configure console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(console_formatter)
    
    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

def list_logs(log_dir: str = "logs") -> list:
    """
    List all available log files.
    
    Parameters:
    -----------
    log_dir : str
        Directory where log files are stored
        
    Returns:
    --------
    list
        List of log file names
    """
    log_path = Path(log_dir)
    if not log_path.exists():
        return []
    
    return sorted(
        [f.name for f in log_path.glob("*.log")],
        reverse=True
    )

def read_log_file(filename: str, log_dir: str = "logs") -> str:
    """
    Read contents of a specific log file.
    
    Parameters:
    -----------
    filename : str
        Name of the log file to read
    log_dir : str
        Directory where log files are stored
        
    Returns:
    --------
    str
        Contents of the log file
    """
    log_path = Path(log_dir) / filename
    if not log_path.exists():
        return f"Log file {filename} not found"
    
    try:
        with open(log_path, 'r') as f:
            return f.read()
    except Exception as e:
        return f"Error reading log file: {str(e)}"

def clear_old_logs(log_dir: str = "logs", keep_days: int = 30) -> None:
    """
    Clear log files older than specified days.
    
    Parameters:
    -----------
    log_dir : str
        Directory where log files are stored
    keep_days : int
        Number of days to keep logs for
    """
    log_path = Path(log_dir)
    if not log_path.exists():
        return
    
    current_time = datetime.now().timestamp()
    
    for log_file in log_path.glob("*.log*"):
        file_age = current_time - os.path.getmtime(log_file)
        if file_age > (keep_days * 86400):  # Convert days to seconds
            try:
                os.remove(log_file)
            except Exception as e:
                print(f"Error removing old log file {log_file}: {str(e)}")