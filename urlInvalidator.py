'''
Implemented as a separate service can actually be done using Cron Job.
This can also be run as a service.
'''

import mysql.connector
from datetime import datetime, date
#data base connector
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="urlshortner"
)

#cursor to the database
mycursor = mydb.cursor()
date_format = "%Y-%m-%d"
while True:
    try:
        mycursor.execute('SELECT * from urls')
        urls = mycursor.fetchall()
        for url in urls:
            #can be logged to a log file
            if (datetime.strptime(datetime.today().strftime('%Y-%m-%d'), date_format)-datetime.strptime(str(url[2]), date_format)).days > 30 :
                id = url[5]
                mycursor.execute('UPDATE urls set active=0 where id=%s', (id,))
                mydb.commit()
    except:
        #log and contiunue
        print('Error occured')