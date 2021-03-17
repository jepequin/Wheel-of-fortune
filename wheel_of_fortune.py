import random
import json
import sys

def input_players():
	stop_input = False
	while not stop_input:
		try:
			num_human = input("Input the number of players: ")
			num_human = int(num_human)
			if num_human < 2:
				print("Game needs at least 2 players")
			else:
				print("Number of human players: {}".format(num_human))
				stop_input = True
		except ValueError:
			print('"{}" is not an integer'.format(num_human))
	players = []
	for i in range(num_human):
		player = input("Enter name of player {}: ".format(i+1))
		players.append(player)
	random.shuffle(players)
	return players

def load_data():
	with open('phrases.json','r') as json_file:
		json_string = json_file.read()
		phrases = json.loads(json_string)
	with open('wheel.json','r') as json_file:
		json_string = json_file.read()
		wheel = json.loads(json_string)	
	return phrases, wheel

def select_wedge(lst):
	wedge = random.sample(lst,1)
	return wedge 

def select_phrase(dic):
	category = random.sample(list(dic),1)[0]
	phrase = random.sample(dic[category],1)[0]
	#print('Category chosen: {}'.format(category))
	#print('Phrase chosen: {}'.format(phrase))
	dic[category].remove(phrase)
	#print('Removed phrase from category: {}'.format(phrase not in dic[category]))
	if len(dic[category]) == 0:
		del dic[category]
		#print('Deleted category "{}"'.format(category))
		#print('Remaining categories: {}'.format(len(dic)))
	if len(dic) == 0:
		sys.exit("There are no more categories available.")
	return category, phrase

class Phrase():
	vowels = ["a", "e", "i", "o", "u", "A", "E", "I", "O", "U"]
	def __init__(self,phrase):
		if not phrase.isascii():
			raise ValueError("Phrase contains non-ascii characters")
		self.phrase = phrase
		self.blanked = "".join(["_" if char.isalnum() else char for char in self.phrase])
		self.guessed = ""
		self.has_vowels = any(char in self.vowels for char in self.phrase)

def guess_letter(phrase,letter):
	letter = letter.lower()
	if letter not in phrase.phrase.lower():
		return False
	else:
		phrase.guessed = phrase.guessed + letter
		phrase.blanked = "".join(["_" if char.lower() not in phrase.guessed and char.isalnum() else char for char in phrase.phrase])
		phrase.has_vowels = any(char in phrase.vowels for char in phrase.phrase if char.lower() not in phrase.guessed and char.isalnum())



