#!/usr/bin/env bash

echo "Environment is ${1}"

export ENVIRONMENT=${1}

echo "Setting environment variables"
export HOST=0.0.0.0
export PORT=8080
export DEBUG=True
export RELOAD=True

envsubst < .env.template > .env_${1}

export $(grep -v '^#' .env_${1} | xargs)

docker-compose -p localrunner -f docker-compose.yml down
docker-compose -p localrunner -f docker-compose.yml build
docker-compose -p localrunner -f docker-compose.yml up