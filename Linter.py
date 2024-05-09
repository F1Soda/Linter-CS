import sys

from Settings import Settings
from Utils import CustomList
from CSFile import CSFile
from Tokenizer import Token
from Flag import CategoryStyleRule
import networkx as nx

# temporary
config_file_path = r'.EditorConfig'  # не используется
cs_file_path = r'TestFiles/Linter/test2.cs'


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

	def analyze(self, conditional=None):
		'''
		Анализирует последовательно блоки. Может быть вызван вложено несколько раз
		:param conditional: Значение токена, при котором прекращается анализ
		:return:
		'''
		token = self.tokens[self.index_token]
		while self.index_token < len(self.tokens) and (
			conditional is None or token.value != conditional):  # type: Token
			found = False

			self._check_offset()  # Предполагается, что в этот момент token -- первый токен в строчке
			for graph in self.graphs:  # type: nx.DiGraph
				if graph.nodes[0]["data"] == token.value:
					self.check_tokens_by_graph(graph)
					found = True
					self.index_token += 1
			if not found:
				self._check_line()
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
		while self.index_token < len(self.tokens):
			found = False

			next_nodes = self._direct_successors(graph, index_node)
			if next_nodes == []:
				return
			token_to_check = self.tokens[self.index_token]
			for next_node_id in next_nodes:
				neighbor = graph.nodes[next_node_id]
				data = neighbor["data"]
				# TODO: Возможно как то можно упростить повторяющиеся блоки кода?
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
				if data == "line":
					self._check_line()
					found = True
					index_node = next_node_id
					break
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
				if data == "block":
					self.analyze(conditional="}")
					found = True
					index_node = next_node_id
					break
				if token_to_check.value == r"\n":
					found = True
					self.index_token += 1
					self._check_offset()
					break

			if not found:
				expected = graph.nodes[next_nodes[0]]["data"]
				self._append_mismatch(token=token_to_check, expected=expected)
				if token_to_check.value.isspace():
					self.index_token += 1
				else:
					index_node = next_nodes[0]

	def _check_expression(self):
		'''
		Проверяет, что выражение соответствует правилам.
		Пока правило одно: больше двух пробелов между токенами быть не может
		Выражение -- то что обычно заключено в скобках
		:return:
		'''
		token = self.tokens[self.index_token]  # type: Token
		count_spaces = 0
		while token.value != ")":
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

	def _check_line(self):
		'''
		Проверяет строчку, если ни один из графов не подошел. Предполагается, что это строчки вызова функции,
		присваивания переменной и прочее.
		:return:
		'''
		token = self.tokens[self.index_token]  # type: Token
		if token.value == "\\n":
			self.index_token += 1
			return

		# TODO: реализовать. Пока он просто по токенам бежит
		while token.value != ";":
			self.index_token += 1
			token = self.tokens[self.index_token]

		# Проверка что после ';' идёт новая строка, а не ещё что то
		self.index_token += 1
		token = self.tokens[self.index_token]
		while True:
			if token.value.isspace() or token.value == "\\t":
				self._append_mismatch(token, expected="\\n")
				self.index_token += 1
				token = self.tokens[self.index_token]
			elif token.value == "\\n":
				self.index_token += 1
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


def main(arguments):
	""" Main program """
	linter = Linter(Settings([]))
	linter.analyze_file(arguments[0])
	for miss in linter.mismatches:
		print(miss)
	return 0


if __name__ == "__main__":
	args = sys.argv[1:]
	if len(args) == 0:
		main([cs_file_path, config_file_path])
	else:
		main(args)
