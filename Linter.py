import argparse
import networkx as nx

from Settings import Settings
from Utils import CustomList
from CSFile import CSFile
from Tokenizer import Token
from Flag import CategoryStyleRule

# temporary
config_file_path = r'.EditorConfig'  # не используется
cs_file_path = r'TestFiles/Linter/test3.cs'


class Mismatch:
	def __init__(self, category: CategoryStyleRule, line: int, index: int, message: str, mismatched_flag):
		self.category = category
		self.line = line
		self.index = index
		self.message = message
		self.mismatched_flag = mismatched_flag

	def __str__(self):
		first_part = f"index = {self.index} "
		second_part = f"Line : {self.line}"
		offset = len(first_part) + 7
		return first_part + second_part + "\n" + " " * (offset + self.index) + "^" + "\n" + self.message

	def __repr__(self):
		return self.__str__()


class Linter:
	def __init__(self, settings: Settings):
		self.setts = settings
		self.mismatches = []
		self.graphs = []
		self._parse_graphs()
		self.index_token = 0
		self.tokens = CustomList()
		self.current_offset = 0
		# TODO: Я сейчас написал специальный класс для хранения данных о файле, который возможно можно просто сократить
		#  до списка токенов
		self.file = None  # type: CSFile

	def _parse_graphs(self):
		'''
		Записывает все графы в список графов для проверки кода. Пока добавление правил происходит вручную
		:return:
		'''
		self.graphs.append(nx.DiGraph(nx.convert_node_labels_to_integers(nx.read_gml("Graphs/if.gml"))))
		self.graphs.append(nx.DiGraph(nx.convert_node_labels_to_integers(nx.read_gml("Graphs/just_block.gml"))))
		self.graphs.append(nx.DiGraph(nx.convert_node_labels_to_integers(nx.read_gml("Graphs/switch.gml"))))
		self.graphs.append(nx.DiGraph(nx.convert_node_labels_to_integers(nx.read_gml("Graphs/case.gml"))))
		self.graphs.append(nx.DiGraph(nx.convert_node_labels_to_integers(nx.read_gml("Graphs/while.gml"))))

	def change_format_rules(self, new_settings: Settings):
		self.setts = new_settings

	def analyze_file(self, file_path):
		'''
		Анализирует весь файл
		:param file_path: путь до файла
		:return:
		'''
		with open(file_path, mode='r', encoding='utf8') as f:
			self.file = CSFile(f.read())
		self.tokens = self.file.tokenizer.tokens
		self.analyze()

	def analyze(self, conditionals=None):
		'''
		Анализирует последовательно блоки. Может быть вызван вложено несколько раз
		:param conditionals: Список значений токенов, при которых прекращается анализ
		:return:
		'''
		if conditionals is None:
			conditionals = []
		was_enter = False
		token = self.tokens[self.index_token]
		while self.index_token < len(self.tokens):
			# if token.value in conditionals:
			# 	break
			if (self.index_token != len(self.tokens) - 1 and token.value == r"\n"
				and self.tokens[self.index_token + 1].value == r"\t"):
				temp_index = self.index_token + 1
				while self.tokens[temp_index].value == r"\t":
					temp_index += 1
				if self.tokens[temp_index].value in conditionals:
					break

			if self.tokens[self.index_token - 1].value == r"\n" and token.value != r"\n":
				self._check_offset()
				token = self.tokens[self.index_token]

			found = False
			# self._check_offset() # Предполагается, что в этот момент token -- первый токен в строчке

			if token.value in conditionals:
				break

			for graph in self.graphs:  # type: nx.DiGraph
				if graph.nodes[0]["data"] == token.value:
					self.check_tokens_by_graph(graph)
					found = True
					self.index_token += 1
			if not found:
				self._check_line(conditionals=conditionals)
			token = self.tokens.at(self.index_token)

	def _direct_successors(self, graph, node):
		'''
		Вспомогательный метод, чтобы получить следующие вершины в ориентированном графе
		:param graph: Граф
		:param node: Вершина из которой исходят ребра
		:return:
		'''
		descendants = nx.descendants(graph, node)
		direct_successors = [n for n in descendants if graph.has_edge(node, n)]
		return direct_successors

	def check_tokens_by_graph(self, graph: nx.DiGraph):
		'''
		Проверяет последовательность токенов по графу.
		Предполагается что помимо токенов в графе присутствуют кодовые слова, как block или line, для которых определены
		специальные действия
		:param graph: граф для сравнения правил и кода
		:return:
		'''
		self.index_token += 1
		index_node = 0
		# tabs_row = 0
		was_enter = False
		while self.index_token < len(self.tokens):
			found = False

			next_nodes = self._direct_successors(graph, index_node)
			if next_nodes == []:
				self.index_token -= 1
				return
			token_to_check = self.tokens[self.index_token]

			for next_node_id in next_nodes:
				neighbor = graph.nodes[next_node_id]
				data = neighbor["data"]
				# TODO: Возможно как то можно упростить повторяющиеся блоки кода

				if data == "increase_offset":
					self.current_offset += 1
					found = True
					index_node = next_node_id
					break
				if data == "decrease_offset":
					self.current_offset -= 1
					found = True
					index_node = next_node_id
					break
				if data != "increase_offset" and data != "decrease_offset" and token_to_check.value == r"\t":
					temp_index = self.index_token
					while self.tokens[temp_index].value == r"\t":
						temp_index += 1
					if token_to_check.value == r"\t" and data == self.tokens[temp_index].value:
						if self.tokens[self.index_token - 1].value == r"\n" and token_to_check.value != r"\n":
							self._check_offset()
							token_to_check = self.tokens[self.index_token]

				if token_to_check.value == data:
					index_node = next_node_id
					self.index_token += 1
					found = True
					break
				if data == "expression":
					self._check_expression()
					found = True
					index_node = next_node_id
					break
				if data == "caseList":
					while self.tokens[self.index_token].value == 'case':
						self.analyze(conditionals=["default", "}"])
					found = True
					index_node = next_node_id
					break
				if data == "identifier":
					index_node = next_node_id
					self.index_token += 1
					found = True
					break
				if data == "line":
					self._check_line()
					found = True
					index_node = next_node_id
					break
				if data == "block":
					self.analyze(conditionals=["}"])
					found = True
					index_node = next_node_id
					break
				if data == "caseBlock":
					self.analyze(conditionals=["break"])
					found = True
					index_node = next_node_id
					break
				# if token_to_check.value == r"\n":
				# 	found = True
				# 	self.index_token += 1
				# 	self._check_offset()
				# 	break

			if self.tokens[self.index_token - 1].value == r"\n" and self.tokens[self.index_token].value != r"\n":
				self._check_offset()
				token_to_check = self.tokens[self.index_token]
			if not found:
				expected = graph.nodes[next_nodes[0]]["data"]
				self._append_mismatch(token=token_to_check, expected=expected)
				if token_to_check.value.isspace() or token_to_check.value == r"\n":
					self.index_token += 1
				else:
					# self.index_token += 1
					index_node = next_nodes[0]

	def _check_expression(self, conditionals=None):
		'''
		Проверяет, что выражение соответствует правилам.
		Пока правило одно: больше двух пробелов между токенами быть не может
		Выражение -- то что обычно заключено в скобках
		:return:
		'''
		if conditionals is None:
			conditionals = []

		token = self.tokens[self.index_token]  # type: Token
		count_spaces = 0
		symbol_index = 0
		while not ((token.value == ")" or token.value == ";" or token.value == ":")
			and self.tokens[self.index_token + 1].value == r"\n"):
			if token.value in conditionals:
				break
			# Проверка на пробел в начале
			if symbol_index == 0 and token.value.isspace():
				self._append_mismatch(token, "Not white Space")
			# Проверка на пробел между элементами
			# TODO: не работает на составных операциях типа ==, <=
			if (not token.value.isspace() and not self.tokens[self.index_token + 1].value.isspace()
				and self.tokens[self.index_token + 1].value != ":"
				and self.tokens[self.index_token + 1].value != ")"
				and self.tokens[self.index_token + 1].value != ";"
				and self.tokens[self.index_token + 1].value != "."
				and self.tokens[self.index_token].value != "."
				and self.tokens[self.index_token].value != "("
				and self.tokens[self.index_token].value != "\\t"):
				self._append_mismatch(token, "Need white Space")

			if token.value.isspace() or token.value == "\\t":
				count_spaces += 1
			elif token.value == "\\n":
				self._append_mismatch(token, "Not New Line")
			else:
				count_spaces = 0
			if count_spaces > 1:
				self._append_mismatch(token, "Not white Space")
			self.index_token += 1
			token = self.tokens[self.index_token]
			symbol_index += 1
			# Проверка на пробел в конце
			if (token.value == ":" or token.value == ")" or token.value == ";") and self.tokens[
				self.index_token - 1].value.isspace():
				self._append_mismatch(self.tokens[self.index_token - 1], "Not white Space")

	def _check_line(self, conditionals=None):
		'''
		Проверяет строчку, если ни один из графов не подошел. Предполагается, что это строчки вызова функции,
		присваивания переменной и прочее.
		:return:
		'''
		if conditionals is None:
			conditionals = []

		token = self.tokens[self.index_token]  # type: Token
		if token.value == "\\n":
			self.index_token += 1
			return

		# TODO: реализовать. Пока он просто по токенам бежит
		# while token.value != ";":
		# 	self.index_token += 1
		# 	token = self.tokens[self.index_token]]
		# Пока сделал так, чтобы работало
		self._check_expression(conditionals=conditionals)
		token = self.tokens[self.index_token]

		# Чтобы не залез на нужные токены
		if token.value in conditionals:
			return
		# Проверка что после ';' идёт новая строка, а не ещё что то
		self.index_token += 1
		token = self.tokens[self.index_token]
		while True:
			if token.value.isspace() or token.value == "\\t":
				self._append_mismatch(token, expected="\\n")
				self.index_token += 1
				token = self.tokens[self.index_token]
			elif token.value == "\\n":
				# self.index_token += 1
				break
			else:
				break

	def _check_offset(self):
		'''
		Проверяет количество отступов в строчке
		# TODO: проверят пока только количество символов табуляции, нужно и для пробела сделать
		:return:
		'''
		count_offsets = 0
		token = self.tokens[self.index_token]  # type: Token
		while token.value == '\\t':
			if token.value == '\\t':
				count_offsets += 1
			if count_offsets > self.current_offset:
				self._append_mismatch(token, "less offset")
			self.index_token += 1
			token = self.tokens[self.index_token]
		if count_offsets < self.current_offset:
			self._append_mismatch(token, "more offset")

	def _append_mismatch(self, token: Token, expected: str):
		self.mismatches.append(Mismatch(CategoryStyleRule.CR, self.file.lines[token.line_index - 1], token.start_index,
										f"Expected '{expected}', but was '{token.value}'\n", None))

	def print(self):
		'''
		Красиво принтует в консоль работу токенайзера
		# TODO: перенсти в токенайзер
		:return:
		'''
		for token in self.file.tokenizer.tokens:  # type: Token
			if token.value == r'\n':
				print("", end="\n")
			if token.value == ' ':
				print(" ", end="")
			else:
				print(token, end="")
		print()


def main():
	""" Main program """
	parser = argparse.ArgumentParser(description='Linter для C#')

	parser.add_argument("-f", "--file",
						help="Путь до CS файла(Если ничего не указать, запустится один из заготовленных)", type=str,
						nargs='?', default="")
	parser.add_argument("-conf", "--config", help="Путь до файла .EditorConfig(Пока не работает)", type=str, nargs='?',
						default="TestFiles/Linter/test1.cs")
	parser.add_argument("-sf", "--save_file", help="Путь, куда сохранять. По умолчанию в файл mismatches.txt", type=str,
						nargs='?',
						default="mismatches.txt")
	parser.add_argument("-p", "--print", help="Вывести результат в консоль", action="store_true")

	args = parser.parse_args()

	linter = Linter(Settings([]))

	if args.file:
		linter.analyze_file(args.file)
	else:
		linter.analyze_file(cs_file_path)

	if args.save_file:
		with open(args.save_file, "w") as f:
			for miss in linter.mismatches:
				if args.print:
					print(miss)
				f.write(f"{miss}\n")

	return 0


if __name__ == "__main__":
	main()
# args = sys.argv[1:]
# if len(args) == 0:
#	main([cs_file_path, config_file_path])
# else:
#	main(args)
