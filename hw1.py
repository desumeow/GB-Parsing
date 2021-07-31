import requests
import os
import json

username = 'desumeow'

token = os.environ.get('GITHUB_TOKEN')

r = requests.get('https://api.github.com/user/repos', auth=(username, token))
data = r.json()

with open('git_repos.json', 'w') as f:
    json.dump(data, f)

for i in r.json():
    print(i['name'])