from fastapi import FastAPI

app = FastAPI()

@app.get("/orders")
def list_orders():
    return [{"id": 101, "item": "Book"}]

@app.delete("/orders/{order_id}")
def delete_order(order_id: int):
    return {"message": f"Order {order_id} deleted"}
