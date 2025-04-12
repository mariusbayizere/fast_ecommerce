from fastapi import FastAPI

app =FastAPI()


@app.get('/')
async def read_root():
    return {"Message":"Hello Marius"}



@app.get('/greet/{name}')
async def greeting(name: str, age : int)-> dict:
    return {"Message":f"my name is {name} I have ", "Age" : age}