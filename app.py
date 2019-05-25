from flask import Flask, request
import json
import uuid
import mysql.connector
from datetime import datetime
#data base connector
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="urlshortner"
)

#cursor to the database
mycursor = mydb.cursor()


app = Flask(__name__)


'''
This end point accepts the original long URL.
It first checks whether the URL already exists in database and is active the just tells that the URL already exists in database and returns the short url.
If the URL exists in data base and is active it updates its status to active and returns the short url.
If the URL is not in data base it generates a short url and inserts the record into the database and returns the short url.
It also stores the params in the URL to be used while getting the orignal url anb making the url dynamic.(Bonus task)
'''
@app.route('/getShort', methods=['POST'])
def getShort():
    longurl = request.form['long_url']
    if '.' not in longurl: #basic test to validate URL
        return json.dumps({'status':'Failed', 'msg':'Kindly give a valid URL'}) 
    #temp = longurl.split("?")[1].split('&')
    #params = [x.split("=")[0] for x in temp]
    #print(params)
    results = None
    try:    
        mycursor.execute("SELECT * FROM urls where original=%s", (longurl, ))
        results = mycursor.fetchall()
    except:
        return json.dumps({'status':'Failed','msg':'Some error in database, try again'})
    if len(results) == 0:
        short_url = 'https://vokal.com/' + str(uuid.uuid1())[:7]
        id = None
        try:    
            mycursor.execute("INSERT INTO urls(original, short_url, last_used, visits, active) values(%s, %s, %s, %s, %s)", (longurl, short_url, datetime.today().strftime('%Y-%m-%d'), 0, 1))
            mydb.commit()
            #mycursor.execute("SELECT id FROM urls where original=%s", (longurl, ))
            #id = mycursor.fetchone()[0]
            #for i in params:
            #    mycursor.execute("INSERT INTO params(id, param) values(%s, %s)", (id, i))
            #    mydb.commit()
            return json.dumps({ 'status':'success','short_url': short_url, 'msg':'Created short url and inserted in database'})
        except:
            return json.dumps({'status':'Failed','msg':'Some error in database, try again'})
        #print(id)
        
    else:
        if int(results[0][4])==0:
            #update to active
            try:
                mycursor.execute("update urls set active=1, last_used=%s where original=%s", (datetime.today().strftime('%Y-%m-%d'), longurl))
                mydb.commit()
                return json.dumps({'status':'success', 'short_url': results[0][1], 'msg':'Updated the the link to active'})
            except:
                return json.dumps({'status':'Failed','msg':'Some error in database, try again'})
        return json.dumps({'status':'success', 'short_url': results[0][1], 'msg':'Already exists in data base'})


'''
This endpoint is called when a the original URL is required from the short URL.
It first checks whether thre URL exists in database and is active if so return the long URL.
If not active return the status not acitve.
If dosen't exist in data base return status dosen't exist. 
'''
@app.route('/getLong', methods=['POST'])
def getLong():
    shorturl = request.form['short_url'].split('?')
    tokenValues = []
    if len(shorturl) >1:
        l = shorturl[1].split('&')
        tokenValues = [x.split('=')[1] for x in l]
    shorturl = shorturl[0] 
    if '.' not in shorturl: #basic test to validate URL
        return json.dumps({'status':'Failed', 'msg':'Kindly give a valid URL'})
    results = None
    try:
        mycursor.execute("SELECT * FROM urls where short_url=%s", (shorturl, ))
        results = mycursor.fetchall()
    except:
        #print("yaha phata")
        return json.dumps({'status':'Failed','msg':'Some error in database, try again'})
    if len(results) == 0:
        return json.dumps({'status':'Failed', 'msg':"Short URL dosen't exist in database."})
    if results[0][4] == 0:
        return json.dumps({'status':'Failed', 'msg':"Short URL inactive kindly activate it."})
    try:
        mycursor.execute("update urls set  last_used=%s, visits=%s where short_url=%s ", (datetime.today().strftime('%Y-%m-%d'), int(results[0][3])+1, shorturl))
        mydb.commit()   
        longurl = results[0][0]
        if len(tokenValues) == 0:
            return json.dumps({'status':'Success', 'long_url':longurl, 'msg':'Last date and visits updated'})
        temp = longurl.split("?")[1].split('&')
        params = [x.split("=")[0] for x in temp]
        longurl = longurl.split('?')[0]
        queryString = ""
        for i in range(len(tokenValues)):
            if(i>0):
                queryString += '&'
            queryString += params[i] + "=" + tokenValues[i]
        longurl += "?" + queryString
        return json.dumps({'status':'Success', 'long_url':longurl, 'msg':'Last date and visits updated and query sting dynamically generated'})
    except:
        return json.dumps({'status':'Failed','msg':'Some error in database, try again'})


if __name__ == "__main__":
    app.run(port=5280, debug=True)


