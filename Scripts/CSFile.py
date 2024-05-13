import enum
from Utils import CustomStr, CustomList
from Tokenizer import Tokenizer


class Namespaces(enum.Enum):
	Absent = 0
	ForEntireFile = 1  # это когда namespace name;


class CSFile:
	def __init__(self, file):
		self.orig = CustomStr(file)
		self.tokenizer = Tokenizer(CustomList(repr(file)[1:-1]))

		temp = file.split("\n")
		self.line_count = len(temp)
		self.lines = []
		for i in range(self.line_count):
			self.lines.append(repr(temp[i])[1:-1])
		self.type_namespace = Namespaces.Absent

	def __getitem__(self, index):
		return self.lines[index]

	def __setitem__(self, index, value):
		self.lines[index] = value
