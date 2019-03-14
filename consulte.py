


class Consulte(object):
	"""docstring for Consulta"""
	def __init__(self,a,operador,b):

		super(Consulte, self).__init__()
		self.rows=[]
		self.a=a#campo | consultas
		self.operador=operador
		self.b=b#valor | consultas
		self.content=[]
		self.stop=None
		self.referencias=[]
		self.alias=False
		self.consultas=[]#para las consultas que esten relacionadas or and
		self.startfind=None
		self.stopfind=None
		self.table=a.table
		
		"""
		(consulta1) and (consulta2) or (consulta3)
		self.consutas=["and",consulta2,"or",consulta3]

		"""

		self._timings=0#cronometro de la consulta
	
	def __str__(self):

		return "Consulte("+"["+self.a.db.dbfile+"]"+"["+self.a.table._tablename+"]"+"["+self.a.name+"]"+self.operador+unicode(self.b)+")["+unicode(len(self.content))+"]"
	def __iter__(self):
		self.c=0

		return self
	def __len__(self):
		return len(self.content)
	#cuando se opera entre consulta
	def __eq__(self,otro):# ==
		return self
	def __and__(self,consulta):

		self.consultas.append("and")
		self.consultas.append(consulta)

		return self

	def __or__(self,consulta):
		self.consultas.append("or")
		self.consultas.append(consulta)
		return self

	def __add__(self,otro):# +
		"""
		fusiona las consultas
		"""
		return self
	def _evaluar(self,campos):
		"""
		evalua si se cumpen todas las consultas adjuntas
		"""
		def compare(a,operador,b):
			
			if operador=="==":
				if type(b)==Reference:
					return a==b.ids
				else:

					return a==b
			elif operador=="!=":				
				return a!=b
			elif operador==">=":
				return a>=b
			elif operador=="<=":
				return a<=b
			elif operador==">":
				return a>b
			elif operador=="<":
				return a<b
			elif operador=="!=":
				return a!=b
			elif operador=="regex":
				return bool(re.findall(b,a))
			elif operador=="type":
				return bool(a.isType(b))
			elif operador=="len":
				return bool(a.length==b)
			elif operador=="in":
				return a in b


		if campos==[None for i in xrange(len(campos))]:
			return False

		index=self.a.table.fields.index(self.a.name)-1
		consulta=compare(campos[index],self.operador,self.b)
		

		operador=None
		
		
		

		#["and",consulte...]

		for k,elem in enumerate(self.consultas):
			

			if type(elem)==str and elem=="and":
				operador="and"

			elif type(elem)==str and elem=="or":
				operador="or"
			else:
				#es una consulta

				index=self.a.table.fields.index(elem.a.name)-1
				if operador=="and": #consulte & ( field==field)
					consulta=compare(campos[index],elem.operador,elem.b)

					if not consulta:
						return False

				else:
					_consulta=compare(campos[index],elem.operador,elem.b)

					if not consulta and _consulta:

						consulta=_consulta
						



		
		return consulta
