import json
import urllib.request
import sqlite3

# website: https://sec-api.io/profile
# tutorial: https://medium.com/@jan_5421/sec-edgar-api-2-b2cfb82c1d9e
TOKEN = "5309a6018a99228cb0c8e8c88ec594d6fefcc3e30ff65808248bb1b1985a7c52"
API = "https://api.sec-api.io?token=" + TOKEN

# SQLite connection
conn = sqlite3.connect('/Users/thomasdodge/Desktop/PythonProjects/BlueprintData/s1/edgar.sqlite')
cur = conn.cursor()

## Uncomment below to CREATE and/or DROP table prior to inserting data
# cur.execute("""DROP TABLE IF EXISTS s1_api_test_2""")
# cur.execute("""CREATE TABLE s1_api_test_2(accessionNo text, cik text, ticker text, companyName text, formType text, 
# 	filedAt text, linkToHtml text, linkToFilingDetails text, irsNo text, sic text )""")

# To be used in "from" field in payload dict
frm = 0

for i in range(40):
	# Prints to terminal for QA purposes
	print("From field value: ", frm)
	print('\n')

	# Define the filter parameters you want to send to the API. 
	# Size limit = 200 so need to create loop that adds 200 to from field and resend API request to capture all results
	payload = {
	  "query": { "query_string": { "query": "filedAt:{2010-01-01 TO 2011-03-17} AND formType:\"S-1\"" } },
	  "from": str(frm),
	  "size": "200",
	  "sort": [{ "filedAt": { "order": "desc" } }]
	}

	# Prints to terminal for QA purposes
	print(payload)
	print('\n')

	# Format your payload to JSON bytes
	jsondata = json.dumps(payload)
	jsondataasbytes = jsondata.encode('utf-8')   # needs to be bytes

	# Increase frm var by 200 for request in next loop
	frm += 200

	## Below block prepares API request and transfroms response into usable format
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

	## Loops through each filings response from API
	for filing in filings['filings']:

		try:
			accessionNo = filing['accessionNo']
			cik = filing['cik']
			ticker = filing['ticker']
			companyName = filing['companyName']
			formType = filing['formType']
			filedAt = filing['filedAt']
			linkToHtml = filing['linkToHtml']
			linkToFilingDetails = filing['linkToFilingDetails']
			irsNo = filing['entities'][0]['irsNo']
			sic = filing['entities'][0]['sic']
		except KeyError:
			continue

		if formType == "S-1":

			cur.execute("""INSERT INTO s1_api_test_2 values (?,?,?,?,?,?,?,?,?,?)""", (accessionNo, cik, ticker, 
			companyName, formType, filedAt, linkToHtml, linkToFilingDetails, irsNo, sic))

		else:
			continue 


conn.commit()
