import requests
import json

url = "https://api.twitter.com/2/tweets/search/recent?query=bali"

payload = {}
headers = {
    'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAAMrIcAEAAAAACpbBIoX2XivfGvPXDjjIxYkbebM%3D9U1MF8cDjAtzEnqpIkO6cQiephCUL5Ra2MKR0oCXwGhcoAEUT3'
}

response = requests.request("GET", url, headers=headers, data=payload)

# print(response.text)

f = open("demofile2.txt", "a")
f.write(response.text)
f.close()

# aa = json.loads(response.text)
# print(aa['meta'])
