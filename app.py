from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

@app.get("/hey/{name}")
def say_hey(name: str):
    return {"message": "Hey, " + name}

@app.get("/hello/{name}")
def say_hello(name: str):
    return {"message": "Hello, " + name}

# break the code
@app.get("/error")
def error():
    return 1/0

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)