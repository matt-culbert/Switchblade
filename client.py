import requests
import subprocess

who = subprocess.Popen('pwd', stdout=subprocess.PIPE)
who = who.stdout.read()

headers = {'X-Transact': 'Action', 'Hello' : str(who)}
r = requests.get('http://localhost:8080', headers=headers)
