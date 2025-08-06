import os
import openai
import time
import requests
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from groq import Groq
import random
import re
import yfinance as yf

from datetime import datetime
def clear_pre_messages(pre_messages):
    """Clear old messages to maintain conversation history within limits"""
    if pre_messages is None:
        pre_messages = []
    if len(pre_messages)/2 > 3:
        pre_messages.pop(0)
        pre_messages.pop(0)
    return pre_messages
class LLM_Chat:
    """LLM Chat class for interacting with Groq API"""
    def __init__(self):
        self.model = "gemma2-9b-it"
        self.api_key = "API KEY"
        self.client =  Groq(api_key=self.api_key)

    def generate_response(self, pre_messages=None):
        """Generate response from LLM using previous messages as context"""
        pre_messages = clear_pre_messages(pre_messages)
        response = self.client.chat.completions.create(
        model=self.model,
        messages=pre_messages,
        temperature=1,
        max_completion_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
        )
        # Stream response processing - collect all chunks to build complete response
        full_content = ""
        for chunk in response:
                # Process each chunk from streaming response
                content = chunk.choices[0].delta.content
                if content is not None:  # Check if content is not None
                    full_content += content
                    # Compress multiple consecutive newlines to single newline
                    display_content = re.sub(r'[\n\r]+', '\r', content)
                    # Remove trailing newlines to avoid extra blank lines
                    display_content = display_content.rstrip('\n\r')
                    print(display_content, end="", flush=True)
        print()
        print()
        # Clean up final content by compressing newlines and trimming whitespace
        full_content = re.sub(r'[\n\r]+', '\n', full_content)
        full_content = full_content.rstrip()
        remember_assistant_previous_messages(pre_messages,full_content)
def personality_choose():
    """Let user choose AI personality type"""
    while True:  # Use loop instead of recursion
        print("--------------------------------")
        print("Personality: ")
        personality = input()
        if personality == "exit":
            print("Goodbye!")
            return None
        if personality == "random":
            personality = str(random.choice(["1", "2", "3"]))
        if personality == "1" or personality == "2" or personality == "3": 
            set_personality(personality)
            return personality
        else:
            print("Invalid personality. Please try again.")
            # Continue loop, don't use recursion
def set_personality(personality):
    """Set AI personality based on user choice"""
    global now_personality  # Declare as global variable
    if personality == "1":
        hint = "you need to play a person that's casual and warm. Do not use emoji or emoticons in your responses."
    elif personality == "2":
        hint = "you need to play a person that's more formal and educational. Do not use emoji or emoticons in your responses."
    elif personality == "3":
        hint ="You need to play a person with a sharp tongue and a good sense of humor, but don't act too exaggerated. Do not use emoji or emoticons in your responses."
    else:
        # Default case to prevent undefined hint variable
        hint = "you need to play a helpful and friendly assistant. Do not use emoji or emoticons in your responses."
    now_personality = {"role": "system", "content": hint}
    llm.generate_response([now_personality])
def remember_users_previous_messages(pre_messages, user_input):
    """Add user message to conversation history"""
    pre_messages.append({"role": "user", "content": user_input})
    pre_messages = clear_pre_messages(pre_messages)
    return pre_messages
def remember_assistant_previous_messages(pre_messages, assistant_input):
    """Add assistant message to conversation history"""
    pre_messages.append({"role": "assistant", "content": assistant_input})
    pre_messages = clear_pre_messages(pre_messages)
    return pre_messages
def is_exit(user_input):
    """Check if user wants to exit"""
    if user_input == "exit":
        return True
    return False
def is_change_personality(user_input):
    """Check if user wants to change personality"""
    if user_input == "change":
        return True
    return False
def is_finance_analysis(user_input):
    """Check if user wants to analyze finance"""
    if user_input == "finance":
        return True
    return False

def validate_date_format(date_string):
    """Validate if date string is in YYYY-MM-DD format"""
    try:
        datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def validate_tickers(tickers_string):
    """Validate if tickers string contains valid ticker symbols"""
    if not tickers_string or not tickers_string.strip():
        return False, "Empty ticker list"
    
    tickers = [t.strip().upper() for t in tickers_string.split(',') if t.strip()]
    if not tickers:
        return False, "No valid tickers found"
    
    # Check if each ticker looks reasonable (letters only, 1-5 characters)
    invalid_tickers = []
    for ticker in tickers:
        if not ticker.isalpha() or len(ticker) < 1 or len(ticker) > 5:
            invalid_tickers.append(ticker)
    
    if invalid_tickers:
        return False, f"Invalid ticker format: {invalid_tickers}"
    
    return True, tickers

def validate_path(path_string):
    """Validate if path string is reasonable"""
    if not path_string or not path_string.strip():
        return False, "Empty path"
    
    # Check for basic path validity (avoid obvious issues)
    # Note: Colon (:) is valid in Unix paths and drive letters in Windows
    invalid_chars = ['<', '>', '"', '|', '?', '*']
    for char in invalid_chars:
        if char in path_string:
            return False, f"Invalid character '{char}' in path"
    
    # Basic length check
    if len(path_string.strip()) > 255:
        return False, "Path too long"
    
    return True, path_string.strip()

def finance_mode():
    """Handle finance analysis mode"""
    print("================================")
    print("Finance Analysis Mode")
    print("================================")
    print("Commands:")
    print("- 'quit': Return to chat mode")
    print("- 'exit': End conversation")
    print("--------------------------------")
    
    while True:
        print("\nWhat would you like to do?")
        print("1. Generate CSV data only")
        print("2. Generate chart visualization")
        print("3. Generate both CSV and chart")
        print("\nYour choice (1/2/3, or quit/exit): ")
        
        choice = input().strip().lower()
        
        if choice == 'quit':
            print("Returning to chat mode...")
            return False
        elif choice == 'exit':
            print("Goodbye!")
            return True
        elif choice not in ['1', '2', '3']:
            print("Invalid choice. Please enter 1, 2, 3, quit, or exit.")
            continue
        
        # Get user inputs with validation
        
        # Get start date with validation
        while True:
            print("\nEnter start date (YYYY-MM-DD): ")
            start_date = input().strip()
            if start_date.lower() == 'quit':
                break
            elif start_date.lower() == 'exit':
                print("Goodbye!")
                return True
            elif validate_date_format(start_date):
                break
            else:
                print("Invalid date format. Please use YYYY-MM-DD format (e.g., 2023-01-01)")
        
        if start_date.lower() == 'quit':
            continue
            
        # Get end date with validation
        while True:
            print("Enter end date (YYYY-MM-DD): ")
            end_date = input().strip()
            if end_date.lower() == 'quit':
                break
            elif end_date.lower() == 'exit':
                print("Goodbye!")
                return True
            elif validate_date_format(end_date):
                # Also check if end date is after start date
                try:
                    start_dt = datetime.strptime(start_date, '%Y-%m-%d')
                    end_dt = datetime.strptime(end_date, '%Y-%m-%d')
                    if end_dt <= start_dt:
                        print("End date must be after start date.")
                        continue
                    break
                except:
                    print("Invalid date format. Please use YYYY-MM-DD format (e.g., 2023-12-31)")
            else:
                print("Invalid date format. Please use YYYY-MM-DD format (e.g., 2023-12-31)")
        
        if end_date.lower() == 'quit':
            continue
            
        # Get tickers with validation
        while True:
            print("Enter stock tickers (comma-separated, e.g., AAPL,GOOGL,MSFT): ")
            tickers_input = input().strip()
            if tickers_input.lower() == 'quit':
                break
            elif tickers_input.lower() == 'exit':
                print("Goodbye!")
                return True
            else:
                is_valid, result = validate_tickers(tickers_input)
                if is_valid:
                    tickers = result
                    break
                else:
                    print(f"Invalid ticker input: {result}")
                    print("Please enter valid stock symbols (1-5 letters, comma-separated)")
        
        if tickers_input.lower() == 'quit':
            continue
            
        # Get saving path with validation
        while True:
            print("Enter saving path (directory): ")
            saving_path = input().strip()
            if saving_path.lower() == 'quit':
                break
            elif saving_path.lower() == 'exit':
                print("Goodbye!")
                return True
            else:
                is_valid, result = validate_path(saving_path)
                if is_valid:
                    saving_path = result
                    break
                else:
                    print(f"Invalid path: {result}")
                    print("Please enter a valid directory path")
        
        if saving_path.lower() == 'quit':
            continue
        
        print(f"\nProcessing analysis...")
        print(f"Date range: {start_date} to {end_date}")
        print(f"Tickers: {tickers}")
        print(f"Output directory: {saving_path}")
        print("-" * 50)
        
        try:
            # Import the analyzer class for more control
            from finance_analysis import StockDataAnalyzer
            analyzer = StockDataAnalyzer()
            
            # Final validation (should pass since we validated inputs above)
            if not analyzer.validate_inputs(start_date, end_date, tickers, saving_path):
                print("Unexpected validation error. Please try again.")
                continue
            
            # Remove duplicates
            unique_tickers = analyzer.remove_duplicates(tickers)
            
            # Fetch data
            combined_data = analyzer.combine_stock_data(unique_tickers, start_date, end_date)
            
            if combined_data.empty:
                print("No valid data was fetched for any ticker.")
                print(f"Failed tickers: {analyzer.failed_tickers}")
                continue
            
            # Generate outputs based on choice
            if choice == '1':  # CSV only
                csv_path = analyzer.save_data_to_csv(combined_data, saving_path)
                print(f"CSV data saved to: {csv_path}")
            elif choice == '2':  # Chart only
                chart_path = analyzer.create_stock_chart(combined_data, saving_path)
                print(f"Chart saved to: {chart_path}")
            elif choice == '3':  # Both
                csv_path = analyzer.save_data_to_csv(combined_data, saving_path)
                chart_path = analyzer.create_stock_chart(combined_data, saving_path)
                print(f"CSV data saved to: {csv_path}")
                print(f"Chart saved to: {chart_path}")
            
            # Show failed tickers if any
            if analyzer.failed_tickers:
                print(f"Failed tickers: {analyzer.failed_tickers}")
            
            # Generate and show summary
            summary = analyzer.generate_summary_report(combined_data)
            print("\nSummary Report:")
            for ticker, stats in summary.items():
                print(f"  {ticker}:")
                print(f"    Records: {stats['records_count']}")
                print(f"    Date Range: {stats['date_range']}")
                print(f"    Avg Close Price: ${stats['avg_close_price']}")
                print(f"    Price Change: ${stats['price_change']}")
                print(f"    Highest Price: ${stats['highest_price']}")
                print(f"    Lowest Price: ${stats['lowest_price']}")
                    
        except Exception as e:
            print(f"Error during analysis: {e}")
            print("Please check your inputs and try again.")
        
        print("\n" + "="*50)
        print("Analysis complete. You can run another analysis or type 'quit' to return to chat mode.")
    
    return False
def main():
    """Main function to run the LLM chat application"""
    global llm 
    global now_personality
    now_personality = None  # Initialize global variable
    llm = LLM_Chat()
    kind_of_personality = ['A FriendlyBot that’s casual and warm','A TeacherBot that’s more formal and educational','A FunnyBot that’s with a sharp tongue and a sense of humor']
    print("Enhanced LLM Chat & Finance Analyzer")
    print("=====================================")
    print("Available Modes:")
    print("Chat Mode - Conversational AI with different personalities")
    print("Finance Mode - Stock data analysis and visualization")
    print("=====================================")
    print("Commands:")
    print("- 'finance': Switch to finance analysis mode")
    print("- 'change': Change AI personality")
    print("- 'exit': End conversation")
    print("=====================================")
    print("AI Personalities:")
    print("1. FriendlyBot - Casual and warm conversations")
    print("2. TeacherBot - Formal and educational responses")
    print("3. FunnyBot - Sharp wit and good humor")
    print("Choose by typing the number, or 'random' for surprise.")
    print("=====================================")
    print("Now, let's start the conversation!")
    personality = personality_choose()
    if personality is None:  # User chose to exit
        return
    print("--------------------------------")
    pre_messages = []
    print("Personality: ",kind_of_personality[int(personality)-1])
    print("You: ")
    user_input = input()
    print()
    if is_exit(user_input):
        print("Goodbye!")
        return
    while is_change_personality(user_input):
        personality = personality_choose()
        if personality is None:  # User chose to exit
            return
        print("--------------------------------")
        print("Personality: ",kind_of_personality[int(personality)-1])
        print("You: ")
        user_input = input()
        if is_exit(user_input):
            print("Goodbye!")
            return
    
    # Check if user wants to enter finance mode
    if is_finance_analysis(user_input):
        should_exit = finance_mode()
        if should_exit:
            return
        print("Back to chat mode.")
        print("Personality: ",kind_of_personality[int(personality)-1])
        print("You: ")
        user_input = input()
        print()
        if is_exit(user_input):
            print("Goodbye!")
            return
    
    pre_messages = remember_users_previous_messages([],user_input)
    background_message = [now_personality]+pre_messages
    print("Assistant: ")
    llm.generate_response(background_message)
    while True:
        print("You: ")
        user_input = input()
        print()
        if is_exit(user_input):
            print("Goodbye!")
            return
        
        # Check for finance mode
        if is_finance_analysis(user_input):
            should_exit = finance_mode()
            if should_exit:
                return
            print("Back to chat mode.")
            print("Personality: ",kind_of_personality[int(personality)-1])
            continue
            
        while is_change_personality(user_input):
            personality = personality_choose()
            if personality is None:  # User chose to exit
                return
            print("--------------------------------")
            print("Personality: ",kind_of_personality[int(personality)-1])
            print("You: ")
            user_input = input()
            print()
            if is_exit(user_input):
                print("Goodbye!")
                return
        clear_pre_messages([pre_messages])
        pre_messages = remember_users_previous_messages(pre_messages,user_input)
        background_message = [now_personality]+pre_messages
        print("Assistant: ")
        llm.generate_response(background_message)
if __name__ == "__main__":
    main()    

