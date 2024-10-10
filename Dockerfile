FROM python:3.10-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt 

RUN pip install -r requirements.txt

RUN apt-get update && apt-get install -y libgl1-mesa-glx libglib2.0-0

COPY . .

CMD ["python", "main.py"]
