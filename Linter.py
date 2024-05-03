import sys

from Settings import Settings
from CSFile import CSFile
from Tokenizer import Token

# temporary
config_file_path = r'.EditorConfig'
cs_file_path = r'TestFiles/test2.cs'


class Mismatch:
	def __init__(self, category, line, index, message, mismatched_flag):
		self.category = category
		self.line = line
		self.index = index
		self.message = message
		self.mismatched_flag = mismatched_flag

	def __str__(self):
		first_part = f"index = {self.index} "
		second_part = f"Line : {self.line}"
		offset = len(first_part) + 7
		return first_part + second_part + "\n" + " " * (offset + self.index) + "^"

	def __repr__(self):
		return self.__str__()


class Linter:
	def __init__(self, settings: Settings):
		self.setts = settings
		self.mismatches = []
		self.file = None  # type: CSFile

	def change_format_rules(self, new_settings: Settings):
		self.setts = new_settings

	def analyze_file(self, file_path):
		with open(file_path, mode='r', encoding='utf8') as f:
			self.file = CSFile(f.read())
		self.print()

	def print(self):
		for token in self.file.tokenizer.tokens:  # type: Token
			if token.value == r'\n':
				print("", end="\n")
			if token.value == ' ':
				print(" ", end="")
			else:
				print(token, end="")


def main(arguments):
	""" Main program """
	# Code goes over here.
	linter = Linter(Settings([]))
	linter.analyze_file(arguments[0])
	return 0


if __name__ == "__main__":
	args = sys.argv[1:]
	if len(args) == 0:
		main([cs_file_path, config_file_path])
	else:
		main(args)
