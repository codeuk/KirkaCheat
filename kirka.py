""" REQUIRES: RICH, COLORAMA, SELENIUM """

from fp.fp import FreeProxy
from requests import get, post

from os import system as sys
from colorama import Fore as f

from rich import box
from rich.table import Table as t
from rich.console import Console as c

from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType

DEBUG = True

class Kirka:
	"""
	KIRKACHEAT -
	V0.2 : 
	1. CHEAT INJECTOR -> ✔
	  > SUPPORT PROXIES -> ✔
	  > MAKE CHEAT MENU -> ✔✖ (some elements are unfinished)
	    - REACTIVE RGB MENU --> ✔
	    - AIMBOT & WALLHACKS -> ✔
	    - PACKET HOLDER ------> ✔
	    - CREATE TOGGLE MENU -> ✖

	2. ACCOUNT LOOKUP -> ✔
	3. ACCOUNT STATS --> ✔
	4. SCRAPE MATCHES -> ✔
	5. SPAMMING TOOL --> ✖
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
		""" Cleaner input function with restricted choices """
		print(text, end="")
		i = input()
		if allowed!=[]:
			if i not in allowed:
				self.KirkaInput(f"\n[{f.RED}*{f.RESET}] Invalid Response! Press any key to return to Menu...\n", [])
				self.Main()
		return i

	def Log(self, sym="!", worked=False, newvalue="", e="\n"):
		""" Log operation success or failure """
		if worked:
			print(f"[{f.GREEN}{sym}{f.RESET}] {f.GREEN}SUCCESS{f.RESET} -> {f.GREEN}{newvalue}{f.RESET}", end=e)
		else:
			print(f"[{f.RED}{sym}{f.RESET}] {f.RED}FAILED{f.RESET} -> {f.RED}{newvalue}{f.RESET}", end=e)

	def GetStats(self, id, use_id=False):
		""" Get Accounts Stats using ID or Auth-Token """
		if use_id:
			data = {"id":id}
			r = post(self.api+'user/getProfile', data=data, headers=self.hdrs)
			return r.json()
		else:
			return get(self.api+'user', headers=self.hdrs).json()

	def GetMatches(self, matchmake_url, from_menu=False):
		""" Get current match list information & display stats """
		r = get(matchmake_url)
		matches = r.json()
		if from_menu: self.ASCII()
		else: print(f"\n[{f.GREEN}+{f.RESET}] {f.RED}Currently Matchmaking! All Matches:{f.RESET}")
		for m in matches:
			table = t(box=box.HEAVY)
			table.add_column("ID", style="white")
			table.add_column("Name", style="green")
			table.add_column("Value", style="red")
			table.add_row("1", "Room ID", str(m['roomId']))
			table.add_row("2", "Map", str(m['metadata']['mapName']))
			table.add_row("3", "Private",  str(m.get('locked')))
			table.add_row("4", "Players", str(m['clients']))
			table.add_row("5", "Max Players", str(m['maxClients']))
			table.add_row("6", "Created", str(m['createdAt']))
			c().print(table)

	def DriverStatus(self):
		""" Return bool based on driver's operational status - NOT WORKING"""
		try:
			driver.current_url
			return True
		except: return False

	def ValidateAuth(self):
		""" Validates user Auth-Token when required """
		validate = get(self.api+"rewards/", headers=self.hdrs)
		if validate.status_code == 200:
			return True
		else:
			self.KirkaInput(f"\n\n[{f.RED}*{f.RESET}] Invalid Auth-Token! Press any key to return to Menu...\n"), self.Main()


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
		self.ValidateAuth()
		self.ASCII()
		stats = self.GetStats(id, use_id=True) if not me else self.GetStats(None, use_id=False)
		email = stats['email'] if me else ''
		table = t(title="KIRKA@~STATS", box=box.HEAVY)
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

	def CheatInjector(self):
		""" Inject script into kirka.io driver & monitor useful network traffic (api) """
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
			newvalue="Browser Driver prepared" if self.DriverStatus else "Install valid Chrome/Firefox driver in this directory!"
		)

		CheatSlot1 = """
		// Super secret injection script ; not released yet (full menu, aimbot, wallhacks, packet holder, etc.)	
		"""

		CheatSlot2 = """
		(function () {
			alert(`CheatSlot2 is Empty`)
		})();
		"""

		driver.get("https://kirka.io")
		self.Log(
			sym="CHEAT",
			worked = True,
			newvalue = f"Loaded Kirka.io {'with HTTP Proxy {prx}'.format(prx=webproxy) if proxy else ''}"
		)

		driver.execute_script(CheatSlot1)
		self.Log(
			sym="CHEAT",
			worked = True,
			newvalue = f"Injected Script"
		)

		if DEBUG == True:
			""" Monitor network data, lookout for api calls, block google/ping packets """
			print(f"\n[{f.GREEN}DEBUG{f.RESET}] {f.RED}Monitoring Network Traffic{f.RESET}")
			return_network = "var performance = window.performance || window.mozPerformance || window.msPerformance || window.webkitPerformance || {}; var network = performance.getEntries() || {}; return network;"
			network_urls = ["https://kirka.io"]
			matchmake_done = True

			while True:
				network   = driver.execute_script(return_network)
				packet    = network[-1]
				packeturl = packet.get('name')
				is_kirkaurl = True if "kirka.io" in packeturl else False
				blacklisted = True if "consent" in packeturl or "analytics" in packeturl else False

				if network_urls[-1] != packeturl and is_kirkaurl and not blacklisted:
					network_urls.append(packeturl)
					print(f"[{f.GREEN}+{f.RESET}] {packeturl}")
					if "/matchmake" in packeturl and len(packeturl) < 34:
						if matchmake_done:
							matchmake_done = False
						else:
							self.GetMatches(packeturl)
							matchmake_done = True

		self.KirkaInput(f"\n\n[{f.RED}*{f.RESET}] Press any key to return to Menu...\n")


	def MatchInfo(self):
		""" Display stats for all current matches """
		self.ASCII()

		self.Options(["EU", "US", "ASIA"], "Region to search for matches")
		region = self.KirkaInput(f"\n\n[{f.RED}*{f.RESET}] Region -> ")

		if region == "1": r_url = "https://eu1.kirka.io/matchmake"
		elif region == "2": r_url = "https://na1.kirka.io/matchmake"
		elif region == "3": r_url = "https://asia1.kirka.io/matchmake"

		self.GetMatches(r_url, from_menu=True)
		self.KirkaInput(f"\n\n[{f.RED}*{f.RESET}] Press any key to return to Menu...\n")


	# MENU
	
	def Main(self):
		""" Tool Options """
		self.ASCII()
		self.Options(
			["Cheat Injector", "Account Lookup", "Account Stats", "Scrape Matches"],
			 "KirkaTools v0.1"
		)

		choice = self.KirkaInput(f"\n[{f.RED}*{f.RESET}] CHOICE -> ", ["1", "2", "3", "4"])
		if choice == "1":   self.CheatInjector()
		elif choice == "2": self.AccountLookup()
		elif choice == "3": self.AccountStats(True, None)
		elif choice == "4": self.MatchInfo()


if __name__ == '__main__':
	""" INITIATE PROGRAM """
	print(f"\n[{f.RED}*{f.RESET}] Auth-Token -> ", end="")

	AUTH  = input()
	Kirka = Kirka(AUTH) # I'm not validating the auth yet because \
						# I need to boot up quickly to test new changes
	while True:
		Kirka.Main()
