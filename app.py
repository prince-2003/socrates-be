import os
import google.generativeai as genai
import streamlit as st
from langchain.prompts import ChatPromptTemplate
from langchain.memory import ConversationBufferMemory
from constants import GEMINI_API_KEY

# Set the API key directly in the notebook

genai.configure(api_key= GEMINI_API_KEY)

# Create the model
model = genai.GenerativeModel("gemini-1.5-flash")

# Set up a chat prompt template with the "Two Sum" question integrated
prompt_template = ChatPromptTemplate.from_template(
    """
    You are a coding assistant. Provide hints and suggestions to help solve coding problems.
    For example, if the user asks about the "Two Sum" problem, provide insights or hints about it.

    User: {user_input}
    Assistant:
    """
)

# Initialize memory to keep track of the conversation
memory = ConversationBufferMemory()

# Define the Streamlit app
def main():
    st.title("Coding Assistant Chatbot")
    st.write("You can ask about coding problems like 'Two Sum'. Type your question below:")

    # User input
    user_input = st.text_input("You:", "")

    if st.button("Submit"):
        if user_input:
            # Save user input to memory
            memory.save_context({"input": user_input}, {"output": ""})

            # Generate the prompt using the user's input and memory context
            context = memory.load_memory_variables({})  # Load conversation history
            chat_prompt = prompt_template.format(user_input=user_input) + "\n" + context.get("history", "")

            # Generate a response using the model
            response = model.generate_content(chat_prompt)

            # Extract the assistant's response from the candidates
            if response.candidates:
                assistant_output = response.candidates[0].content.parts[0].text
            else:
                assistant_output = "No response generated."

            # Save the assistant's response to memory
            memory.save_context({"input": user_input}, {"output": assistant_output})

            # Print the assistant's response
            st.write(f"Assistant: {assistant_output}")

if __name__ == "__main__":
    main()
