from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

import shutil
import os

from src.deployment.app import ask, ask_image, ask_sql_query

app = FastAPI(title="Enterprise RAG API")

# ---------------------------
# FOLDERS
# ---------------------------
UPLOAD_DIR = "uploads"
DATA_DIR = "src/data/raw/data_inside/EnterpriseRAG_2025_02_markdown"

os.makedirs(UPLOAD_DIR, exist_ok=True)

# 🔥 Serve uploaded images
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

# 🔥 Serve RAG dataset images
app.mount(
    "/data",
    StaticFiles(directory="src/data/raw/data_inside"),
    name="data"
)

# ---------------------------
# CORS
# ---------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------
# Request Models
# ---------------------------
class TextRequest(BaseModel):
    question: str

class SQLRequest(BaseModel):
    question: str


# -------------------------------------------------------
# 🔥 HELPER → LOCAL IMAGE PATH → PUBLIC URL
# -------------------------------------------------------
def convert_image_path(image_path: str):
    if not image_path:
        return None

    # uploaded image case
    if image_path.startswith("uploads"):
        filename = os.path.basename(image_path)
        return f"http://127.0.0.1:8000/uploads/{filename}"

    # rag dataset image case
    if "data_inside/" in image_path:
        filename = image_path.split("data_inside/")[-1]
        return f"http://127.0.0.1:8000/data/{filename}"

    return image_path


# ---------------------------
# TEXT RAG
# ---------------------------
@app.post("/ask")
def ask_endpoint(req: TextRequest):

    result = ask(req.question)

    # 🔥 Convert image path
    if result.get("image"):
        result["image"] = convert_image_path(result["image"])

    return result


# ---------------------------
# IMAGE RAG (UPLOAD)
# ---------------------------
@app.post("/ask-image")
async def ask_image_endpoint(file: UploadFile = File(...)):

    save_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = ask_image(save_path)

    # 🔥 Convert image path
    if result.get("image"):
        result["image"] = convert_image_path(result["image"])

    return result


# ---------------------------
# SQL RAG
# ---------------------------
@app.post("/ask-sql")
def ask_sql_endpoint(req: SQLRequest):
    result = ask_sql_query(req.question)
    return result


# ---------------------------
# HEALTH CHECK
# ---------------------------
@app.get("/")
def root():
    return {"status": "RAG API Running"}
