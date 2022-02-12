FROM python:3.8

WORKDIR /app

RUN apt-get update && apt-get install -y portaudio19-dev && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY *.py ./
COPY static static


ENV PYTHONPATH .

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]