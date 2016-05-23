from lxml import etree
from webcrawler import SpellParser

if __name__ == '__main__':
	parser = SpellParser()
	spells = parser.getSpells()

	doc = etree.parse("spells/spells.xml")
	for spell in doc.getiterator("instant"):
		word = spell.get("words")
		if word in spells:
			level = spell.get("lvl")
			cost = spell.get("mana")
			premium = spell.get("prem") == "1" and "yes" or "no"
			if level != spells[word]["level"] or cost != spells[word]["cost"] or premium != spells[word]["premium"]:
				print(word)
				print(premium, spells[word]["premium"])
				print(level, spells[word]["level"])
				print(cost, spells[word]["cost"])

	for spell in doc.getiterator("conjure"):
		word = spell.get("words")
		if word in spells:
			level = spell.get("lvl")
			cost = spell.get("mana")
			premium = spell.get("prem") == "1" and "yes" or "no"
			if level != spells[word]["level"] or cost != spells[word]["cost"] or premium != spells[word]["premium"]:
				print(word)
				print(premium, spells[word]["premium"])
				print(level, spells[word]["level"])
				print(cost, spells[word]["cost"])
