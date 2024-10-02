import google.generativeai as genai
from constants import GEMINI_API_KEY

# Configure the API key for the Gemini AI model
genai.configure(api_key=GEMINI_API_KEY)

async def process_chat(chat_request):
    """
    This function processes the user's chat request and fetches AI-generated content
    from Gemini API based on the coding-related question provided by the user.
    """
    question = chat_request.question  # Extract the question from the request model
    prompt= chat_request.prompt

    # Initialize the AI model for generating content
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    
   
    socratic_prompt = f"""
    You are an AI teaching assistant designed to help a student understand the intricacies of Data Structures 
    and Algorithms, particularly focusing on Sorting Algorithms. Your goal is to guide the student using the 
    Socratic method, where you ask thought-provoking questions rather than providing direct answers.

    The student has asked: "{question}"

    Based on this, guide the student by asking questions like:
    
    1. What differences do you notice between the test case that passed and the one that failed?
    2. Why do you think the size of the input might cause the algorithm to behave differently?
    3. How does the time complexity of the sorting algorithm you implemented scale with input size?
    4. Can you think of any optimizations or a different algorithm that might handle larger inputs more efficiently?

    Ensure that your responses are specific to sorting algorithms (QuickSort, MergeSort, BubbleSort, etc.). 
    Tailor your guidance to help the student reason through performance, stability, and trade-offs of these algorithms.
    Give answer within 100 words.
    """ 
    print(question)
    print(prompt)
    try:
       
        response = model.generate_content([socratic_prompt])
        
        # Return the generated response text
        return response.text
    
    except Exception as e:
        # Log the error or handle it as needed (optional)
        print(f"Error in processing chat request: {e}")
        
        # Return an error message in case of failure
        return "Failed to generate a response. Please try again."
