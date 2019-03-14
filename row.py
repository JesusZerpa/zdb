# -*- coding: utf-8 -*-
from collections import deque
import json
class Row(object):
	"""docstring for Row"""
	def __init__(self,table,cursor=None):
		super(Row, self).__init__()
		self.table = table
		self.db=table.db
		self.grud=deque()
		self.use_cache=False#esto es para no hacer la lectura de los ficheros
		if cursor==None:
			self._n=table.cursor#posicion del cursor en la tabla
		else:
			self._n=cursor
	def __getitem__(self,clave):
		if not self.use_cache:
			from datetime import date,time,datetime
			self.grud=deque()
			for k,elem in enumerate(self.table._fields):
				with open(self.db.path+"/"+self._tablename+"/"+k+"/"+json.dumps(self._n)+".py","w") as f:
					data=json.loads(f.read())
					if elem.type=="date":
						data=date.strptime(data,elem.format)
					elif elem.type=="datetime":
						data=datetime.strptime(data,elem.format)
					elif elem.type=="time":
						data=time.strptime(data,elem.format)
					self.grud.append(data)
	

		if type(clave)==slice:

			return self.grud[clave]
		if type(clave)==int:
			if clave<len(self.grud):return self.grud[clave]
			else:raise
		elif type(clave)==unicode and type(clave)==str:
			for k in xrange(len(self.table.fields)):
				if self.table.fields[k]==clave:
					return self.grud[k]
	def __setitem__(self,clave,valor):
		from datetime import date,time,datetime

		if type(clave)==int:
			
				if ((type(valor)==str or type(valor)==unicode) and self.table._fields[clave].type=="string"):
					self.grud.append(valor)
				elif type(valor)==int and self.table._fields[clave].type=="integer":
					self.grud.append(valor)
				elif (type(valor)==int or type(valor)==str or type(valor)==unicode) and (self.table._fields[clave].type=="id"):
					self.grud.append(valor)
				elif valor==None and self.table._fields[clave].type=="id":
					self.grud.append(self.table.cursor)

				elif (type(valor)==float and self.table._fields[clave].type=="double"):
					self.grud.append(valor)
				elif ((type(valor)==str or type(valor)==unicode) and self.table._fields[clave].type=="password"):
					import hashlib
					valor=hashlib.md5(valor).hexdigest()
					self.grud.append(valor)
				elif (type(valor)==bool and self.table._fields[clave].type=="boolean"):
					self.grud.append(valor)
				elif (type(valor)==bool and self.table._fields[clave].type=="blob"):
					self.grud.append(valor)
				elif (type(valor)==date and self.table._fields[clave].type=="date"):
					self.grud.append(valor)
				elif (type(valor)==datetime and self.table._fields[clave].type=="datetime"):
					self.grud.append(valor)
				elif (type(valor)==time and self.table._fields[clave].type=="time"):
					self.grud.append(valor)
				elif (self.table._fields[clave]=="json"):
					json.dumps(valor)#prueba de que es serializable
					self.grud.append(valor)

				else:
					print valor==None , self.table._fields[clave]
					raise


			
		else:
			raise
	def update(self,*fields,**kwargs):
		for elem in fields:
			self[elem]=fields[elem]


	def write(self):

		for k,elem in enumerate(self.grud):
			if self.table._fields[k].type=="datetime" or  self.table._fields[k].type=="time" or  self.table._fields[k].type=="date":
				with open(self.db.path+"/"+self.table._tablename+"/"+json.dumps(k)+"/"+json.dumps(self._n)+".py","w") as f:
					f.write(json.dumps(elem.strftime(self.table._fields[k].format)))
			elif self.table._fields[k].type=="blob":
				with open(self.db.path+"/"+self.table._tablename+"/"+json.dumps(k)+"/"+json.dumps(self._n)+".py","wb") as f:
					f.write(elem)
			else:
				with open(self.db.path+"/"+self.table._tablename+"/"+json.dumps(k)+"/"+json.dumps(self._n)+".py","w") as f:
					f.write(json.dumps(elem))

		