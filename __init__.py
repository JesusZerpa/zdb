# -*- coding: utf-8 -*-
def send(message):
	print(message)
class ZDB(object):
	"""docstring for ZDB"""
	def __init__(self):
		super(ZDB, self).__init__()
		
		self.cline=None
		self.is_runtime=False
	def create_db(self,*args,**kwargs):
		import os
		os.mkdir(kwargs["name"])

	def process(self,instruction):
		if self.is_runtime:
			if self.cline:
				self.cline.run(instruction)


	def run(self,*args,**kwargs):
		import sys,imp 
		LineInstructions=imp.load_source("line_instructions","../line_instructions/__init__.py").LineInstructions
		self.is_runtime=True
		self.cline=LineInstructions()
		self.cline.add_directive(["con el nombre",
							 "de nombre"],lambda env,parameters:setattr(env,"db_name",parameters[0]))
		self.cline.add(["create new db",
				   "crea una nueva base de datos"],
				   lambda env:self.create_db(name=env.db_name) if "db_name" in dir(env) else send("Necesita indicar el nombre de la base de datos"))
		entrada=None
		print "ZDB console v0.0.1"
		while entrada!="salir" or entrada!="exit":
			entrada=raw_input("[consulte] ")
			self.process(entrada)


		
if __name__=="__main__":
	zdb=ZDB()
	zdb.run()