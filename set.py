# -*- coding: utf-8 -*-
from row import Row

class Set(object):
	"""docstring for Set"""
	def __init__(self,db,consulta=None):
		class Content(set):
			"""docstring for Content"""
			def __init__(self, valor,_set):
				self._value=valor
				self.set=_set
			def __str__(self):
				return unicode(self._value)
			def __or__(self,otro):
				if self._value==set():
					self._value=set(self.set.rows)

				return self._value | otro
			def add(self,nuevo):
				return self.set.rows.append(nuevo)


		super(Set, self).__init__()
		self.db = db
		self.consulta=consulta
		self._content=Content(set(),self)
		self.rows=[]#lo uso para tener un orden por indice en lugar de content
		self.c=0
		self.length=None#para uso de row listas
		self.referencias=[]
		self.part=None
		self.consultada=None
		self.c2=0






	def select(self,orderby=None , groupby=None , limitby=None , distinct=None , having=None,cache=None, cacheable=False,stop=None,#stop es hasta cuantas iteraciones de busqueda esta permitido
		start=0,end=None,step=1,jump=0,repeat=0,
		startfind=None,#startfind empieza a contar un contador a partir del primer resultado valido de la consulta
		stopfind=None,#stopfind detiene la consulta hasta tantos elementos encontrados en ella
		invert=False,
		*campos):#stop es un args propio de zdb e indica despues de cuantas conincidencia detiente el recorrido
		"""
		personalizados

		start = id del registro desde donde se empieza la busqueda de la consulta
		step = saltos que da el cursor de registros entre el rango start y end
		end = id final del registro en el rango de busqueda
		stop =  maximo de registros encontrados en un rango
		jump = saltos que da el cursor de registros despues de un stop
		repeat = numero de veces que se repetira el stop, acompaña a jump

		transforma una consulta para retornar
			Rows

			select(campos a recuperar)
			ejemplo:
			select(db.campo.)

			orderby , groupby , limitby , distinct , having


			having=consulta2

			A efectos de utilizar el caché, se debería especificar una tupla donde el primer elemento
			es el modelo de caché (cache.ram, cache.disk, etc.), y el segundo elemento es plazo
			de vencimiento en segundos.

			cache=(cache.ram,60))

			El método select
			acepta un argumento opcional llamado
			cacheable , que
			normalmente es False .
			Si se ha establecido la opción cacheable=False (por defecto) sólo se hara un caché
			de los resultados de la base de datos, pero no del objeto Rows en sí.

		"""

		self.consulta.stop=stop
		self.consulta.start=start
		self.consulta.end=end
		self.consulta.step=step
		self.consulta.startfind=startfind
		self.consulta.stopfind=stopfind
		self.invert=invert

		
		self.consultada=self.consulta()

		self.db.consulta=self
		
		
		#self.db.cache=[tabla,campo,operador,campo2,rows]
		#despues de 60 segundos esta cache se elimina
		#db(consulta).select(cache=(cache.ram, 3600), cacheable=True)

		if type(self.consultada)!=list:

			if self.consultada.referencias!=[]:
				self.referencias=self.consultada.referencias

		"""
		#prueba
		for elem in self.consultada:
			if type(elem[1])==int:
				self.rows.append(elem)
			else:
				for elem2 in range(elem[1][0],elem[1][1],elem[1][2]):
					self.rows.append((elem[0],elem2))
		"""
		"""
		if "rows" in self.consulta:
			del self.consulta.rows
		if "content" in self.consulta:
			del self.consulta.content
		del self.consulta
		"""


		return self

	def as_list(self,skip=None,replace={},filters={},tableZDB=None):
		"""
		No implementado en pydal, uso propio de ZDB

		*tableZDB permite colocar el indice statico al principo ejemplo
		["Usuario",0]


		"""
		l=[]

		for _set in self:
                    if _set!=None:
        		l.append(_set.as_list(skip=skip,replace=replace,filters=filters,tableZDB=tableZDB))
		self.db.consulta=l
		return l
	def as_dict(self,filters={}):
		d=[]
		for elem in self:
			d.append(elem.as_dict(filters=filters))
		return d




	def __getitem__(self,indice):
		
		
		if type(indice)==int:
			before_length=0

			
			for c,elem in enumerate(self.consultada):
				#si es un solo registro simple			
				
				if type(elem[1])==int:

					#self.rows.append(elem)
					
					before_length+=1
					

					if indice>=0 and indice==c:
						

						row=Row(self.db[elem[0]],elem[1])
						row.referencias=self.referencias
						row.part=self.part
						self.db.consultada=row

						return row
						break
					elif indice<0 and indice==-c-1:
						
						row=Row(self.consultada[indice],self.db)
						row.referencias=self.referencias
						row.part=self.part
						self.db.consultada=row


						return row
						break
					

				else:#si es un grupo de registros
					start=elem[1][0]
					end=elem[1][1]
					step=elem[1][2]
					#en caso de que el final no fuese definido

					if end==None:
						
						end=len(self.db.tableobjects[elem[0]])
					c2=0
					
					for i in xrange(start,end+1,step):
						
						
						if before_length+c2==indice:

							row=Row((elem[0],i if not self.invert else -i-1),self.db)
							row.referencias=self.referencias
							row.part=self.part
							self.db.consultada=row
							before_length+=end-start

							
							return row
						
						c2+=1
					
										
		if type(indice)==slice:
			l=[]
			c=0
			
			for elem in self.consultada:
				if type(elem[1])==int:
					#self.rows.append(elem)

					if (indice.start<c and c<indice.stop) or (indice.start==c or c==indice.stop):

						row=Row(self.rows[indice],self.db)
						row.referencias=self.referencias
						row.part=self.part
						l.append(row)
					c+=indice.step


				else:

					for i in xrange(elem[1][0],elem[1][1],elem[1][2]):
						#self.rows.append((elem[0],elem2))

						if (indice.start<c and c<indice.stop) or (indice.start==c or c==indice.stop):

							row=Row((elem[0],i),self.db)
							row.referencias=self.referencias
							row.part=self.part
							l.append(row)
						else:
							break

						c+=indice.step
			self.db.consultada=l
			return l





	def __setitem__(self,clave,valor):
		for row in self.rows:
			for x,campo in  enumerate(self.db.tableobjects[row[0]].rows[row[1]]):
				self.db.tableobjects[row[0]].rows[row[1]][x]


	def __iter__(self):
		"""
		type:Set
		aqui no es consulta.start puesto que esto es el inicio los elementos en la consulta no el de los registros de la tabla
		"""
		self.c=0#grupo actual



		return self
	def getEmptys(self):
		pass
	
	def getLength(self):
		"""
		Retorna la cantidad de registros en la consulta
		"""

		
		if self.length==None:
			c=0

			for elem in self.consultada:

				
				if type(elem[1])==int:
					#self.rows.append(elem)
					c+=1


				else:

					end=elem[1][1]

					if end==None:

						end=len(self.db.tableobjects[elem[0]])
					i=float(end-elem[1][0])/float(elem[1][2])
					c+=int(i)



					"""	
					#-----------------------------			
					#pendiente de revicion

					for i in xrange(elem[1][0],end,elem[1][2]):
						#self.rows.append((elem[0],elem2))	
						print i
						
						if not self[i].isEmpty():
							c+=1
					#-----------------------------
					"""

			self.length=c
		return self.length
		
	def __len__(self):
		"""
		type:Set
		Esta longitud corresponde a la logitud de registros en la consulta
		"""
		self.c=0
		return len(self.consultada)

		

	def next(self):
		
		x=self.c
		
		if self.c<self.getLength():
			try:
				a=self[x if not self.invert else -x-1]
				self.c+=1
				return a
			except:
				self.c+=1
				self.next()
		
		else:			
			raise StopIteration

		"""
		self.consultada
		if self.c<len(self.rows):
			x=self.c
			self.c+=1

			row=Row(self.rows[x],self.db)
			row.table=self.db.tableobjects[self.rows[x][0]]
			row.referencias=self.referencias


			return row

		else:

			raise StopIteration
		"""


	def update(self,**kwargs):

		for k2,row in enumerate(self.rows):
			for k,campo in self.table._fields:
				for ncampo in kwargs:
					if campo.name==ncampo:
						row[k]=kwargs[ncampo]
						break
					else:
						row[k]=None
						break





	def delete(self):
		"""
		elimina un registro(filea) por su id
		"""
		return [elem.delete() for elem in self]




	def count(self):
		return len(self.rows)
	def __str__(self):
		import json
		content=""
		for row in self:

			for k,campo in enumerate(row.table.fields):
				content+=json.dumps(row[k])+("," if k<len(row.table.fields)-1 else "")
			content+="\n"

		return content
