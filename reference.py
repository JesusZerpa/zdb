
class Reference(object):
	def __init__(self,tabla,ids):
		self.tabla=tabla
		self.ids=ids
	def __getitem__(self,campo):



		if type(self.ids)==int:
			db=self.tabla.db
			table=self.tabla
			
			return db(table[table.getPrimaryKey()]==self.ids).select(stop=1)[0][campo]
			"""
			else:
				return self.tabla[self.ids][campo]
			"""
		else:
			l=[]
			for _id in self.ids:
				l.append(self.tabla[_id])
			return l[campo]

		"""
		if type(ids)==list:#uno a muchos
			db=self.tabla.db
			db(self.tabla[campo]==ids)
			return self.tabla[campo]
		elif type(ids)==int:#uno a uno
			return db(self.tabla[campo]==self.tablaReferida["id"])
		"""

	def __str__(self):

		if type(self.ids)==int:
			return unicode(self.tabla[self.ids])
		else:
			l=[]
			if self.ids!=None:
				for _id in self.ids:
					l.append(self.tabla[_id])

			return unicode(l)
