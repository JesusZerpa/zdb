# -*- coding: utf-8 -*-
from db import DB
from table import Table 
from field import Field
db=DB("test.db")

print db(db.prueba_table).select()
#db.commit()

"""
db.define_table("prueba_table",
	Field("id","id"),
	Field("campo_1","string"),
	Field("campo_2","integer"))

db.commit()
"""