import enum
from Utils import CustomStr, CustomList
from Tokenizer import Tokenizer
from Settings import Settings


class Namespaces(enum.Enum):
	Absent = 0
	ForEntireFile = 1  # это когда namespace name;


class CSFile:
	def __init__(self, path_to_file, settings: Settings):
		self.file_path = path_to_file
		self.settings = settings
		with open(path_to_file, mode='r', encoding='utf8') as f:
			data = f.read()
			temp = data.split("\n")
			self.line_count = len(temp)
			self.lines = []
			for i in range(self.line_count):
				self.lines.append(repr(temp[i])[1:-1])
			self.orig = CustomStr(data)
			self.tokenizer = Tokenizer(CustomList(repr(data)[1:-1]), self.settings, self.lines)

		self.type_namespace = Namespaces.Absent

	def __getitem__(self, index):
		return self.lines[index]

	def __setitem__(self, index, value):
		self.lines[index] = value
