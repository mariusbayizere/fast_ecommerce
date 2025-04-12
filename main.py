from fastapi import FastAPI
from typing import Optional


app =FastAPI()


@app.get('/')
async def read_root():
    """
    This is the root function that returns a welcome message.
    """
    return {"Message":"Hello Marius"}



@app.get('/greet/{name}')
async def greeting(name: str, age : int)-> dict:
    """
    This is a greeting function that takes a name and age as parameters.
    It returns a dictionary with the name and age.
    """
    return {"Message":f"my name is {name} I have ", "Age" : age}


@app.get('/greets')
async def greeting_name(name: Optional[str]="User", age : Optional[int]=20)-> dict:
    """"
    This is a greeting function that takes a name and age as parameters.
    It returns a dictionary with the name and age.
    """
    return {"Message":f"My name is {name}", "Age":age}