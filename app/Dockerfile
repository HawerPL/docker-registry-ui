FROM python:3.9.19-slim

COPY . /app

RUN pip install -r /app/requirements.txt

EXPOSE 8080

WORKDIR /

ENTRYPOINT ["waitress-serve"]

CMD ["--host=0.0.0.0", "--call", "app:create_app"]