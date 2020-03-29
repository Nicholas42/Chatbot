#!/bin/bash

docker run --name chatbot -p 5000:9003 --restart always -d chatbot:latest
