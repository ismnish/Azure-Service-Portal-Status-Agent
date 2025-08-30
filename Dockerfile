FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["adk", "web", "--host", "0.0.0.0", "--port", "8000", "azure_portal_agent"]
