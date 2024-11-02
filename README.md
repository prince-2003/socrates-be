# Socrates Backend

The backend of Socrates, an AI-powered code assistance platform, provides core API functionality for user authentication, session management, and AI-driven code assistance. Built with FastAPI and Firebase, it serves as the backbone for the Socrates frontend.

## Features

- **Session Management**: Maintains secure user sessions with Firebase authentication.
- **AI Code Assistance**: Provides real-time suggestions and debugging help through AI-powered endpoints.
- **RESTful API Integration**: Enables seamless communication with the Socrates frontend for responsive user interactions.

## Technologies Used

- **Backend Framework**: FastAPI
- **Authentication & Database**: Firebase
- **Hosting**: Render

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/prince-2003/socrates-be.git
   cd socrates-be
2. Set up a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
4. Configure environment variables for Gemini API credentials in .env and secret file for Firebase Admin.
5. Start the FastAPI server:
   ```bash
   uvicorn app:app --host 0.0.0.0 --port 8000
6. Access the API at http://localhost:8000.

## API Endpoints

- **/sessionLogin**
  - **Method**: POST
  - **Description**: Authenticates the user and establishes a session by setting an authentication cookie.
  - **Request Body**: User credentials (e.g., email, password).
  - **Response**: Returns a success message if the login is successful and the session cookie is set.

- **/check_session**
  - **Method**: GET
  - **Description**: Verifies if the user has an active session.
  - **Request**: No body required, but the session cookie is expected in the request.
  - **Response**: Returns session status, indicating whether the user is logged in.

- **/sessionLogout**
  - **Method**: POST
  - **Description**: Logs the user out by invalidating the session and clearing the session cookie.
  - **Request**: No body required, but the session cookie is expected in the request.
  - **Response**: Confirms the user has been logged out.

- **/fetch-data**
  - **Method**: GET
  - **Description**: Retrieves coding problems for the logged-in user.
  - **Request**: No body required, but the session cookie is expected in the request.
  - **Response**: Returns problem statement sets.

- **/add-data**
  - **Method**: POST
  - **Description**: Allows the user to add new data (i.e problems).
  - **Request Body**: Data payload to be stored.
  - **Response**: Returns a success message if data is added successfully.

- **/api/ask**
  - **Method**: POST
  - **Description**: Provides AI-driven assistance based on the code input, giving feedback, debugging help, or suggestions.
  - **Request Body**: Code or programming query from the user.
  - **Response**: Returns AI-generated feedback or suggestions related to the submitted code.

## Future Goals
- Enhanced Security: Implement additional security measures for improved data integrity.
- Multi-Language Support: Expand AI assistance for additional programming languages.
   
