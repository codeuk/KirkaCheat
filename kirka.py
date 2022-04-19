""" REQUIRES: RICH, COLORAMA, SELENIUM """

from fp.fp import FreeProxy
from os import system as sys
from selenium import webdriver
from requests import get, post
from colorama import Fore as f
from rich.table import Table as t
from rich.console import Console as c
from selenium.webdriver.common.proxy import Proxy, ProxyType

class Kirka:
	"""
	V0.2 : 
	1. CHEAT INJECTOR -> ✔
	  > SUPPORT PROXIES -> ✔
	  > MAKE CHEAT MENU -> ~✔
	    - AIMBOT & WALLHACKS -> ✔

	2. ACCOUNT LOOKUP -> ✔
	3. ACCOUNT STATS --> ✔
	4. SPAMMING TOOLS -> ✖
	  > WORKING ON FRIEND SPAMMER
	"""

	def __init__(self, AUTH=""):
		self.amt  = 0
		self.hdrs = {"authorization":AUTH}
		self.api  = 'https://api.kirka.io/api/'
		r, g, re  = f.RED, f.GREEN, f.RESET
		self.art  = f"""
    {r} __   .__       {re}{g} __            
    {r}|  | _|__|______{re}{g}|  | _______   
    {r}|  |/ /  \_  __ \{re}{g}  |/ /\__  \  
    {r}|    <|  ||  | \/{re}{g}    <  / __ \_
    {r}|__|_ \__||__|  {re}{g}|__|_ \(____  /
    {r}     \/              {re}{g}\/     \/ {re}
     created by github.com/codeuk
		"""


	# NON-TOOL FUNCTIONS

	def ASCII(self):
		sys('cls')
		print(self.art)

	def Options(self, options, notice="", _=""):
		""" Print options and notice cleaner """
		print(f"{_}[{f.YELLOW}{notice}{f.RESET}]")
		for index in range(len(options)):
			print(f"	[{f.RED}{index+1}{f.RESET}] {options[index]}")

	def KirkaInput(self, text, allowed=[]):
		print(text, end="")
		i = input()
		if allowed!=[]:
			if i not in allowed:
				self.KirkaInput(f"\n[{f.RED}*{f.RESET}] Invalid Response! Press any key to return to Menu...\n", [])
				self.Main()
		return i

	def Log(self, sym="!", worked=False, newvalue="", e="\r"):
		""" Log operation success or failure """
		if worked:
			print(f"[{f.GREEN}{sym}{f.RESET}] {f.GREEN}SUCCESS{f.RESET} -> {f.GREEN}{newvalue}{f.RESET}", end=e)
		else:
			print(f"[{f.RED}{sym}{f.RESET}] {f.RED}FAILED{f.RESET} -> {f.RED}{newvalue}{f.RESET}", end=e)

	def GetStats(self, id, use_id=False):
		""" Get Accounts Stats using ID or Bearer Token """
		if use_id:
			data = {"id":id}
			r = post(self.api+'user/getProfile', data=data, headers=self.hdrs)
			return r.json()
		else:
			return get(self.api+'user', headers=self.hdrs).json()

	def DriverStatus(self):
		try:
			driver.current_url
			return True
		except: return False


	# KIRKA.IO TOOLS

	def AccountLookup(self):
		""" Look up account information using Public Long ID """
		user_id = self.KirkaInput(f"[{f.RED}*{f.RESET}] Account's Long ID -> ")
		self.AccountStats(
			False,
			user_id
		)

	def AccountStats(self, me, id):
		""" Print parsed account stats from json """
		self.ASCII()
		stats = self.GetStats(id, use_id=True) if not me else self.GetStats(None, use_id=False)
		email = stats['email'] if me else ''
		table = t(title="KIRKA@~STATS")
		table.add_column("ID",    style="white")
		table.add_column("Name",  style="green")
		table.add_column("Value", style="red")
		table.add_row("1", "User",    stats['name'])
		table.add_row("2", "Level",   str(stats['level']))
		table.add_row("3", "XP",      str(stats['totalXp']))
		table.add_row("4", "Role",    stats['role'])
		table.add_row("5", "Coins",   str(stats['coins']))
		table.add_row("6", "Gems",    str(stats['diamonds']))
		table.add_row("7", "ID",      stats['shortId'])
		table.add_row("8", "Email", 'None' if email=='' else email)
		table.add_row("9", "Created", stats['createdAt'])
		c().print(table)

		self.KirkaInput(f"[{f.RED}*{f.RESET}] Press any key to return to Menu...")

	def SpammingTools(self):
		""" Spam Friends, Clans, etc. """
		self.ASCII()
		self.Options(["Friend Requests", "Clan Invites"], "Currently Being Worked on - Doesn't Currently Work")
		c = self.KirkaInput(f"\n[{f.RED}*{f.RESET}] Thing to spam -> ", ["1", "2"])

		if c == "1":
			user_id = self.KirkaInput(f"[{f.RED}*{f.RESET}] Account's Short ID -> ")
			data = {'shortId':user_id}
			r = post(self.api+'user/offerFriendship', headers=self.hdrs, data=data)

			self.Log(
				sym = "SPAM",
				worked = True if r.status_code == 200 or r.status_code == 201 else False,
				newvalue = user_id,
				e="\n"
			)

		if c == "2":
			pass

		self.KirkaInput(f"\n[{f.RED}*{f.RESET}] Press any key to return to Menu...")


	def CheatInjector(self):
		""" Inject cheat menu script into kirka.io driver """
		self.ASCII()

		settings = webdriver.ChromeOptions()
		settings.add_argument('--log-level=3')

		self.Options(["Proxies", "Proxyless"], "Using proxies ensures that you can't be IP banned")
		p = self.KirkaInput(f"\n[{f.RED}*{f.RESET}] Option -> ", ["1", "2"])

		self.Options(
			["Cheat Slot 1", "Cheat Slot 2"],
			"All cheats are safe (Using Proxies and Non-Caching Browser)",
			_="\n"
		)
		c = self.KirkaInput(f"\n[{f.RED}*{f.RESET}] Cheat to Inject -> ", ["1", "2"])

		if p == "1":
			countries = ['US', 'BR']
			self.Options(countries, "Use the nearest region to you for the best connection", _="\n")
			r = self.KirkaInput(f"\n[{f.RED}*{f.RESET}] Proxy region -> ", ["1", "2"])

			country = 'US' if r=="1" else 'BR'
			webproxy = webproxy = FreeProxy(country_id=country).get()
			proxy=True
			prox = Proxy()
			prox.proxy_type = ProxyType.MANUAL
			prox.ssl_proxy = webproxy

			capabilities = webdriver.DesiredCapabilities.CHROME	
			prox.add_to_capabilities(capabilities)
			driver = webdriver.Chrome(desired_capabilities=capabilities)
		else:
			proxy=False
			driver = webdriver.Chrome()

		print()
		self.Log(
			sym="CHEAT",
			worked = self.DriverStatus,
			newvalue="Browser Driver prepared" if self.DriverStatus else "Install valid Chrome/Firefox driver in this directory!",
			e="\n"
		)

		INJECTION = """
		function menu() {
			// This is a SUPER SECRET SCRIPT SHHHH NOT RELEASED YET!
			// Basically a cheat menu with many injectable scripts 
			// > Aimbot, WallHacks, Packet Holder, etc.
			// Made to be customizable and fun
			// > Change Menu colors, Custom Scripts, Spamming Tools, etc.
		}
		"""

		driver.get("https://kirka.io")
		self.Log(
			sym="CHEAT",
			worked = True,
			newvalue = f"Loaded Kirka.io {'with HTTP Proxy {prx}'.format(prx=webproxy) if proxy else ''}",
			e="\n"
		)

		driver.execute_script(INJECTION)
		self.Log(
			sym="CHEAT",
			worked = True,
			newvalue = f"Injected Script",
			e="\n"
		)

		self.KirkaInput(f"\n\n[{f.RED}*{f.RESET}] Press any key to return to Menu...\n")


	# MENU
	
	def Main(self):
		""" Tool Options """
		self.ASCII()
		self.Options(
			["Cheat Injector", "Account Lookup", "Account Stats", "Spamming Tools"],
			 "KirkaTools v0.1"
		)

		choice = self.KirkaInput(f"\n[{f.RED}*{f.RESET}] CHOICE -> ", ["1", "2", "3", "4"])
		if choice == "1":   self.CheatInjector()
		elif choice == "2": self.AccountLookup()
		elif choice == "3": self.AccountStats(True, None)
		elif choice == "4": self.SpammingTools()


if __name__ == '__main__':
	""" INITIATE PROGRAM """
	print(f"\n[{f.RED}*{f.RESET}] Bearer Token -> ", end="")

	AUTH  = input()
	Kirka = Kirka(AUTH)
	while True:
		Kirka.Main()
