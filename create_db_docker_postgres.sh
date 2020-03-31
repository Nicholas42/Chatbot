#!/usr/bin/env bash

# Load Variables from .env. Needs:
# POSTGRES_USER (=chatbot)
# POSTGRES_DB (=chatbot)
# POSTGRES_PASSWORD

DATA_DIR=~/.postgres/chatbot

mkdir -p "$DATA_DIR"
docker run --name postgres_chatbot -v $DATA_DIR:/var/lib/postgresql/data -p 5432:5432 -d --env-file .env postgres
