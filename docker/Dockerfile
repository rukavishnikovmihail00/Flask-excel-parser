FROM python:3.11-slim

WORKDIR /app

COPY . /app/

EXPOSE 5000

RUN python -m pip install Flask requests openpyxl

CMD ["python", "main.py", "--host", "0.0.0.0"]