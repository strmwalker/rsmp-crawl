from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from orm_model import *

from datetime import date
from dateparser import parse


class XMLReport(object):
	"""docstring for XMLReport"""
	def __init__(self, session=None):
		super(XMLReport, self).__init__()
		self.session = session

	def start_engine(self, user='root', password='1234'):
		self.engine = create_engine(f'mysql+mysqldb://{root}:{password}\
			@localhost:3306/rsmp?charset=utf8')
		self.Session = sessionmaker(bind=self.engine)
	
	def create_session(self):
		session = self.Session()
		return session

	def function(self):
		pass
