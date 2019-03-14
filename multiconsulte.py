# -*- coding: utf-8 -*-
from table import Table
from set import Set
class MultiConsulte(object):
	"""
	Este es para los casos (consulte|consule) & consulte
	"""
	def __init__(self,db,consulte):
		super(MultiConsulte, self).__init__()
		self.consultas=[consulte]
		self.db=db
		if type(consulte)==Table:
			self.table=consulte
		else:
			self.table=consulte.table
		self.content=[]
		self.referencias=[]

		self.c=0
	def __getitem__(self,x):
		return self.content[x]
	def next(self):
		
		if self.c<len(self.content):

			x=self.c
			self.c+=1

			return self.content[x]

		else:
			raise StopIteration
	def select(self,*args,**kwargs):
		return Set(self.db,self).select(*args,**kwargs)
	def __and__(self,consulta):

		self.consultas.append("and")
		self.consultas.append(consulta)
		self.table=consulta.table


		return self
	def __len__(self):
		return len(self.content)


	def __or__(self,consulta):
		self.consultas.append("or")
		self.consultas.append(consulta)
		self.table=consulta.table
		return self
	def _evaluar(self,campos):
		"""
		evalua si se cumpen todas las consultas adjuntas
		"""
		
		consulta=False
		operador=None
		
		for k,elem in enumerate(self.consultas):

			if type(elem)==str and elem=="and":
				operador="and"

			elif type(elem)==str and elem=="or":
				operador="or"
			else:
				#es una consulta

				if operador=="and":
					elem.evaluate()
						
				else:

					_consulta=elem.evaluate()
					

					if not consulta and (operador=="or" or  operador==None):

						consulta=_consulta




		
		return consulta
	def __call__(self):
		#multiconsulte
		import re

		c=self.start
		
		table=self.table
		finds=0
		if table.cursor>0:
			for c in xrange(table.cursor):

				try:

					if table[c]:

						if self._evaluar(table[c]):

							if self.startfind!=None:

								if finds>=self.startfind and ((self.stopfind!=None and finds<=self.stopfind) or self.stopfind==None):
									self.content.append((table._tablename,c ))
									finds+=1
							else:

								self.content.append((table._tablename,c))
						
						c+=self.step
						if type(self.end)==int and  c>=self.end:
							break

				except Exception as e:
					print e

		
		return self
