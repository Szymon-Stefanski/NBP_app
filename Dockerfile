FROM python:3.12

WORKDIR /app

COPY . .

RUN pip install flask flask_sqlalchemy plotly pandas requests --no-cache-dir

EXPOSE 5000

CMD ["python", "main.py"]
