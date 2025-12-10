from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers.story_router import story_router
from .routers.user_router import user_router
from .routers.chat_router import chat_router

app = FastAPI() 
# Configure CORS settings
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173", 
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # Allows these specific origins
    allow_credentials=True,      # Allows cookies/auth headers
    allow_methods=["*"],         # Allows all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],         # Allows all headers
)
app.include_router(user_router)
app.include_router(story_router)
app.include_router(chat_router)