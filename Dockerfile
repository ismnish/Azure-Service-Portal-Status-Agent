# Use official Python 3.11 slim image
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all code
COPY . .


CMD ["python", "agent.py"]  # Adjust to your actual agent entrypoint
