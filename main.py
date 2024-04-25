import sys
import editorconfig
import enum

# temporary
config_file_path = r'C:\Users\TIm\PycharmProjects\linter\.EditorConfig'
cs_file_path = r'C:\Users\TIm\PycharmProjects\linter\Program.cs'

def example():
	def get_all_editorconfig_flags(file_path):
		config = editorconfig.get_properties(file_path)

		flags = []
		for key, value in config.items():
			flags.append(f"{key} = {value}")

		return flags

	all_flags = get_all_editorconfig_flags(config_file_path)

	# for flag in all_flags:
	#     print(flag)

	with open(cs_file_path, mode='r', encoding='utf8') as f:
		counter = 1
		for line in f:
			print(f"{counter:>{2}} {repr(line)}")
			counter += 1

class CategoryStyleRule(enum.Enum):
	LanguageAndUnnecessaryCodeRules = 0
	FormattingRules = 1
	NamingRules = 2
	OtherRules = 3


class Mismatch:
	def __init__(self, category, line, index, message, mismatched_flag):
		self.category = category
		self.line = line
		self.index = index
		self.message = message
		self.mismatched_flag = mismatched_flag


class Linter:
	def __init__(self, rules_flags):
		self.flags = rules_flags
		self.mismatches = []

	def change_rules(self, new_flags):
		self.flags = new_flags

	def analyze_file(self, file_path):
		with open(file_path, mode='r', encoding='utf8') as f:
			for line in f:
				self.analyze_line(line)

	def analyze_line(self, line):
		# Вот это нужно сделать!
		pass


def main(args):
	""" Main program """
	# Code goes over here.
	print(args)
	return 0


if __name__ == "__main__":
	args = sys.argv[1:]
	if (len(args) == 0):
		main([cs_file_path, config_file_path])
	else:
		main(args)
