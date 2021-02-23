FROM python:3.8.2
ENV PYTHONUNBUFFERED 1
EXPOSE 8080
WORKDIR /src
ENV PYTHONPATH src
COPY poetry.lock pyproject.toml Makefile .env.example ./
RUN make install
COPY . ./
ENTRYPOINT ["./entrypoint.sh"]