import requests

resp = requests.post("http://localhost:5000/", files={'file': open('data.json')})
print(resp.json())
