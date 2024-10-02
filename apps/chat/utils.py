import google.generativeai as genai
from langchain.prompts import ChatPromptTemplate
from langchain.memory import ConversationBufferMemory
from constants import GEMINI_API_KEY


genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel(model_name="gemini-1.5-flash")

# Initialize memory to keep track of the conversation
memory = ConversationBufferMemory()

async def process_chat(chat_request):
    """
    This function processes the user's chat request and fetches AI-generated content
    from Gemini API based on the coding-related question provided by the user.
    """
    question = chat_request.question  # Extract the question from the request model
    prompt = chat_request.prompt
    code = chat_request.dict_of_vars

    
    socratic_prompt = f"""
    You are an AI teaching assistant designed to help a student understand the intricacies of Data Structures 
    and Algorithms. Your goal is to guide the student using the 
    Socratic method, where you ask thought-provoking questions rather than providing direct answers.

    The student has asked: "{prompt}" on the question: "{question}" and the following code is written by the user: 
    
    {code}
    

    Provide feedback on the code, including suggestions and possible issues that are in his code. Additionally, if there is code involve then give in to pretty format,
    if there are some mistake(s) in the code or spelling error than give them instructions to fix them.And limit your response in to 30 words.
    format the output in to text. Respond in a way that makes the code readable and formatted properly.
"""

    try:
        # Save user input to memory
        memory.save_context({"input": prompt}, {"output": ""})

        # Load memory (previous conversation context)
        context = memory.load_memory_variables({})
        chat_prompt = socratic_prompt + "\n" + context.get("history", "")

        # Generate a response using the model
        response = model.generate_content(chat_prompt)

        # Extract the assistant's response from the candidates
        if response.candidates:
            assistant_output = response.candidates[0].content.parts[0].text
        else:
            assistant_output = "No response generated."

        # Save the assistant's response to memory
        memory.save_context({"input": question}, {"output": assistant_output})

        # Return the generated response text with markdown-style formatting for code
        return assistant_output

    except Exception as e:
        # Log the error or handle it as needed (optional)
        print(f"Error in processing chat request: {e}")
        return "Failed to generate a response. Please try again."
