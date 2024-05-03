import enum
from Utils import CustomList

# TODO: Пока токенайзер работает с файлами без комментариев

keywords = ['abstract', 'as', 'base', 'bool', 'break', 'byte', 'case', 'catch', 'char', 'checked', 'class', 'const',
			'continue', 'decimal', 'default', 'delegate', 'do', 'double', 'else', 'enum', 'event', 'explicit', 'extern',
			'false', 'finally', 'fixed', 'float', 'for', 'foreach', 'goto', 'if', 'implicit', 'in', 'int', 'interface',
			'internal', 'is', 'lock', 'long', 'namespace', 'new', 'null', 'object', 'operator', 'out', 'override',
			'params', 'private', 'protected', 'public', 'readonly', 'ref', 'return', 'sbyte', 'sealed', 'short',
			'sizeof', 'stackalloc', 'static', 'string', 'struct', 'switch', 'this', 'throw', 'true', 'try', 'typeof',
			'uint', 'ulong', 'unchecked', 'unsafe', 'ushort', 'using', 'virtual', 'void', 'volatile', 'while']

# TODO: Я короче ленивая жопа и потому механизм ? : просто сюда вставлю пока ↓
punctuations = [';', ':', ',', '.', '(', ')', '[', ']', '{', '}', '<', '>', '?']

# TODO: И ещё не работает ++ и --. Парсятся как '-','-'
operators = ['+', '-', '*', '/', '%', '=', '>>', '<<', '&', '&&', '|', '||', '!', '^', '>', '>=', '<', '<=', '==', '!=',
			 '~', '+=', '-=', '/=', '*=', '%=', '++', '--']

backslash_character_literals = [r'\n', r'\r', r'\f', r'\t', r'\a', r'\b', r'\o', r'\v', r'\\', r"\'", r'\"']

number_postfixes = ['f', 'l', 'd']


class KindToken(enum.Enum):
	identifier = 0
	keyword = 1
	literal = 2  # Аналог expression
	operator = 3
	punctuation = 4
	whiteSpace = 5
	none = None


class Token:
	def __init__(self, start_index: int, line_index: int, value: str, kind=KindToken.none):
		self.start_index = start_index
		self.line_index = line_index
		self.value = value
		self.kind = kind if kind is not KindToken.none else self._define_kind_token()

	def _define_kind_token(self) -> KindToken:
		if self.value in keywords:
			return KindToken.keyword
		if self.value in punctuations:
			return KindToken.punctuation
		if self.value in operators:
			return KindToken.operator
		if '\'' in self.value or '"' in self.value or any(oper in self.value for oper in operators):
			return KindToken.literal
		if self.value.isspace():
			return KindToken.whiteSpace
		else:
			return KindToken.identifier

	def __str__(self):
		return self._str_v2()

	def __repr__(self):
		return self.__str__()

	def _str_v1(self):
		return f"'{self.value}' is {self.kind.name} token at {self.line_index} line, {self.start_index} char"
	def _str_v2(self):
		return f"'{self.value}'"


class Tokenizer:
	def __init__(self, rfile: CustomList):
		self.tokens = CustomList([])
		self.rfile = rfile
		self.abs_index_char = 0
		self.index_line = 1
		self.index_char = -1
		self.current_char = ""
		self.next_char = ""
		self._tokenize()

	def _tokenize(self):
		token = ""
		while self.abs_index_char < len(self.rfile):
			self._update_data()

			# Token
			if self.current_char.isalpha():
				token += self.current_char
				continue
			elif token != '':
				self.tokens.append(Token(self.index_char, self.index_line, token))
				token = ""

			if (self._check_white_spaces() or
				self._check_punctuation() or
				self._check_operators() or
				self._check_string_literal() or
				self._check_integer_literal()):
				continue

			raise Exception(
				"Undefined char = " +
				f'"{self.current_char}"\nLine was:' +
				f"...{''.join(self.rfile[self.abs_index_char - 10:self.abs_index_char + 10])}...")

	def _update_data(self):
		self.current_char = self.rfile[self.abs_index_char]
		self.next_char = self.rfile.at(self.abs_index_char + 1)
		self.index_char += 1
		self.abs_index_char += 1

	def _check_string_literal(self, nested=False):
		if self.current_char == '"' or self.current_char == "'":
			res = self._get_string_literal(self.current_char)
			if nested:
				return res
			self.tokens.append(Token(self.index_char, self.index_line, res))
			return True

		elif self.current_char == '$':
			index = self.index_char
			self._update_data()
			res = "$" + self._check_string_literal(nested=True)
			if nested:
				return res
			self.tokens.append(Token(index, self.index_line, res))
			return True

		elif self.current_char == '@':
			index = self.index_char
			self._update_data()
			res = "@" + self._check_string_literal(nested=True)
			if nested:
				return res
			self.tokens.append(Token(index, self.index_line, res))
			return True

		return False

	def _check_integer_literal(self) -> bool:
		if self.current_char.isdigit():
			self.tokens.append(Token(self.index_char, self.index_line, self._get_integer_literal()))
			return True
		return False

	def _check_operators(self) -> bool:
		if self.current_char in operators:
			self.tokens.append(Token(self.index_char, self.index_line, self.current_char))
			return True

		elif self.next_char is not None and self.current_char + self.next_char in operators:
			self.tokens.append(Token(self.index_char, self.index_line, self.current_char + self.next_char))
			self.abs_index_char += 1
			return True

		return False

	def _check_punctuation(self) -> bool:
		if self.current_char in punctuations:
			if self.current_char == '<' and self.next_char is not None and self.next_char == '<':
				self.tokens.append(Token(self.index_char, self.index_line, '<<'))
				self.abs_index_char += 1
				return True
			elif self.current_char == '>' and self.next_char is not None and self.next_char == '>':
				self.tokens.append(Token(self.index_char, self.index_line, '>>'))
				self.abs_index_char += 1
				return True
			else:
				self.tokens.append(Token(self.index_char, self.index_line, self.current_char))
				return True
		return False

	def _check_white_spaces(self) -> bool:
		if self.current_char.isspace():
			self.tokens.append(Token(self.index_char, self.index_line, self.current_char))
			return True
		elif self.next_char is not None:
			if self.current_char + self.next_char == r'\n':
				self.tokens.append(Token(self.index_char, self.index_line, self.current_char + self.next_char))
				self.index_line += 1
				self.index_char = -1
				self.abs_index_char += 1
				return True
			elif self.current_char + self.next_char in backslash_character_literals:
				self.tokens.append(Token(self.index_char, self.index_line, self.current_char + self.next_char))
				self.abs_index_char += 1
				self.index_char += 1
				return True
		return False

	def _get_string_literal(self, quote='"') -> str:
		literal = quote
		while True:
			self.current_char = self.rfile[self.abs_index_char]
			if self.current_char == quote:
				self.abs_index_char += 1
				return literal + quote
			literal += self.current_char
			self.abs_index_char += 1

	def _get_integer_literal(self) -> str:
		literal = self.rfile[self.abs_index_char - 1]
		while True:
			char = self.rfile[self.abs_index_char]  # type: str
			next_char = self.rfile.at(self.abs_index_char + 1)
			if char.isspace() or next_char is not None and char + next_char in backslash_character_literals:
				return literal
			if not char.isdigit() and char not in number_postfixes + ['E', 'e', '.']:
				return literal
			literal += char
			self.abs_index_char += 1
