import requests
import csv
import json
from requests.auth import HTTPBasicAuth
from getpass import getpass

#address = input("Enter IP Address of the FMC: ")"
#username = input ("Enter Username: ")
#password = getpass("Enter Password: ")

address = "10.71.132.226"
username = "admin"
password = "C1sco12345!"

api_uri = "/api/fmc_platform/v1/auth/generatetoken"
url = "https://" + address + api_uri

response = requests.request("POST", url, verify=False, auth=HTTPBasicAuth(username, password))

accesstoken = response.headers["X-auth-access-token"]
refreshtoken = response.headers["X-auth-refresh-token"]
DOMAIN_UUID = response.headers["DOMAIN_UUID"]

#csvFilePath = input("fmc/objects.csv")
csvFilePath = "objects.csv"

host = []

with open(csvFilePath, encoding='utf-8-sig') as csvf:
	csvReader = csv.DictReader(csvf)


	for rows in csvReader:
		if rows['type'] == "Host":
			host.append(rows)
	host_payload = json.dumps(host)

	host_api_uri = "/api/fmc_config/v1/domain/" + DOMAIN_UUID + "/object/hosts?bulk=true"
	host_url = "https://" + address + host_api_uri
	headers = {'Content-Type': 'application/json', 'x-auth-access-token': accesstoken}

	if host != []:
		response = requests.request("POST", host_url, headers=headers, data=host_payload, verify=False)
	else:
		print("Please Validate that the CSV file provided is correct or at correct location")

	if response.status_code == 201 or response.status_code == 202:
		print("Host Objects successfully pushed")
	else:
		print("Host Object creation failed")
