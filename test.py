import requests
url = "https://10.10.20.48:443/restconf/data/Cisco-IOS-XE-native:native/interface/Loopback/"
headers = {'Content-Type': 'application/yang-data+json', 'Accept': 'application/yang-data+json'} 
response = requests.get(url, auth=('developer', 'C1sco12345'), headers=headers, verify=False)
print(response.text)
