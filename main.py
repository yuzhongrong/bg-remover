import os
import io
from fastapi import FastAPI, UploadFile, File, Response
from PIL import Image
from rembg import remove, new_session

os.environ["U2NET_HOME"] = "/app/models"

app = FastAPI()

session = new_session("u2net")

@app.post("/api/remove-bg")
async def remove_bg(file: UploadFile = File(...)):
    img_data = await file.read()
    input_image = Image.open(io.BytesIO(img_data))
    input_image.thumbnail((1200, 1200))
    output_image = remove(input_image, session=session)
    img_byte_arr = io.BytesIO()
    output_image.save(img_byte_arr, format='PNG')
    return Response(content=img_byte_arr.getvalue(), media_type="image/png")
