# local
from src.db.connection import Session


session = Session()

def truncate_table(table: str):
  session.execute('TRUNCATE TABLE {}'.format(table))
  session.commit()
  session.close()