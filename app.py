from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/hello/{name}")
def say_hello(name: str):
    return {"message": "Hello, " + name}

@app.get("/add/{a}/{b}")
def add(a: int, b: int):
    return {"result": a + b}

@app.get("/divide/{a}/{b}")
def divide(a: int, b: int):
    result = a / b if b != 0 else "division by zero"
    return {"result": result}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)