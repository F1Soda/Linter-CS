import argparse
import networkx as nx
import enum

from Settings import Settings
from Utils import CustomList
from CSFile import CSFile
from Tokenizer import Token, KindToken
from Flag import CategoryStyleRule

# temporary
config_file_path = r'../data/.EditorConfig'  # не используется
cs_file_path = r'../TestFiles/Linter/test3.cs'
modifiers = [['public', 'private', 'protected', 'internal', 'protected internal', 'private protected', 'file'],
			 ['abstract', 'virtual'],
			 ['static'], ['sealed'], ['override'], ['new'], ['extern'], ['unsafe'], ['readonly'], ['volatile']]


class Graphs(enum.Enum):
	if_ = "if"
	switch_ = "switch"
	just_block_ = "just_block"
	case_ = "case"


class Mismatch:
	def __init__(self, category: CategoryStyleRule, line: int, index: int, index_line: int, message: str,
				 mismatched_flag):
		self.category = category
		self.line = line
		self.index = index
		self.index_line = index_line
		self.message = message
		self.mismatched_flag = mismatched_flag

	def __str__(self):
		first_part = f"index = {self.index} "
		second_part = f"Line {self.index_line}: {self.line}"
		offset = len(first_part) + 7
		return first_part + second_part + "\n" + " " * (offset + self.index) + "^" + "\n" + self.message

	def __repr__(self):
		return self.__str__()


class Linter:
	def __init__(self, settings: Settings):
		self.setts = settings
		self.mismatches = []
		self.graphs = {}
		self._parse_graphs()
		self.index_token = 0
		self.tokens = CustomList()
		self.current_offset = 0
		self.prev_modifier_id = -1
		# TODO: Я сейчас написал специальный класс для хранения данных о файле, который возможно можно просто сократить
		#  до списка токенов
		self.file = None  # type: CSFile
		self._keywords_to_func = {
			"expression": lambda: self._check_expression_new(),
			"switch_block": lambda: self._check_switch_block(),
			"identifier": lambda: self._increment("index_token", self.index_token),
			"line": lambda: self._check_line(),
			"block": lambda: self.analyze(conditionals=["}"]),
			"just_block": lambda: self.check_tokens_by_graph(graph=nx.DiGraph(nx.convert_node_labels_to_integers(nx.read_gml(
			"../Graphs/Standarts/just_block.gml")))),
			"case_block": lambda: self.analyze(conditionals=["break", "return"]),  # TODO: еще нужно рассмотреть case
			"increase_offset": lambda: self._increment("current_offset", self.current_offset),
			"decrease_offset": lambda: self._decrement("current_offset", self.current_offset)
		}

	def _call_func_by_keyword(self, name: str, args):
		self._keywords_to_func[name](**args)

	# дурацкий питон
	def _increment(self, name: str, value):
		self.__setattr__(name, value + 1)

	def _decrement(self, name: str, value):
		self.__setattr__(name, value - 1)

	def _parse_graphs(self):
		'''
		Записывает все графы в список графов для проверки кода. Пока добавление правил происходит вручную
		:return:
		'''
		self.graphs[Graphs.if_] = nx.DiGraph(nx.convert_node_labels_to_integers(nx.read_gml(
			"../Graphs/Standarts/if.gml")))
		self.graphs[Graphs.just_block_] = nx.DiGraph(
			nx.convert_node_labels_to_integers(nx.read_gml("../Graphs/Standarts/just_block.gml")))
		self.graphs[Graphs.switch_] = nx.DiGraph(
			nx.convert_node_labels_to_integers(nx.read_gml("../Graphs/Standarts/switch.gml")))
		self.graphs[Graphs.case_] = nx.DiGraph(nx.convert_node_labels_to_integers(nx.read_gml(
			"../Graphs/Standarts/case.gml")))

	# self.graphs[Graphs.case_] = nx.DiGraph(nx.convert_node_labels_to_integers(nx.read_gml(
	# 	"../Graphs/Standarts/while.gml")))

	def change_format_rules(self, new_settings: Settings):
		self.setts = new_settings

	def get_modifier_id(self):
		for i, row in enumerate(modifiers):
			if self.tokens[self.index_token].value in row:
				return i

	def check_modifiers(self):
		# Проверка порядка
		curr_id = self.get_modifier_id()
		if self.prev_modifier_id != -1:
			if curr_id < self.prev_modifier_id:
				self._append_mismatch(self.tokens[self.index_token], "Wrong modifiers order")

		self.prev_modifier_id = curr_id

		# Проверка на пробелы
		space_count = 0
		while self.tokens[self.index_token + 1].value.isspace():
			self.index_token += 1
			space_count += 1
			if space_count > 1:
				self._append_mismatch(self.tokens[self.index_token], "Not white Space")

		if space_count == 0:
			self._append_mismatch(self.tokens[self.index_token], "white space")

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
		while self.index_token < len(self.tokens):

			found = False
			token = self.tokens[self.index_token]
			if token.value == r"\n":
				self.index_token += 1
				if token.value == r"\t":
					self._check_offset()
				else:
					continue
			if token.value == r"\t":
				self._check_offset()
			token = self.tokens[self.index_token]
			if token.value in conditionals:
				return

			# Проверка на модификаторы
			if any(token.value in modifier_list for modifier_list in modifiers):
				self.check_modifiers()
				self.index_token += 1
				continue
			else:
				self.prev_modifier_id = -1

			for graph in self.graphs.values():  # type: nx.DiGraph
				for start_node_index in self._get_start_nodes(graph):
					if graph.nodes[start_node_index]["data"] == token.value:
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

	def _get_start_nodes(self, graph) -> []:
		'''
		Возвращает начальные вершины графа, то есть вершины без входящих рёбер
		:param graph: Граф
		:return:
		'''
		isolated_nodes = [node for node in graph.nodes() if not list(graph.predecessors(node))]
		return isolated_nodes

	def check_tokens_by_graph(self, graph: nx.DiGraph):
		'''
		Проверяет последовательность токенов по графу.
		Предполагается что помимо токенов в графе присутствуют кодовые слова, как block или line, для которых определены
		специальные действия
		:param graph: граф для сравнения правил и кода
		:return:
		'''

		index_node = 0
		for index_start_node in self._get_start_nodes(graph):
			if self.tokens[self.index_token].value == graph.nodes[index_start_node]["data"]:
				index_node = index_start_node
				break
		self.index_token += 1
		while self.index_token < len(self.tokens):
			found = False

			next_nodes = self._direct_successors(graph, index_node)
			if next_nodes == []:
				return
			token_to_check = self.tokens[self.index_token]
			for next_node_id in next_nodes:
				neighbor = graph.nodes[next_node_id]
				data = neighbor["data"]
				if data in self._keywords_to_func:
					res = self._keywords_to_func[data]()
					found = True
					index_node = next_node_id
				elif token_to_check.value == data:
					index_node = next_node_id
					self.index_token += 1
					if data == "\\n":
						self._check_offset()
					if data == ";":
						self._check_new_line_after_semicolon()
					found = True
				elif token_to_check.value == r"\n":
					found = True
					self.index_token += 1
					self._check_offset()


			if not found:
				expected = graph.nodes[next_nodes[0]]["data"]
				self._append_mismatch(token=token_to_check, expected=expected)
				if token_to_check.value.isspace():
					self.index_token += 1
				else:
					# self.index_token += 1
					index_node = next_nodes[0]

	def _check_expression(self, conditionals=None):
		token = self.tokens[self.index_token]  # type: Token
		count_spaces = 0
		while token.value != ")" and token.value != ":" and token.value != ";":
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

	def _check_expression_new(self, conditionals=None):
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
			if (self.conditions_for_space()):
				self._append_mismatch(token, "white Space")

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

	def conditions_for_space(self):
		current_token = self.tokens[self.index_token]
		next_token = self.tokens[self.index_token + 1] if self.index_token + 1 < len(self.tokens) else None

		if current_token and next_token:
			current_kind = current_token.kind
			next_kind = next_token.kind

			if (current_kind == KindToken.operator and next_kind == KindToken.identifier) or \
					(current_kind == KindToken.operator and next_kind == KindToken.keyword) or \
					(current_kind == KindToken.keyword and next_kind == KindToken.operator) or \
					(current_kind == KindToken.identifier and next_kind == KindToken.operator) or \
					(current_kind == KindToken.literal and next_kind == KindToken.operator) or \
					(current_kind == KindToken.operator and next_kind == KindToken.literal):
				return True
		return False

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
			self._check_offset()
			return

		# TODO: реализовать. Пока он просто по токенам бежит
		self._check_expression_new(conditionals=conditionals)
		# while token.value != ";":
		# 	self.index_token += 1
		# 	token = self.tokens[self.index_token]
		self.index_token += 1
		self._check_new_line_after_semicolon()

	def _check_new_line_after_semicolon(self):
		token = self.tokens[self.index_token]
		while token.kind == KindToken.whiteSpace:
			if token.value != r'\n':
				self._append_mismatch(token, expected="new line")
				self.index_token += 1
				token = self.tokens[self.index_token]
			else:
				return
		self._append_mismatch(token, expected="new line")

	def _check_offset(self):
		'''
		Проверяет количество отступов в строчке
		# TODO: проверят пока только количество символов табуляции, нужно и для пробела сделать
		:return:
		'''

		count_offsets = 0
		token = self.tokens[self.index_token]  # type: Token
		if token.value == "\\n":
			self.index_token += 1
			return

		while token.value == '\\t':
			if token.value == '\\t':
				count_offsets += 1
			if count_offsets > self.current_offset:
				self._append_mismatch(token, "less offset")
			self.index_token += 1
			token = self.tokens[self.index_token]
		if count_offsets < self.current_offset:
			self._append_mismatch(token, "more offset")

	def _check_switch_block(self):
		while self.index_token < len(self.tokens):
			token = self.tokens[self.index_token]
			if token.value == "case" or token.value == "default":
				self._roll_back(r'\n')
				self.index_token += 1
				self._check_offset()
				self.check_tokens_by_graph(self.graphs[Graphs.case_])
			if token.value == "}":
				break
			self.index_token += 1

	def _roll_back(self, token_value: str):
		while self.index_token > 0:
			if self.tokens[self.index_token].value == token_value:
				return
			self.index_token -= 1

	def _append_mismatch(self, token: Token, expected: str, qutie_expected=False):
		if qutie_expected:
			expected = f"'{expected}'"
		self.mismatches.append(
			Mismatch(CategoryStyleRule.CR, self.file.lines[token.line_index - 1], token.start_index, token.line_index,
					 f"Expected {expected}, but was '{token.value}'\n", None))

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

	testing = False

	if args.file:
		linter.analyze_file(args.file)
	else:
		testing = True
		linter.analyze_file(cs_file_path)

	if args.save_file:
		with open(args.save_file, "w") as f:
			for miss in linter.mismatches:
				if args.print:
					print(miss)
				f.write(f"{miss}\n")
	if testing:
		for miss in linter.mismatches:
			print(miss)

	return 0


if __name__ == "__main__":
	main()
