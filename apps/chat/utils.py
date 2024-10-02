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
    # Extract the prompt from the request model
    # Prepare a Socratic teaching prompt
    socratic_prompt = f"""
    You are an AI teaching assistant designed to help a student understand the intricacies of Data Structures 
    and Algorithms, particularly focusing on Sorting Algorithms. Your goal is to guide the student using the 
    Socratic method, where you ask thought-provoking questions rather than providing direct answers.

    The student has asked: "{prompt}" on the question: "{question}" and the following code is written by user: "{code}"

    Based on this, guide the student by asking questions like:

    1. What differences do you notice between the test case that passed and the one that failed?
    2. Why do you think the size of the input might cause the algorithm to behave differently?
    3. How does the time complexity of the sorting algorithm you implemented scale with input size?
    4. Can you think of any optimizations or a different algorithm that might handle larger inputs more efficiently?
    5. How does the time complexity of the algorithm you implemented scale with input size?
    6. How does the space complexity of the algorithm you implemented scale with input size?
    7. Have you checked if there is any spelling or declaration error in the code?
    8. Give answer to basic question like if there is any spelling error or if time complexity or space complexity is asked.

    Ensure that your responses are specific to data structures and algorithms.
    Tailor your guidance to help the student reason through performance, stability, and trade-offs of these algorithms.
    Give your responses within the context of the data structures and algorithms.
    Give your responses within 100 words or less.
    """
    print(question)
    print(prompt)
    print(code)
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

        # Return the generated response text
        return assistant_output

    except Exception as e:
        # Log the error or handle it as needed (optional)
        print(f"Error in processing chat request: {e}")
        
        
        return "Failed to generate a response. Please try again."
