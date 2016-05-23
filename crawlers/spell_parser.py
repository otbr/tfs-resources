from html.parser import HTMLParser
from urllib.request import urlopen

url = "http://tibia.wikia.com/wiki/Spells"

class SpellParser(HTMLParser):
	start_name_td = False
	td = 0

	spells = {}
	spell = {}
	word = ""

	def handle_starttag(self, tag, attrs):
		if tag == "td":
			for (key, value) in attrs:
				if key == "class" and value == "spell-words":
					self.start_name_td = True
					self.td = 0

	def handle_endtag(self, tag):
		if tag == "td":
			if self.start_name_td or self.td != 0:
				self.td = self.td + 1

			self.start_name_td = False

	def handle_data(self, data):
		if self.start_name_td:
			self.word = data.lower().strip()
		elif self.td == 1:
			self.spell['premium'] = data.lower().strip()
		elif self.td == 2:
			self.spell['cost'] = data.strip()
		elif self.td == 3:
			self.spell['level'] = data.strip()
			self.spells[self.word] = self.spell
			self.spell = {}
			self.td = 0

	def getSpells(self):
		response = urlopen(url)
		print(response.getheader("Content-Type"))
		if response.getheader("Content-Type") == "text/html; charset=utf-8":
			htmlString = response.read().decode("utf-8")
			self.feed(htmlString)

		return self.spells
