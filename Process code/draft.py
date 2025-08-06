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
class LLM_Finance:
    """LLM Finance class for analyzing finance"""
    def __init__(self,start_date,end_date,ticker,saving_path="data.csv"):
        self.start_date = start_date
        self.end_date = end_date
        self.ticker = ticker
        self.saving_path = saving_path
    def get_data(self):
        """Get data from Yahoo Finance"""
        data = yf.download(self.ticker, start=self.start_date, end=self.end_date)
        data.to_csv(self.saving_path)
        return data
    def save_png(self,data,saving_path):
        """Save data to jpg"""
        data.plot(kind="line")
        plt.savefig(saving_path)
        plt.close()
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
        hint = "you need to play a person that’s casual and warm"
    elif personality == "2":
        hint = "you need to play a person that’s more formal and educational"
    elif personality == "3":
        hint ="You need to play a person with a sharp tongue and a good sense of humor,but don't act too exaggerated."
    else:
        # Default case to prevent undefined hint variable
        hint = "you need to play a helpful and friendly assistant"
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
def main():
    """Main function to run the LLM chat application"""
    global llm 
    global now_personality
    now_personality = None  # Initialize global variable
    llm = LLM_Chat()
    kind_of_personality = ['A FriendlyBot that’s casual and warm','A TeacherBot that’s more formal and educational','A FunnyBot that’s with a sharp tongue and a sense of humor']
    print("Welcome to the LLM Chat! Type 'exit' to end the conversation.")
    print("Our LLM Chat has two modes:")
    print("1. Chat")
    print("2. Finance Analysis")
    print("You can shift between the two modes by typing 'shift'.")
    print("--------------------------------")
    print("Our LLM Chat has three different personalities:")
    print("1. A FriendlyBot that’s casual and warm")
    print("2. A TeacherBot that’s more formal and educational")
    print("3. A FunnyBot that’s with a sharp tongue and a sense of humor")
    print("You can choose a personality by typing the number of the personality you want to chat with.")
    print("You can also choose to chat with a random personality by typing 'random'.")
    print("during the conversation, you can also choose to change the personality by typing 'change'and then the number of the personality you want to chat with.")
    print("--------------------------------")
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

