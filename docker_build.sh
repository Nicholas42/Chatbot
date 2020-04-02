#!/bin/bash

DOCKER_BUILDKIT=1 docker build -t chatbot:latest .
docker-compose build
