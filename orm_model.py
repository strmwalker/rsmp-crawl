import datetime
from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Document(Base):
    """Состав и структура документа"""
    ru_map = {'ind_ent_id': 'ИПВклМСП',
         'region': "Регион",
         'district': "Район",
         'city': "Город",
         'locality': "НаселПункт",
         'region_code': "КодРегион",
         'okved_primary': "СвОКВЭДОсн"}

    __tablename__ = 'document'

    id = Column(Integer, primary_key=True)
    origin_file_id = Column(Integer,
        ForeignKey('xml_meta.id'),
        nullable=False)
    entity_type = Column(String(9), nullable=False)
    ind_ent_id = Column(Integer,
        ForeignKey('individual_enterpreneur.id'),
        nullable=False)
    leg_ent_id = Column(Integer,
        ForeignKey('legal_entity.id'),
        nullable=False)
    region = Column(Integer,
        ForeignKey('adress_req.id'),
        nullable=False)
    district = Column(Integer,
        ForeignKey('adress_req.id'),
        nullable=True)
    city = Column(Integer,
        ForeignKey('adress_req.id'),
        nullable=True)
    locality = Column(Integer,
        ForeignKey('adress_opt.id'),
        nullable=True)
    region_code = Column(String(2), nullable=False)
    okved_flag = Column(String(1), nullable=False)
    licenses_flag = Column(String(1), nullable=False)
    products_flag = Column(String(1), nullable=False)
    partner_program_flag = Column(String(1), nullable=False)
    contract_flag = Column(String(1), nullable=False)
    agreement_flag = Column(String(1), nullable=False)


class OKVED2Doc(Base):
    """Таблица соединения Документа и КодОКВЭД"""
    
    __tablename__ = 'okved2doc'
    id = Column(Integer, primary_key=True, nullable=False)
    doc_id = Column(Integer,
        ForeignKey('document.id'),
        nullable=False)
    okved_id = Column(Integer,
        ForeignKey('okved_codes.id'),
        nullable=False)
    primary_flag = Column(String(1), nullable=False)
        

class License(Base):
    """Сведения о лицензиях, выданных субъекту МСП"""

    __tablename__ = 'license'

    id = Column(Integer, primary_key=True, nullable=False)

    series = Column(String(10),
        nullable=True)
    number = Column(String(100),
        nullable=False)
    type_ = Column(String(10),
        nullable=True)
    date = Column(Date,
        nullable=False)
    start_date = Column(Date,
        nullable=False)
    end_date = Column(Date,
        nullable=True)
    license_provider = Column(String(500),
        nullable=True)
    stop_date = Column(Date,
        nullable=True)
    license_stopper = Column(String(500),
        nullable=True) 
        

class License2Doc(Base):
    """Таблица соединения Документа и лицензий субъекта"""
    __tablename__ = 'license2doc'

    id = Column(Integer, primary_key=True, nullable=False)
    doc_id = Column(Integer,
        ForeignKey('document.id'),
        nullable=False)     
    license_id = Column(Integer,
        ForeignKey('license.id'),
        nullable=False)


class LicenseName(Base):
    """Наименование лицензируемого вида деятельности, на который выдана
    лицензия"""
    
    __tablename__ = 'license_names'

    id = Column(Integer,
        primary_key=True,
        nullable=False)

    license_id = Column(Integer,
        ForeignKey('license.id'),
        nullable=False)
    name = Column(String(1000),
        nullable = False)
    part = Column(Integer,
        nullable=False)


class LicenseAdress(Base):
    """Сведения об адресе места осуществления лицензируемого 
    вида деятельности"""
    
    __tablename__ = 'license_adress'

    id = Column(Integer,
        primary_key=True,
        nullable=False)

    license_id = Column(Integer,
        ForeignKey('license.id'),
        nullable=False)
    license_adress = Column(String(500),
        nullable=False)
    license_adress_part = Column(Integer,
        nullable=False)


class Product(Base):
    """Сведения о производимой субъектом МСП продукции"""
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True, nullable=False)

    code = Column(String(18),
        nullable=False)
    name = Column(String(1000),
        nullable=False)
    innovative_flag = Column(String(1),
        nullable=False)

class Product2Doc(Base):
    """Соединение продукта и Документа"""
    __tablename__ = 'product2doc'

    id = Column(Integer, primary_key=True, nullable=False)
    doc_id = Column(Integer,
        ForeignKey('document.id'),
        nullable=False)     
    product_id = Column(Integer,
        ForeignKey('product.id'),
        nullable=False)


class PartnerProgram(Base):
    """Сведения о включении субъекта МСП в реестры программ партнерства"""
    __tablename__ = 'partner_program'

    id = Column(Integer, primary_key=True, nullable=False)

    customer_name = Column(String(1000),
        nullable=False)
    leg_ent_inn = Column(String(12),
        nullable=False)
    agreement_number = Column(String(60),
        nullable=False)
    agreement_date = Column(Date,
        nullable=False)


class Program2Doc(Base):
    """Соединение программ партнерства и Документа"""
    __tablename__ = 'program2doc'

    id = Column(Integer, primary_key=True, nullable=False)

    doc_id = Column(Integer,
        ForeignKey('document.id'),
        nullable=False)
    program_id = Column(Integer,
        ForeignKey('partner_program.id'),
        nullable=False)
        

class Contract(Base):
    """Сведения о наличии у субъекта МСП в предшествующем календарном году 
    контрактов, заключенных в соответствии с Федеральным законом от 5 апреля 
    2013 года №44-ФЗ"""
    __tablename__ = 'contract'

    id = Column(Integer, primary_key=True, nullable=False)

    customer_name = Column(String(1000),
        nullable=False)
    lcustomer_inn = Column(String(12),
        nullable=False)
    subject = Column(String(1000),
        nullable=True)
    registry_number = Column(String(60),
        nullable=False)
    date = Column(Date,
        nullable=True)


class Contract2Doc(Base):
    """Соединение Документ и контрактов"""
    __tablename__ = 'contract2doc'

    id = Column(Integer, primary_key=True, nullable=False)
    doc_id = Column(Integer,
        ForeignKey('document.id'),
        nullable=False)
    contract_id = Column(Integer,
        ForeignKey('contract.id'),
        nullable=False)
        

class Agreement(Base):
    """Сведения о наличии у субъекта МСП в предшествующем календарном году 
    договоров, заключенных в соответствии с Федеральным законом от 18 июля
    2011 года №223-ФЗ"""
    __tablename__ = 'agreement'
    
    id = Column(Integer, primary_key=True, nullable=False)

    customer_name = Column(String(1000),
        nullable=False)
    customer_inn = Column(String(12),
        nullable=False)
    subject = Column(String(1000),
        nullable=True)
    registry_number = Column(String(60),
        nullable=False)


class Agreement2Doc(Base):
    """Соединение Документа и договоров"""
    __tablename__ = 'agreement2doc'

    id = Column(Integer, primary_key=True, nullable=False)

    doc_id = Column(Integer,
        ForeignKey('document.id'),
        nullable=False)
    agreement_id = Column(Integer,
        ForeignKey('agreement.id'),
        nullable = False)
        


class LegalEntity(Base):
    """Сведения о юридическом лице, включенном в реестр МСП"""
    __tablename__ = 'legal_entity'

    id = Column(Integer, primary_key=True)
    org_name_full = Column(String(1000), nullable=False)
    org_name_short = Column(String(500), nullable=True)
    inn = Column(String(12), nullable=False)


class Individual(Base):
    """Сведения об индивидуальном предпренимателе, включенном в 
    реестр МСП"""
    __tablename__ = 'individual_enterpreneur'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(60), nullable=False)
    last_name = Column(String(60), nullable=False)
    middle_name = Column(String(60), nullable=True)
    inn = Column(String(12), nullable=False)
        

class Sender(Base):
    """Сведения об отправителе"""
    
    __tablename__ = 'senders'

    id = Column(Integer, primary_key=True)
    last_name = Column(String(60), nullable=False)
    first_name = Column(String(60), nullable=False)
    middle_name = Column(String(60), nullable=True)
    position = Column(String(100), nullable=True)
    phone_number = Column(String(20), nullable=True)
    email = Column(String(45), nullable=True)


class OriginFile(Base):
    """Сведения из единого реестра субъектов малого и среднего 
    предпренимательства"""
    
    __tablename__ = 'xml_meta'

    id = Column(Integer, primary_key=True)
    file_id = Column(String(255), nullable=False)
    format_version = Column(String(5), nullable=False)
    info_type = Column(String(50), nullable=False)
    prog_version = Column(String(40), nullable=True)
    doc_count = Column(Integer, nullable=False)
    sender_id = Column(Integer,
        ForeignKey('senders.id'),
        nullable=False)
    actuality_date = Column(Date, nullable=False)


class OkvedCode(Base):
    """Сведения о кодах по Общероссийскому классификатору видов экономической 
    деятельности"""
    __tablename__ = 'okved_codes'

    id = Column(Integer, primary_key=True)
    code = Column(String(8), nullable=False,
        doc='Код вида деятельности по Общероссийскому классификатору видов\
         экономической деятельности'
        )
    name = Column(String(1000), nullable=False,
        doc='Наименование вида деятельности по Общероссийскому классификатору\
         видов экономической деятельности'
         )
    version = Column(String(4), nullable=False)


class AdressReq(Base):
    """Сведения о наименование адресного элемента тип 1"""
    __tablename__ = 'adress_req'

    id = Column(Integer, primary_key=True)
    adress_type = Column(String(50), nullable=False)
    adress_name = Column(String(255), nullable=False)


class AdressOpt(Base):
    """Сведения о наименование адресного элемента тип 2"""
    __tablename__ = 'adress_opt'

    id = Column(Integer, primary_key=True)
    adress_type = Column(String(50), nullable=True)
    adress_name = Column(String(255), nullable=False)


if __name__ == '__main__':
    # execute basestart.sql before running this script

    from sqlalchemy import create_engine
    engine = create_engine('mysql+mysqldb://root:1234@localhost:3306/rsmp?charset=utf8')
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    # add dummy legal entity and indiv ent
    Session = sessionmaker(bind=engine)
    le_in_ind = Individual(first_name='-', middle_name='-', last_name='-', inn='-')
    ie_in_leg = LegalEntity(org_name_full='-', org_name_short='-', inn='-')
    session = Session()
    session.add(le_in_ind)
    session.add(ie_in_leg)
    session.commit()
    session.close()
