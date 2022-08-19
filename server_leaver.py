try:
	import os
	import requests
	from plyer import notification
except:
	exit("[!] ERROR Install 'plyer' and 'discord.py-self'")


def check_token(token,url):
	response = requests.get(url, headers={"Authorization" : token})
	return response.text if response.status_code == 200 or response.status_code == 204 else False

def get_servers(tkn):
	return requests.get("https://discord.com/api/v9/users/@me/guilds", headers={"Authorization" : tkn}).json()

def leave_server(token,sid):
	response = requests.delete("https://discord.com/api/v9/users/@me/guilds/" + sid, headers={"Authorization" : token})
	if response.status_code == 200 or response.status_code == 204: return True
	elif response.status_code == 400: 
		response2 = requests.delete("https://discord.com/api/v9/guilds/" + sid, headers={"Authorization" : token})
		return True if response2.status_code == 200 or response2.status_code == 204 else False
	return False

def read_tokens(filedir):
	f=open(filedir,'r')
	lines=f.readlines()
	f.close()

	return lines

def main():
	print('[+] Reading Tokens File')

	tokens = []

	while len(tokens) == 0:
		try:
			tokens = read_tokens(os.getcwd() + '\\' + "tokens.txt")
			if len(tokens) > 0: break
		except FileNotFoundError:
			open(os.getcwd() + '\\' + "tokens.txt","w+")
		input("[!] No Tokens Found\n[>] Put tokens into 'tokens.txt'")

	working = []

	print(f'[+] {len(tokens)} Tokens leaving')

	for tkn in tokens:
		tkn = tkn.strip('\n')

		a = check_token(tkn,'https://discordapp.com/api/users/@me')
		username =''

		if not a: continue

		for line in a.split(','):
			if 'username' in line:
				line = line.replace('"username": ','')
				username = line.replace('"','')[1:]
				break

		if username == '': continue

		servers = get_servers(tkn)

		for s in servers:
			try:
				worked = leave_server(tkn,s['id'])

				if worked: working.append(s)
				print(username + '/' + s['id'])
			except:
				pass

		print(f"[DONE] {tkn}")

	print('[+] Finished with {} valid leaves'.format(len(working)))

if __name__ == "__main__":
	main()

	notification.notify(title="Discord Server Leaver", message="Finished leaving server!", app_icon=None, timeout=5)
	input('[?] Press ENTER to close script')