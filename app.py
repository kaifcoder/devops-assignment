from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/hello/{name}")
def say_hello(name: str):
    return {"message": "Hello, " + name}

# New endpoint introducing a breaking change
@app.get("/greet/{name}")
def greet(name: str, format: str = "new"):
    if format == "old":
        return {"message": "Hello, " + name}
    return {"greeting": f"Hi, {name}!", "status": "success"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)