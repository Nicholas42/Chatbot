FROM python:3
MAINTAINER Nicholas Schwab "chat@nicholas-schwab.de"
EXPOSE 5001

RUN apt-get update -y && apt-get upgrade -y && apt-get install netcat rlwrap -y

COPY . /bot
WORKDIR /bot

RUN pip install -e .

RUN chmod u+x start.sh
ENTRYPOINT ["./start.sh"]