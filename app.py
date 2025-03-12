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

@app.get("/multiply/{a}/{b}")
def multiply(a: int, b: int):
    if type(a) is not int or type(b) is not int:
        return {"error": "Both a and b must be integers."}
    return {"result": a * b}

@app.get("/divide/{a}/{b}")
def divide(a: int, b: int):
    return {"result": a / b}

@app.get("/subtract/{a}/{b}")
def subtract(a: int, b: int):
    return {"result": a - b}

@app.get("/power/{a}/{b}")
def power(a: int, b: int):
    return {"result": a ** b}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)