FROM mcr.microsoft.com/windows/servercore:ltsc2019
FROM python:3.12.2

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

CMD ["python", "app.py"]