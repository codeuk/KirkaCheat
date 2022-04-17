""" REQUIRES: RICH, COLORAMA """

from os import system as sys
from requests import get, post
from colorama import Fore as f
from rich.table import Table as t
from rich.console import Console as c

class Kirka:
	""" 
	V0.1 : 
	1. COIN BOOSTING --> ✖
	2. ACCOUNT LOOKUP -> ✔
	3. ACCOUNT STATS --> ✔
	4. SPAMMING TOOLS -> ✖
	"""

	def __init__(self, AUTH=""):
		self.amt  = 0
		self.hdrs = {"authorization":AUTH}
		self.api  = 'https://api.kirka.io/api/rewards'
		r, g, re  = f.RED, f.GREEN, f.RESET
		self.art  = f"""
    {r} __   .__       {re}{g} __            
    {r}|  | _|__|______{re}{g}|  | _______   
    {r}|  |/ /  \_  __ \{re}{g}  |/ /\__  \  
    {r}|    <|  ||  | \/{re}{g}    <  / __ \_
    {r}|__|_ \__||__|  {re}{g}|__|_ \(____  /
    {r}     \/              {re}{g}\/     \/ {re}
		"""

	# NON-TOOL FUNCTIONS

	def ASCII(self):
		sys('cls')
		print(self.art)

	def Log(self, sym="!", worked=False, coins=""):
		""" Log operation success or failure """
		if worked:
			print(f"[{f.GREEN}{sym}{f.RESET}] {f.GREEN}SUCCESS{f.RESET} -> {f.GREEN}{coins}{f.RESET}", end="\r")
		else:
			print(f"[{f.RED}{sym}{f.RESET}] {f.RED}FAILED{f.RESET} -> {f.RED}{coins}{f.RESET}", end="\r")

	def GetStats(self, id, use_id=False):
		""" Get Accounts Stats using ID or Bearer Token """
		if use_id:
			data = {"id":id}
			r = post('https://api.kirka.io/api/user/getProfile', data=data, headers=self.hdrs)
			return r.json()
		else:
			return get('https://api.kirka.io/api/user', headers=self.hdrs).json()


	# KIRKA.IO TOOLS

	def BoostCoins(self):
		""" Loop Rewards Request """
		self.ASCII()
		try:
			while True:
				self.amt += 1
				r = get(self.api, headers=self.hdrs)
				stats = self.GetStats(None, use_id=False)
		
				self.Log(
					self.amt,
					True if r.status_code == 200 else False,
					stats['coins']
				)
		except KeyboardInterrupt:
			input(f"[{f.RED}*{f.RESET}] Press any key to return to Menu...")

	def AccountLookup(self):
		""" Look up account information using Public Long ID """
		user_id = input(f"[{f.RED}*{f.RESET}] Account's Long ID -> ")
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

		input(f"[{f.RED}*{f.RESET}] Press any key to return to Menu...")


	# MENU
	
	def Main(self):
		""" Tool Options """
		self.ASCII()
		print(f"""
	[{f.RED}1{f.RESET}] Coin Boosting
	[{f.RED}2{f.RESET}] Account Lookup
	[{f.RED}3{f.RESET}] Account Stats
	[{f.RED}4{f.RESET}] Spamming Tools
		""")

		choice = input(f"[{f.RED}*{f.RESET}] CHOICE -> ")
		if choice == "1":   self.BoostCoins()
		elif choice == "2": self.AccountLookup()
		elif choice == "3": self.AccountStats(True, None)
		elif choice == "4": self.SpammingTools()


if __name__ == '__main__':
	""" KIRKA.IO TOOL PROGRAM """
	print(f"\n[{f.RED}*{f.RESET}] Bearer Token -> ", end="")

	AUTH  = input()
	Kirka = Kirka(AUTH)
	while True:
		Kirka.Main()
