
import requests
import json
import os

# insert your api key here
api_key = os.getenv('H_API_KEY')
url = f'https://api.hubapi.com/crm/v3/imports?hapikey={api_key}'

data = {
    "name": "hubspot",
    "files": [
        {
            "fileName": "hubspot.csv",
            "fileFormat": "CSV",
            "fileImportPage": {
                "hasHeader": True,
                "columnMappings": [
                    {
                        "ignored": False,
                        "columnName": "Name",
                        "idColumnType": None,
                        "propertyName": "name",
                        "foreignKeyType": None,
                        "columnObjectType": "COMPANY",
                        "associationIdentifierColumn": False
                    },
                    {
                        "ignored": False,
                        "columnName": "Company Domain",
                        "idColumnType": "HUBSPOT_ALTERNATE_ID",
                        "propertyName": "domain",
                        "foreignKeyType": None,
                        "columnObjectType": "COMPANY",
                        "associationIdentifierColumn": False
                    }
                ]
            }
        }
    ]}

datastring = json.dumps(data)

payload = {"importRequest": datastring}

with open("files/hubspot.csv", "r") as file:
    files = [('files', file)]
    response = requests.request("POST", url, data=payload, files=files)
    response_dict = response.json()

print(json.dumps(response_dict, indent=4))
print(response.status_code)