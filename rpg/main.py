import requests

url = 'http://up.hydrax.net/f547407c3f05c55d4a8e9e5dc5358e95'

file_name = 'demo.mp4'
file_type = 'video/mp4'
file_path = './demo.mp4'
files = { 'file': (file_name, open(file_path, 'rb'), file_type) }

r = requests.post(url, files=files)
print(r.text)
print(r.text)