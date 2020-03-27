FROM python:3
MAINTAINER Nicholas Schwab "chat@nicholas-schwab.de"

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . /bot
WORKDIR /bot

RUN chmod u+x start.sh
ENTRYPOINT ["./start.sh"]