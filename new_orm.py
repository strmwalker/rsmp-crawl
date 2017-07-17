'''
This module creates database schema with declarative base, also creates
dummy individual enterpreneur and dummy legal entity so they can flag
if there is one or another in document.

Every class here has an attrib_dict attribute which can be used to map
things from cyrillic names in xml file to regular latin ones in database.
'''

import datetime
from sqlalchemy import Table
from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer, String, Date, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()


Document2OKVED = Table('document2okved', Base.metadata,
    Column('document_id', Integer, ForeignKey('document.id')),
    Column('okved_codes.id', Integer, ForeignKey('okved_codes.id'))
    )
Document2Product = Table('document2product', Base.metadata,
    Column('document_id',
        Integer,
        ForeignKey('document.id'),
        nullable=False),
    Column('product_id',
        Integer,
        ForeignKey('product.id'),
        nullable=False)
    )


class File(Base):
    __tablename__ = 'files'
    id = Column(Integer, primary_key=True)

    # xpath: /Файл
    file_id = Column(String(255), nullable=False)
    format_version = Column(String(255), nullable=False)
    data_type = Column(String(50), nullable=True)
    program_version = Column(String(40), nullable=True)
    document_count = Column(Integer, nullable=False)

    # xpath: /Файл/ИдОтпр
    sender_id = Column(Integer,
        ForeignKey('senders.id'),
        nullable=False)

    # special column passed from script, not from xml file
    actuality_date = Column(Date, nullable=False)

    # relationships section
    sender = relationship('Sender', uselist=False, back_populates='files')
    documents = relationship('Document', back_populates='files')

    attrib_dict = {'file_id': 'ИдФайл',
        'format_version': 'ВерсФорм',
        'data_type': 'ТипИнф',
        'program_version': 'ВерсПрог',
        'doc_count': 'КолДок'}


class Sender(Base):
    __tablename__ = 'senders'
    id = Column(Integer, primary_key=True)

    # xpath: /Файл/ИдОтпр/ФИООтв
    f = Column(String(60), nullable=False)
    i = Column(String(60), nullable=False)
    o = Column(String(60), nullable=False)

    # xpath: /Файл/ИдОтпр
    position = Column(String(100), nullable=True)
    phone_number = Column(String(20), nullable=True)
    email = Column(String(45), nullable=False)

    # ../
    file_id = Column(Integer,
        ForeignKey('files.id'),
        nullable=False)
    file = relationship('File',
        back_populates='senders')

    attrib_dict = {'position':'ДолжОтв',
        'phone_number':'Тлф',
        'email':'E-mail'}


class Document(Base):
    __tablename__ = 'documents'
    id = Column(Integer, primary_key=True)

    # xpath: ../
    file_id = Column(Integer,
        ForeignKey('files.id'),
        nullable=False)

    # xpath: /Файл/Документ
    doc_id = Column(String(36), nullable=False)

    # xpath: /Файл/Документ/(ИПВклМСП|ОргВклМСП)
    entity_type = Column(String(9), nullable=False)
    ie_id = Column(Integer,
        ForeignKey('ind_ent.id'),
        nullable=False)
    le_id = Column(Integer,
        ForeignKey('leg_ent.id'),
        nullable=False)

    # xpath: /Файл/Документ/СведМН/
    region = Column(Integer,
        ForeignKey('adress_req.id'),
        nullable=False)
    district = Column(Integer,
        ForeignKey('adress_req.id'),
        nullable=False)
    city = Column(Integer,
        ForeignKey('adress_req.id'),
        nullable=True)
    locality = Column(Integer,
        ForeignKey('adress_opt.id'),
        nullable=True)
    # xpath: /Файл/Документ/СведМН
    region_code = Column(String(2), nullable=False)

    # xpath: /Файл/Документ
    compile_date = Column(Date, nullable=False)
    include_date = Column(Date, nullable=False)
    msp_subject_type = Column(String(1), nullable=False)
    msp_subject_cat  = Column(String(1), nullable=False)
    new_msp_flag = Column(String(1), nullable=False)

    # xpath: /Файл/Документ/
    okved_flag = Column(Boolean, nullable=False)
    licenses_flag = Column(Boolean, nullable=False)
    products_flag = Column(Boolean, nullable=False)
    partner_program_flag = Column(Boolean, nullable=False)
    contract_flag = Column(Boolean, nullable=False)
    agreement_flag = Column(Boolean, nullable=False)


    # registry subject relationship
    ie = relationship('Individual',
        back_populates='document')
    le = relationship('LegalEntity',
        back_populates='document')

    # parent file relationship
    file = relationship('File', back_populates='document')
    # СведМН relationship
    _region = relationship('AdressReq')
    _district = relationship('AdressReq')
    _city = relationship('AdressReq')
    _locality = relationship('AdressOpt')

    # child relationship
    okved_codes = relationship('OKVED',
        secondary=Document2OKVED)
    licenses = relationship('License',
        back_populates='documents')
    products = relationship('Product',
        secondary=Document2Product)
    partnerships = relationship('Partnership')
    contracts = relationship('Contract')
    agreements = relationship('Agreement')


    attrib_dict = {'doc_id': 'ИдДок',
        'compile_date': 'ДатаСост',
        'include_date': 'ДатаВклМСП',
        'msp_subject_type': 'ВидСубМСП',
        'msp_subject_category': 'КатСубМСП',
        'new_msp_flag': 'ПризНовМСП'}


class Individual(Base):
    __tablename__ = 'ind_ent'
    id = Column(Integer, primary_key=True)

    # xpath: /Файл/Документ/ИПВклМСП/ФИОИП
    f = Column(String(60), nullable=False)
    i = Column(String(60), nullable=False)
    o = Column(String(60), nullable=True)

    # xpath: /Файл/Документ/ИПВклМСП
    inn = Column(String(12), nullable=False)

    document = relationship('Document',
        uselist=False,
        back_populates='ind_ent')

    attrib_dict = {'inn': 'ИННФЛ'}


class LegalEntity(Base):
    __tablename__ = 'leg_ent'
    id = Column(Integer, primary_key=True)

    # xpath: /Файл/Документ/ОргВклМСП
    org_name_full = Column(String(1000), nullable=False)
    org_name_short = Column(String(500), nullable=True)
    inn = Column(String(10), nullable=False)

    # relationship
    document = relationship('Document',
        uselist=False,
        back_populates='leg_ent')

    attrib_dict = {'org_name_full': 'НаимОрг',
        'org_name_short': 'НаимОргСокр',
        'inn': 'ИННЮЛ'}


class AdressReq(Base):
    __tablename__ = 'adress_req'
    id = Column(Integer, primary_key=True)

    # xpath: /Файл/Документ/СведМН/НаимАдрТип1
    adress_type = Column(String(50), nullable=False)
    adress_name = Column(String(255), nullable=False)

    attrib_dict = {'adress_type': 'Тип',
        'adress_name': 'Наим'}


class AdressOpt(Base):
    __tablename__ = 'adress_opt'
    id = Column(Integer, primary_key=True)


    # xpath: /Файл/Документ/СведМН/НаимАдрТип2
    adress_type = Column(String(50), nullable=True)
    adress_name = Column(String(255), nullable=False)

    attrib_dict = {'adress_type': 'Тип',
        'adress_name': 'Наим'}


class OKVED(Base):
    __tablename__ = 'okved_codes'
    id = Column(Integer, primary_key=True)

    # xpath: /Файл/Документ/(СвОКВЭДОсн|СвОКВЭДДоп)
    code = Column(String(8), nullable=False)
    name = Column(String(1000), nullable=False)
    version = Column(String(4), nullable=False)

    primary_flag = Column(Boolean, nullable=False)

    attrib_dict = {'code': 'КодОКВЭД',
        'name': 'НаимОКВЭД',
        'version': 'ВерсОКВЭД'}


class License(Base):
    __tablename__ = 'licenses'
    id = Column(Integer, primary_key=True)

    document_id = Column(Integer,
        ForeignKey('document.id'),
        nullable=False)

    # xpath: /Файл/Документ/СвЛиценз
    series = Column(String(10), nullable=True)
    number = Column(String(100), nullable=False)
    license_type = Column(String(10), nullable=True)
    date = Column(Date, nullable=False)
    start_date = Column(Date, nullable=False)
    expiration_date = Column(Date, nullable=True)
    organization = Column(String(500), nullable=True)
    suspend_date = Column(Date, nullable=True)
    suspend_org = Column(String(500), nullable=True)

    # children relationship
    name = relationship('LicenseName', back_populates='licenses')
    adress = relationship('LicenseAdress', back_populates='licenses')

    # parent relationship
    document = relationship('Document', back_populates='licenses')

    attrib_dict = {'series': 'СерЛиценз',
        'number': 'НомЛиценз',
        'license_type': 'ВидЛиценз',
        'date': 'ДатаЛиценз',
        'start_date': 'ДатаНачЛиценз',
        'expiration_date': 'ДатаКонЛиценз',
        'organization': 'ОргВыдЛиценз',
        'suspend_date': 'ДатаОстЛиценз',
        'suspend_org': 'ОргОстЛиценз'}


class LicenseName(Base):
    __tablename__ = 'license_names'
    id = Column(Integer, primary_key=True)

    # xpath: ../
    license_id = Column(Integer,
        ForeignKey('licenses.id'),
        nullable=False)

    # xpath: /Файл/Документ/СвЛиценз/НаимЛицВД
    name = Column(String(1000), nullable=False)
    # explicit order
    part = Column(Integer, nullable=False)

    # relationship
    license = relationship('License', back_populates='license_names')


class LicenseAdress(Base):
    __tablename__ = 'license_adresses'
    id = Column(Integer, primary_key=True)

    # xpath: ../
    license_id = Column(Integer,
        ForeignKey('licenses.id'),
        nullable=False)

    # xpath: /Файл/Документ/СвЛиценз/СведАдрЛицВД
    adress = Column(String(500), nullable=False)
    # explicit order
    part = Column(Integer, nullable=False)

    # relationship
    license = relationship('License', back_populates='license_adresses')


class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)

    # xpath: /Файл/Документ/СвПрод
    code = Column(String(18), nullable=False)
    name = Column(String(1000), nullable=False)
    innovative_flag = Column(String(1), nullable=False)

    attrib_dict = {'code': "КодПрод",
        'name': "НаимПрод",
        'innovative_flag': "ПрОтнПрод"}


class Partnership(Base):
    __tablename__ = 'partnerships'
    id = Column(Integer, primary_key=True)

    # xpath: /Файл/Документ/СвПрогПарт
    le_name = Column(String(1000), nullable=False)
    le_inn = Column(String(10), nullable=False)
    number = Column(String(60), nullable=False)
    date = Column(Date, nullable=False)

    document_id = Column(Integer,
        ForeignKey('document.id'),
        nullable=False)
    document = relationship('Document', back_populates='partnerships')

    attrib_dict = {'le_name': 'НаимЮЛ_ПП',
        'le_inn': 'ИННЮЛ_ПП',
        'number': 'НомДог',
        'date': 'ДатаДог'}


class Contract(Base):
    __tablename__ = 'contracts'
    id = Column(Integer, primary_key=True)

    # xpath: /Файл/Документ/СвКонтр
    le_name = Column(String(1000), nullable=False)
    le_inn = Column(String(10), nullable=False)
    subject = Column(String(1000), nullable=True)
    registry_number = Column(String(60), nullable=False)
    date = Column(Date, nullable=True)

    document_id = Column(Integer,
        ForeignKey('document.id'),
        nullable=False)

    document = relationship('Document', back_populates='contracts')

    attrib_dict = {'le_name': 'НаимЮЛ_ЗК',
        'le_inn': 'ИННЮЛ_ЗК',
        'subject': 'ПредмКонтр',
        'registry_number': 'НомКонтрРеестр',
        'date': 'ДатаКонтр'}


class Agreement(Base):
    __tablename__ = 'agreements'
    id = Column(Integer, primary_key=True)

    # xpath: /Файл/Документ/СвДог
    le_name = Column(String(1000), nullable=False)
    le_inn = Column(String(10), nullable=False)
    subject = Column(String(1000), nullable=True)
    registry_number = Column(String(60), nullable=False)
    date = Column(Date, nullable=True)

    document_id = Column(Integer,
        ForeignKey('document.id'),
        nullable=False)

    document = relationship('Document', back_populates='agreements')

    attrib_dict = {'le_name': 'НаимЮЛ_ЗД',
        'le_inn': 'ИННЮЛ_ЗД',
        'subject': 'ПредмДог',
        'registry_number': 'НомДогРеестр',
        'date': 'ДатаДог'}


if __name__ == '__main__':
    from sqlalchemy import create_engine

    engine = create_engine('mysql+mysqldb://root:1234@localhost:3306/rsmp?charset=utf8')
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)

    dummy_ie = Individual(f='-', i='-', inn='-')
    dummy_le = LegalEntity(org_name_full='-', org_name_short='-', inn='-')

    session = Session()
    session.add(dummy_le)
    session.add(dummy_ie)
    session.commit()
    session.close()
