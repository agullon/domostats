import sqlite3, datetime 
import temperature, domostats, hue_requests

db = None
DATABASE_NAME = 'domostats.db'

def create_temperature_table():
      db = sqlite3.connect(DATABASE_NAME)
      db.execute('''
            CREATE TABLE
            IF NOT EXISTS
            TEMPERATURE(
                  ROOM TEXT NOT NULL,
                  TEMP REAL NOT NULL,
                  DATE DATE NOT NULL
            );
      ''')      
      db.commit()
      db.close()

def insert_temperature_table(room, temp, date):
      db = sqlite3.connect(DATABASE_NAME)
      db.execute('''
                  INSERT INTO TEMPERATURE (ROOM,TEMP,DATE)
                  VALUES ("'''+room+'''",'''+str(temp)+''',"'''+date+'''")
            ''')
      db.commit()
      db.close()

def add_temperature(room, temp, date):
      if (not room or not temp or not date):
            print('ERROR: data not inserted on db')
            return

      create_temperature_table()
      insert_temperature_table(room, temp, date)

def print_db_last_rows(num_rows=-1):
      db = sqlite3.connect(DATABASE_NAME)
      cursor = db.execute('''
            SELECT * from TEMPERATURE 
            ORDER BY DATE DESC
            LIMIT ''' + str(num_rows))
      print('ROOM|TEMP|DATE')
      for row in cursor:
            print(row[0]+'|'+str(row[1])+'|'+row[2])
      db.close()

def read_temperature(hours=24, room='%'):
      date = datetime.datetime.now() - datetime.timedelta(hours=hours)
      try:
            db = sqlite3.connect(DATABASE_NAME)
            cursor = db.execute('\
                  SELECT * from TEMPERATURE \
                  WHERE date > "{}" \
                  AND ROOM LIKE "{}" \
                  LIMIT -1'.format(date, room))
            return cursor.fetchall()
      finally:
            db.close()
      
if __name__ == '__main__':
      hue_requests.set_endpoint()
      temp, date = temperature.get_room_info(domostats.BEDROOM)
      add_temperature(domostats.BEDROOM, temp, date)
      temp, date = temperature.get_room_info(domostats.KITCHEN)
      add_temperature(domostats.KITCHEN, temp, date)
      print_db_last_rows(4)