import random
import json
import sys
import time

from pprint import pprint

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
	wedge = random.sample(lst,1)[0]
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
		stripped = "".join([char for char in phrase if char.isalnum()])
		if not stripped.isalpha():
			raise ValueError("Phrase contains numbers")
		if len(stripped) == 0:
			raise ValueError("Phrase must contain alphabetical characters")		
		self.category = category
		self.phrase = phrase
		self.blanked = "".join(["_" if char.isalnum() else char for char in self.phrase])
		self.guessed = ""
		self.has_vowels = any(char in self.vowels for char in self.phrase)

	def guess_letter(self,letter):
		letter = letter.lower()
		if letter not in self.phrase.lower():
			return False, 0
		else:
			self.guessed = self.guessed + letter
			self.blanked = "".join(["_" if char.lower() not in self.guessed and char.isalnum() else char for char in self.phrase])
			self.has_vowels = any(char in self.vowels for char in self.phrase if char.lower() not in self.guessed and char.isalnum())	
			return True, self.phrase.lower().count(letter)

	def guess_phrase(self,phrase):
		phrase = phrase.lower()
		if phrase == self.phrase.lower():
			self.blanked = self.phrase
			return True

class Player():
	def __init__(self,name):
		self.name = name
		self.money = 0
		self.prize = []
	
	def bankrupt(self):
		self.money = 0

	def buy_vowel(self):
		self.money = self.money - 250

	def guessed_letter(self,amount,guessed_letters,prize=False):
		self.money = self.money + amount*guessed_letters
		if prize:
			#print("Prize to be added: {}".format(prize))
			self.prize.append(prize)
			#print("Updated prize list: {}".format(self.prize))

	def __str__(self):
		info = "Name: {} \nMoney prize: {} \nPrizes: {}".format(self.name,self.money,self.prize)
		return info

def game_turn(phrase,player):
	continue_turn = True
	while continue_turn:
		print("Category: {} \nPhrase: {} \nBlanked {} \nLetters already guessed: {}".format(phrase.category,phrase.phrase,phrase.blanked,phrase.guessed))
		input("It's {}'s turn now! Please press 'Enter' to spin the wheel.".format(player.name))
		wedge = spin_wheel(WHEEL)
		print("Spinning ...")
		time.sleep(4)
		if wedge["type"] == "bankrupt":
			print("Too bad, {} goes bankrupt".format(player.name))
			player.bankrupt()
			return False
		elif wedge["type"] == "loseturn":
			print("Too bad, {} looses a turn".format(player.name))
			return False
		else:
			print("Great! {} landed in a {} cash wedge".format(player.name,wedge['value']))
			prize = wedge["prize"]
			if prize:
				print("In addition, {} has the opportunity to gain {}".format(player.name,prize))
			stop_input = False
			while not stop_input:	
				action = input('''{}, what do you want to do: 
a) Buy a vowel for 250$ (Input "vowel")
b) Guess letter (Input "consonant"). 
c) Guess phrase (Input "phrase"). 
d) Pass your turn (Input "pass"). 
It's up to you: '''.format(player.name)
							).lower()
				if action in ["vowel","consonant","phrase","pass"]:
					stop_input = True
				else:
					print('Please input one of the following: "vowel", "consonant", "phrase", "pass".')
			if action == "vowel":
				if player.money < 250:
					print("You don't have enough money to buy a vowel.")
				else:
					stop_input = False
					while not stop_input:
						guess = input("Input the vowel you want to buy: ").lower()
						if guess in ["a","e","i","o","u"]:
							stop_input = True
						else:
							print('"{}" input a vowel'.format(guess))
					player.buy_vowel()
					print("Now {} has {} dollars".format(player.name,player.money))
					success, guessed_letters = phrase.guess_letter(guess)
					if success:
						print('Great! The letter "{}" appears {} times in the phrase'.format(guess,guessed_letters))
						player.guessed_letter(wedge["value"],guessed_letters,prize=prize)
						print("Now {} has a total of {} dollars.".format(player.name,player.money))
						if prize:
							print("In adition, {} has now the following prizes {}.".format(player.name,player.prize))
						if phrase.blanked == phrase.phrase:
							print("Great! {} has successfully guessed the phrase!".format(player.name))
							return True
					else:
						print('Sorry, the letter "{}" does not appear in the phrase.'.format(guess))
						return False		
			elif action == 'consonant':
				consonant_orders = [number for number in range(97,123) if number not in [97,101,105,111,117]]
				stop_input = False
				while not stop_input:
					guess = input("Input the consonant you want to guess: ").lower()
					if ord(guess.lower()) in consonant_orders:
						stop_input = True
					else:
						print('"{}" is not a consonant'.format(guess))
				time.sleep(1)
				success, guessed_letters = phrase.guess_letter(guess)
				if success:
					print('Great! The letter "{}" appears {} times in the phrase'.format(guess,guessed_letters))
					player.guessed_letter(wedge["value"],guessed_letters,prize=prize)
					print("Now {} has a total of {} dollars.".format(player.name,player.money))
					if prize:
						print("In adition, {} has now the following prizes {}.".format(player.name,player.prize))
					if phrase.blanked == phrase.phrase:
						print("Great! {} has successfully guessed the phrase!".format(player.name))
						return True
				else:
					print('Sorry, the letter "{}" does not appear in the phrase.'.format(guess))
					return False			
			elif action == "phrase":
				guess = input("Guess a phrase: ").lower()
				success = phrase.guess_phrase(guess)
				if success:
					print("Great! {} has successfully guessed the phrase!".format(player.name))
					return True
				else:
					print("Sorry, the phrase you guessed is not correct")
					return False
			else:
				print("Ok. Let's go to our next player.")
				return False

def game_round(phrase,players,player_number): 
	total_players = len(players)
	player = players[player_number]
	stop_round = phrase.phrase == phrase.blanked
	while not stop_round:
		stop_round = game_turn(phrase,player)
		player_number = (player_number + 1) % total_players
		player = players[player_number]
	return player_number

def game():
	players = input_players()
	stop_game = False
	player_number = 0
	while not stop_game:
		phrase = select_phrase(PHRASES)
		player_number = game_round(phrase,players,player_number)
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

PHRASES, WHEEL = load_data()
game()
