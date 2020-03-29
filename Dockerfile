FROM python:3
MAINTAINER Nicholas Schwab "chat@nicholas-schwab.de"
EXPOSE 5000

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . /bot
WORKDIR /bot

RUN pip install -e .

RUN chmod u+x start.sh
ENTRYPOINT ["./start.sh"]