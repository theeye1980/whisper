from classes.bd import bdSQLite

db = bdSQLite()

db.export("speakers")
db.export("text_autotrans")