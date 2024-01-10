import platform
import psutil
import speedtest
from screeninfo import get_monitors
import wmi
import socket
import uuid


def installed_software():
    software_list = [process.info['name'] for process in psutil.process_iter(['pid', 'name'])]
    return software_list

def internet_speed():
    st = speedtest.Speedtest()
    download_speed = st.download() / 1e6
    upload_speed = st.upload() / 1e6 
    return download_speed, upload_speed

def screen_resolution():
    monitors = get_monitors()
    resolutions = [(monitor.width, monitor.height) for monitor in monitors]
    return resolutions

def cpu_info():
    cpu_info = {
        'model': platform.processor(),
        'cores': psutil.cpu_count(logical=False),
        'threads': psutil.cpu_count(logical=True)
    }
    return cpu_info

def gpu_info():
    try:
        w = wmi.WMI()
        gpu_info = [item.Name for item in w.Win32_PnPEntity if "NVIDIA" in str(item)]
        return gpu_info[0] if gpu_info else None
    except Exception as e:
        return None

def ram_size():
    ram_info = psutil.virtual_memory()
    return ram_info.total // (1024 ** 3)  

def screen_size():
    monitors = get_monitors()
    return f"{monitors[0].width} inch, {monitors[0].height} inch"

def network_info():
    mac_address = ':'.join(f'{byte:02x}' for byte in uuid.getnode().to_bytes(6, 'big'))
    return mac_address


def public_ip():
    try:
        return socket.gethostbyname(socket.gethostname())
    except Exception as e:
        return None

def windows_version():
    return platform.version()


print("Installed Software:", installed_software())
print("Internet Speed (Download, Upload):", internet_speed(),"Mbps")
print("Screen Resolution:", screen_resolution())
print("CPU Info:",  cpu_info())
print("GPU Info:", gpu_info())
print("RAM Size:",  ram_size(), "GB")
print("Screen Size:", screen_size())
print("Wifi/Ethernet MAC Address:", network_info())
print("Public IP Address:", public_ip())
print("Windows Version:",  windows_version())
