from fastapi import FastAPI
from app.routes import router

app = FastAPI(title="接口测试平台")

app.include_router(router)

@app.get("/")
def root():
    return {"message": "接口测试平台已启动"}
