FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y libgl1 libglib2.0-0 && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir fastapi uvicorn rembg pillow onnxruntime

RUN python -c "import os; os.environ['U2NET_HOME'] = '/app/models'; from rembg import new_session; new_session('u2net')"

COPY main.py .

EXPOSE 8080

ENV PORT=8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
