from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from apps.chat.route import router 
from constants import SERVER_URL, PORT, ENV
from fastapi import FastAPI, Request, HTTPException, Response
from firebase_admin import auth
import firebase_admin
from firebase_admin import credentials
from fastapi import Depends, HTTPException
from firebase_admin import auth

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(lifespan=lifespan)
if not firebase_admin._apps:
    cred = credentials.Certificate('./socratic.json')  # Correct path to your service account key
    firebase_admin.initialize_app(cred)


app.add_middleware(
    CORSMiddleware,
    allow_origins=['https://socrates-two.vercel.app' , 'http://localhost:3000'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
async def check_session(request: Request):
    session_cookie = request.cookies.get("session")
    if session_cookie:
        try:
            
            decoded_claims = auth.verify_session_cookie(session_cookie)
            return decoded_claims 
        except auth.InvalidSessionCookieError:
           
            raise HTTPException(status_code=401, detail="Invalid session cookie")
    else:
        
        return None 

@app.get('/')
async def root():
    return {"message": "Server is running"}

app.include_router(router, prefix="/api", tags=["chat"])

@app.post("/session_login")
async def session_login(request: Request, user_claims: dict = Depends(check_session)):
    
    if user_claims:
        return {"message": "User already logged in", "user": user_claims}
    data = await request.json()
    id_token = data.get("idToken")
    if not id_token:
        raise HTTPException(status_code=400, detail="ID token is required")

    try:
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token["uid"]

        
        expires_in = 60 * 60 * 24 * 14  
        session_cookie = auth.create_session_cookie(id_token, expires_in=expires_in)

        response = Response("Session created")
        response.set_cookie(
            key="session",
            value=session_cookie,
            httponly=True,
            max_age=expires_in,
            secure=True, 
            samesite="Strict",
        )
        return response

    except auth.InvalidIdTokenError:
        raise HTTPException(status_code=401, detail="Invalid ID token")


@app.post("/session_logout")
async def session_logout(response: Response):
    response.delete_cookie("session")
    return {"message": "Session cleared"}

if __name__ == "__main__":
    uvicorn.run("main:app", host=SERVER_URL, port=int(PORT), reload=(ENV == "dev"))