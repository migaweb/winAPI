import ctypes
import argparse


def open_proc_handle(process_id):
    k_handle = ctypes.WinDLL("Kernel32.dll")
    PROCESS_ALL_ACCESS = (0x000F0000 | 0x00100000 | 0xFFF)  # Shortcut to all access
    dwDesiredAccess = PROCESS_ALL_ACCESS
    bInheritHandle = False
    dwProcessId = process_id
    print(dwProcessId)

    response = k_handle.OpenProcess(dwDesiredAccess, bInheritHandle, dwProcessId)
    error = k_handle.GetLastError()
    if error != 0:
        print(f"Error code: {error}")
        exit(1)
    if response <= 0:
        print('Handle was not created')
    else:
        print(f'Handle was created {response}')


def argument_parser():
    parser = argparse.ArgumentParser(description="Get process handle")
    parser.add_argument('-p', '--pid', dest='process_id', type=int, help='Process id (integer)')
    args = parser.parse_args()
    return int(args.process_id)


if __name__ == '__main__':
    process_id = argument_parser()
    open_proc_handle(process_id)
