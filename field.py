# -*- coding: utf-8 -*-
from consulte import Consulte
import os
class request(object):
	"""docstring for request"""
	folder="uploads/"
class Field(object):
	"""

	referencia a de un campo a otra tabla

	db.define_table('cosa',
	Field('nombre'),
	Field('id_propietario','reference persona'))

	esta se pasa como un tipo en el campo
	"""
	_updates=[]
	def __init__(self, name,type,length=None, default=None,
		required=False, requires='<default>',
		ondelete='CASCADE', notnull=False, unique=False,
		uploadfield=True, widget=None, label=None, comment=None,
		writable=True, readable=True, update=None, authorize=None,
		autodelete=False, represent=None, 
		compute=lambda x:x,#mover esta linea puede causar problemas con inspect.getsource
		uploadfolder=os.path.join(request.folder,'uploads'),
		uploadseparate=None,uploadfs=None,encode="md5",autosize=True):
		class Virtual(object):
			"""docstring for Virtual"""
			def __init__(self, _lambda):
				super(Virtual, self).__init__()
				self._lambda=_lambda

		"type id=clave_primaria integer"
		super(Field, self).__init__()
		self.name=name
		self._value=None
		self.type=type #reference tabla
		self.unique=False
		self.uploadfolder=uploadfolder
		self.ondelete=ondelete
		self.required=required
		self.label=label
		self.comment=comment
		self.writable=writable
		self.readable=readable
		self.encode=encode
		self.autosize=autosize
		self.notnull=notnull
		self.default=default
		self.compute=compute
		if self.type=="date":
			self.format="%Y-%m-%d"
		elif self.type=="time":
			self.format="%H:%M:%S"
		elif self.type=="datetime":
			self.format="%Y-%m-%d %H:%M:%S"
		if length==None:
			self.length=50
		else:
			self.length=length #devolvera un entero
		self._table=None#sera la tabla a la que pertenece
		self.cursor=0
		#=================
		#para los datetime
		


	@classmethod
	def Method(cls,_lambda):
		"""
		util para campos virtuales
		"""
		return _lambda








	def filter_in(self,a,b):
		"""
		antes de que se inserte en la base de datos
		"""
		pass
	def filter_out(self,a,b):
		"""
		despues que se inserte en la base de datos
		"""
		pass


	def __eq__(self,otro):
		if  self.type.startswith("reference "):
			self.db[self.type[len("reference "):].strip()].referencias.append(self)
		elif self.type.startswith("list:reference "):
			self.db[self.type[len("list:reference "):].strip()].referencias.append(self)
		return Consulte(self,"==",otro)
	def __ne__(self,otro):
		if  self.type.startswith("reference "):
			self.db[self.type[len("reference "):].strip()].referencias.append(self)
		elif self.type.startswith("list:reference "):
			self.db[self.type[len("list:reference "):].strip()].referencias.append(self)
		return Consulte(self,"!=",otro)



	@property
	def value(self):
		return self.compute(self._value)
	@value.setter
	def value(self,valor):
		try:
			if self.isType(valor):
				self._value=valor
				return True
			else:
				raise TipoError("El campo insertado es tipo: "+valor.__class__.__name__+" y debe que ser: "+self.type)
		except TipoError as e:
			print(e)


	@value.deleter
	def value(self):
		del self._value
	def like(self,valor,case_sensitive=False):
		"""
		for registro in db(db.log.evento.like('escáner%')).select():
			print registro.evento
		escáner de puertos

		Aquí "escáner%" especifica una cadena que comienza con "escáner". El signo de
		porcentaje, "%", es un signo especial o wild-card que quiere decir "toda secuencia de
		caracteres".
		"""
	def contains(lista,all=False):
		"""
		El método contains también acepta una lista de valores y un argumento opcional
		booleano all , que busca registros que contengan todos los valores de la lista:

		db.mitabla.micampo.contains(['valor1','valor2'], all=True)

		o al menos uno de los valores de la lista
		db.mitabla.micampo.contains(['valor1','valor2'], all=false)
		"""
	def regexp(self):
		"""
		similar a like pero para expresiones regulares
		"""
	def upper(self):
		pass
	def lower(self):
		pass
	def belongs(self):
		"""
		El operador de SQL IN se implementa a través del método belongs, que devuelve true
		cuando el valor del campo pertenece (belongs) al conjunto especificado (una lista o
		tupla):

		>>> for registro in db(db.log.severidad.belongs((1, 2))).select():
				print registro.event

		escáner de puertos
		secuencia de comandos en sitios cruzados
		La DAL también permite usar un comando select anidado como
		"""
		pass
	def count(self):
		pass
	def sum(self):
		"""
		Previamente, hemos usado el operador count para contar registros. En forma similar,
		puedes usar el operador sum para sumar los valores de un campo específico a partir
		de un conjunto de registros. Como en el caso de count, el resultado de una suma se
		recupera a través del objeto store:
		Create PDF in your applications with the Pdfcrowd HTML to PDF API
		PDFCROWD1
		>>> suma = db.log.severidad.sum()
		>>> print db().select(suma).first()[suma]
		"""
	def _getattrs(self):
		atributos={}
		if self.type=="upload":
			atributos["uploadfolder"]=self.uploadfolder
		atributos["name"]=self.name
		atributos["type"]=self.type
		atributos["ondelete"]=self.ondelete
		atributos["required"]=self.required
		atributos["unique"]=self.unique

		atributos["label"]=self.label
		atributos["comment"]=self.comment
		atributos["writable"]=self.writable
		atributos["autosize"]=self.autosize
		atributos["readable"]=self.readable
		atributos["notnull"]=self.notnull
		atributos["default"]=self.default
		import inspect
		atributos["compute"]=self.compute#elem.writable
		atributos["represent"]=None#elem.readable
		return atributos
	def avg(self):
		"""
		"""
	def min(self):
		"""
		"""
	def max(self):
		"""
		"""
	def len(self):
		"""
		"""
	def year(self):
		self._datetime.type="year"
		return self._datetime
	def month(self):
		self._datetime.type="month"
		return self._datetime
	def day(self):
		self._datetime.type="day"
		return self._datetime
	def hour(self):
		self._datetime.type="hour"
		return self._datetime
	def minutes(self):
		self._datetime.type="minutes"
		return self._datetime
	def seconds(self):
		self._datetime.type="segundos"
		return self._datetime

	#=================

	def isType(self,dato):
		from datetime import date,time,datetime
		import hashlib
		if self.unique:
			db=self.table.db

			row=db(db[self.table._tablename][self.name]==dato).select(stop=1)
			
			if len(row)>0 and not row[0].isEmpty():


				return False

		if self.notnull and dato==None:
			return False


		
		if type(dato)==type(hashlib.new(self.encode,"") and self.type=="password"):
			return True

		elif type(dato)==Upload and (self.type=="upload" or self.type==Upload):
			return True
		elif type(dato)==time and (self.type=="time" or self.type==time):
			return True
		elif type(dato)==Text and (self.type=="text" or self.type==Text):
			return True
		elif type(dato)==datetime and (self.type=="datetime" or self.type==datetime):
			return True
		elif type(dato)==date and  (self.type=="date" or self.type==date):
			return True
		elif type(dato)==int and (self.type=="integer"  or self.type==Integer or self.type.startswith("reference ")):
			return True
		elif type(dato)==str or type(dato)==unicode and  (self.type=="string"):
			return True
		elif type(dato)==str and dato.isdigit() and (self.type.startswith("reference ")):
			return True
		elif type(dato)==float and (self.type=="double" or self.type==float):
			return True
		elif type(dato)==dict and (self.type=="dict"  or self.type=="upload" or self.type==dict):
			#upload:{"name":"","url":"","size":0,"type":"png"}
			return True
		elif type(dato)==int and (self.type=="id"):
			return True

		elif type(dato)==bool and (self.type=="boolean" or self.type=="bool" or  self.type==bool):
			return True

		elif type(dato)==list and (self.type=="list" or self.type==list or  self.type.startswith("list:reference ")):
			return True
		elif type(dato)==str and self.type.startswith("list:reference "):
			if type(normalizar(dato))==list:
				return True
		elif dato==None:
			return True
		elif self.type=="json":
			try:
				import json
				json.dumps(dato)
				return True
			except Exception as e:
				return False
		elif self.type=="undefined" or self.type=="all" :
			
			return True
		else:
			return False

	def validate(self,valor):
		#db.persona.nombre.validate('Juan')
		#return (valor,error) error es None si pasa pasa la validacion
		pass
	def alias(self,*sinonimos):
		"""
		Este metodo nos permite encontrar una coincidencia de string mediante sinonimos del mismo
		"""
		consulta=Consulte(self,"==",sinonimos)
		consulta.alias=True
		self.db.consulta=consulta
		return consulta
	def __str__(self):
		return unicode(self._value)
	def __eq__(self,otro):
		consulta=Consulte(self,"==",otro)
		self.db.consulta=consulta
		return consulta
	def __ne__(self,otro):
		consulta=Consulte(self,"!=",otro)
		self.db.consulta=consulta
		return consulta
	def __contains__(self,otro):
		consulta=Consulte(self,"in",otro)
		self.db.consulta=consulta
		return consulta

	def __lt__(self,otro):
		consulta=Consulte(self,"<",otro)
		self.db.consulta=consulta
		return consulta
	def __le__(self,otro):
		consulta=Consulte(self,"<=",otro)
		self.db.consulta=consulta
		return consulta
	def __gt__(self,otro):
		consulta=Consulte(self,">",otro)
		self.db.consulta=consulta
		return consulta
	def __ge__(self,otro):
		consulta=Consulte(self,">=",otro)
		self.db.consulta=consulta
		return consulta
	def re(self,patron):
		consulta=Consulte(self,"regex",patron)
		self.db.consulta=consulta
		return consulta

	def update(self,attr={}):
		self.table._create_consulte()

		for elem in attr:
			self._updates.append(elem)
			_elem=attr[elem]
			if elem=="type":
				self.type=_elem #reference tabla
			elif elem=="unique":
				self.unique=_elem
			elif elem=="uploadfolder":
				self.uploadfolder=_elem
			elif elem=="ondelete":
				self.ondelete=_elem
			elif elem=="required":
				self.required=_elem
			elif elem=="label":
				self.label=_elem
			elif elem=="comment":
				self.comment=_elem
			elif elem=="autosize":
				self.autosize=_elem
			elif elem=="writable":
				self.writable=_elem
			elif elem=="readable":
				self.readable=_elem
			elif elem=="encode":
				self.encode=_elem
			elif elem=="notnull":
				self.notnull=_elem
			elif elem=="default":
				self.default=_elem


	def __str__(self):
		return "Field('"+self.name+"',type='"+unicode(self.type)+"',length="+unicode(self.length)+")"
