'''
# 실습1. FastAPI Start 
1. Import FastAPI and Union from typing
2. Create an instance of FastAPI
3. Define a root endpoint that returns a greeting message
4. Define an endpoint to read an item by its ID and an optional query parameter
'''
from fastapi import FastAPI
from typing import Union

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "FastAPI"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


