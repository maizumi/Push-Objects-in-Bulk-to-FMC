import requests
import csv
import json
from requests.auth import HTTPBasicAuth
from getpass import getpass
import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, session
from werkzeug.utils import secure_filename

#address = input("Enter IP Address of the FMC: ")"
#username = input ("Enter Username: ")
#password = getpass("Enter Password: ")

app = Flask(__name__)

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['csv'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET'])
def login():
    return render_template("index.html")

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/send', methods=['GET', 'POST'])
def send():
    if request.method == 'POST':
        csv_file = request.files['csv_file']
        if csv_file and allowed_file(csv_file.filename):
            filename = secure_filename(csv_file.filename)
            csv_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #csv_url = '/uploads/' + filename
            csv_url = app.config['UPLOAD_FOLDER'] + '/' + filename
            abspath  = os.path.abspath(filename)
            #print(csv_url)
            #print(abspath)
            
            fmc_ip = request.form.get('fmc_ip')
            fmc_username = request.form.get('fmc_username')
            fmc_password = request.form.get('fmc_password')
         
            #address = "10.71.132.226"
            #username = "admin"
            #password = "C1sco12345!"
            address = fmc_ip
            username = fmc_username
            password = fmc_password
                        
            api_uri = "/api/fmc_platform/v1/auth/generatetoken"
            url = "https://" + address + api_uri
            
            response = requests.request("POST", url, verify=False, auth=HTTPBasicAuth(username, password))
            
            accesstoken = response.headers["X-auth-access-token"]
            refreshtoken = response.headers["X-auth-refresh-token"]
            DOMAIN_UUID = response.headers["DOMAIN_UUID"]
            
            #csvFilePath = input("fmc/objects.csv")
            csvFilePath = csv_url
            
            host = []
            network = []
            nwrange = []
            
            with open(csvFilePath, encoding='utf-8-sig') as csvf:
            	csvReader = csv.DictReader(csvf)
            	
            	for rows in csvReader:
            		if rows['type'] == "Host":
            			host.append(rows)
            			host_payload = json.dumps(host)
            		
            		if rows['type'] == "Network":
            			network.append(rows)
            			network_payload = json.dumps(network)

            		if rows['type'] == "Range":
            			nwrange.append(rows)
            			nwrange_payload = json.dumps(nwrange)
            	         			            		            	
            	host_api_uri = "/api/fmc_config/v1/domain/" + DOMAIN_UUID + "/object/hosts?bulk=true"
            	host_url = "https://" + address + host_api_uri
            	
            	network_api_uri =  "/api/fmc_config/v1/domain/" + DOMAIN_UUID + "/object/networks?bulk=true"
            	network_url = "https://" + address + network_api_uri
            	
            	nwrange_api_uri =  "/api/fmc_config/v1/domain/" + DOMAIN_UUID + "/object/ranges?bulk=true"
            	nwrange_url = "https://" + address + nwrange_api_uri
            	            	
            	headers = {'Content-Type': 'application/json', 'x-auth-access-token': accesstoken}            	
            	
            	#print(host_payload, network_payload, nwrange_payload)            	
            	
            	if host != []:
            		response = requests.request("POST", host_url, headers=headers, data=host_payload, verify=False)
            		
            		if network != []:
            		    response = requests.request("POST", network_url, headers=headers, data=network_payload, verify=False)
            		    
            		    if nwrange != []:
            		        response = requests.request("POST", nwrange_url, headers=headers, data=nwrange_payload, verify=False)
            		            		
            	else:
            		print("Please Validate that the CSV file provided is correct or at correct location")
            	
            	if response.status_code == 201 or response.status_code == 202:
            		print("Host Objects successfully pushed")
            	else:
            		print("Host Object creation failed")

            return render_template('index.html', csv_url=csv_url)
        else:
            return ''' <p>許可されていない拡張子です</p> '''
    else:
        return redirect(url_for('index'))
        
if __name__ == '__main__':
    app.debug = True
    app.run()
