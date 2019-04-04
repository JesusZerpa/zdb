# -*- coding: utf-8 -*-
from db import DB
from table import Table 
from field import Field
db=DB("test.db")
#print db(db(db.prueba_table.campo_1=="la que sigue") & ).select()
"""
db.define_table("prueba_table",
	Field("id","id"),
	Field("campo_1","string"),
	Field("campo_2","integer"))
"""
db.prueba_table.insert(None,"la que sigue3",300)
db.prueba_table.insert(None,"la que sigue4",300)


db.commit()