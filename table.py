# -*- coding: utf-8 -*-
from row import Row
from collections import Counter,deque
from field import Field
import json,os,inspect

class Table(object):
	"""docstring for Table"""
	settings={"fields":[],"cursor":0}
	@classmethod
	def get_settings(cls,name,db):
		
		if os.path.exists(db.path+"/"+name+"/settings.py"):
			with open(db.path+"/"+name+"/settings.py") as f:
					cls.settings=json.loads(f.read())
					fields=[]

					for field in cls.settings["fields"]:
						exec("v="+field["compute"])
						field["compute"]=v
						f=Field(field["name"],field["type"])

						f.update(field)
						fields.append(f)
					cls.settings["fields"]=fields
		
	@classmethod
	def load(cls,name,db):

		cls.get_settings(name,db)
		table=Table(name,db,cls.settings["fields"],cls.settings["cursor"])
		
		setattr(db,name,table)
		return table 


	def __init__(self,name,db,fields,cursor=0):
		super(Table, self).__init__()
		self._tablename=name
		self._fields=fields
		self.fields=[]

		for elem in fields:
			elem.table=self
			elem.db=db
			self.fields.append(elem.name)
		self.db = db
		self.grud=Counter()#este debe ordenar los elementos de menor a mayor
		self.c=0
		self.cursor=cursor#este es el cursor actual de la tabla

	def __len__(self):
		pass
	def __iter__(self):
		self.c=0
	def insert(self,*args,**kwargs):
		self.get_settings(self._tablename,self.db)
		self.cursor+=1
		row=Row(self,self.cursor)

		for k,elem in enumerate(args):
			row[k]=elem
		row.update(kwargs)
		

		self.grud[self.cursor]=row
		print self.grud


	def __getitem__(self,cursor):

		if type(cursor)==slice:
			return itertools.islice(self,cursor.start,cursor.stop,cursor.step)#indice.stop es el self.end solo que del itertools
		elif type(cursor)==int and cursor<self.cursor:
			l=deque()

			if os.path.exists(self.db.path+"/"+self._tablename+"/0/"+json.dumps(cursor)+".py"):
				for k,elem in enumerate(self.fields):
					with open(self.db.path+"/"+self._tablename+"/"+json.dumps(k)+"/"+json.dumps(cursor)+".py") as f:
						l.append(json.loads(f.read()))
			row=Row(self,cursor)
			row.update(*l)

			self.grud[cursor]=row

			return row

	def __setitem__(self,clave,value):
		pass
	def evaluate(self):
		return True

	def commit(self):
		
		settings=self.settings
		settings["fields"]=[]		
		settings["cursor"]=self.cursor
		if not os.path.exists(self.db.path+"/"+self._tablename):
			os.mkdir(self.db.path+"/"+self._tablename)
		
		for k,elem in enumerate(self._fields):
			if not os.path.exists(self.db.path+"/"+self._tablename+"/"+json.dumps(k)):
				os.mkdir(self.db.path+"/"+self._tablename+"/"+json.dumps(k))
			attrs=elem._getattrs()
			source=inspect.getsource(attrs["compute"])
			attrs["compute"]=source[source.find("=")+1:]
			attrs["name"]=elem.name
			attrs["type"]=elem.type
			settings["fields"].append(attrs)
		data=json.dumps(settings)
		with open(self.db.path+"/"+self._tablename+"/settings.py","w") as f:
				f.write(data)
		
		for row in self.grud:
			self.grud[row].write()

		


		