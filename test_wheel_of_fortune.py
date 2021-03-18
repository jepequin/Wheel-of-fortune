import unittest
from wheel_of_fortune import Phrase, Player

class TestPhrase(unittest.TestCase):
	def test_initial_value(self):
		# Test with alphanumerical strings 
		phrase_1 = Phrase(category="Film",phrase="Die Hard 2")
		self.assertEqual(phrase_1.category,"Film")
		self.assertEqual(phrase_1.phrase,"Die Hard 2")
		self.assertEqual(phrase_1.blanked ,"___ ____ _")
		self.assertEqual(phrase_1.guessed,"")
		self.assertEqual(phrase_1.has_vowels,True)
		# Test with strings containing non-alphanumerical characters
		phrase_2 = Phrase("Film","Spider-Man: Into the Spider-Verse")
		self.assertEqual(phrase_2.phrase,"Spider-Man: Into the Spider-Verse")
		self.assertEqual(phrase_2.blanked,"______-___: ____ ___ ______-_____")
		self.assertEqual(phrase_2.guessed,"")
		self.assertEqual(phrase_2.has_vowels,True)
		# Test with strings containing only non-alphanbetical characters
		phrase_3 = Phrase("Film","4.3.2.1.")
		self.assertEqual(phrase_3.phrase,"4.3.2.1.")
		self.assertEqual(phrase_3.blanked,"_._._._.")
		self.assertEqual(phrase_3.guessed,"")
		self.assertEqual(phrase_3.has_vowels,False)
		# Test with empty strings
		phrase_4 = Phrase("","")
		self.assertEqual(phrase_4.category,"")
		self.assertEqual(phrase_4.phrase,"")
		self.assertEqual(phrase_4.blanked,"")
		self.assertEqual(phrase_4.guessed,"")
		self.assertEqual(phrase_4.has_vowels,False)

	def test_ascii_values(self):
		# Test ValueError is raised when string has non-ascii characters 
		self.assertRaises(ValueError, Phrase, "Film","後來的我們") 

	def test_guess_letter(self):
		# Test that function returns False if guessed letter is not in phrase
		phrase_1 = Phrase("Song","Whitney Houston's I Will Always Love You")
		self.assertEqual(phrase_1.guess_letter('x'),False)
		# Test that instance variables are correctly updated after correctly guessing numerical character
		phrase_2 = Phrase("Film","Mission Impossible 3")
		phrase_2.guess_letter('3')
		self.assertEqual(phrase_2.blanked,"_______ __________ 3")
		self.assertEqual(phrase_2.guessed,'3')
		self.assertEqual(phrase_2.has_vowels,True)
		# Test that instance variables are correctly updated after correctly guessing letter
		phrase_3 = Phrase("Film","Pulp Fiction")
		phrase_3.guess_letter('p')
		self.assertEqual(phrase_3.blanked,"P__p _______")
		self.assertEqual(phrase_3.guessed,'p')
		self.assertEqual(phrase_3.has_vowels,True)
		# Test that "has_vowels" variable correctly changes from True to False
		phrase_4 = Phrase("Film","Hachi: A Dog's Tale")
		phrase_4.blanked = "Ha_hi: A ___'_ _a_e"
		phrase_4.guessed = "pbahrei"
		phrase_4.has_vowels = True
		phrase_4.guess_letter('O')
		self.assertEqual(phrase_4.blanked,"Ha_hi: A _o_'_ _a_e")
		self.assertEqual(phrase_4.guessed,"pbahreio")
		self.assertEqual(phrase_4.has_vowels,False)

class TestPlayer(unittest.TestCase):
	def test_initial_value(self):
		# Test instance variables are correctly initialized
		player = Player("Carmen")
		self.assertEqual(player.name,"Carmen")
		self.assertEqual(player.money,0)
		self.assertEqual(player.prize,[])

	def test_bankrupt(self):
		# Test "money" variable is correctly updated and "prize" variable remains unchanged
		player = Player("Rosa")
		player.money = 100
		player.prize = ["A brand new car!"]
		player.bankrupt()
		self.assertEqual(player.money,0)
		self.assertEqual(player.prize,["A brand new car!"])

	def test_buy_vowel(self):
		# Test "money" variable is correctly updated and "prize" variable remains unchanged
		player = Player("Nancy")
		player.money = 400
		player.prize = ["A trip to Ann Arbor!"]
		player.buy_vowel()
		self.assertEqual(player.money, 150)
		self.assertEqual(player.prize,["A trip to Ann Arbor!"])

	def test_guessed_letter(self):
		# Test "money" variable is correctly updated
		player_1 = Player("Jay")
		player_1.guessed_letter(amount=900,nb_letters=3)
		self.assertEqual(player_1.money,2700)
		self.assertEqual(player_1.prize,[])
		# Test passing default value (False) to "prize" parameter has no additional effect
		player_2 = Player("Mitchel")
		player_2.guessed_letter(amount=400,nb_letters=2,prize=False)
		self.assertEqual(player_2.money,800)
		self.assertEqual(player_2.prize,[])
		# Test "prize" vaable is correctly updated
		player_3 = Player("Phil")
		player_3.money = 750
		player_3.prize = ["A trip to Ann Arbor!"]
		player_3.guessed_letter(amount=250,nb_letters=1,prize="A brand new car!")
		self.assertEqual(player_3.money,1000)
		self.assertEqual(player_3.prize,["A trip to Ann Arbor!","A brand new car!"])
		