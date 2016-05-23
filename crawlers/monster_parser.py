import pdb

from html.parser import HTMLParser
from urllib.request import urlopen
from urllib.error import HTTPError

class MonsterParser(HTMLParser):
	start_tr = False
	name_link = False
	td = 0

	monsters = {}
	monster = {}
	name = ""

	def handle_starttag(self, tag, attrs):
		if tag == "tr":
			self.start_tr = True
		elif tag == "td":
			if self.start_tr or self.td != 0:
				self.td = self.td + 1
				self.start_tr = False
		elif tag == "a":
			self.name_link = True

	def handle_endtag(self, tag):
		if tag == "a":
			self.name_link = False

	def handle_data(self, data):
		if self.td == 1 and self.name_link:
			self.name = data.lower().strip()
		elif self.td == 3:
			self.monster['exp'] = data.lower().strip()
		elif self.td == 4:
			self.monster['hp'] = data.strip()
			self.monsters[self.name] = self.monster
			self.monster = {}
			self.td = 0

	def getMonsters(self):
		monsters_url = "http://tibia.wikia.com/wiki/List_of_Creatures"
		response = urlopen(monsters_url)
		print(response.getheader("Content-Type"))
		if response.getheader("Content-Type") == "text/html; charset=utf-8":
			htmlString = response.read().decode("utf-8")
			self.feed(htmlString)

		return self.monsters

class LootParser(HTMLParser):
	open_tr = False
	name_link = False
	td_data = False
	td = 0

	monster_loots = {}
	loots = []
	loot = {}

	monster_name = ""
	processed_loot = False

	def handle_starttag(self, tag, attrs):
		if self.processed_loot:
			return

		if tag == "tr":
			self.open_tr = True
		elif self.open_tr and tag == "td":
			self.td_data = True
			self.td = self.td + 1
		elif self.open_tr and tag == "a":
			self.name_link = True

	def handle_endtag(self, tag):
		if self.processed_loot:
			return

		if tag == "tr":
			self.open_tr = False

			self.td_data = False
			self.td = 0
		elif tag == "a" and self.name_link:
			self.name_link = False
		elif tag == "table":
			self.processed_loot = True

	def handle_data(self, data):
		if self.processed_loot:
			return

		if self.td == 2 and self.td_data:
			self.td_data = False
			self.loot["amount"] = data
			print("Amount: " + data)
		elif self.td == 3 and self.name_link:
			self.name_link = False
			self.loot["name"] = data
			print("Name: " + data)
		elif self.td == 6 and self.td_data:
			self.td_data = False
			if "name" not in self.loot:
				print("Empty loot\n")
				self.loot = {}
				return

			self.loot["percentage"] = data
			print("Percentage: " + data + "\n")

			self.loots.append(self.loot)
			self.loot = {}

	def fetchMonstersLoot(self, monsters):
		loot_url = "http://tibia.wikia.com/wiki/Loot_Statistics:"
		for monster_name in monsters:
			monster_url = monster_name.title().replace(" ", "_")
			try:
				response = urlopen(loot_url + monster_url)
				print(loot_url + monster_url)
				if response.getheader("Content-Type") == "text/html; charset=utf-8":
					htmlString = response.read().decode("utf-8")

					self.processed_loot = False
					self.feed(htmlString)

					self.monster_loots[monster_name] = self.loots
					self.loots = []
			except HTTPError:
				print(monster_name.title() + " does not drop loot")
				self.monster_loots[monster_name] = {}

if __name__ == '__main__':
	parser = MonsterParser()
	monsters = parser.getMonsters()

	loot_parser = LootParser()
	pdb.run("loot_parser.fetchMonstersLoot(monsters)")
