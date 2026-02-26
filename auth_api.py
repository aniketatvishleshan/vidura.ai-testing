from fastapi import FastAPI

app = FastAPI()

@app.post("/login")
def login(username: str, password: str):
    return {"token": "fake-jwt-token"}