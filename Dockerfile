FROM python:3.8

COPY ./requirements.txt /src/requirements.txt

WORKDIR /src

RUN pip install --no-cache-dir -r requirements.txt

COPY . /src

EXPOSE 8000

ENTRYPOINT ["gunicorn","run:app","-w","4", "--bind", "0.0.0.0:8000"]



