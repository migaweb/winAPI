import ctypes
from ctypes.wintypes import HANDLE, DWORD, LPSTR, WORD, LPBYTE

k_handle = ctypes.WinDLL("Kernel32.dll")

# https://docs.microsoft.com/en-us/windows/win32/api/processthreadsapi/ns-processthreadsapi-startupinfoa
class STARTUPINFO(ctypes.Structure):
    _fields_ = [
        ("cb", DWORD),
        ("lpReserved", LPSTR),
        ("lpDesktop", LPSTR),
        ("lpTitle", LPSTR),
        ("dwX", DWORD),
        ("dwY", DWORD),
        ("dwXSize", DWORD),
        ("dwYSize", DWORD),
        ("dwXCountChars", DWORD),
        ("dwYCountChars", DWORD),
        ("dwFillAttribute", DWORD),
        ("dwFlags", DWORD),
        ("wShowWindow", WORD),
        ("cbReserved2", WORD),
        ("lpReserved2", LPBYTE),
        ("hStdInput", HANDLE),
        ("hStdOutput", HANDLE),
        ("hStdError", HANDLE),
    ]


class PROCESS_INFORMATION(ctypes.Structure):
    _fields_ = [
        ("hProcess", HANDLE),
        ("hThread", HANDLE),
        ("dwProcessId", DWORD),
        ("dwThreadId", DWORD)
    ]


lpApplicationName = 'C:\\Windows\\System32\\cmd.exe'
lpCommandLine = None
lpProcessAttributes = None
lpThreadAttributes = None
lpEnvironment = None
lpCurrentDirectory = None

dwCreationFlags = 0x00000010  # CREATE_NEW_CONSOLE
bInheritHandle = False
lpProcessInformation = PROCESS_INFORMATION()  # Receives identification info

lpStartupInfo = STARTUPINFO()
lpStartupInfo.wShowWindow = 0x1  # Need to set flags also
lpStartupInfo.dwFlags = 0x1  # Look at showWindow

response = k_handle.CreateProcessW(
    lpApplicationName,
    lpCommandLine,
    lpProcessAttributes,
    lpThreadAttributes,
    bInheritHandle,
    dwCreationFlags,
    lpEnvironment,
    lpCurrentDirectory,
    ctypes.byref(lpStartupInfo),
    ctypes.byref(lpProcessInformation)
)

if response > 0:
    print("Proc is running")
else:
    print("Failed. error code: {0}".format(k_handle.GetLastError()))






