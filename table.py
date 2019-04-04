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


	
	def get_settings(self,name,db):
		
		if os.path.exists(db.path+"/"+name+"/settings.py"):
			with open(db.path+"/"+name+"/settings.py") as f:
					self.settings=json.loads(f.read())
					fields=[]
					null=None
					true=True
					false=False

					for field in self.settings["fields"]:
						exec("v="+field["compute"])
						field["compute"]=v
						if type(field["default"])==str or type(field["default"])==unicode:
							exec("v="+field["default"])
						else:
							v=field["default"]
						field["default"]=v
						f=Field(field["name"],field["type"])
						f.table=self
						f.update(field)
						fields.append(f)
					self.settings["fields"]=fields

	@classmethod
	def load_fields(cls,name,db):
		l=[]	
		if os.path.exists(db.path+"/"+name+"/settings.py"):
			with open(db.path+"/"+name+"/settings.py") as f:
					cls.settings=json.loads(f.read())
					fields=[]
					null=None
					true=True
					false=False

					for field in cls.settings["fields"]:
						l.append(Field(field["name"],field["type"]))
						
		return l
	@classmethod
	def load(cls,name,db):

		
		table=Table(name,db,cls.load_fields(name,db),cls.settings["cursor"])
		
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
	def _create_consulte(self):
		import time
		
		if os.path.exists(self.db.path+"/"+self._tablename):
			
			exists=existed=os.path.exists(self.db.path+"/"+self._tablename+"/.consulte")
			consulte=None 
		
			if exists:
				with open(self.db.path+"/"+self._tablename+"/.consulte") as f:
					read=f.read()
					if read:
						consulte=json.loads(read)
				os.remove(self.db.path+"/"+self._tablename+"/.consulte")

			if consulte and consulte["id"]!=id(self):

				tiempo=time.time()
			
				while exists:
					time.sleep(0.2)
					if time.time()-tiempo>consulte["timeout"]:
						os.remove(self.db.path+"/"+self._tablename+"/.consulte")
						exists=False
						break
					exists=os.path.exists(self.db.path+"/"+self._tablename+"/.consulte")

			with open(self.db.path+"/"+self._tablename+"/.consulte","w") as f:
				if existed:
					self.get_settings(self._tablename,self.db)
				if consulte:
					f.write(json.dumps({"timeout":self.timeout,"id":id(self),"message":{"consulte":consulte["id"],"status":404}}))
				else:
					f.write(json.dumps({"timeout":self.timeout,"id":id(self)}))
				
	def _has_consulte(self):

		exists=existed=os.path.exists(self.db.path+"/"+self._tablename+"/.consulte")

		if exists:
			with open(self.db.path+"/"+self._tablename+"/.consulte") as f:
				read=f.read()
				if read:
					consulte=json.loads(read)
				else:
					consulte=None
			if consulte==None:
				os.remove(self.db.path+"/"+self._tablename+"/.consulte")
				return False
			if consulte["id"]==id(self):
				return True
		else:
			return False
	def _end_consulte(self):
		if os.path.exists(self.db.path+"/"+self._tablename+"/.consulte"):
			with open(self.db.path+"/"+self._tablename+"/.consulte") as f:
				consulte=json.loads(f.read())
			if consulte["id"]==id(self):
				os.remove(self.db.path+"/"+self._tablename+"/.consulte")

				





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
		
		self._create_consulte()

		self.grud[self.cursor]=row
		self.do_commit=True
		return self.cursor



	def __getitem__(self,cursor):


		if type(cursor)==slice:
			return itertools.islice(self,cursor.start,cursor.stop,cursor.step)#indice.stop es el self.end solo que del itertools
		elif type(cursor)==int and cursor<=self.cursor:

			row=Row(self,cursor)
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
			is_new=False
			exists=os.path.exists(self.db.path+"/"+self._tablename)
			if not os.path.exists(self.db.path+"/"+self._tablename):
					os.mkdir(self.db.path+"/"+self._tablename)
					is_new=True
					for k,elem in enumerate(self._fields):
						os.mkdir(self.db.path+"/"+self._tablename+"/"+json.dumps(k))
			for row in self.grud:
				self.grud[row].write()
			
			if self._has_consulte() or not exists:
				settings["fields"]=[]		
				settings["cursor"]=self.cursor
			

				for k,elem in enumerate(self._fields):
					attrs=elem._getattrs()
					if not is_new:						
						if "compute" in elem._updates:
							source=inspect.getsource(attrs["compute"])
							attrs["compute"]=source[source.find("=")+1:]
						if "default" in elem._updates:
							if attrs["default"]!=None:
								source=inspect.getsource(attrs["default"])
								attrs["default"]=source[source.find("=")+1:]
							else:
								attrs["default"]=json.dumps(attrs["default"])
					else:
						if "__call__" in dir(attrs["compute"]):
							source=inspect.getsource(attrs["compute"])
							attrs["compute"]=source[source.find("=")+1:]
						else:
							attrs["compute"]=json.dumps(attrs["compute"])

						if "__call__" in dir(attrs["default"]):
							source=inspect.getsource(attrs["default"])
							attrs["default"]=source[source.find("=")+1:]
						else:
							attrs["default"]=json.dumps(attrs["default"])


					
					settings["fields"].append(attrs)
					
				data=json.dumps(settings)
				with open(self.db.path+"/"+self._tablename+"/settings.py","w") as f:
						f.write(data)
				self._end_consulte()
				
			
			


			