from bs4 import BeautifulSoup
from requests import Session

from chatbot import glob

URL = "https://qeddb.qed-verein.de/"


def login():
    data = {"anmelden": "anmelden", "username": glob.config["qeddb"]["username"],
            "password": glob.config["qeddb"]["password"]}
    session = Session()
    res = session.post(f"{URL}index.php", data=data)
    sid = res.url.partition("=")[2]
    if not sid:
        raise RuntimeError("Could not login to qeddb.")

    return dict(session=session, sid=sid)


def lookup_persons(session, sid):
    res = session.get(f"{URL}personen.php", params={"session_id2": sid})
    return BeautifulSoup(res.text)
