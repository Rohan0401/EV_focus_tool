FROM python:3.8.2
ENV PYTHONUNBUFFERED 1
EXPOSE 8080
WORKDIR /src
ENV PYTHONPATH src
COPY requirements.txt entrypoint.sh ./
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY . ./
ENTRYPOINT ["./entrypoint.sh"]