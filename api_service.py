from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from deep_core.link_guard import is_valid_web_link
from deep_core.task_flow import handle_video_request

app = FastAPI(title="Deep_bot Download Service")


class VideoRequest(BaseModel):
    url: str


@app.get("/ping")
async def ping():
    return {"status": "Deep_bot API is online"}


@app.post("/fetch")
async def fetch_video(request: VideoRequest):
    if not is_valid_web_link(request.url):
        raise HTTPException(status_code=400, detail="Invalid link.")

    try:
        result = await handle_video_request(request.url)
        return result

    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error)) from error