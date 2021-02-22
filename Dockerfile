FROM python:3.8.2

ENV PYTHONUNBUFFERED 1

EXPOSE 8080
WORKDIR /app

ENV PYTHONPATH app

COPY poetry.lock pyproject.toml Makefile .env.example ./

#RUN pip install --upgrade pip && \
#    pip install poetry && \
#    poetry config virtualenvs.create false && \
#    poetry install --no-dev

RUN make install

COPY . ./

ENTRYPOINT ["./entrypoint.sh"]