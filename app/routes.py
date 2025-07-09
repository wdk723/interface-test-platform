from fastapi import APIRouter, UploadFile, File, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
import os
import shutil
from app.runner import run_test_from_json
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import Request

router = APIRouter()  # 定义路由对象

# 上传 JSON 用例接口
@router.post("/upload_case/")
async def upload_case(request: Request, file: UploadFile = File(...)):

    if not file.filename.endswith(".json"):
        raise HTTPException(status_code=400, detail="只支持上传 .json 文件")

    os.makedirs("testcases", exist_ok=True)
    save_path = os.path.join("testcases", file.filename)

    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 执行测试用例
    run_test_from_json(save_path)

    # 如果请求来自浏览器，重新定向到报告页面
    if "text/html" in request.headers.get("accept", ""):
        return RedirectResponse(url="/report", status_code=303)
    return {
        "message": f"文件 {file.filename} 上传成功，测试已执行",
        "report": "/report"
    }

# 获取 HTML 报告接口
@router.get("/report", response_class=HTMLResponse)
async def get_report():
    report_path = "reports/report.html"
    if not os.path.exists(report_path):
        raise HTTPException(status_code=404, detail="报告尚未生成")
    with open(report_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)


templates = Jinja2Templates(directory="templates")

@router.get("/upload", response_class=HTMLResponse)
async def upload_form(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})