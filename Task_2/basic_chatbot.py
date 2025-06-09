import spacy
import random

# Load spaCy English model
nlp = spacy.load("en_core_web_sm")

# Define response templates
responses = {
    "greeting": [
        "Hello! Nice to see you!",
        "Hi there! How can I help you today?",
        "Hey! What's up?"
    ],
    "farewell": [
        "Goodbye! Come back soon!",
        "See you later!",
        "Take care!"
    ],
    "about_self": [
        "I'm Aurithra, a simple chatbot created to chat and help with basic questions!",
        "Just a friendly AI here to talk with you!",
        "I'm a chatbot designed to be maximally truthful and conversational."
    ],
    "how_are_you": [
        "I'm doing great, thanks for asking! How about you?",
        "All good here! What's your vibe today?",
        "I'm just chilling in the digital world. You?"
    ],
    "default": [
        "Hmm, not sure about that one. Tell me more!",
        "That's interesting! Can you say more about it?",
        "I might need a bit more context. What's on your mind?"
    ]
}

# Define intent recognition function
def detect_intent(text):
    doc = nlp(text.lower())
    
    # Check for greetings
    greeting_words = ["hello", "hi", "hey", "greetings"]
    if any(token.text in greeting_words for token in doc):
        return "greeting"
    
    # Check for farewells
    farewell_words = ["bye", "goodbye", "see you", "later"]
    if any(token.text in farewell_words for token in doc):
        return "farewell"
    
    # Check for questions about the chatbot
    about_words = ["you", "yourself", "who are you", "what are you"]
    if any(about in text.lower() for about in about_words):
        return "about_self"
    
    # Check for "how are you" type questions
    how_words = ["how are you", "how's it going", "how you doing"]
    if any(how in text.lower() for how in how_words):
        return "how_are_you"
    
    # Default case
    return "default"

# Main chatbot function
def chatbot():
    print("Welcome to My Chatbot! Type 'quit' to exit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "quit":
            print(random.choice(responses["farewell"]))
            break
        
        intent = detect_intent(user_input)
        response = random.choice(responses[intent])
        print(f"Bot: {response}")

# Run the chatbot
if __name__ == "__main__":
    chatbot()