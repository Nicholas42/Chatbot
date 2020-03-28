#!/usr/bin/env bash

# Load Variables from .env. Needs:
# POSTGRES_USER (=chatbot)
# POSTGRES_DB (=chatbot)
# POSTGRES_PASSWORD

DATA_DIR = ~/.postgres/chatbot

mkdir -p "$DATA_DIR"
docker run --name postgres_chatbot "$DATA_DIR":/var/lib/postgresql/data -d --env-file .env postgres
