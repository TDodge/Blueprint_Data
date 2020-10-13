import json
import urllib.request
import sqlite3

# website: https://sec-api.io/profile
# tutorial: https://medium.com/@jan_5421/sec-edgar-api-2-b2cfb82c1d9e
TOKEN = "5309a6018a99228cb0c8e8c88ec594d6fefcc3e30ff65808248bb1b1985a7c52"
API = "https://api.sec-api.io?token=" + TOKEN

# define the filter parameters you want to send to the API 
payload = {
  "query": { "query_string": { "query": "filedAt:{2020-01-01 TO 2020-10-10} AND formType:\"S-1\"" } },
  "from": "0",
  "size": "10000",
  "sort": [{ "filedAt": { "order": "desc" } }]
}

# format your payload to JSON bytes
jsondata = json.dumps(payload)
jsondataasbytes = jsondata.encode('utf-8')   # needs to be bytes

# instantiate the request 
req = urllib.request.Request(API)

# set the correct HTTP header: Content-Type = application/json
req.add_header('Content-Type', 'application/json; charset=utf-8')
# set the correct length of your request
req.add_header('Content-Length', len(jsondataasbytes))
# send the request to the API
response = urllib.request.urlopen(req, jsondataasbytes)
# read the response 
res_body = response.read()
# transform the response into JSON
filings = json.loads(res_body.decode("utf-8"))

# SQLite connection
conn = sqlite3.connect('/Users/thomasdodge/Desktop/PythonProjects/BlueprintData/s1/edgar.sqlite')
cur = conn.cursor()
cur.execute("""DROP TABLE IF EXISTS s1_api""")
cur.execute("""CREATE TABLE s1_api(accessionNo text, cik text, ticker text, 
	companyName text, formType text, filedAt text, linkToHtml text, irsNo text, sic text )""")

# count = 1
for filing in filings['filings']:
# 	count = count + 1
# 	print(count)

	try:
		accessionNo = filing['accessionNo']
		cik = filing['cik']
		ticker = filing['ticker']
		companyName = filing['companyName']
		formType = filing['formType']
		filedAt = filing['filedAt']
		linkToHtml = filing['linkToHtml']
		irsNo = filing['entities'][0]['irsNo']
		sic = filing['entities'][0]['sic']
	except KeyError:
		continue

	cur.execute("""INSERT INTO s1_api values (?,?,?,?,?,?,?,?,?)""", (accessionNo, cik, ticker, 
		companyName, formType, filedAt, linkToHtml, irsNo, sic))

conn.commit()
