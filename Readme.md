URL Shortner-

Implemented as an API based service.
Tech used - 
Python, Flask, MySQL.

MySQL's SQL file is included which can be used to create and get the database up and running for testing.

Features with both the Bonus points are implemented.

Two endpoints are -
/getShort

Accepts a long url as input (input- "long_url")
It checks if the URL already exists in database and is active if so returns the short url.'
If inactive activates the url and sends the short url from database.
If dosen't exist in database short url is created and inserted into database.

Output format(JSON) -
{'status':'success/Failed', 'short_url':'if error ocuurs this field is not present', 'msg':'stating what happened during the execution'}

/getLong

Accepts the short url as input (input - "short_url")
It checks if the URL exist in database if not returns failed.
If exist but is inactive returns inactive.
If active returns the URL by considering the params if exist dynamically.
Updates the last date viewed and visits.

Output fromat(JSON) -
{'status': 'success/Failed', 'long_url':'if error occurs this field is not present', 'msg':'stating what happened during the execution'}

URL invalidator - 
 Checks which URL hasn't been used for more than 30 days and sets them as inactive.


DataBase -

Table urls -
__________________________________________________________
| id | original | short_url | last_used | visits | active |
```````````````````````````````````````````````````````````
