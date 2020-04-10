import Run_Linux
db=Run_Linux.PostgresDB()
print(db.createTable('mautd'))
db.close()


