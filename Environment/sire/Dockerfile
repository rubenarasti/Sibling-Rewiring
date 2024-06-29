FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV MYSQL_ROOT_PASSWORD=root
ENV MYSQL_DATABASE=sire


EXPOSE 5000

#CMD ["python", "sire.py"]
CMD ["gunicorn", "-b", "0.0.0.0:5000", "wsgi:app"]
