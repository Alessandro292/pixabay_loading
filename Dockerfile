FROM python:3.8

COPY ./requirements.txt /tmp/requirements.txt

RUN pip install -r /tmp/requirements.txt

WORKDIR /code

COPY ./app /code/app

EXPOSE 8000

CMD ["uvicorn", "app.src.main:app", "--host", "0.0.0.0", \
     "--port", "8000", "--log-config", "/code/app/src/config/logging.conf"]