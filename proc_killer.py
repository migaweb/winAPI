
# FindWindowA
# GetWindowThreadProcessId
# OpenProcess
# TerminateProcess

import ctypes
import argparse

PROCESS_ALL_ACCESS = (0x000F0000 | 0x00100000 | 0xFFF)  # Shortcut to all access
k_handle = ctypes.WinDLL("Kernel32.dll")
u_handle = ctypes.WinDLL("User32.dll")


def terminate_process(handle):
    result = k_handle.TerminateProcess(handle, 0x1)
    if result == 0:
        print(f'Error code: {k_handle.GetLastError()}. Could not terminate process.')
        exit(1)
    else:
        print('Process terminated.')


def open_proc_handle(process_id):
    dwDesiredAccess = PROCESS_ALL_ACCESS
    bInheritHandle = False
    dwProcessId = process_id
    result = k_handle.OpenProcess(dwDesiredAccess, bInheritHandle, dwProcessId)
    if result <= 0:
        print(f'Error code: {k_handle.GetLastError()}. Could not grab proc handle.')
        exit(1)
    else:
        print('Got proc handle.')

    return result


def find_window(class_name, window_name):
    lp_class_name = class_name
    lp_window_name = ctypes.c_char_p(window_name.encode('utf-8'))
    hwnd = u_handle.FindWindowA(lp_class_name, lp_window_name)
    if hwnd == 0:
        print(f'Error code: {k_handle.GetLastError()}. Could not grab handle.')
        exit(1)
    else:
        print('Got handle.')
    return hwnd


def get_window_thread_process_id(hwnd):
    pid = ctypes.c_ulong()
    result = u_handle.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
    if result == 0:
        print(f'Error code: {k_handle.GetLastError()}. Could not get window thread process id.')
        exit(1)
    else:
        print('Got window thread process id.')
    return pid


def argument_parser():
    parser = argparse.ArgumentParser(description="Get process handle")
    parser.add_argument('-n', dest='window_name', type=str, help='Window name')
    args = parser.parse_args()
    return str(args.window_name)


if __name__ == '__main__':
    window_name = argument_parser()
    hwnd = find_window(None, window_name)

    process_id = get_window_thread_process_id(hwnd=hwnd)
    handle = open_proc_handle(process_id)
    terminate_process(handle)

