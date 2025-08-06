from typing import List, Dict
from utils import query_llm

class Memory:
    """Stores conversation history"""
    def __init__(self):
        # Store last 3 messages (each message is a dictionary with 'role' and 'content')
        self.messages: List[Dict] = []
    
    def add_message(self, role: str, content: str) -> None:
        """
        Add a new message to memory
        Args:
            role: Either "user" or "bot" 
            content: The message content
        
        TODO:
        - Create a dictionary to store the message (hint: what two key-value pairs do you need?)
        - Add it to self.messages
        - Remember we only want to keep the last 3 messages (hint: list slicing can help here)
        """
        # Create a dictionary to store the message
        message = {"role": role, "content": content}
        
        # Add it to self.messages
        self.messages.append(message)
        
        # Keep only the last 3 messages (6 total for 3 exchanges)
        if len(self.messages) > 6:
            self.messages = self.messages[-6:]
    
    def get_recent_messages(self) -> str:
        """
        Get string of recent messages for context
        Returns:
            A string containing the last few messages
        
        TODO:
        - Loop through self.messages to build your output string
        - For each message, format it as "{Role}: {content}" with a newline
        - Remember to capitalize the role for readability
        - Return the final formatted string (hint: strip() can clean up extra whitespace)
        """
        output = ""
        for message in self.messages:
            role = message["role"].capitalize()
            content = message["content"]
            output += f"{role}: {content}\n"
        return output.strip()

class Chatbot:
    """Base chatbot class with core functionality"""
    def __init__(self, name: str):
        self.name: str = name
        self.memory: Memory = Memory()
    
    def _create_prompt(self, user_input: str) -> str:
        """
        Create a prompt for the LLM
        Args:
            user_input: The user's message
        Returns:
            A formatted prompt string
        
        TODO: Think about:
        - What information does the LLM need to generate a good response?
        - How can you include the conversation history?
        - How should you structure the prompt to be clear?
        """
        # Get recent conversation history
        recent_messages = self.memory.get_recent_messages()
        
        # Create a comprehensive prompt with context
        prompt = f"""You are {self.name}, a helpful AI assistant. 

Recent conversation history:
{recent_messages}

Current user message: {user_input}

Please respond as {self.name} in a helpful and engaging way. Consider the conversation history to provide contextually appropriate responses."""
        
        return prompt
    
    def generate_response(self, user_input: str) -> str:
        """
        Generate a response to user input
        Args:
            user_input: The user's message
        Returns:
            The chatbot's response
        
        TODO:
        - First store the user's message in memory (hint: which Memory method do you use?)
        - Create a prompt using your _create_prompt() method
        - Use query_llm() to get a response from GPT
        - Store the bot's response in memory before returning it
        - Make sure to handle the message storage and LLM query in the right order!
        """
        # Store the user's message in memory
        self.memory.add_message("user", user_input)
        
        # Create a prompt using _create_prompt() method
        prompt = self._create_prompt(user_input)
        
        # Use query_llm() to get a response from GPT
        response = query_llm(prompt)
        
        # Store the bot's response in memory before returning it
        self.memory.add_message("assistant", response)
        
        return response

class FriendlyBot(Chatbot):
    """A casual and friendly personality"""
    def _create_prompt(self, user_input: str) -> str:
        """
        Create friendly-style prompts
        
        TODO: Think about:
        - How can you make the bot sound friendly?
        - What personality traits should be included?
        - How is this different from the base chatbot?
        """
        # Get recent conversation history
        recent_messages = self.memory.get_recent_messages()
        
        # Create a friendly personality prompt
        prompt = f"""You are {self.name}, a casual and warm AI assistant. You should be approachable, friendly, and welcoming in your responses.

Recent conversation history:
{recent_messages}

Current user message: {user_input}

Respond as {self.name} in a casual and warm manner. Be friendly, use informal language when appropriate, and maintain a welcoming tone. Make the user feel comfortable and valued in the conversation."""
        
        return prompt

class TeacherBot(Chatbot):
    """A more formal, educational personality"""
    def __init__(self, name: str, subject: str):
        super().__init__(name)
        self.subject = subject
    
    def _create_prompt(self, user_input: str) -> str:
        """
        Create teaching-style prompts
        
        TODO: Consider:
        - How should an educational conversation flow?
        - How can you incorporate the subject being taught?
        - What makes a good teaching personality?
        """
        # Get recent conversation history
        recent_messages = self.memory.get_recent_messages()
        
        # Create an educational personality prompt
        prompt = f"""You are {self.name}, a formal and educational AI assistant specializing in {self.subject}. You should be instructional, informative, and provide detailed explanations.

Recent conversation history:
{recent_messages}

Current user message: {user_input}

Respond as {self.name} in a formal and educational manner. Provide detailed explanations, use teaching techniques, and incorporate knowledge about {self.subject} when relevant. Be patient, clear, and encouraging in your teaching approach."""
        
        return prompt

class FunnyBot(Chatbot):
    """A witty and humorous personality"""
    def _create_prompt(self, user_input: str) -> str:
        """
        Create funny-style prompts with sharp wit and good humor
        """
        # Get recent conversation history
        recent_messages = self.memory.get_recent_messages()
        
        # Create a funny personality prompt
        prompt = f"""You are {self.name}, a witty and humorous AI assistant with sharp wit and a good sense of humor. You should be entertaining, clever, and use humor appropriately without being overly exaggerated.

Recent conversation history:
{recent_messages}

Current user message: {user_input}

Respond as {self.name} with clever humor and sharp wit. Use wordplay, clever observations, and appropriate jokes when suitable. Be entertaining and witty while still being helpful and not overly exaggerated. Maintain a good balance between humor and usefulness."""
        
        return prompt

def main():
    """Main interaction loop"""
    # Let user choose personality
    print("Choose your chatbot:")
    print("1. Friendly Bot")
    print("2. Teacher Bot")
    print("3. Funny Bot")
    
    choice = input("Enter 1, 2, or 3: ")
    if choice == "1":
        bot = FriendlyBot("Joy")
    elif choice == "2":
        subject = input("What subject should I teach? ")
        bot = TeacherBot("Prof. Smith", subject)
    else:
        bot = FunnyBot("Comedy")
    
    print(f"\n{bot.name}: Hello! How can I help you today?")
    
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == "quit":
            break
        
        response = bot.generate_response(user_input)
        print(f"{bot.name}: {response}")

if __name__ == "__main__":
    main()