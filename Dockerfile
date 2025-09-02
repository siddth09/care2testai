# Use Python 3.11 slim image
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies (needed for PyTorch + HuggingFace)
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy source code
COPY . .

EXPOSE 8000

# Start FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
