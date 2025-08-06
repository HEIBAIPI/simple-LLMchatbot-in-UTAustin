"""
Stock data analysis tool using yfinance
A modular tool for fetching, processing and visualizing stock data
"""

import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import os
from typing import List, Tuple, Dict, Optional

class StockDataAnalyzer:
    """
    Main class for analyzing stock data from Yahoo Finance
    Handles multiple tickers, error handling, and creates charts
    """
    
    def __init__(self):
        """Set up the analyzer"""
        self.failed_tickers = []
        
    def validate_inputs(self, start_time: str, end_time: str, tickers: List[str], saving_path: str) -> bool:
        """
        Check if all inputs are valid before processing
        
        Args:
            start_time: Start date (YYYY-MM-DD)
            end_time: End date (YYYY-MM-DD)
            tickers: List of stock symbols
            saving_path: Where to save the files
            
        Returns:
            True if everything looks good, False if there's an issue
        """
        try:
            # Make sure dates are in the right format
            datetime.strptime(start_time, '%Y-%m-%d')
            datetime.strptime(end_time, '%Y-%m-%d')
            
            # Check that we have some tickers to work with
            if not isinstance(tickers, list) or len(tickers) == 0:
                raise ValueError("Tickers must be a non-empty list")
            
            # Create the output folder if it doesn't exist
            os.makedirs(saving_path, exist_ok=True)
            
            return True
            
        except ValueError as e:
            return False
        except Exception as e:
            return False
    
    def remove_duplicates(self, tickers: List[str]) -> List[str]:
        """
        Get rid of duplicate tickers but keep the order
        
        Args:
            tickers: List of stock symbols
            
        Returns:
            Clean list without duplicates
        """
        unique_tickers = list(dict.fromkeys([ticker.upper().strip() for ticker in tickers]))
        
        return unique_tickers
    
    def fetch_stock_data(self, ticker: str, start_time: str, end_time: str) -> Optional[pd.DataFrame]:
        """
        Download stock data for one ticker
        
        Args:
            ticker: Stock symbol like 'AAPL'
            start_time: When to start (YYYY-MM-DD)
            end_time: When to end (YYYY-MM-DD)
            
        Returns:
            Stock data if successful, None if it failed
        """
        try:
            stock = yf.Ticker(ticker)
            data = stock.history(start=start_time, end=end_time)
            
            if data.empty:
                raise ValueError(f"No data available for {ticker}")
            
            # Add a column to know which stock this data is for
            data['Ticker'] = ticker
            data.reset_index(inplace=True)
            
            return data
            
        except Exception as e:
            self.failed_tickers.append(ticker)
            return None
    
    def combine_stock_data(self, tickers: List[str], start_time: str, end_time: str) -> pd.DataFrame:
        """
        Download data for multiple stocks and put them all together
        
        Args:
            tickers: List of stock symbols
            start_time: Start date
            end_time: End date
            
        Returns:
            All the stock data combined into one table
        """
        all_data = []
        
        for ticker in tickers:
            data = self.fetch_stock_data(ticker, start_time, end_time)
            if data is not None:
                all_data.append(data)
        
        if all_data:
            combined_data = pd.concat(all_data, ignore_index=True)
            return combined_data
        else:
            return pd.DataFrame()
    
    def save_data_to_csv(self, data: pd.DataFrame, saving_path: str, filename: str = None) -> str:
        """
        Save the stock data to a CSV file
        
        Args:
            data: The stock data to save
            saving_path: Where to put the file
            filename: What to call the file (optional)
            
        Returns:
            The full path where the file was saved
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"stock_data_{timestamp}.csv"
        
        full_path = os.path.join(saving_path, filename)
        data.to_csv(full_path, index=False)
        
        return full_path
    
    def calculate_date_interval(self, start_date, end_date):
        """
        Figure out how often to show dates on the chart
        
        Args:
            start_date: When the data starts
            end_date: When the data ends
            
        Returns:
            How many months between each date label (1 for short periods, 6+ for longer)
        """
        # Convert strings to datetime objects if needed
        if isinstance(start_date, str):
            start_date = pd.to_datetime(start_date)
        if isinstance(end_date, str):
            end_date = pd.to_datetime(end_date)
        
        # How many days are we looking at?
        time_span_days = (end_date - start_date).days
        
        # Take 1/10 of that time span in months
        tenth_span_months = (time_span_days / 30.44) / 10  # 30.44 days per month on average
        
        # For short periods, show monthly labels
        if tenth_span_months < 6:
            interval_months = 1
        else:
            # For longer periods, round up to the nearest half-year
            interval_months = int((tenth_span_months + 5) // 6) * 6
        
        return interval_months

    def create_stock_chart(self, data: pd.DataFrame, saving_path: str, filename: str = None) -> str:
        """
        Make a chart showing stock prices over time
        
        Args:
            data: The stock data to plot
            saving_path: Where to save the chart
            filename: What to call the chart file (optional)
            
        Returns:
            The full path where the chart was saved
        """
        if data.empty:
            return ""
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"stock_chart_{timestamp}.png"
        
        # Set up the chart
        fig, ax = plt.subplots(1, 1, figsize=(12, 8))
        fig.suptitle('Stock Price Analysis', fontsize=16, fontweight='bold')
        
        # Draw lines for each stock
        unique_tickers = data['Ticker'].unique()
        colors = plt.cm.Set3(range(len(unique_tickers)))
        
        for i, ticker in enumerate(unique_tickers):
            ticker_data = data[data['Ticker'] == ticker]
            ax.plot(ticker_data['Date'], ticker_data['Close'], 
                   label=ticker, color=colors[i], linewidth=2)
        
        # Figure out how often to show dates on the x-axis
        min_date = data['Date'].min()
        max_date = data['Date'].max()
        interval_months = self.calculate_date_interval(min_date, max_date)
        
        ax.set_title('Closing Prices Over Time', fontsize=14, fontweight='bold')
        ax.set_xlabel('Date')
        ax.set_ylabel('Price ($)')
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        ax.grid(True, alpha=0.3)
        
        # Set up the date labels on the x-axis
        if interval_months >= 12:
            # For long periods, just show the year
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
        else:
            # For shorter periods, show year and month
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=interval_months))
        
        # Tilt the date labels so they don't overlap
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
        
        plt.tight_layout()
        
        # Save the chart to a file
        full_path = os.path.join(saving_path, filename)
        plt.savefig(full_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return full_path
    
    def generate_summary_report(self, data: pd.DataFrame) -> Dict:
        """
        Create a summary of the stock data
        
        Args:
            data: The stock data to summarize
            
        Returns:
            A dictionary with key stats for each stock
        """
        if data.empty:
            return {}
        
        summary = {}
        for ticker in data['Ticker'].unique():
            ticker_data = data[data['Ticker'] == ticker]
            summary[ticker] = {
                'records_count': len(ticker_data),
                'date_range': f"{ticker_data['Date'].min()} to {ticker_data['Date'].max()}",
                'avg_close_price': round(ticker_data['Close'].mean(), 2),
                'price_change': round(ticker_data['Close'].iloc[-1] - ticker_data['Close'].iloc[0], 2),
                'highest_price': round(ticker_data['High'].max(), 2),
                'lowest_price': round(ticker_data['Low'].min(), 2)
            }
        
        return summary
    




