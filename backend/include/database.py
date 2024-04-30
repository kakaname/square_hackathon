import sqlite3

def get_connection():
  return sqlite3.connect("data.db")

def check_table_exists():
  con = get_connection()
  cur = con.cursor()
  res = cur.execute("SELECT name FROM sqlite_master")
  if res.fetchone() == None:
    con.close()
    return False
  else:
    con.close()
    return True

def create_table():
  con = get_connection()
  cur = con.cursor()
  cur.execute("CREATE TABLE payments(giftcard, total)")
  con.close()

def remove_table():
  con = get_connection()
  cur = con.cursor()
  cur.execute("DROP TABLE payments")
  con.close()

def display_all():
  con = get_connection()
  cur = con.cursor()
  res = cur.execute("SELECT * FROM payments")
  con.close()
  print("displaying all elements :", res.fetchall())

def fetch_all():
  con = get_connection()
  cur = con.cursor()
  cur.execute("SELECT giftcard, total FROM payments")
  payments = [{'giftcard' : row[0], 'total' : row[1]} for row in cur.fetchall()]  
  return payments

def record_data(value, service):
  con = get_connection()
  cur = con.cursor()
  if not check_table_exists():
    create_table()
  body = f'INSERT INTO payments VALUES ({value}, {service})'
  cur.execute(body) 
  con.commit()
  con.close()

  display_all()



