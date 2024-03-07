from fastapi import FastAPI

app: FastAPI = FastAPI()


@app.get("/hi")
def greet_with_name(name: str):
    return "Hello? World, " + name
