import os
import random
import shutil

from typing import Union
import datetime
from starlette.responses import FileResponse
from fastapi import FastAPI, UploadFile, File

#Вводи в терминал
#pip install fastapi
#pip install "uvicorn[standard]"
#uvicorn API:app --reload

app = FastAPI()

if not os.path.isdir("memes"):
    os.mkdir("memes")

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/datetime/{datetype}")
def read_item(datetype: Union[str, None] = None):
    if datetype == "date":
        return {"datetime": "info", "date": datetime.date.today()}
    elif datetype == "time":
        return {"datetime": "info", "time": datetime.datetime.now().time()}
    else:
        return {"datetime": "info", "now": datetime.datetime.now()}



@app.get("/memes")
async def get_image():
    memes = os.listdir("memes")
    mem_id = random.choice(memes)
    image_path = f"memes/{mem_id}"
    return FileResponse(image_path, media_type="image/jpeg", headers={"Cache-Control": "max-age=0"})



@app.get("/memes/download")
async def dAUNLOAD():
    memes = os.listdir("memes")
    mem_id = random.choice(memes)
    image_path = f"memes/{mem_id}"
    return FileResponse(image_path, media_type="application/octet-stream")


@app.post("/memes/upload")
async def upload_meme(file: UploadFile = File(...)):
    #filename = str(uuid.uuid4()) + ".jpg"
    path = os.path.join("./memes", file.filename)
    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"filename": file.filename}

