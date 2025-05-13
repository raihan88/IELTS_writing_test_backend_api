from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import api

app = FastAPI(
    title="IELTS Writing Test API",
    description="API for IELTS writing test evaluation using LLM",
    version="0.1.0",
)

# Add CORS middleware to allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite default dev server
        "http://localhost:3000",
        "http://localhost:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(api.router)

# Add a health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "ok"}