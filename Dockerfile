FROM  python:3.6.5-slim-stretch

ENV PYMSSQL_BUILD_WITH_BUNDLED_FREETDS=1

COPY . /app

RUN pip install --no-cache-dir -r /app/requirements.txt

WORKDIR /app

VOLUME ["/app"]

EXPOSE 8000

CMD ["gunicorn", "--reload", "-b", "0.0.0.0:8000", "api:app"]
