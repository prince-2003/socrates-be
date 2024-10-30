from contextlib import asynccontextmanager
from typing import Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from apps.chat.route import router 
from constants import SERVER_URL, PORT, ENV
from fastapi import FastAPI, Request, HTTPException, Response
from firebase_admin import auth
import firebase_admin
from firebase_admin import credentials, firestore
from fastapi import Depends, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse
from firebase_admin import auth
from datetime import datetime, timedelta, timezone
from firebase_admin import auth, exceptions
from firebase_client import db

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=['https://socrates1.vercel.app','https://socrates-two.vercel.app', 'http://localhost:3000'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def verify_session_token(request: Request):
    session_cookie = request.cookies.get("session")
    if not session_cookie:
        raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        # Verify the session cookie
        decoded_token = auth.verify_session_cookie(session_cookie, check_revoked=True)
        return decoded_token
    except auth.InvalidSessionCookieError:
        raise HTTPException(status_code=401, detail="Session expired or invalid")

@app.get('/')
async def root():
    return {"message": "Server is running"}

app.include_router(router, prefix="/api", tags=["chat"])

@app.post('/sessionLogin')
async def session_login(request: Request):
    if request.cookies.get('session'):
        return JSONResponse(content={'status': 'already_logged_in'})
    
    body = await request.json()
    id_token = body.get('idToken')
    if not id_token:
        raise HTTPException(status_code=400, detail="ID token is required")

    expires_in = timedelta(hours=1)
    try:
        session_cookie = auth.create_session_cookie(id_token, expires_in=expires_in)
        response = JSONResponse(content={'status': 'success'})
        expires = datetime.now(timezone.utc) + expires_in  # Ensure expires is in UTC
        response.set_cookie(
            key='session', value=session_cookie, expires=expires, httponly=True, secure=True, samesite='None')
        return response
    except exceptions.FirebaseError:
        raise HTTPException(status_code=401, detail="Failed to create a session cookie")

@app.post('/check_session')
async def access_restricted_content(request: Request):
    session_cookie = request.cookies.get('session')
    if not session_cookie:
        # Session cookie is unavailable. Inform the frontend to handle login.
        return JSONResponse(content={'error': 'Session cookie is unavailable. Please login.'}, status_code=401)

    # Verify the session cookie. In this case an additional check is added to detect
    # if the user's Firebase session was revoked, user deleted/disabled, etc.
    try:
        decoded_claims = auth.verify_session_cookie(session_cookie, check_revoked=True)
        return serve_content_for_user(decoded_claims)
    except auth.InvalidSessionCookieError:
        # Session cookie is invalid, expired or revoked. Inform the frontend to handle login.
        return JSONResponse(content={'error': 'Invalid session cookie. Please login again.'}, status_code=401)

def serve_content_for_user(decoded_claims):
    # Implement the logic to serve content for the user based on decoded_claims
    return JSONResponse(content={'status': 'content_served', 'claims': decoded_claims})


@app.post('/sessionLogout')
async def session_logout():
    response = JSONResponse(content={'status': 'logged_out'})
    response.delete_cookie('session', samesite='None',httponly=True, secure=True)
    return response

@app.get("/fetch-data")
async def fetch_data(id: Optional[str] = None, token_data=Depends(verify_session_token)):
    doc_ref = db.collection("problems")
    
    if id:
        doc = doc_ref.document(id).get()
        if not doc.exists:
            raise HTTPException(status_code=404, detail="Document not found")
        documents = [{'id': doc.id, **doc.to_dict()}]
    else:
        docs = doc_ref.get()
        if not docs:
            raise HTTPException(status_code=404, detail="No documents found")
        documents = [{'id': doc.id, **doc.to_dict()} for doc in docs]
    
    return JSONResponse(content={'status': 'success', 'documents': documents})

@app.post("/add-data")
async def add_data(request: Request, token_data=Depends(verify_session_token)):
    doc_ref = db.collection("problems")
    body = await request.json()
    doc_ref.add(body)
    return JSONResponse(content={'status': 'success', 'message': 'Document added successfully'})




if __name__ == "__main__":
    uvicorn.run("main:app", host=SERVER_URL, port=8900, reload=(ENV == "dev"))
