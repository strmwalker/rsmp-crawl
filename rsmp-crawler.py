import requests # get archive
import lxml     # find links and process xml
import re       # find links
import zipfile  # work with archive
import json     # save outputs
from bs4 import BeautifulSoup # nice html processing
import xmltodict
from orm_model import DocumentLE, DocumentIP, License, Product, PartnerProgram
from orm_model import Contract, Agreement, LegalEntity, Individual, OriginFile
from orm_model import Sender, OkvedCode, AdressReq, AdressOpt


def get_archive():
    page = requests.get('https://www.nalog.ru/opendata/7707329152-rsmp/')
    c = page.text

    print(f'Server status code: {page.status_code}')
    soup = BeautifulSoup(c, 'lxml')
    dataset_link = soup.find_all('a', text=re.compile(r'https'))[0].string
    # archive = requests.get(dataset_link).content

    archive_name = dataset_link[dataset_link.rfind('/') + 1:]
    return archive_name


def main():
    archive_name = get_archive()
    archive = zipfile.ZipFile(archive_name, 'r')
    xml_names = archive.namelist()

    for name in xml_names[:3]:
        print(f'Working on {name}.')
        with archive.open(name) as xmlf:
            d = xmltodict.parse(xmlf.read())
            with open(name[:-4] + '.json', 'w') as jsonf:
                json.dump(d, jsonf, ensure_ascii=False)
        print(f'Saved {name} as json.')


def xml_to_orm():
    pass


if __name__ == '__main__':
    main()
