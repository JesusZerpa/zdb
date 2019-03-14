# -*- coding: utf-8 -*-
from table import Table
from multiconsulte import MultiConsulte
import os
class DB(object):
	"""docstring for DB"""
	def __init__(self,path):
		super(DB, self).__init__()
		self.path = path
		self.tables=[]
		self._tables=[]

		for table in os.listdir(path):
			self[table]

	def define_table(self,tablename,*fields):
		table=Table(tablename,self,fields)
		self.tables.append(table._tablename)
		self._tables.append(table)

	def __getitem__(self,tablename):
		
		if tablename in self.tables:
			self.tables.append(tablename)

			for k,elem in enumerate(self._tables):
				if elem._tablename==tablename:
					return elem
					
		else:
			table=Table.load(tablename,self)
			self.tables.append(table._tablename)
			self._tables.append(table)
			return table

		
		
		

	def __call__(self,consulte):
		return MultiConsulte(self,consulte)
	def commit(self):
		for table in self._tables:
			table.commit()
		
		

		