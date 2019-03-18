# -*- coding: utf-8 -*-
from table import Table
from multiconsulte import MultiConsulte
import os,time,json

class DB(object):
	"""docstring for DB"""
	

	def __init__(self,path):
		super(DB, self).__init__()
		self.path = path
		
		self._tables=[]
		self.__tablesbycreate=[]

		for table in os.listdir(path):
			self[table]
	@property
	def tables(self):
		l=[]
		for table in os.listdir(self.path):
			os.path.exists(self.path+"/"+table+"/settings.py")
			l.append(table)
		return l


	def define_table(self,tablename,*fields,**kwargs):
		table=Table(tablename,self,fields,0,True)
		if "comment" in kwargs: table.settings["comment"]=kwargs["comment"]
		self._tables.append(table)
		self.__tablesbycreate.append(table._tablename)

	def __getitem__(self,tablename):
		
		if tablename in self.tables or tablename in self.__tablesbycreate:

			for k,elem in enumerate(self._tables):
				if elem._tablename==tablename:

					return elem
			else:
				table=Table.load(tablename,self)
				self._tables.append(table)
				return table

		
		
		

	def __call__(self,consulte):
		return MultiConsulte(self,consulte)
	def commit(self):
		for table in self._tables:
			table.commit()

	
		
		

		