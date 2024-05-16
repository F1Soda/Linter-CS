import unittest
import sys
import os

current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir + "/Scripts")

from Scripts.Tokenizer import Tokenizer
from Scripts.Utils import CustomList



class TestTokenizer(unittest.TestCase):
	def test_simple_line(self):
		line = "var a = 10;"
		tokenizer = Tokenizer(CustomList(repr(line)[1:-1]))
		self.assertEqual([x.value for x in tokenizer.tokens], ["var", " ", "a", " ", "=", " ", "10", ";"])

	def test_file_with_comments(self):
		with open("../TestFiles/Tokenizer/test_comments.cs", "r", encoding="utf-8") as f:
			tokenizer = Tokenizer(CustomList(repr(f.read())[1:-1]))
			self.assertEqual([x.value for x in tokenizer.tokens],
							 ["var", " ", "полезный", " ", "=", " ", "кусок", " ", "+", " ", "кода", ";", '\\n', '\\n'])


	def test_case(self):
		with open("../TestFiles/Tokenizer/test_case.cs", "r", encoding="utf-8") as f:
			tokenizer = Tokenizer(CustomList(repr(f.read())[1:-1]))
			pass



	def test_caseasas(self):
		with open("../TestFiles/Tokenizer/test_comments.cs", "r", encoding="utf-8") as f:
			tokenizer = Tokenizer(CustomList(repr(f.read())[1:-1]))
			self.assertEqual([x.value for x in tokenizer.tokens],
							 ["var", " ", "полезный", " ", "=", " ", "кусок", " ", "+", " ", "кода", ";", '\\n', '\\n'])