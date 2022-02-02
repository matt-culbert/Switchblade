import requests
import subprocess
import time

who = subprocess.Popen('pwd', stdout=subprocess.PIPE)
who = who.stdout.read()

headers = {'X-Transact': 'Action', 'Hello' : str(who), 'ID' : '1'}
data = {'ID' : '1'}

r = requests.post('http://localhost:8443', headers=headers, data=data)
time.sleep(20)
print('Sending GET')
a = requests.get('http://localhost:8443', headers=headers)
print(a.headers)
