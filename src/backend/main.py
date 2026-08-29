from backend.config import settings
from fastapi import FastAPI
from backend import models
from backend.database import engine
from backend.router import applications, auth

app = FastAPI()


models.Base.metadata.create_all(bind=engine)
app.include_router(applications.router)
app.include_router(auth.router)

@app.get("/")
def hello():
    return "hello job interviewwer"


print(settings.database_url)
