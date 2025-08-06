# AI Chatbot with Finance Analysis - Feature Summary

## How Your Chatbot Works

The chatbot is built with a modular architecture consisting of several key components:

### Core Architecture
- **`chatbot_logic.py`**: Contains the core chatbot classes with memory management and personality system
- **`utils.py`**: Handles API communication with Groq's LLM service using the `gemma2-9b-it` model
- **`app.py`**: Provides a modern Streamlit web interface for user interaction
- **`finance_analysis.py`**: Modular stock analysis tool integrated into the chatbot

### Conversation Management
The chatbot maintains conversation context through a `Memory` class that stores the last 6 messages (3 exchanges) to provide relevant context for responses. Each interaction follows this flow:
1. User input is stored in memory
2. A context-aware prompt is created using conversation history
3. The LLM generates a response based on the selected personality
4. The bot's response is stored in memory for future context

### Dual Interface Support
- **Command Line Interface**: Direct interaction through `LLM-chat.py` for quick testing
- **Web Interface**: Modern Streamlit-based UI in `app.py` with sidebar configuration and real-time chat display

## What Makes Each Personality Unique

### 1. FriendlyBot (Joy)
- **Style**: Casual and warm approach
- **Characteristics**: Uses informal language, welcoming tone, makes users feel comfortable
- **Use Case**: General conversation, casual assistance, creating a relaxed atmosphere
- **Prompt Style**: "You are Joy, a casual and warm AI assistant. Be approachable, friendly, and welcoming in your responses."

### 2. TeacherBot (Professor)
- **Style**: Formal and educational approach
- **Characteristics**: Provides detailed explanations, uses teaching techniques, patient and clear communication
- **Use Case**: Educational content, detailed explanations, structured learning
- **Prompt Style**: "You are Professor [Name], a formal and educational AI assistant specializing in [Subject]. Provide detailed explanations and use teaching techniques."

### 3. FunnyBot (Comedy)
- **Style**: Witty and humorous with sharp wit
- **Characteristics**: Uses clever humor, wordplay, entertaining responses while remaining helpful
- **Use Case**: Entertainment, light-hearted conversations, clever problem-solving
- **Prompt Style**: "You are Comedy, a witty and humorous AI assistant with sharp wit and a good sense of humor. Use clever observations and appropriate jokes."

## Extra Features Added

### 1. Finance Analysis Module
**Integration**: Seamlessly integrated into both CLI and web interfaces
**Capabilities**:
- Fetch real-time stock data from Yahoo Finance using `yfinance`
- Generate CSV exports with combined data from multiple tickers
- Create professional stock charts with dynamic x-axis scaling
- Handle duplicate tickers automatically
- Track and report failed ticker symbols
- Generate comprehensive summary reports with key statistics

**Key Features**:
- **Dynamic Chart Scaling**: X-axis intervals automatically adjust based on time span (monthly for <6 months, half-year intervals for longer periods)
- **Error Handling**: Robust validation for dates, tickers, and file paths with real-time feedback
- **Data Management**: Automatic duplicate removal and failed ticker tracking
- **Professional Output**: High-quality charts with proper formatting and statistics

### 2. Advanced Input Validation
- **Date Format Validation**: Ensures YYYY-MM-DD format with immediate feedback
- **Ticker Symbol Validation**: Checks for valid stock symbols (1-5 letters, alpha only)
- **Path Validation**: Verifies file/directory paths are accessible
- **Real-time Feedback**: Users receive immediate error messages rather than waiting for process completion

### 3. Memory Management System
- **Context Preservation**: Maintains conversation history for contextual responses
- **Memory Limits**: Automatically manages memory to prevent context overflow
- **Smart Trimming**: Keeps last 6 messages (3 exchanges) for optimal context

### 4. Dual Mode Operation
- **Chat Mode**: Standard conversational AI with personality-based responses
- **Finance Mode**: Specialized stock analysis with data visualization
- **Seamless Switching**: Users can switch between modes without losing conversation context

### 5. Professional UI/UX
- **Clean Interface**: Removed all emoji icons for professional appearance
- **Responsive Design**: Streamlit interface adapts to different screen sizes
- **Session Management**: Maintains state across interactions
- **Progress Indicators**: Loading spinners and status messages for better user experience

### 6. Error Handling and Robustness
- **API Error Management**: Graceful handling of API key issues and connection problems
- **Data Validation**: Comprehensive input checking before processing
- **Exception Handling**: User-friendly error messages for all failure scenarios
- **Fallback Mechanisms**: Alternative responses when primary functions fail

## Technical Implementation

### API Integration
- Uses Groq's `gemma2-9b-it` model for fast, reliable responses
- Streaming support for real-time response generation
- Error handling for authentication and connection issues

### Modular Design
- Separated concerns across multiple files for maintainability
- Reusable components (finance analysis, memory management)
- Easy to extend with new personalities or features

### Data Processing
- Pandas for efficient data manipulation
- Matplotlib for professional chart generation
- YFinance for reliable stock data access

This chatbot demonstrates advanced AI integration with practical financial analysis capabilities, creating a versatile tool for both casual conversation and professional stock market analysis. 