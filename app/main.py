from fastapi import FastAPI

from app.routes.ai import router as ai_router

app = FastAPI()

app.include_router(ai_router)


@app.get("/")
def root():

    return {
        "status": "FitCoach Backend Running"
    }