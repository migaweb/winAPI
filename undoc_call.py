import ctypes
from ctypes.wintypes import DWORD, HANDLE, LPWSTR

k_handle = ctypes.WinDLL("Kernel32.dll")
d_handle = ctypes.WinDLL("DNSAPI.dll")

# DNS_CACHE_ENTRY Structure
class DNS_CACHE_ENTRY(ctypes.Structure):
    _fields_ = [
        ("pNext", HANDLE),  # Handle to the next DNS cache entry
        ("recName", LPWSTR),  # Host name
        ("wType", DWORD),  # Type of DNS entry
        ("wDataLength", DWORD),  # Length of the DNS entry
        ("dwFlags", DWORD)
    ]


dns_entry = DNS_CACHE_ENTRY()
dns_entry.wDataLength = 1024  # Configures the size of the entry

# Exec win API call to grab the DNS entry cache
response = d_handle.DnsGetCacheDataTable(ctypes.byref(dns_entry))

if response == 0:
    print("Error code: {0}".format(k_handle.GetLastError()))

# grabbing First pNext
# convert a pointer to a structure to ignore the first entry as its 0
dns_entry = ctypes.cast(dns_entry.pNext, ctypes.POINTER(DNS_CACHE_ENTRY))

while True:
    # Handle try catch for when we don't have any more entries
    try:
        print("DNS Entry {0} - Type {1}".format(dns_entry.contents.recName, dns_entry.contents.wType))
        dns_entry = ctypes.cast(dns_entry.pNext, ctypes.POINTER(DNS_CACHE_ENTRY))
    except:  # end
        break


