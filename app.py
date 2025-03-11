from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/hello/{name}")
def say_hello(name: str):
    # Breaking change: Change the JSON structure returned by this endpoint
    return {"greeting": f"Hi, {name}!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)