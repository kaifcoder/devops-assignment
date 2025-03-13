from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/hello/{name}")
def say_hello(name: str):
    return {"message": "Hello, " + name}


'''
    ENDPOINT: /add/{a}/{b}
    PARAMS:
        a: int
        b: int
        new: bool
    RETURNS:
        {
            "result": int
        }
    DESCRIPTION:
        Returns the sum of a and b.
        If the new key is set to True, the key will be "sum" instead of "result".
'''
@app.get("/add/{a}/{b}")
def add(a: int, b: int, new: bool = Query(False,alias="new")):
    # if user wants to use the new key, return the sum with the key "sum" instead of "result"
    if new:
        return {"sum": a + b}
    # otherwise, return the sum with the key "result" as usual
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