#!/usr/bin/env bash

heroku container:login
docker build . --file Dockerfile --tag registry.heroku.com/${HEROKU_APP_NAME}/web
docker push registry.heroku.com/${HEROKU_APP_NAME}/web
heroku container:release -a ${HEROKU_APP_NAME} web
