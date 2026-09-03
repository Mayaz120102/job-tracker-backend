from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from backend.config import settings

from backend.router import applications, auth

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(applications.router)
app.include_router(auth.router)


@app.get("/")
def hello():
    return "hello job interviewwer"
