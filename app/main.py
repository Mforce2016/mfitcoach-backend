from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware

from app.routes.ai import router as ai_router
from app.routes.chat import router as chat_router

# 🔹 Rate limit
limiter = Limiter(
    key_func=get_remote_address
)

# 🔹 App
app = FastAPI(
    title="FitCoach Backend",
    version="1.0.0"
)

# 🔹 Limiter
app.state.limiter = limiter

# 🔹 Middleware rate limit
app.add_middleware(
    SlowAPIMiddleware
)

# 🔹 CORS
app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "*"
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)

# 🔹 Routes
app.include_router(
    ai_router,
    prefix="/api/ai",
    tags=["AI"]
)

app.include_router(
    chat_router,
    prefix="/api/chat",
    tags=["Chat AI"]
)

# 🔹 Root
@app.get("/")
def root():

    return {
        "status": "FitCoach Backend Running"
    }