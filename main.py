from fastapi import FastAPI

app = FastAPI()

@app.get("/init")
async def init():
    return {"msg": "initialized"}