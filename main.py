import os
import io
import time
import threading
from fastapi import FastAPI, UploadFile, File, Response
from PIL import Image
from rembg import remove, new_session

os.environ["U2NET_HOME"] = "/app/models"

app = FastAPI()

session = None
model_loaded = False

def init_session():
    global session, model_loaded
    print("Loading rembg model...")
    try:
        session = new_session("u2net")
        model_loaded = True
        print("Model loaded successfully.")
    except Exception as e:
        print(f"Failed to load model: {e}")

# 在后台线程中预加载模型
threading.Thread(target=init_session, daemon=True).start()

@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": model_loaded}

@app.post("/api/remove-bg")
async def remove_bg(file: UploadFile = File(...)):
    max_retries = 30
    for i in range(max_retries):
        if session is not None:
            break
        time.sleep(1)
    if session is None:
        return Response(content=b"Model not ready", status_code=503)

    img_data = await file.read()
    input_image = Image.open(io.BytesIO(img_data))
    input_image.thumbnail((1200, 1200))
    output_image = remove(input_image, session=session)
    img_byte_arr = io.BytesIO()
    output_image.save(img_byte_arr, format='PNG')
    return Response(content=img_byte_arr.getvalue(), media_type="image/png")
