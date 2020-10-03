import ctypes


def display_modal_dialog(text, title):
    user_handle = ctypes.WinDLL("User32.dll")
    k_handle = ctypes.WinDLL("Kernel32.dll")  # Used for getting any possible errors
    hWnd = None  # Not used, owner window
    lpText = text  # String, Message to be displayed
    lpCaption = title  # Dialog box title
    uType = 0x00000001  # Buttons displayed, OKCANCEL

    response = user_handle.MessageBoxW(hWnd, lpText, lpCaption, uType)
    error = k_handle.GetLastError()
    if error != 0:
        print(f"Error code: {error}")
        exit(1)

    if response == 1:
        print("User clicked OK!")
    elif response == 2:
        print("User clicked Cancel!")


if __name__ == '__main__':
    display_modal_dialog("This is the message", "My Title")

