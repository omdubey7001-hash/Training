# 1. Base image
FROM python:3.12-slim

# 2. Set working directory
WORKDIR /app

# 3. Copy dependency file
COPY requirements.txt .

# 4. Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy project code
COPY . .

# 6. Expose API port
EXPOSE 8000

# 7. Run FastAPI app
CMD ["uvicorn", "src.deployment.api:app", "--host", "0.0.0.0", "--port", "8000"]