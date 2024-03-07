from fastapi import FastAPI

app: FastAPI = FastAPI()


@app.get("/")
def index() -> dict:
    return {"message": "Hello World"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("hello:app", reload=True)
