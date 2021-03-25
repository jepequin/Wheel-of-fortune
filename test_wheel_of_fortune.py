import unittest
from wheel_of_fortune import Phrase, Player

class TestPhrase(unittest.TestCase):
	def test_init_value(self):
		# Test with alphabetical strings 
		phrase_1 = Phrase(category="Film",phrase="Die Hard")
		self.assertEqual(phrase_1.category,"Film")
		self.assertEqual(phrase_1.phrase,"Die Hard")
		self.assertEqual(phrase_1.blanked ,"___ ____")
		self.assertEqual(phrase_1.guessed,"")
		self.assertEqual(phrase_1.vowels_unguessed,"aei")
		# Test with strings containing non-alphabetical characters
		phrase_2 = Phrase("Film","Spider-Man: Into the Spider-Verse")
		self.assertEqual(phrase_2.phrase,"Spider-Man: Into the Spider-Verse")
		self.assertEqual(phrase_2.blanked,"______-___: ____ ___ ______-_____")
		self.assertEqual(phrase_2.guessed,"")
		self.assertEqual(phrase_2.vowels_unguessed,"aeio")

	def test_init_numerical_values(self):
		# Test ValueError is raised when string has numerical characters 
		self.assertRaises(ValueError, Phrase, "Title","Home alone 2") 
		self.assertRaises(ValueError, Phrase, "Title","4.3.2.1.")
		# Test ValueError is raised when input string is empty
		self.assertRaises(ValueError, Phrase, "","") 

	def test_guess_letter(self):
		# Test that function returns tuple (False,0) if guessed letter is not in phrase
		phrase_1 = Phrase("Song","Whitney Houston's I Will Always Love You")
		self.assertEqual(phrase_1.guess_letter('x'),(False,0))
		# Test that function returns tuple (True,guessed_letters) if letter is correctly guessed 
		phrase_2 = Phrase("Title","Dr. Quinn Medicine Woman")
		self.assertEqual(phrase_2.guess_letter('n'),(True,4))
		# Test that instance variables are correctly updated after correctly guessing letter
		phrase_3 = Phrase("Film","Pulp Fiction")
		phrase_3.guess_letter('p')
		self.assertEqual(phrase_3.blanked,"P__p _______")
		self.assertEqual(phrase_3.guessed,'p')
		self.assertEqual(phrase_3.vowels_unguessed,"iou")
		# Test that "vowels_unguessed" variable correctly changes after correct guess
		phrase_4 = Phrase("Film","Hachi: A Dog's Tale")
		phrase_4.blanked = "Ha_hi: A ___'_ _a_e"
		phrase_4.guessed = "pbahrei"
		phrase_4.vowels_unguessed = "o"
		phrase_4.guess_letter('O')
		self.assertEqual(phrase_4.blanked,"Ha_hi: A _o_'_ _a_e")
		self.assertEqual(phrase_4.guessed,"pbahreio")
		self.assertEqual(phrase_4.vowels_unguessed,"")

	def test_guess_letter_numerical_values(self):
		# Test TypeError is raised if input has more than 1 character
		self.assertRaises(TypeError, Phrase.guess_letter,"ab")

	def test_guess_phrase(self):
		# Test that method returns True when phrase is correctly guessed
		phrase_1 = Phrase("Headline","Madonna Gives Birth To A Baby Girl")
		self.assertEqual(phrase_1.guess_phrase("Madonna Gives Birth To A Baby Girl"),True)
		# Test that method returns None when phrase is not correctly guessed
		phrase_2 = Phrase("Things","Espresso Cappuccino & Decaf Coffee")
		self.assertEqual(phrase_2.guess_phrase("Expresso Cappuccino & Decaf Coffee"),None)
		# Test that "blanked" variable is correctly updated if phrase is correctly guessed
		phrase_3 = Phrase("Nickname","The Land Of Plenty")
		phrase_3.guess_phrase("The Land Of Plenty")
		self.assertEqual(phrase_3.blanked,"The Land Of Plenty")

class TestPlayer(unittest.TestCase):
	def test_initial_value(self):
		# Test instance variables are correctly initialized
		player = Player("Carmen")
		self.assertEqual(player.name,"Carmen")
		self.assertEqual(player.money,0)
		self.assertEqual(player.prizes,[])

	def test_bankrupt(self):
		# Test "money" variable is correctly updated and "prizes" variable remains unchanged
		player = Player("Rosa")
		player.money = 100
		player.prizes = ["A brand new car!"]
		player.bankrupt()
		self.assertEqual(player.money,0)
		self.assertEqual(player.prizes,["A brand new car!"])

	def test_buy_vowel(self):
		# Test "money" variable is correctly updated and "prizes" variable remains unchanged
		player = Player("Nancy")
		player.money = 400
		player.prizes = ["A trip to Ann Arbor!"]
		player.buy_vowel()
		self.assertEqual(player.money, 150)
		self.assertEqual(player.prizes,["A trip to Ann Arbor!"])

	def test_guessed_letter(self):
		# Test "money" variable is correctly updated
		player_1 = Player("Jay")
		player_1.guessed_letter(amount=900,guessed_letters=3)
		self.assertEqual(player_1.money,2700)
		self.assertEqual(player_1.prizes,[])
		# Test passing default value (False) to "prizes" parameter has no additional effect
		player_2 = Player("Mitchel")
		player_2.guessed_letter(amount=400,guessed_letters=2,prize=False)
		self.assertEqual(player_2.money,800)
		self.assertEqual(player_2.prizes,[])
		# Test "prizes" vaable is correctly updated
		player_3 = Player("Phil")
		player_3.money = 750
		player_3.prizes = ["A trip to Ann Arbor!"]
		player_3.guessed_letter(amount=250,guessed_letters=1,prize="A brand new car!")
		self.assertEqual(player_3.money,1000)
		self.assertEqual(player_3.prizes,["A trip to Ann Arbor!","A brand new car!"])
	

		