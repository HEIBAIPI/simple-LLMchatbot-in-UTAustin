# app.py

import streamlit as st
from chatbot_logic import FriendlyBot, TeacherBot, FunnyBot
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os
from finance_analysis import StockDataAnalyzer

# --- Page Configuration ---
st.set_page_config(
    page_title="My AI Chatbot",
    page_icon="",
    layout="centered"
)

st.title("UTBot: Your AI Chat Companion")
st.write("Choose a personality from the sidebar and start chatting!")

# --- Sidebar for Bot Selection and Control ---
with st.sidebar:
    st.header("Configuration")

    # Initialize bot in session state if not present
    if 'bot' not in st.session_state:
        st.session_state.bot = None

    bot_choice = st.radio(
        "Choose your chatbot personality:",
        ('Friendly', 'Teacher', 'Funny'),
        key="bot_choice_radio",
        disabled=(st.session_state.bot is not None) # Disable after selection
    )

    subject = ""
    if bot_choice == 'Teacher':
        subject = st.text_input(
            "What subject should the teacher focus on?",
            "Quantum Mechanics",
            key="subject_input",
            disabled=(st.session_state.bot is not None)
        )
        bot_name = st.text_input(
           "What is the teacher's name?",
           "Albert",
           key="name_input",
           disabled=(st.session_state.bot is not None)
        )

    if st.button("Start Chat", key="start_button", disabled=(st.session_state.bot is not None)):
        if bot_choice == 'Friendly':
            st.session_state.bot = FriendlyBot(name="Joy")
        elif bot_choice == 'Teacher':
            if subject and bot_name:
                st.session_state.bot = TeacherBot(name=f"Professor {bot_name}", subject=subject)
            else:
                st.warning("Please enter BOTH a subject and a name for the Teacher Bot.")
                st.stop()
        else:  # Funny
            st.session_state.bot = FunnyBot(name="Comedy")
        
        # Initialize chat history
        st.session_state.messages = [{"role": "assistant", "content": "Hello! How can I help you today?"}]
        st.rerun()

    if st.session_state.bot is not None:
        if st.button("Reset Conversation", key="reset_button"):
            st.session_state.bot = None
            st.session_state.messages = []
            st.rerun()

# --- Finance Analysis Section ---
if st.session_state.bot is not None:
    st.sidebar.header("Finance Analysis")
    
    if st.sidebar.button("Finance Mode"):
        st.session_state.finance_mode = True
        st.rerun()

# --- Finance Mode Interface ---
if st.session_state.get('finance_mode', False):
    st.header("Finance Analysis Mode")
    
    # Analysis type selection
    analysis_type = st.selectbox(
        "What would you like to generate?",
        ["CSV data only", "Chart visualization", "Both CSV and chart"]
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        start_date = st.date_input("Start Date", value=datetime(2023, 1, 1))
        end_date = st.date_input("End Date", value=datetime(2023, 12, 31))
    
    with col2:
        tickers_input = st.text_input("Stock Tickers (comma-separated)", "AAPL,GOOGL,MSFT")
        saving_path = st.text_input("Saving Directory", "./finance_data")
    
    if st.button("Analyze Stocks"):
        if start_date >= end_date:
            st.error("End date must be after start date.")
        elif not tickers_input.strip():
            st.error("Please enter at least one ticker symbol.")
        else:
            with st.spinner("Processing analysis..."):
                try:
                    # Convert dates to string format
                    start_date_str = start_date.strftime('%Y-%m-%d')
                    end_date_str = end_date.strftime('%Y-%m-%d')
                    
                    # Parse tickers
                    tickers = [t.strip().upper() for t in tickers_input.split(',') if t.strip()]
                    
                    # Create analyzer
                    analyzer = StockDataAnalyzer()
                    
                    # Validate inputs
                    if not analyzer.validate_inputs(start_date_str, end_date_str, tickers, saving_path):
                        st.error("Invalid inputs. Please check your data.")
                        st.stop()
                    
                    # Remove duplicates
                    unique_tickers = analyzer.remove_duplicates(tickers)
                    
                    # Fetch data
                    combined_data = analyzer.combine_stock_data(unique_tickers, start_date_str, end_date_str)
                    
                    if combined_data.empty:
                        st.error("No valid data was fetched for any ticker.")
                        if analyzer.failed_tickers:
                            st.write(f"Failed tickers: {analyzer.failed_tickers}")
                        st.stop()
                    
                    # Generate outputs
                    results = []
                    
                    if analysis_type in ["CSV data only", "Both CSV and chart"]:
                        csv_path = analyzer.save_data_to_csv(combined_data, saving_path)
                        results.append(f"CSV data saved to: {csv_path}")
                    
                    if analysis_type in ["Chart visualization", "Both CSV and chart"]:
                        chart_path = analyzer.create_stock_chart(combined_data, saving_path)
                        results.append(f"Chart saved to: {chart_path}")
                    
                    # Display results
                    st.success("Analysis completed successfully!")
                    for result in results:
                        st.write(result)
                    
                    # Show failed tickers if any
                    if analyzer.failed_tickers:
                        st.warning(f"Failed tickers: {analyzer.failed_tickers}")
                    
                    # Generate and show summary
                    summary = analyzer.generate_summary_report(combined_data)
                    st.subheader("Summary Report")
                    
                    for ticker, stats in summary.items():
                        with st.expander(f"{ticker} Statistics"):
                            col1, col2 = st.columns(2)
                            with col1:
                                st.metric("Records", stats['records_count'])
                                st.metric("Avg Close Price", f"${stats['avg_close_price']}")
                                st.metric("Price Change", f"${stats['price_change']}")
                            with col2:
                                st.metric("Highest Price", f"${stats['highest_price']}")
                                st.metric("Lowest Price", f"${stats['lowest_price']}")
                                st.write(f"**Date Range:** {stats['date_range']}")
                
                except Exception as e:
                    st.error(f"Error during analysis: {e}")
    
    if st.sidebar.button("Back to Chat"):
        st.session_state.finance_mode = False
        st.rerun()

# --- Main Chat Interface ---
elif 'bot' in st.session_state and st.session_state.bot is not None:
    # Display chat messages
    for message in st.session_state.get('messages', []):
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("What would you like to say?"):
        # Add user message to display history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate and display assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = st.session_state.bot.generate_response(prompt)
                st.markdown(response)
        
        # Add assistant response to display history
        st.session_state.messages.append({"role": "assistant", "content": response})
else:
    st.info("Please configure your chatbot in the sidebar and click 'Start Chat'.")