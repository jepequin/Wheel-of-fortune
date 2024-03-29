# Wheel of Fortune in python

This game is the project of the fourth course in Python 3 Programming Specialization, offered by University of Michigan via Coursera (https://www.coursera.org/learn/python-classes-inheritance). The goal is to practice with the notion of classes introduced in the course. We also create tests for several functions inside our code.

## Description

The program initially asks to input the number of players and their names. Each player has some amount of money ($0 at the start of the game), a set of prizes (none at the start of the game).

#### The goal of the game is to guess a phrase within a category. For example:
- Category: Artist & Song.
- Phrase: Whitney Houston's I Will Always Love You.

#### Players see the category and an obscured version of the phrase where every alphabetic character in the phrase starts out as hidden (using underscores: _):
- Category: Artist & Song
- Phrase: _______ ______' _ ____ ______ ____ ___

#### During their turn, every player spins the wheel to determine a prize amount and:
- If the wheel lands on a cash square, players may do one of three actions:

	- Guess any letter that hasn’t been guessed by typing a letter (a-z)

		- Vowels (a, e, i, o, u) cost $250 to guess and can’t be guessed if the player doesn’t have enough money or there are no more remaining vowels to be guessed. All consonants are “free” to guess.

		- The player can guess any letter that hasn’t been guessed (these are shown to the player) and gets that cash amount for every time that letter appears in the phrase. 

		- If there is a prize, the user also gets that prize (in addition to any prizes they already had).

		- If the letter does appear in the phrase, the player spins the wheel again and repeats the process. Otherwise, it’s the next player’s turn.

		- Example: The user lands on $500 and guesses ‘W’.

			- There are three W’s in the phrase, so the player wins $1500.

	- Guess the complete phrase by typing a phrase (anything over one character that isn’t ‘pass’).

		- If it is correct, the player wins that round and is asked if she wants to continue playing (with a new category and phrase).
		
		- If they are incorrect, it is the next player’s turn. 
		
	- Pass their turn by entering 'pass'.

- If the wheel lands on “lose a turn”, the player loses their turn and the game moves on to the next player.

- If the wheel lands on “bankrupt”, the player loses their turn and loses their money but they keep all of the prizes they have won so far.

The game continues until the entire phrase is revealed (or one player guesses the complete phrase). At this point the player is asked if she wants to continue playing (with a new category and phrase).

## Author

Jesua Epequin. Contact me at jesua.epequin@gmail.com.