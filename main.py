import sql_functions as sqlf

#sqlf.add_user('Bruker1', '123')
print(sqlf.check_password('Bruker1', '123'))
sqlf.close()
