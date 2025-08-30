FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY azure_portal_agent ./azure_portal_agent

CMD ["python", "azure_portal_agent/agent.py"]
