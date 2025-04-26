'''
# 실습1. FastAPI Start 
step01. 
1. Import FastAPI and Union from typing
2. Create an instance of FastAPI
3. Define a root endpoint that returns a greeting message
4. Define an endpoint to read an item by its ID and an optional query parameter

step02. controller 추가
5. Create a controller directory and add items.py and users.py files
6. Define a router in each controller file with a prefix and tags
7. Import the router in main.py and include it in the FastAPI app
8. Test the endpoints using a web browser or API client
9. Verify the functionality of the endpoints
# 10. Add a new endpoint to read a user by ID and two optional query parameters
# 11. Test the new endpoint using a web browser or API client
# 12. Verify the functionality of the new endpoint
'''
# main.py

from fastapi import FastAPI
from typing import Union
from controller import items, users

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "FastAPI"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/users/{user_id}")
def read_user(user_id: int, q1: Union[str, None] = None, q2: Union[str, None] = None):
    return {"user_id": user_id, "q1": q1, "q2": q2}



