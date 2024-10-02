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

    # Initialize the AI model for generating content
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    
   
    prompt = f"Answer this question about coding: {question}"

    try:
       
        response = model.generate_content([prompt])
        
        # Return the generated response text
        return response.text
    
    except Exception as e:
        # Log the error or handle it as needed (optional)
        print(f"Error in processing chat request: {e}")
        
        # Return an error message in case of failure
        return "Failed to generate a response. Please try again."
