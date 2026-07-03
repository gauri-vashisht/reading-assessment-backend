from fastapi import FastAPI

app = FastAPI(title="Reading Assessment API", version="1.0.0")


@app.get("/")
def home():
    return {"message": "Backend is running successfully!"}
