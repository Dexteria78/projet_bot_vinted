FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt && playwright install --with-deps
COPY . .
CMD ["python", "bot_vinted.py"]
