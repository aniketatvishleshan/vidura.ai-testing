from fastapi import FastAPI, APIRouter
from pydantic import BaseModel

app = FastAPI()
router = APIRouter()

@app.get("/users")
def get_users():
    return [{"id": 1, "name": "Alice"}]

@app.post("/users")
def create_user(user: dict):
    return {"message": "User created", "user": user}

class CreatePayment(BaseModel):
    amount: int
    currency: str
    customer_id: str

@router.post("/payments")
def create_payment(req: CreatePayment):
    return {"status": "ok"}