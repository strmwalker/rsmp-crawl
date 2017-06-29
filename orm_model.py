from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class DocumentLE(Base):
	"""Состав и структура документа юридического лица"""
	__tablename__ = 'doc_leg_ent'

	id = Column(Integer, primary_key=True)
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
	okved_primary = Column(Integer,
		ForeignKey('okved_codes.id'),
		nullable=True)
	licenses_flag = Column(String(1), nullable=False)
	products_flag = Column(String(1), nullable=False)
	partner_program_flag = Column(String(1), nullable=False)
	contract_flag = Column(String(1), nullable=False)
	agreement_flag = Column(String(1), nullable=False)


class DocumentIP(Base):
	"""Состав и структура документа индивидуального предпренимателя"""
	__tablename__ = 'doc_ind_ent'

	id = Column(Integer, primary_key=True)
	ind_ent_id = Column(Integer,
		ForeignKey('individual_enterpreneur.id'),
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
	okved_primary = Column(Integer,
		ForeignKey('okved_codes.id'),
		nullable=True)
	licenses_flag = Column(String(1), nullable=False)
	products_flag = Column(String(1), nullable=False)
	partner_program_flag = Column(String(1), nullable=False)
	contract_flag = Column(String(1), nullable=False)
	agreement_flag = Column(String(1), nullable=False)


class License(Base):
	"""Сведения о лицензиях, выданных субъекту МСП"""
	__tablename__ = 'license'

	id = Column(Integer, primary_key=True, nullable=False)

	# doc_le_id/doc_ip_id должно быть 0
	doc_le_id = Column(Integer,
		ForeignKey('doc_leg_ent.id'),
		nullable=False)
	doc_ip_id = Column(Integer,
		ForeignKey('doc_ind_ent.id'),
		nullable=False)
	activity_flag = Column(String(1),
		nullable=False)
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
	organization = Column(String(500),
		nullable=True)
		

class Product(Base):
	"""Сведения о производимой субъектом МСП продукции"""
	__tablename__ = 'product'

	id = Column(Integer, primary_key=True, nullable=False)

	# doc_le_id/doc_ip_id должно быть 0
	doc_le_id = Column(Integer,
		ForeignKey('doc_leg_ent.id'),
		nullable=False)
	doc_ip_id = Column(Integer,
		ForeignKey('doc_ind_ent.id'),
		nullable=False)
	code = Column(String(18),
		nullable=False)
	name = Column(String(1000),
		nullable=False)
	innovative_flag = Column(String(1),
		nullable=False)


class PartnerProgram(Base):
	"""Сведения о включении субъекта МСП в реестры программ партнерства"""
	__tablename__ = 'partner_program'

	id = Column(Integer, primary_key=True, nullable=False)

	# doc_le_id/doc_ip_id должно быть 0
	doc_le_id = Column(Integer,
		ForeignKey('doc_leg_ent.id'),
		nullable=False)
	doc_ip_id = Column(Integer,
		ForeignKey('doc_ind_ent.id'),
		nullable=False)
	customer_name = Column(String(1000),
		nullable=False)
	leg_ent_inn = Column(String(12),
		nullable=False)
	agreement_number = Column(String(60),
		nullable=False)
	agreement_date = Column(Date,
		nullable=False)


class Contract(Base):
	"""Сведения о наличии у субъекта МСП в предшествующем календарном году 
	контрактов, заключенных в соответствии с Федеральным законом от 5 апреля 
	2013 года №44-ФЗ"""
	__tablename__ = 'contract'

	id = Column(Integer, primary_key=True, nullable=False)

	# doc_le_id/doc_ip_id должно быть 0
	doc_le_id = Column(Integer,
		ForeignKey('doc_leg_ent.id'),
		nullable=False)
	doc_ip_id = Column(Integer,
		ForeignKey('doc_ind_ent.id'),
		nullable=False)

	lcustomer_inn = Column(String(12),
		nullable=False)
	subject = Column(String(1000),
		nullable=True)
	registry_number = Column(String(60),
		nullable=False)
	date = Column(Date,
		nullable=True)


class Agreement(Base):
	"""Сведения о наличии у субъекта МСП в предшествующем календарном году 
	договоров, заключенных в соответствии с Федеральным законом от 18 июля
	2011 года №223-ФЗ"""
	__tablename__ = 'agreement'
	
	id = Column(Integer, primary_key=True, nullable=False)

	# doc_le_id/doc_ip_id должно быть 0
	doc_le_id = Column(Integer,
		ForeignKey('doc_leg_ent.id'),
		nullable=False)
	doc_ip_id = Column(Integer,
		ForeignKey('doc_ind_ent.id'),
		nullable=False)

	customer_name = Column(String(1000),
		nullable=False)
	customer_inn = Column(String(12),
		nullable=False)
	subject = Column(String(1000),
		nullable=True)
	registry_number = Column(String(60),
		nullable=False)


class LegalEntity(Base):
	"""Сведения о юридическом лице, включенном в реестр МСП"""
	__tablename__ = 'legal_entity'

	id = Column(Integer, primary_key=True)
	org_name_full = Column(String(1000), nullable=False)
	org_name_short = Column(String(500), nullable=True)
	inn = Column(String(12), nullable=False)


class IndividualEnterpreneur(Base):
	"""Сведения об индивидуальном предпренимателе, включенном в 
	реестр МСП"""
	__tablename__ = 'individual_enterpreneur'

	id = Column(Integer, primary_key=True)
	first_name = Column(String(60), nullable=False)
	last_name = Column(String(60), nullable=False)
	middle_name = Column(String(60), nullable=True)
	inn = Column(String(12), nullable=False)
		

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
	type_num = Column(Integer, nullable=False)
	adress_type = Column(String(50), nullable=False)
	adress_name = Column(String(255), nullable=False)


class AdressOpt(Base):
	"""Сведения о наименование адресного элемента тип 2"""
	__tablename__ = 'adress_opt'

	id = Column(Integer, primary_key=True)
	type_num = Column(Integer, nullable=False)
	adress_type = Column(String(50), nullable=True)
	adress_name = Column(String(255), nullable=False)


if __name__ == '__main__':
	from sqlalchemy import create_engine
	engine = create_engine('mysql+mysqldb://root:1234@localhost:3306/rsmp')
	Base.metadata.create_all(engine)
