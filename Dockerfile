FROM python:3.11

WORKDIR /teamproject
COPY .env /teamproject/.env
ENV PYTHONPATH "${PYTHONPATH}:/app"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /teamproject/requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./app /teamproject/app

CMD ["python", "app/main.py"]