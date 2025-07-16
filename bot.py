from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello, FastAPI is working!"}

@app.post("/process")
async def process_data(request: Request):
    data = await request.json()
    # Здесь можешь добавить обработку данных
    return JSONResponse(content={"received": data})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("bot:app", host="0.0.0.0", port=8000)
