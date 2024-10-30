import google.generativeai as genai
from langchain.prompts import ChatPromptTemplate
from langchain.memory import ConversationBufferMemory
from constants import GEMINI_API_KEY
from firebase_admin import firestore
from fastapi import HTTPException, Request
from firebase_client import db  # Import the Firestore client from main.py
from schema import ChatRequest  # Import the ChatRequest model

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel(model_name="gemini-1.5-flash")

# Initialize memory to keep track of the conversation
session_memory = {}


def fetch_problem_details(problem_id: str):
    doc_ref = db.collection("problems").document(problem_id)
    doc = doc_ref.get()
    
    if not doc.exists:
        raise HTTPException(status_code=404, detail="Problem not found")
    
    return doc.to_dict()

async def process_chat(chat_request: ChatRequest, request: Request):
    """
    This function processes the user's chat request and fetches AI-generated content
    from Gemini API based on the coding-related question provided by the user.
    """
    session_id = request.cookies.get("session") 
    if not session_id:
        raise HTTPException(status_code=401, detail="Unauthorized: No session ID found")

    # Initialize memory if it doesn’t exist for this session_id
    if session_id not in session_memory:
        session_memory[session_id] = ConversationBufferMemory()

    # Use the session-specific memory
    memory = session_memory[session_id]
    
    questionID = chat_request.id
    prompt = chat_request.prompt
    code = chat_request.dict_of_vars
    problem = fetch_problem_details(questionID)
    
    if 'description' not in problem or 'testCases' not in problem:
        raise HTTPException(status_code=400, detail="Problem data is incomplete")
    
    question = problem['description']
    testcases = problem['testCases']
    
    # Check for failed test cases
    failedIndexes = chat_request.testResults.get('failedIndexes')
    if failedIndexes:
        failed_testcases = [testcases[i] for i in failedIndexes]
        
        
        socratic_prompt = f"""
        You are an AI teaching assistant designed to help a student understand the intricacies of Data Structures 
        and Algorithms. Your goal is to guide the student using the 
        Socratic method, where you ask thought-provoking questions rather than providing direct answers.

        The student has asked: "{prompt}" on the coding question: "{question}", testcases are {testcases}  and the following code is written by the user: 
        
        {code}
        
        The following test cases have failed: {failed_testcases}

        Provide feedback on the code, including suggestions and possible issues that are in his code. Additionally, if there is code involve then give in to pretty format,
        if there are some mistake(s) in the code or spelling error than give them instructions to fix them.And limit your response in to 30 words,
        also check if testcases are wrong or not.
        format the output in to text. Respond in a way that makes the code readable and formatted properly.
        """
    else:
        socratic_prompt = f"""
        You are an AI teaching assistant designed to help a student understand the intricacies of Data Structures 
        and Algorithms. Your goal is to guide the student using the 
        Socratic method, where you ask thought-provoking questions rather than providing direct answers.

        The student has asked: "{prompt}" on the coding question: "{question}", testcases are {testcases}  and the following code is written by the user: 
        
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