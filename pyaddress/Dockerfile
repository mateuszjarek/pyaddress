FROM python:3.9

WORKDIR /pyaddress

COPY ./requirements.txt /code/requirements.txt
COPY ./requirements-dev.txt /code/requirements-dev.txt

RUN pip install --no-cache-dir --upgrade -r /pyaddress/requirements-dev.txt

COPY ./app /pyaddress/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080", "--log-config","app/logging.conf", "--no-server-header"]
