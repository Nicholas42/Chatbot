from chatbot.database.db import database
from chatbot.database.nickname import QEDler
from ..qeddb import login, lookup_persons


def parse_html(soup):
    ret = dict()
    for row in soup.find_all('tr', class_='data'):
        d = dict()
        plink = row.find('td', class_="personenlink").find('div').find('a').get('href')

        user_id = int(plink.split('person=')[1].split('&')[0])
        d["user_id"] = user_id
        d["surname"] = str(row.find('td', class_="personennachname").find('div').string).strip()
        d["forename"] = str(row.find('td', class_="personenvorname").find('div').string).strip()
        ret[user_id] = d

    return ret


def add_to_db(values):
    with database.context as session:
        existing = set(i[0] for i in session.query(QEDler.user_id).all())
        new = set(values).difference(existing)
        session.bulk_insert_mappings(QEDler, [values[i] for i in new])


def updatepersons():
    session = login()
    soup = lookup_persons(**session)
    qedler = parse_html(soup)
    add_to_db(qedler)


def count_qedler():
    with database.context as session:
        return session.query(QEDler).count()


def run():
    old_count = count_qedler()
    updatepersons()
    new_count = count_qedler()

    return {"old_count": old_count, "new_count": new_count}
