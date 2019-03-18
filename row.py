# -*- coding: utf-8 -*-
from collections import Counter
import json,os
class void(object):
	"""docstring for empty"""
	def __str__(self):
		return "void"

class Row(object):
	"""docstring for Row"""
	def __init__(self,table,cursor=None,create=False):
		super(Row, self).__init__()
		self.table = table
		self.db=table.db
		
		if not os.path.exists(self.db.path+"/"+self.table._tablename+"/0/"+json.dumps(cursor)+".py") and not create:
			raise Exception("No existe el registro")
		elif create:
			self.use_cache=True#esto es para no hacer la lectura de los ficheros
		else:
			self.use_cache=False#esto es para no hacer la lectura de los ficheros

		self.campos=(table._tablename,cursor)

		self.grud=Counter()
		
		if cursor==None:
			self._n=table.cursor#posicion del cursor en la tabla
		else:
			self._n=cursor

	def __getitem__(self,clave):

		if not self.use_cache:

			from datetime import date,time,datetime
			
			self.grud=Counter()
			for k,elem in enumerate(self.table._fields):
				if os.path.exists(self.db.path+"/"+self.table._tablename+"/"+json.dumps(k)+"/"+json.dumps(self._n)+".py"):
					with open(self.db.path+"/"+self.table._tablename+"/"+json.dumps(k)+"/"+json.dumps(self._n)+".py") as f:
						data=json.loads(f.read())
						if elem.type=="date":
							data=date.strptime(data,elem.format)
						elif elem.type=="datetime":
							data=datetime.strptime(data,elem.format)
						elif elem.type=="time":
							data=time.strptime(data,elem.format)
						self.grud[k]=data
				else:
					self.grud[k]=void()


		if type(clave)==slice:

			return self.grud[clave]
		if type(clave)==int:
			if clave<=max(list(self.grud)):
				if clave in self.grud:
					return self.grud[clave]
				else:
					if type(self.table._fields[clave].default)!=None and "__call__" in dir(self.table._fields[clave].default):
						self.grud[clave]=self.table._fields[clave].default()
					elif type(self.table._fields[clave].default)!=None:
						self.grud[clave]=self.table._fields[clave].default
					return self.grud[clave]
			else:raise
		elif type(clave)==unicode or type(clave)==str:

			for k in xrange(len(self.table.fields)):

				if self.table.fields[k]==clave:
					return self.grud[k]

	def __setitem__(self,clave,valor):
		from datetime import date,time,datetime
		
		if type(clave)==int:

			
				if ((type(valor)==str or type(valor)==unicode) and self.table._fields[clave].type=="string"):
					self.grud[clave]=valor
				elif type(valor)==int and self.table._fields[clave].type=="integer":
					self.grud[clave]=valor
				elif (type(valor)==int or type(valor)==str or type(valor)==unicode) and (self.table._fields[clave].type=="id" or self.table._fields[clave].type.startswith("reference ")):
					self.grud[clave]=valor
				elif valor==None and self.table._fields[clave].type=="id":
					self.grud[clave]=self.table.cursor

				elif (type(valor)==float and self.table._fields[clave].type=="double"):
					self.grud[clave]=valor
				elif ((type(valor)==str or type(valor)==unicode) and self.table._fields[clave].type=="password"):
					import hashlib
					valor=hashlib.md5(valor).hexdigest()
					self.grud[clave]=valor
				elif (type(valor)==bool and self.table._fields[clave].type=="boolean"):
					self.grud[clave]=valor
				elif (type(valor)==bool and self.table._fields[clave].type=="blob"):
					self.grud[clave]=valor
				elif (type(valor)==date and self.table._fields[clave].type=="date"):
					self.grud[clave]=valor
				elif (type(valor)==datetime and self.table._fields[clave].type=="datetime"):
					self.grud[clave]=valor
				elif (type(valor)==time and self.table._fields[clave].type=="time"):
					self.grud[clave]=valor
				elif (self.table._fields[clave].type=="json"):
					json.dumps(valor)#prueba de que es serializable
					self.grud[clave]=valor
				elif (valor==None and not self.table._fields[clave].notnull):
					self.grud[clave]=valor

				else:					
					raise Exception("El campo: '"+self.table._fields[clave].name+" es de tipo: '"+valor.__class__.__name__+"' y debe ser '"+self.table._fields[clave].type+"'")
		elif type(clave)==str or type(clave)==unicode:
				clave=self.table.fields.index(clave)
				

				if clave!=-1:
					if ((type(valor)==str or type(valor)==unicode) and self.table._fields[clave].type=="string"):
						self.grud[clave]=valor
					elif type(valor)==int and self.table._fields[clave].type=="integer":
						self.grud[clave]=valor
					elif (type(valor)==int or type(valor)==str or type(valor)==unicode) and (self.table._fields[clave].type=="id"):
						self.grud[clave]=valor
					elif valor==None and self.table._fields[clave].type=="id":
						self.grud[clave]=self.table.cursor

					elif (type(valor)==float and self.table._fields[clave].type=="double"):
						self.grud[clave]=valor
					elif ((type(valor)==str or type(valor)==unicode) and self.table._fields[clave].type=="password"):
						import hashlib
						valor=hashlib.md5(valor).hexdigest()
						self.grud[clave]=valor
					elif (type(valor)==bool and self.table._fields[clave].type=="boolean"):
						self.grud[clave]=valor
					elif (type(valor)==bool and self.table._fields[clave].type=="blob"):
						self.grud[clave]=valor
					elif (type(valor)==date and self.table._fields[clave].type=="date"):
						self.grud[clave]=valor
					elif (type(valor)==datetime and self.table._fields[clave].type=="datetime"):
						self.grud[clave]=valor
					elif (type(valor)==time and self.table._fields[clave].type=="time"):
						self.grud[clave]=valor
					elif (self.table._fields[clave].type=="json"):
						json.dumps(valor)#prueba de que es serializable
						self.grud[clave]=valor
					elif (valor==None and not self.table._fields[clave].notnull):
						self.grud[clave]=valor

					else:
						
						raise Exception("El campo: '"+self.table._fields[clave].name+" es de tipo: '"+valor.__class__.__name__+"' y debe ser '"+self.table._fields[clave].type+"'")
				else:
					
					raise Exception("No se encontro el indice del campo")

			
		else:

			raise Exception("La clave de busqueda deber ser un str,unicode o int ")
		for k,elem in enumerate(self.table._fields):
			if elem.notnull:
				if (k in self.grud and self.grud[k]==None) or k not in self.grud:
					raise Exception("El campo: '"+elem.name+"' no permite valores nulos")


		self.table.do_commit=True
	def update(self,*fields,**kwargs):

		for k,elem in enumerate(self.table.fields):
			if k<len(fields):

				self[elem]=fields[k]
			for field in kwargs:
				if field==elem:
					self[elem]=kwargs[field]



	def write(self):
		
		for k in self.grud:
			elem=self.grud[k]
			
			if self.table._fields[k].type=="datetime" or  self.table._fields[k].type=="time" or  self.table._fields[k].type=="date":

				with open(self.db.path+"/"+self.table._tablename+"/"+json.dumps(k)+"/"+json.dumps(self._n)+".py","w") as f:

					f.write(json.dumps(elem.strftime(self.table._fields[k].format)))
			elif self.table._fields[k].type=="blob":
				with open(self.db.path+"/"+self.table._tablename+"/"+json.dumps(k)+"/"+json.dumps(self._n)+".py","wb") as f:
					f.write(elem)
			elif type(elem)!=void:
				with open(self.db.path+"/"+self.table._tablename+"/"+json.dumps(k)+"/"+json.dumps(self._n)+".py","w") as f:
					f.write(json.dumps(elem))


		