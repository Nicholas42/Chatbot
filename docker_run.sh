#!/bin/bash

#                                       vvvv bind the pip cache to the local, improves compile times.
docker run --name chatbot -p 5000:9003 -v $HOME/.cache/pip/:/root/.cache/pip --restart on-failure:3 -d chatbot:latest
