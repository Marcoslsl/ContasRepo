FROM python:3.11

WORKDIR /app

COPY requirements.txt .

# for mysql 
RUN pip install cryptography

RUN pip install -r requirements.txt

COPY . /app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]

