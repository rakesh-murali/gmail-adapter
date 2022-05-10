import MySQLdb

class SQLClient:

  def __init__(self, host, user, password, db):
    self.dbconnect = MySQLdb.connect(host, user, password, db)
    self.cursor = self.dbconnect.cursor()

  def insert(self, table_name, field_names, args):
    query = 'insert into %s(%s, %s, %s, %s)' % (table_name, *field_names) + ' values (%s, %s, %s, %s)'
    self.cursor.executemany(query, args)
    self.dbconnect.commit()
    self.dbconnect.close()

  def delete_email(self, args):
    pass