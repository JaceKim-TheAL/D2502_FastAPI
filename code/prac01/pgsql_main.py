# pgsql_main.py

from fastapi import FastAPI
from controller import items, users, admins

app = FastAPI()

app.include_router(items.router)
app.include_router(users.router)
app.include_router(admins.router)

@app.get("/")
def read_root():
    return {"Hello": "FastAPI"}

# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}

# @app.get("/users/{user_id}")
# def read_user(user_id: int, q1: Union[str, None] = None, q2: Union[str, None] = None):
#     return {"user_id": user_id, "q1": q1, "q2": q2}

@app.get("/list")
def list_admin():
    """
    List all admins from the database.
    """
    results = admins.list_admin()
    return results



