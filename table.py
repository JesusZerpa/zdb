# -*- coding: utf-8 -*-
from row import Row
from collections import Counter,deque
from field import Field
import json,os,inspect

class Table(object):
	"""docstring for Table"""
	settings={"fields":[],"cursor":0}
	timeout=5
	do_commit=False
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


	def __init__(self,name,db,fields,cursor=0,create=False):
		super(Table, self).__init__()
		self._tablename=name
		self._fields=fields
		self.fields=[]
		self.do_commit=True
		if not create:
			if not os.path.exists(db.path+"/"+name):
				raise Exception("La tabla: '"+name+"' no existe")
		for elem in fields:
			elem.table=self
			elem.db=db
			try:
				if elem.name not in dir(self):
					setattr(self,elem.name,elem)
				else:
					setattr(self,elem.name+"_field",elem)
			except:
				pass
			self.fields.append(elem.name)
		self.db = db
		self.grud=Counter()#este debe ordenar los elementos de menor a mayor
		self.c=0
		self.cursor=cursor#este es el cursor actual de la tabla


	def __len__(self):
		pass
	def __iter__(self):
		self.c=0

		return self
		
	def next(self):
	
		if self.c<=self.cursor:
			
			self.c+=1
			try:
				
				x=self[self.c-1]
				return x
			except Exception as e:
				
				return self.next()
				
		else:
			raise StopIteration("No hay mas registros en la tabla")
	


	def insert(self,*args,**kwargs):
		import time

		self.get_settings(self._tablename,self.db)
		self.cursor+=1

		row=Row(self,self.cursor,True)

		for k,elem in enumerate(args):

			row[k]=elem
		row.update(**kwargs)
		
		

		if os.path.exists(self.db.path+"/"+self._tablename):
			exists=existed=os.path.exists(self.db.path+"/"+self._tablename+"/.consulte")
			consulte={"timeout":5}
			if exists:
				with open(self.db.path+"/"+self._tablename+"/.consulte") as f:
					consulte=json.loads(f.read())

			tiempo=time.time()
			while exists:
				if time.time()-tiempo>consulte["timeout"]:
					break
				exists=os.path.exists(self.db.path+"/"+self._tablename+"/.consulte")
			if existed:
				self.get_settings(self._tablename,self.db)

			with open(self.db.path+"/"+self._tablename+"/.consulte","w") as f:
				f.write(json.dumps({"timeout":self.timeout}))

		self.grud[self.cursor]=row
		self.do_commit=True
		return self.cursor



	def __getitem__(self,cursor):


		if type(cursor)==slice:
			return itertools.islice(self,cursor.start,cursor.stop,cursor.step)#indice.stop es el self.end solo que del itertools
		elif type(cursor)==int and cursor<=self.cursor:
			l=deque()

			if os.path.exists(self.db.path+"/"+self._tablename+"/0/"+json.dumps(cursor)+".py"):
				for k,elem in enumerate(self.fields):
					with open(self.db.path+"/"+self._tablename+"/"+json.dumps(k)+"/"+json.dumps(cursor)+".py") as f:
						l.append(json.loads(f.read()))

			row=Row(self,cursor)


			row.update(*l)



			self.grud[cursor]=row


			return row
		elif type(cursor)==str or type(cursor)==unicode:

			for elem in self._fields:

				if elem.name==cursor:
					return elem

	def __setitem__(self,clave,value):
		pass
	def evaluate(self):
		return True

	def commit(self):
		

		if self.do_commit:
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
			if os.path.exists(self.db.path+"/"+self._tablename+"/.consulte"):
				os.remove(self.db.path+"/"+self._tablename+"/.consulte")
			
			for row in self.grud:
				self.grud[row].write()

			


			