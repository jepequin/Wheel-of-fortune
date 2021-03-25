import random
import json
import sys
import time

def input_players():
	'''Inputs players using a listener loop. Returns list of "Player" class instances'''
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
	'''Loads json files containing the phrases dictionary and the wheel wedges list'''
	with open('phrases.json','r') as json_file:
		json_string = json_file.read()
		phrases = json.loads(json_string)
	with open('wheel.json','r') as json_file:
		json_string = json_file.read()
		wheel = json.loads(json_string)	
	return phrases, wheel

def spin_wheel(lst):
	'''Simulates the wheel spinning'''
	wedge = random.sample(lst,1)[0]
	return wedge

def select_phrase(dic):
	'''Takes a phrases dictionary as input. Selects category and phrase at random. Returns "Phrase" class instance'''
	if len(dic) == 0:
		sys.exit("There are no more categories available.")
	category = random.sample(list(dic),1)[0]
	phrase = random.sample(dic[category],1)[0]
	dic[category].remove(phrase)
	if len(dic[category]) == 0:
		del dic[category]
	phrase = Phrase(category, phrase)	
	return phrase

class Phrase():
	'''Phrase class. 
An instance of this class has the following attributes:
	category: string containing the category of the phrase.
	phrase: string containing the phrase to guess.
	blanked: obscured version of phrase. every alphabetical character starts out as hidden.
	guessed: string containing already guessed letters.
	vowels_unguessed: string containing vowels to be guessed.
Methods in this class are the following:
	guess_letter(st): 
		Input: 'st' = string containing a letter. 
		Output: tuple (False,0) if letter does not appear in phrase
			tuple (True,number) where "number" is the number of times letter appears in phrase
		Side effects: updates "guessed", "blanked" and "vowels_unguessed" instance variables
	guess_phrase('st'):
		Input: 'st' = string containing the attempted guess
		Output: True if guess is successful 
			None otherwise
		Side effect: updates "blanked" instance variable
	__str__(): prints relevant informacion about the Phrase instance'''
	vowels = ["a","e","i","o","u"]
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
		self.vowels_unguessed = "".join([char for char in self.vowels if char in self.phrase.lower()])
	def guess_letter(self,letter):
		letter = letter.lower()
		try:
			ord(letter)
		except TypeError:
			raise TypeError("Input must be a string of length 1")
		if letter not in self.phrase.lower():
			self.guessed = self.guessed + letter
			return False, 0
		else:
			self.guessed = self.guessed + letter
			self.blanked = "".join(["_" if char.lower() not in self.guessed and char.isalnum() else char for char in self.phrase])
			self.vowels_unguessed = "".join([char for char in self.vowels if char in self.phrase.lower() and char not in self.guessed])	
			return True, self.phrase.lower().count(letter)
	def guess_phrase(self,phrase):
		phrase = phrase.lower()
		if phrase == self.phrase.lower():
			self.blanked = self.phrase
			return True

	def __str__(self):
		info = '''Remember that: 
- The category is: {} 
- The blanked phrase is: {} 
- The letters already guessed are: {}'''.format(self.category,self.blanked,self.guessed)
		return info

class Player():
	'''Player class. 
An instance of this class has the following attributes:
	name: string containing the name of the player.
	money: non-negative integer representing the amount of money won by the player.
	prizes: list of prizes won by the player
Methods in this class are the following:
	guessed_letter(amount,guessed_letters,prize): 
		Input: 'amount' = integer representing the money amount to be won.
		       'guessed_letters' = integer representing how many letters were correctly guessed 
		       'prize' = string containing the prize to be won (default value is 'False')
		Side effects: updates "money" and "prizes" instance variables
	__str__(): prints relevant informacion about the Player instance'''
	def __init__(self,name):
		self.name = name
		self.money = 0
		self.prizes = []
	
	def bankrupt(self):
		self.money = 0

	def buy_vowel(self):
		self.money = self.money - 250

	def guessed_letter(self,amount,guessed_letters,prize=False):
		self.money = self.money + amount*guessed_letters
		if prize:
			self.prizes.append(prize)

	def __str__(self):
		info = "{}, up to now you have won: \n- An amount of {} dollars. ".format(self.name,self.money)
		if len(self.prizes) == 0:
			info = info + "\n- No prizes (yet)"
		else:
			for prize in self.prizes:
				info = info + "\n- {}".format(prize)
		return info

def game_turn(phrase,player):
	'''Simulates a player turn.
Returns True if player successfully guesses the phrase, otherwise returns False.'''
	name = player.name
	print("="*80 + "\nIt's {}'s turn now!\n".format(name) + "="*80)
	time.sleep(1)
	continue_turn = True
	while continue_turn:
		money = player.money
		print(player)
		print(phrase)	
		print(phrase.phrase.upper())
		if len(phrase.vowels_unguessed) == 0:
			print('- There are no more vowels to guess')
		time.sleep(1)
		input("Please press 'Enter' to spin the wheel.".format(name))
		wedge = spin_wheel(WHEEL)
		print("Spinning ...")
		time.sleep(4)
		if wedge["type"] == "bankrupt":
			print("Too bad, the wheel landed on 'bankrupt'. {} you lose all your money ".format(name))
			time.sleep(1)
			player.bankrupt()
			return False
		elif wedge["type"] == "loseturn":
			print("Too bad, the wheel landed on 'loseturn'. {} you lose a turn".format(name))
			time.sleep(1)
			return False
		else:
			print("Great! the wheel landed in a {} cash wedge".format(wedge['value']))
			time.sleep(1)
			prize = wedge["prize"]
			wedge["prize"] = False
			if prize:
				print("In addition, {} has the opportunity to gain {}".format(name,prize))
			stop_input = False
			while not stop_input:
				print('''{}, what do you want to do: 
- Pass your turn (Input "pass").
- Guess the phrase (Input "phrase").
- Guess a letter (Input "consonant").'''.format(name)
					)	
				if money > 250 and len(phrase.vowels_unguessed) != 0:
					print('- Buy a vowel for 250$ (Input "vowel")')
				time.sleep(1)
				action = input("It's up to you: ").lower()
				time.sleep(1)
				if money > 250 and len(phrase.vowels_unguessed) != 0:
					if action in ["vowel","consonant","phrase","pass"]:
						stop_input = True
					else:
						print('Please input one of the following: "vowel","consonant", "phrase", "pass".')
						time.sleep(1)
				else:	
					if action in ["consonant","phrase","pass"]:
						stop_input = True
					else:
						print('Please input one of the following: "consonant", "phrase", "pass".')
						time.sleep(1)
			if action == "vowel":				
				stop_input = False
				while not stop_input:
					guess = input("Input the vowel you want to buy: ").lower()
					if ord(guess) in VOWEL_ORDERS:
						if guess not in phrase.guessed:
							stop_input = True
						else:
							print('"{}" has already been guessed'.format(guess))
					else:
						print('"{}" is not a vowel'.format(guess))
				player.buy_vowel()
				success, guessed_letters = phrase.guess_letter(guess)
				if success:
					print('Great! The letter "{}" appears {} times in the phrase'.format(guess,guessed_letters))
					time.sleep(1)
					player.guessed_letter(wedge["value"],guessed_letters,prize=prize)
					if phrase.blanked == phrase.phrase:
						print("Great! {} has successfully guessed the phrase!".format(name))						
						print(player)
						return True
				else:
					print('Sorry, the letter "{}" does not appear in the phrase.'.format(guess))
					return False		
			elif action == 'consonant':
				stop_input = False
				while not stop_input:
					guess = input("Input the consonant you want to guess: ").lower()
					if ord(guess) in CONSONANT_ORDERS:
						if guess not in phrase.guessed:
							stop_input = True
						else:
							print('"{}" has already been guessed'.format(guess))
					else:
						print('"{}" is not a consonant'.format(guess))
				time.sleep(1)
				success, guessed_letters = phrase.guess_letter(guess)
				if success:
					print('Great! The letter "{}" appears {} times in the phrase'.format(guess,guessed_letters))
					time.sleep(1)
					player.guessed_letter(wedge["value"],guessed_letters,prize=prize)
					if phrase.blanked == phrase.phrase:
						print("Great! {} has successfully guessed the phrase!".format(name))
						print(player)
						return True
				else:
					print('Sorry, the letter "{}" does not appear in the phrase.'.format(guess))
					return False			
			elif action == "phrase":
				guess = input("Guess a phrase: ").lower()
				success = phrase.guess_phrase(guess)
				if success:
					print("Great! {} has successfully guessed the phrase!".format(name))
					print(player)
					return True
				else:
					print("Sorry, the phrase you guessed is not correct")
					return False
			else:
				time.sleep(1)
				print(player)
				print("Ok. Let's go to our next player.")
				return False
		print("-"*80)
					
def game_round(phrase,players,player_number):
	'''Simulates a round. 
Ends when a player guesses the phrase, returns integer indicating whose turn it is.''' 
	print("*"*40 + "\nA new round begins\n" + "*"*40)
	total_players = len(players)
	player = players[player_number]
	stop_round = False
	while not stop_round:
		stop_round = game_turn(phrase,player)
		player_number = (player_number + 1) % total_players
		player = players[player_number]
	return player_number

def game():
	'''Simulates the whole game.
After a phrase is guessed asks the user if she wants to continue game.'''
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

# Declare global variables
CONSONANT_ORDERS = [number for number in range(97,123) if number not in [97,101,105,111,117]]
VOWEL_ORDERS = [97,101,105,111,117]
LETTER_ORDERS = CONSONANT_ORDERS + VOWEL_ORDERS
PHRASES, WHEEL = load_data()

# Play game
game()

