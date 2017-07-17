import requests # get archive
import lxml     # find links and process xml
import re       # find links
import zipfile  # work with archive
import json     # save outputs
from bs4 import BeautifulSoup # nice html processing
import xmltodict
from orm_model import OriginFile
from datetime import date
from dateparser import parse
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

engine = create_engine('mysql+mysqldb://root:1234@localhost:3306/rsmp?charset=utf8')
Session = sessionmaker(bind=engine)

def get_archive():
    page = requests.get('https://www.nalog.ru/opendata/7707329152-rsmp/')
    c = page.text

    print(f'Server status code: {page.status_code}')
    soup = BeautifulSoup(c, 'lxml')
    d = soup(text=re.compile(r'\d{2}\.\d{2}\.\d{4}'))[2]

    session = Session()
    try:
        q = session.query(OriginFile).first()
        act_date = q.actuality_date
    except Exception as e:
        act_date = parse('01.01.1900')
    if act_date > parse(d):
        return None

    dataset_link = soup.find_all('a', text=re.compile(r'https'))[0].string
    # archive = requests.get(dataset_link).content

    archive_name = dataset_link[dataset_link.rfind('/') + 1:]
    return archive_name


def main():
    archive_name = get_archive()
    if archive_name:
        archive = zipfile.ZipFile(archive_name, 'r')
        xml_names = archive.namelist()

        for name in xml_names:
            print(f'Working on {name}.')
            with archive.open(name) as xmlf:
                d = xmltodict.parse(xmlf.read())
                with open(name[:-4] + '.json', 'w') as jsonf:
                    json.dump(d, jsonf, ensure_ascii=False)
            print(f'Saved {name} as json.')
    else:
        print('You already have latest dataset!')



if __name__ == '__main__':
    main()
