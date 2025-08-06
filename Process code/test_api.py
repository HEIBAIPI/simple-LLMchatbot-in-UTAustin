#!/usr/bin/env python3
"""
Test script to check if the Groq API key is working
"""

from utils import query_llm

def test_api():
    """Test the API connection"""
    print("Testing Groq API connection...")
    
    try:
        response = query_llm("Hello, can you respond with 'API is working' if you can see this message?")
        print(f"Response: {response}")
        
        if "Error" in response:
            print("❌ API test failed")
            return False
        else:
            print("✅ API test successful")
            return True
            
    except Exception as e:
        print(f"❌ Error during API test: {e}")
        return False

if __name__ == "__main__":
    test_api() 