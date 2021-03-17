import unittest
from wheel_of_fortune import Phrase, guess_letter

class TestPhrase(unittest.TestCase):
	def test_initial_value(self):
		# Test alphanumerical string
		phrase_1 = Phrase("Die Hard 2")
		self.assertEqual(phrase_1.phrase,"Die Hard 2")
		self.assertEqual(phrase_1.blanked ,"___ ____ _")
		self.assertEqual(phrase_1.guessed,"")
		self.assertEqual(phrase_1.has_vowels,True)
		# Test string with non-alphanumerical characters
		phrase_2 = Phrase("Spider-Man: Into the Spider-Verse")
		self.assertEqual(phrase_2.phrase,"Spider-Man: Into the Spider-Verse")
		self.assertEqual(phrase_2.blanked,"______-___: ____ ___ ______-_____")
		self.assertEqual(phrase_2.guessed,"")
		self.assertEqual(phrase_2.has_vowels,True)
		# Test string with only non-alphanbetical characters
		phrase_3 = Phrase("4.3.2.1.")
		self.assertEqual(phrase_3.phrase,"4.3.2.1.")
		self.assertEqual(phrase_3.blanked,"_._._._.")
		self.assertEqual(phrase_3.guessed,"")
		self.assertEqual(phrase_3.has_vowels,False)
		# Test empty string
		phrase_4 = Phrase("")
		self.assertEqual(phrase_4.phrase,"")
		self.assertEqual(phrase_4.blanked,"")
		self.assertEqual(phrase_4.guessed,"")
		self.assertEqual(phrase_4.has_vowels,False)

	def test_ascii_values(self):
		# Make sure ValueError are raised when string has non-ascii characters 
		self.assertRaises(ValueError, Phrase, "後來的我們") 


class TestGuessLetter(unittest.TestCase):
	def test_guess_letter(self):
		phrase_1 = Phrase("Whitney Houston's I Will Always Love You")
		self.assertEqual(guess_letter(phrase_1,'x'),False)

		phrase_2 = Phrase("Mission Impossible 3")
		guess_letter(phrase_2,'3')
		self.assertEqual(phrase_2.blanked,"_______ __________ 3")
		self.assertEqual(phrase_2.guessed,'3')
		self.assertEqual(phrase_2.has_vowels,True)

		phrase_3 = Phrase("Pulp Fiction")
		guess_letter(phrase_3,'p')
		self.assertEqual(phrase_3.blanked,"P__p _______")
		self.assertEqual(phrase_3.guessed,'p')
		self.assertEqual(phrase_3.has_vowels,True)

		phrase_4 = Phrase("Hachi: A Dog's Tale")
		phrase_4.blanked = "Ha_hi: A ___'_ _a_e"
		phrase_4.guessed = "pbahrei"
		phrase_4.has_vowels = True
		guess_letter(phrase_4,'O')
		self.assertEqual(phrase_4.blanked,"Ha_hi: A _o_'_ _a_e")
		self.assertEqual(phrase_4.guessed,"pbahreio")
		self.assertEqual(phrase_4.has_vowels,False)