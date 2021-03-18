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
		name = input("Enter name of player {}: ".format(i+1))
		player = Player(name)
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

def spin_wheel(lst):
	wedge = random.sample(lst,1)
	return wedge 

def select_phrase(dic):
	if len(dic) == 0:
		sys.exit("There are no more categories available.")
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
	phrase = Phrase(category, phrase)	
	return phrase

class Phrase():
	vowels = ["a", "e", "i", "o", "u", "A", "E", "I", "O", "U"]
	def __init__(self,category,phrase):
		if not phrase.isascii():
			raise ValueError("Phrase contains non-ascii characters")
		self.category = category
		self.phrase = phrase
		self.blanked = "".join(["_" if char.isalnum() else char for char in self.phrase])
		self.guessed = ""
		self.has_vowels = any(char in self.vowels for char in self.phrase)

	def guess_letter(self,letter):
		letter = letter.lower()
		if letter not in self.phrase.lower():
			return False
		else:
			self.guessed = self.guessed + letter
			self.blanked = "".join(["_" if char.lower() not in self.guessed and char.isalnum() else char for char in self.phrase])
			self.has_vowels = any(char in self.vowels for char in self.phrase if char.lower() not in self.guessed and char.isalnum())

class Player():
	def __init__(self,name):
		self.name = name
		self.money = 0
		self.prize = []
	
	def bankrupt(self):
		self.money = 0

	def buy_vowel(self):
		self.money = self.money - 250

	def guessed_letter(self,amount,nb_letters,prize=False):
		self.money = self.money + amount*nb_letters
		if prize:
			#print("Inside conditional")
			#print("Prize to be added: {}".format(prize))
			self.prize.append(prize)
			#print("Updated prize list: {}".format(self.prize))

def game_round(phr,players):
	print("Phrase to guess: {}".format(phr.phrase))
	print("Game round finished")

def game(phrases,wheel):
	players = input_players()
	stop_game = False
	while not stop_game:
		phrase = select_phrase(phrases)
		game_round(phrase,players)
		stop_input = False
		while not stop_input:
			answer = input("Continue playing (y/n): ")
			if answer.lower() in ['y','n']:
				stop_input = True
			else:
				print("Please enter 'y' to continue, and 'n' to stop the game.")
		if answer.lower() == 'n':
			stop_game = True
			print("Good bye!")



phrases, wheel = load_data()
game(phrases, wheel)
