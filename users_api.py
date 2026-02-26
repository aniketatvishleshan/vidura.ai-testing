from fastapi import FastAPI

app = FastAPI()

@app.get("/users")
def get_users():
    return [{"id": 1, "name": "Alice"}]

@app.post("/users")
def create_user(user: dict):
    return {"message": "User created", "user": user}