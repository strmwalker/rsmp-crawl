from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from orm_model import *

from zipfile import ZipFile
from lxml import etree

from datetime import date
from dateparser import parse

engine = create_engine('mysql+mysqldb://root:1234@localhost:3306/rsmp?charset=utf8')
Session = sessionmaker(bind=engine)
session = Session() # this shoudl be class instance

sender_dict = dict(position='ДолжОтв',
                   phone_number='Тлф',
                   email='E-mail')

file_dict = dict(file_id='ИдФайл',
              format_version='ВерсФорм',
              info_type='ТипИнф',
              prog_version='ВерсПрог',
              doc_count='КолДок')

ind_ent_dict = dict(first_name='Имя',
                    last_name='Фамилия',
                    middle_name='Отчество',
                    inn='ИННФЛ')

leg_ent_dict = dict(org_name_full='НаимОрг',
                    org_name_short='НаимОргСокр',
                    inn='ИННЮЛ')

doc_ind_dict = {'region': "Регион",
         'district': "Район",
         'city': "Город",
         'locality': "НаселПункт",
         'region_code': "КодРегион",
         'okved_primary': "СвОКВЭДОсн"}

adress_dict = {'adress_type': 'Тип',
               'adress_name': 'Наим'}

okved_dict = {'code': "КодОКВЭД",
              'name': "НаимОКВЭД",
               'version': "ВерсОКВЭД"}

license_dict = {'series': 'СерЛиценз',
    'number': "НомЛиценз",
    'type_': "ВидЛиценз",
    'date': "ДатаЛиценз",
    'start_date': "ДатаНачЛиценз",
    'end_date': "ДатаКонЛиценз",
    'license_provider': "ОргВыдЛиценз",
    'license_stopper': "ОргОстЛиценз",
    'stop_date': "ДатаОстЛиценз"}


product_dict = {'code': 'КодПрод',
    'name': 'НаимПрод',
    'innovative_flag': 'ПрОтнПрод'}

contract_dict = {'lcustomer_inn': 'ИННЮЛ_ЗК',
    'customer_name': 'НаимЮЛ_ЗК',
    'subject': 'ПредметКонтр',
    'registry_number': 'НомКонтрРеестр',
    'date': 'ДатаКонтр'}

agreement_dict = {'lcustomer_inn': 'ИННЮЛ_ЗК',
    'customer_name': 'НаимЮЛ_ЗК',
    'subject': 'ПредмДог',
    'registry_number': 'НомДогРеестр',
    'date': 'ДатаДог'}

prog_dict = {'customer_name': 'НаимЮЛ_ПП',
    'leg_ent_inn': 'ИННЮЛ_ПП',
    'agreement_number': 'НомДог',
    'agreement_date': 'ДатаДог'}

def load_sender(root):
    s = {}
    for k,v in sender_dict.items():
        s[k] = root.attrib.get(v)

    name = root.find('ФИООтв')
    s['first_name'] = name.attrib.get('Имя')
    s['last_name'] = name.attrib.get('Фамилия')
    s['middle_name'] = name.attrib.get('Отчество')
    
    q = session.query(Sender).filter_by(**s)
    if len(q.all()) == 0:
        sender = Sender(**s)
        session.add(sender)
        session.flush()
        i = sender.id
        session.commit()
    else:
        i = q.one().id

    return i


def load_ind_ent(root):
    full_name = root.find('ФИОИП')
    rev_dict = {'Фамилия': 'last_name',\
        'Имя': 'first_name',\
        'Отчество': 'middle_name'}

    ip = {}

    for k,v in rev_dict.items():
        ip[v] = full_name.attrib.get(k)

    ip['inn'] = root.get('ИННФЛ')

    q = session.query(Individual).filter_by(**ip)
    if len(q.all()) == 0:
        indiv = Individual(**ip)
        session.add(indiv)
        session.flush()
        i = indiv.id
        session.commit()
    else:
        i = q.one().id

    return i


def load_leg_ent(root):
    le = {}
    for k,v in leg_ent_dict.items():
        le[k] = root.attrib.get(v)

    q = session.query(LegalEntity).filter_by(**le)
    if len(q.all()) == 0:
        leg_ent = LegalEntity(**le)
        session.add(leg_ent)
        session.flush()
        i = leg_ent.id
        session.commit()
    else:
        i = q.one().id

    return i


def load_adress_req(root):
    
    addr = {}

    for k,v in adress_dict.items():
        addr[k] = root.attrib.get(v)

    a = AdressReq(**addr)
    q = session.query(AdressReq).filter_by(**addr)
    if len(q.all()) == 1:
        i = q.one().id
    else:
        session.add(a)
        session.flush()
        i = a.id
        session.commit()

    return i


def load_adress_opt(root):
    
    addr = {}

    for k,v in adress_dict.items():
        addr[k] = root.attrib.get(v)

    a = AdressOpt(**addr)
    q = session.query(AdressOpt).filter_by(**addr)
    if len(q.all()) == 1:
        i = q.one().id
    else:
        session.add(a)
        session.flush()
        i = a.id
        session.commit()

    return i


def loc_idx(root):
    region = root.find('Регион')
    region_id = load_adress_req(region)

    if root.find('Район'):
        district = load_adress_req(root.find('Район'))
    else: 
        district = None
    if root.find('Город'):
        city = load_adress_req(root.find('Город'))
    else:
        city = None
    if root.find('НаселПункт'):
        locality = load_adress_opt(root.find('НаселПункт'))
    else:
        locality = None

    return region_id, district, city, locality


def load_okved(root):
    c = {}

    for k,v in okved_dict.items():
        c[k] = root.attrib.get(v)

    code = OkvedCode(**c)
    q = session.query(OkvedCode).filter_by(**c)
    if len(q.all()) == 1:
        i = q.one().id
    else:
        session.add(code)
        session.flush()
        i = code.id
        session.commit()

    return i


def save_okved(root):
    codes = root.find('СвОКВЭД').getchildren()

    primary_i = [load_okved(codes[0])]
    secondary_i = []
    if len(codes) > 1:
        for code in codes[1:]:
            secondary_i.append(load_okved(code))

    return primary_i + secondary_i


def connect_license_names(root, license_id):
    names = root.findall('НаимЛицВД')
    for name in names:
        l = {'name': name.text,
            'part': names.index(name) + 1,
            'license_id': license_id}
        session.add(LicenseName(**l))
    session.commit()


def connect_license_adress(root, license_id):
    adresses = root.findall('СведАдрЛицВД')
    for adress in adresses:
        l = {'name': adress.text,
            'part': adresses.index(adress),
            'license_id': license_id}
        session.add(LicenseName(**l))
    session.commit()


def save_license(root):
    license_list = root.findall('СвЛиценз')
    l_list = []
    for ch in license_list:
        l = {}
        for k,v in license_dict.items():
            l[k] = ch.attrib.get(v)
        l['date'] = parse(ch.attrib.get('ДатаЛиценз', "31.12.5999")).date()
        l['start_date'] = parse(ch.attrib.get('ДатаНачЛиценз', "01.01.1900")).date()
        l['end_date'] = parse(ch.attrib.get('ДатаКонЛиценз', "01.01.1900")).date()
        l['stop_date'] = parse(ch.attrib.get('ДатаОстЛиценз', "01.01.1900")).date()
        license = License(**l)
        session.add(license)
        session.flush()
        l_id = license.id
        session.commit()
        connect_license_names(ch, l_id)
        connect_license_adress(ch, l_id)
        l_list.append(l_id)
    return l_list 


def save_products(root):
    prod_list = root.findall('СвПрод')
    for prod in prod_list:
        p = {}
        for k,v in product_dict.items():
            p[k] = prod.attrib.get(v)
        product = Product(**p)
        session.add(product)
        session.flush()
        p_list.append(product.id)
    session.close()
    return p_list


def save_programs(root):
    prog_list = root.findall('СвПрогПарт')
    p_list = []
    for p in prog_list:
        p_args = {}
        for k,v in prog_dict.items():
            p_args[k] = p.attrib.get(v)

        p['agreement_date'] = parse(p.attrib.get('ДатаДог', "01.01.1900")).date()
        program = PartnerProgram(**p_args)
        session.add(program)
        session.flush()
        p_list.append(program.id)

    return p_list


def save_contracts(root):
    c_list = root.findall('СвКонтр')
    contract_list
    for c in c_list:
        c_args = {}
        for k,v in contract_dict.items():
            c_args[k] = c.attrib.get(v)
        c_args['date'] = parse(c.attrib.get('ДатаКонтр', "01.01.1900")).date()
        contract = Contract(**c_args)
        session.add(contract)
        session.flush()
        contract_list.append(contract.id)

    return contract_list


def save_agreements(root):
    agr_list = root.findall('СвДог')
    a_list = []

    for a in agr_list:
        a_args = {}
        for k, v in agreement_dict.items():
            a_args[k] = a.attrib.get(v)
        a['date'] = parse(a.attrib.get('ДатаДог', "01.01.1900")).date()
        agreement = Agreement(**a_args)
        session.add(agreement)
        session.flush()
        a_list.append(agreement.id)
    return a_list


def save_doc(root):
    doc = {}
    origin_file = (session.query(OriginFile).
            filter_by(file_id = root.getparent().get('ИдФайл')).
            one())
    doc.update(dict(origin_file_id=origin_file.id))
    doc.update({'doc_id': root.attrib.get('ИдДок')})
    doctype = root.getchildren()[0].tag
    print(f'Документ.ДокИд: {doc.get("doc_id")}')
    # print(doctype)
    if doctype == 'ИПВклМСП':
        ie_id = load_ind_ent(root.getchildren()[0])
        le_id = 1
    elif doctype == 'ОргВклМСП':
        ie_id = 1
        le_id = load_leg_ent(root.getchildren()[0])

    doc.update({'entity_type': doctype,
        'ind_ent_id': ie_id,
        'leg_ent_id': le_id})

    # location routine
    location = root.find('СведМН')
    r, d, c, l = loc_idx(location)
    r_code = location.attrib.get('КодРегион')

    # SvOKVED routine
    if root.find('СвОКВЭД'):
        okved_flag_ = 'Y'
        okved_list = save_okved(root)
    else:
        okved_flag_ = 'N'
        okved_list = []

    # licenses routine
    if root.find('СвЛиценз'):
        license_flag_ = 'Y'
        license_list = save_license(root)
    else:
        license_flag_ = 'N'
        license_list = []

    # Product routine
    if root.find('СвПрод'):
        prod_flag = 'Y'
        prod_list = save_products(root)
    else:
        prod_flag = 'N'
        prod_list = []

    # PartnerProgram routine
    if root.find('СвПрогПарт'):
        prog_flag = 'Y'
        prog_list = save_programs(root)
    else:
        prog_flag = 'N'
        prog_list = []

    # Contracts routine
    if root.find('СвКонтр'):
        c_flag = 'Y'
        c_list = save_contracts(root)
    else:
        c_flag = 'N'
        c_list = []

    # Agreements routine
    if root.find('СвДог'):
        a_flag = 'Y'
        a_list = save_agreements(root)
    else:
        a_flag = 'N'
        a_list = []

    rest_args = dict(region=r,
        district=d,
        city=c,
        locality=l,
        region_code=int(r_code),
        okved_flag=okved_flag_,
        licenses_flag=license_flag_,
        products_flag=prod_flag,
        partner_program_flag=prog_flag,
        contract_flag=c_flag,
        agreement_flag=a_flag)
    
    doc.update(rest_args)
    document = Document(**doc)
    session.add(document)
    session.flush()
    docid = document.id

    c = Okved2Doc(doc_id=docid, okved_id=okved_list[0], primary_flag='Y')
    session.add(c)
    for idx in okved_list[1:]:
        c = Okved2Doc(doc_id=docid, okved_id=idx, primary_flag='N')
        session.add(c)
    for idx in license_list:
        l = License2Doc(doc_id=docid, license_id=idx)
        session.add(l)
    for idx in prod_list:
        p = Product2Doc(doc_id=docid, product_id=idx)
        session.add(p)
    for idx in prog_list:
        p = Program2Doc(doc_id=docid, program_id=idx)
        session.add(p)
    for idx in c_list:
        c = Contract2Doc(doc_id=docid, contract_id=idx)
        session.add(c)
    for idx in a_list:
        a = Agreement2Doc(doc_id=docid, agreement_id=idx)
        session.add(a)

    session.commit()

    # print(f'Finished Документ.ДокИд: {doc.get("doc_id")}')


def load_origin_file(root):
    sender = root.find('ИдОтпр')
    f = {}

    for k,v in file_dict.items():
        f[k] = root.attrib.get(v)

    f.update(dict(sender_id=load_sender(sender)))
    f.update(dict(actuality_date=parse('11.07.2017')))

    file = OriginFile(**f)

    session.add(file)
    session.commit()


def main():
    # now should unpack 20 docs from xml

    z = ZipFile('data-11062017-structure-08012016.zip', 'r')
    with z.open(z.namelist()[0]) as f:
        xmlf = etree.parse(f)
        root = xmlf.getroot()

    load_origin_file(root)
    for ch in root.getchildren()[1:]:
        save_doc(ch)
    session.close()

if __name__ == '__main__':
    main()
