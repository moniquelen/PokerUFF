from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.session_router import router as session_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(session_router)

@app.get("/")
def root():
    return {"message": "PokerUFF backend rodando"}