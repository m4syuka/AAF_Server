FROM python:3.10-slim

WORKDIR /opt/app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python3", "main.py"]