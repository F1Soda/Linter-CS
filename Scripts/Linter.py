import argparse
import networkx as nx
import enum
import os
import exceptions

from Settings import Settings
from Utils import CustomList
from CSFile import CSFile
from Tokenizer import Token, KindToken
from Flag import CategoryStyleRule

cs_file_path = r'TestFiles/Linter/Program.cs'
modifiers = [['public', 'private', 'protected', 'internal', 'protected internal', 'private protected', 'file'],
             ['abstract', 'virtual', 'record', 'partial'],
             ['static'], ['sealed'], ['override'], ['new'], ['extern'], ['unsafe'], ['readonly'], ['volatile']]


class Graphs(enum.Enum):
    """
    Класс Enum для работы со словарём self.graph, используется для нахождения по ключам
    """
    if_ = "if"
    else_ = "else"
    switch_ = "switch"
    just_block_ = "just_block"
    just_block_for_func_ = "just_block_for_func"
    just_block_for_new_ = "just_block_for_new"
    case_ = "case"
    while_ = "while"
    for_ = "for"
    foreach_ = "foreach"
    namespace_ = "namespace"
    do_while_ = "do_while"
    class_ = "class"
    enum_ = "enum"
    new_ = "new"
    try_catch_finally_ = "try_catch_finally"


class Mismatch:
    """
    Класс описания несовпадения в коде. Содержит категорию ошибку, строку, индекс в строке, сообщение
    """

    def __init__(self, category: CategoryStyleRule, line: str, index: int, index_line: int, message: str,
                 mismatched_flag, expected: str):
        self.category = category
        self.line = line
        self.index = index
        self.index_line = index_line
        self.message = message
        self.expected = expected
        self.mismatched_flag = mismatched_flag

    def __str__(self):
        first_part = f"index = {self.index} Line {self.index_line}: "
        offset = len(first_part)
        return first_part + self.line + "\n" + " " * (offset + self.index) + "^" + "\n" + self.message

    def __repr__(self):
        return self.__str__()


def _check_passage_allowed(graph: nx.DiGraph, index_node: int, next_node_id: int, res_of_keyword_func) -> bool:
    """
    Проверяет, что ребро открыто для прохода по нему
    :param graph: граф
    :param index_node: индекс стартовой ноды
    :param next_node_id: индекс следующей ноды
    :param res_of_keyword_func: результат работы прошлой функции
    :return: True, если разрешён проход и False в противном
    """
    condition = "default"
    if index_node != next_node_id:
        condition = graph[index_node][next_node_id]['condition']
    if condition == "True" and (res_of_keyword_func is not None and res_of_keyword_func != True):
        return False
    if condition == "False" and (res_of_keyword_func is not None and res_of_keyword_func != False):
        return False
    return True


def center_text(text, total_width):
    space = total_width - len(text)
    if space % 2 == 0:
        left_space = right_space = space // 2
    else:
        left_space = space // 2
        right_space = space // 2 + 1

    return '-' * left_space + text + '-' * right_space


class Linter:
    def __init__(self, settings: Settings, file_to_save_mismatches="None", print_to_console=False):
        self.setts = settings
        self.mismatches = []
        self.graphs = {}
        self.extension_graphs = {}
        self._parse_graphs()
        self.index_token = 0
        self.tokens = CustomList()
        self.current_offset = 0
        self.prev_modifier_id = -1
        self.file_to_save_mismatches = file_to_save_mismatches
        self.was_public_in_line = False
        self.was_private_in_line = False
        self.print_to_console = print_to_console
        self.file = None  # type: CSFile|None

        self._keywords_to_func = {
            "expression_)": lambda: self._check_expression(conditionals=[")"]),
            "expression_)_skip_first": lambda: self._check_expression(conditionals=[")"], skip_first_white_space=True),
            "expression_;": lambda: self._check_expression(conditionals=[";"]),
            "expression_;_skip_first": lambda: self._check_expression(conditionals=[";"], skip_first_white_space=True),
            "expression_:": lambda: self._check_expression(conditionals=[":"]),
            "expression_>": lambda: self._check_expression(conditionals=[">"]),
            "expression_]": lambda: self._check_expression(conditionals=["]"]),
            "switch_block": lambda: self._check_switch_block(),
            "identifier": lambda: self._check_identifier(),
            "type": lambda: self._check_type(),
            "line": lambda: self._check_line(),
            "block": lambda: self.analyze(conditionals=["}"]),
            "block_,": lambda: self.analyze(conditionals=["}"], condition_for_line=[","]),
            "case_block": lambda: self.analyze(conditionals=["break", "return"]),
            "increase_offset": lambda: self._increment("current_offset", self.current_offset),
            "decrease_offset": lambda: self._decrement("current_offset", self.current_offset),
            "line_or_block": lambda: self._line_or_block(),
            "just_block": lambda: self._just_block(),
            "initialization": lambda: self._check_initialization(),
            "check_()_in_catch": lambda: self._check_expression_in_catch()
        }

    def _just_block(self):
        self._add_mismatches_in_range(self.first_next_not_whitespace_index(), "not whitespace")
        self.index_token -= 1
        self.check_tokens_by_graph(graph=self.graphs[Graphs.just_block_])

    def _save_mismatches_to_file(self):
        total_width = 110
        data_to_save = "\n" + center_text(self.file.file_path, total_width) + "\n\n"

        if len(self.mismatches) == 0:
            data_to_save += "File clean!" + "\n\n"
        else:
            data_to_save += "Mismatches:" + "\n"
            for miss in self.mismatches:
                data_to_save += f"{miss}\n"

        data_to_save += "-" * total_width + "\n\n"
        if self.file_to_save_mismatches == "None":
            return
        with open(self.file_to_save_mismatches, mode="a", encoding="utf-8") as f:
            f.write(data_to_save)

        if self.print_to_console:
            print(data_to_save)

    def _analyze_file(self, file_path):
        """
        Анализирует весь файл
        :param file_path: путь до файла
        :return:
        """
        self.file = CSFile(file_path, self.setts)
        self.tokens = self.file.tokenizer.tokens
        self.analyze()
        self._save_mismatches_to_file()

    def _reset(self):
        self.mismatches = []
        self.index_token = 0
        self.prev_modifier_id = -1
        self.tokens = CustomList()
        self.current_offset = 0
        self.was_private_in_line = False
        self.was_public_in_line = False

    def _clean_mismatches_file(self):
        with open(self.file_to_save_mismatches, 'w+') as file:
            file.write("")

    def analyze_files(self, file_paths: list, print_to_console: bool):
        """
        Анализирует файлы
        :param file_paths: список путей
        :return:
        """
        self._clean_mismatches_file()

        for file_path in file_paths:
            self._analyze_file(file_path)
            self._reset()

    def analyze(self, conditionals=None, condition_for_line=[";"]):
        """
        Анализирует последовательно блоки. Может быть вызван вложено несколько раз
        :param conditionals: Список значений токенов, при которых прекращается анализ
        :return:
        """
        if conditionals is None:
            conditionals = []
        while self.index_token < len(self.tokens):
            found = False
            token = self.tokens[self.index_token]
            if token.value == r"\n":
                self._check_empty_line()
                self.index_token += 1
                self._check_offset()
                continue
            if token.value == r"\t" or token.value == " ":
                self._check_offset()
            token = self.tokens[self.index_token]
            if token.value in conditionals:
                self.index_token -= 1
                self._roll_back_first_not_white_space_token()
                self.index_token += 1
                return

            graph = self._try_find_graph(token)
            if graph:
                name_graph = self._define_name_of_graph(graph)
                self.check_tokens_by_graph(graph)
                found = True
                # self.index_token += 1
                token = self.tokens.at(self.index_token)
                if token is None:
                    break

            # Проверка на модификаторы
            if any(token.value in modifier_list for modifier_list in modifiers):
                self.check_modifiers()
                self.index_token += 1
                continue
            else:
                self.prev_modifier_id = -1

            if not found:
                self._check_line(conditions=condition_for_line)

        if not conditionals:
            last_token = self.tokens[-1]  # type: Token
            if last_token.value != r"\n" and self.setts.insert_final_newline.value:
                self._append_mismatch(last_token.line_index, "Should use final new line.", "analyze")

            for line in self.file.tokenizer.too_long_lines:
                self._append_mismatch(line[0], f"Too long line({line[1]} > {self.setts.hard_wrap_at.value}).",
                                      "analyze")

    def _check_expression_in_catch(self) -> bool:
        next_token = self.tokens[self.first_next_not_whitespace_index()]
        return next_token.value == "("

    def _check_type(self):
        token = self.tokens[self.index_token]
        while token.kind == KindToken.whiteSpace:
            self.mismatches.append(self._create_mismatch_by_token(token, "not white space", "_check_type"))
            self.index_token += 1
            token = self.tokens[self.index_token]
        if self.tokens[self.index_token].value != "var":
            self._create_mismatch_by_token(self.tokens[self.index_token], "var",
                                           "_check_type")
        self.index_token += 1

    def _check_initialization(self):
        """
        Проверяет, что происходит инициализация объекта. В случае если инициализации нету, то ничего не делает
        """
        first_next_not_whitespace_index = self.first_next_not_whitespace_index()
        token = self.tokens[first_next_not_whitespace_index]
        if token.value == ";" or token.value == "(" or token.value == ",":
            self._add_mismatches_in_range(first_next_not_whitespace_index, "not white space")
            self.index_token = first_next_not_whitespace_index
            return False
        if token.kind == KindToken.identifier or token.kind == KindToken.keyword:
            return False
        current_token = self.tokens[self.index_token - 1]
        if current_token.value == "\\n":
            self._check_offset()
            del self.mismatches[-1]
            del self.mismatches[-1]
            self.check_tokens_by_graph(self.extension_graphs[Graphs.just_block_for_new_])
            return True

        order_tokens = []
        if current_token.kind == KindToken.identifier:
            order_tokens = [" "]
        order_tokens += ["{", " "]
        self._check_order_token_by_array(order_tokens=order_tokens)
        token = self.tokens[self.index_token]
        while token.value != "}":
            self._check_expression(["}"])
            token = self.tokens[self.index_token]
            if token.value == "}":
                break
            self.index_token += 1
        self.index_token += 1
        return True

    def _check_order_token_by_array(self, order_tokens):
        """
        Проверяет последовательность токенов. Используется вместо _check_by_graph, для вызова из кода.
        :param order_tokens: Последовательность токенов
        """
        expected_next_token_index = 0
        while expected_next_token_index < len(order_tokens):
            token = self.tokens[self.index_token]
            self.index_token += 1
            if token.value == "\\n":
                self._check_offset()
            if token.value == order_tokens[expected_next_token_index]:
                expected_next_token_index += 1
                continue
            self.mismatches.append(
                self._create_mismatch_by_token(token, order_tokens[expected_next_token_index],
                                               "_check_order_token_by_array", qutie_expected=True))
            if order_tokens[expected_next_token_index] in ["\\n", "\\t", " "]:
                expected_next_token_index += 1
                self.index_token -= 1

    def _check_identifier(self):
        """
        Проверка на идентификатор
        """
        token = self.tokens[self.index_token]
        while token.kind == KindToken.whiteSpace:
            self.mismatches.append(self._create_mismatch_by_token(token, "not white space", "_check_identifier"))
            self.index_token += 1
            token = self.tokens[self.index_token]
        while token.kind == KindToken.identifier or token.value == ".":
            self.index_token += 1
            token = self.tokens[self.index_token]

    def _call_func_by_keyword(self, name: str, args):
        self._keywords_to_func[name](**args)

    def _increment(self, name: str, value):
        self.__setattr__(name, value + 1)

    def _decrement(self, name: str, value):
        self.__setattr__(name, value - 1)

    def _parse_graphs(self):
        """
        Записывает все графы из папки Graphs/Standards в список графов для проверки кода
        :return:
        """
        directory = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Graphs/Standards")

        for filename in os.listdir(directory):
            if filename.endswith(".gml"):
                graph_name = os.path.splitext(filename)[0] + "_"
                graph_path = os.path.join(directory, filename)
                graph = nx.DiGraph(nx.convert_node_labels_to_integers(nx.read_gml(graph_path)))
                self.graphs[Graphs[graph_name]] = graph
        directory = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Graphs/Extensions")
        for filename in os.listdir(directory):
            if filename.endswith(".gml"):
                graph_name = os.path.splitext(filename)[0] + "_"
                graph_path = os.path.join(directory, filename)
                graph = nx.DiGraph(nx.convert_node_labels_to_integers(nx.read_gml(graph_path)))
                self.extension_graphs[Graphs[graph_name]] = graph

    def change_format_rules(self, new_settings: Settings):
        """
        Изменяет флаги описывающие правило стиля кода
        :param new_settings:
        """
        self.setts = new_settings

    def get_modifier_id(self):
        """
        Получает номер модификатора в строке
        Например: public static readonly
        public -> 0
        static -> 1
        readonly -> 2
        :return:
        """
        for i, row in enumerate(modifiers):
            if self.tokens[self.index_token].value in row:
                return i

    def check_modifiers(self):
        """
        Проверяет порядок постановки модификаторов, а также пробелы между ними
        :return:
        """
        # Проверка порядка
        curr_id = self.get_modifier_id()
        if self.prev_modifier_id != -1:
            if curr_id < self.prev_modifier_id:
                self.mismatches.append(
                    self._create_mismatch_by_token(self.tokens[self.index_token], "Different modifiers order",
                                                   "check_modifiers"))

        self.prev_modifier_id = curr_id

        if self.tokens[self.index_token].value == "public":
            self.was_public_in_line = True
        if self.tokens[self.index_token].value == "private":
            self.was_private_in_line = True

        # Проверка на пробелы
        space_count = 0
        while self.tokens[self.index_token + 1].value.isspace() or self.tokens[self.index_token + 1].value == "\\t":
            self.index_token += 1
            space_count += 1
            if space_count > 1:
                self.mismatches.append(
                    self._create_mismatch_by_token(self.tokens[self.index_token], "Not white Space", "check_modifiers"))

        if space_count == 0:
            self.mismatches.append(
                self._create_mismatch_by_token(self.tokens[self.index_token], "White space", "check_modifiers"))

    def check_naming(self, token_identifier_after_modifiers_id):
        """
        Проверяет регистр первой буквы в зависимости от модификатора public, private
        :param token_identifier_after_modifiers_id: id названия метода(поля)
        :return:
        """
        if self.was_public_in_line and self.tokens[self.index_token].kind == KindToken.identifier:
            self.was_public_in_line = False
            if self.tokens[self.index_token].value[0].islower():
                self.mismatches.append(
                    self._create_mismatch_by_token(self.tokens[self.index_token], "Uppercase first letter",
                                                   "analyze"))

        if ((self.tokens[self.index_token].value == "(" or self.tokens[self.index_token].value == ";") and
                self.was_private_in_line):
            self.was_private_in_line = False
            if (self.tokens[token_identifier_after_modifiers_id].value[0].isupper()
                    and self.tokens[self.index_token].value == ";"):
                self.mismatches.append(
                    self._create_mismatch_by_token(self.tokens[token_identifier_after_modifiers_id],
                                                   "Lowercase first letter",
                                                   "analyze"))
            if (self.tokens[token_identifier_after_modifiers_id].value[0].islower()
                    and self.tokens[self.index_token].value == "("):
                self.mismatches.append(
                    self._create_mismatch_by_token(self.tokens[token_identifier_after_modifiers_id],
                                                   "Uppercase first letter",
                                                   "analyze"))

    def _check_empty_line(self) -> bool:
        """
        Проверяет, что если есть пустая строчка, то она должна быть пустой
        Пример :
        \t\t \t\n -- выдать ошибку
        \n -- то что надо
        :return: True, если строка пустая(то есть состояла из whitespaces) или первый символ был сразу ;
        """
        index = self.index_token - 1
        token = self.tokens[index]
        if token.value == r"\n" or token.value == ";" or token.line_index in self.file.tokenizer.lines_with_comments:
            return True
        while index >= 0:
            if self.tokens[index].kind != KindToken.whiteSpace:
                return False
            if self.tokens[index].value == r"\n":
                self.mismatches.append(
                    self._create_mismatch_by_token(self.tokens[index + 1], expected="Remove useless white spaces",
                                                   called_from="_check_empty_line"))
                return True
            index -= 1

    def _line_or_block(self) -> bool:
        """
        Метод, который вызывает check_tokens_by_graph. Используется для ветвления и циклов, когда тело может быть
        из одной строчки или целого блока
        :return: если была строка, вернёт True
        """
        index = self.index_token
        is_line = False
        token = self.tokens[index]
        while index < len(self.tokens):
            token = self.tokens[index]
            if token.value == "{":
                break
            if token.kind != KindToken.whiteSpace:
                self.current_offset += 1
                is_line = True
                break
            index += 1

        token_to_come_back = self.index_token
        self._roll_back_first_not_white_space_token()
        if is_line and token.line_index == self.tokens[self.index_token].line_index:
            self.index_token = token_to_come_back
            while len(self.mismatches) > 0:
                if self.mismatches[-1].expected == "\\n":
                    del self.mismatches[-1]
                else:
                    break
            self.current_offset -= 1
            self._check_line()
            return is_line
        self.index_token = token_to_come_back
        self._check_offset()
        if is_line:
            self._check_line()
            self.current_offset -= 1
        else:
            self.check_tokens_by_graph(self.graphs[Graphs.just_block_])
        return is_line

    @staticmethod
    def _direct_successors(graph, node):
        """
        Вспомогательный метод, чтобы получить следующие вершины в ориентированном графе
        :param graph: Граф
        :param node: Вершина из которой исходят ребра
        :return:
        """
        descendants = nx.descendants(graph, node)
        if descendants is None:
            return None
        direct_successors = [n for n in descendants if graph.has_edge(node, n)]
        return direct_successors

    @staticmethod
    def _get_start_nodes(graph) -> []:
        """
        Возвращает начальные вершины графа, то есть вершины без входящих рёбер
        :param graph: Граф
        :return:
        """
        isolated_nodes = [node for node in graph.nodes() if not list(graph.predecessors(node))]
        return isolated_nodes

    def check_tokens_by_graph(self, graph: nx.DiGraph):
        """
        Проверяет последовательность токенов по графу.
        Предполагается что помимо токенов в графе присутствуют кодовые слова, как block или line, для которых определены
        специальные действия
        :param graph: граф для сравнения правил и кода
        :return:
        """

        # Определяем стартовый индекс вершины
        index_node = 0
        for index_start_node in self._get_start_nodes(graph):
            if self.tokens[self.index_token].value == graph.nodes[index_start_node]["data"]:
                index_node = index_start_node
                break

        # Некоторые функции могут возвращать True или False, которые будут определять выбор следующей ноды
        # Потому результат нужно куда-то сохранять
        res_of_keyword_func = None

        next_nodes = [index_node]
        data_to_compair = graph.nodes[index_node]["data"]
        past_node = index_node
        while next_nodes and len(next_nodes) > 0:
            found = False
            token_to_check = self.tokens.at(self.index_token)
            if token_to_check is None:
                self.index_token -= 1
                token_to_check = self.tokens[self.index_token]
            is_last_node = True
            for next_node_id in next_nodes:
                if not _check_passage_allowed(graph, index_node, next_node_id, res_of_keyword_func):
                    continue
                is_last_node = False
                next_node = graph.nodes[next_node_id]
                data_to_compair = next_node["data"]
                if data_to_compair == "end_node":
                    return

                should_check_offset = next_node["should_check_offset"]
                if data_to_compair in self._keywords_to_func:
                    res_of_keyword_func = self._keywords_to_func[data_to_compair]()
                    found = True
                    index_node = next_node_id
                    if should_check_offset == "true":
                        self._check_offset()
                    break
                if self._check_token_by_value(data_to_compair, should_check_offset):
                    index_node = next_node_id
                    found = True
                    break

            past_node = index_node
            next_nodes = self._direct_successors(graph, index_node)

            if is_last_node:
                return

            if not found and token_to_check.value == r"\n":
                if not self._check_empty_line():
                    self.mismatches.append(
                        self._create_mismatch_by_token(token_to_check, "Not new line", "check_tokens_by_graph"))
                found = True

                self.index_token += 1
                self._check_offset()

            if not found:
                expected = graph.nodes[next_nodes[0]]["data"]

                if token_to_check.kind == KindToken.whiteSpace:
                    self.index_token += 1
                    self.mismatches.append(self._create_mismatch_by_token(token=token_to_check, expected=expected,
                                                                          called_from="check_tokens_by_graph"))
                elif data_to_compair in [" ", "\\n", "\\t"]:
                    past_node = index_node
                    index_node = next_nodes[0]
                    if len(next_nodes) > 1:
                        if _check_passage_allowed(graph, past_node, next_nodes[1], res_of_keyword_func):
                            index_node = next_nodes[1]
                    expected = graph.nodes[index_node]["data"]
                    next_nodes = self._direct_successors(graph, index_node)
                    self.mismatches.append(self._create_mismatch_by_token(token=token_to_check, expected=expected,
                                                                          called_from="check_tokens_by_graph"))
                else:
                    raise exceptions.NodeInGraphNotFound(token_to_check, graph_name=self._define_name_of_graph(graph))

    def _check_token_by_value(self, value: str, should_check_offset) -> bool:
        """
        Проверяет токен, на который указывает указатель index_token.
        :param value: Значение для сравнения
        :param should_check_offset: Флаг, которой задается в GraphCreator.
        :return: True, если значение токена совпало с value, False в противном случае
        """
        token_to_check = self.tokens[self.index_token]
        if token_to_check.value == value:
            checked = False
            if should_check_offset == "true":
                self._check_offset()
                checked = True
            self.index_token += 1
            if value == "\\n":
                self._check_empty_line()
                if not checked and (should_check_offset == "default" or should_check_offset == "true"):
                    self._check_offset()
            return True
        return False

    def _define_name_of_graph(self, graph: nx.DiGraph) -> str:
        """
        Определяет имя графа по переданному graph: nx.DiGraph
        :param graph: Граф.
        :return: Имя графа
        """
        for key, item in self.graphs.items():
            if item == graph:
                return key
        raise exceptions.GraphNotFound(graph)

    def _check_expression(self, conditionals=None, skip_first_white_space=False):
        """
        Проверяет, что выражение соответствует правилам.
        Пока правило одно: больше двух пробелов между токенами быть не может,
        устанавливает метку на первый токен из conditionals
        Указатель должен быть на выражение, а не на скобки!
        :param conditionals: Условие для остановки работы метода
        """
        token = self.tokens[self.index_token]  # type: Token
        count_spaces = 0
        symbol_index = 0
        enter_count = 0
        was_enter = False
        while not (token.value in conditionals):
            if token.value == "{":
                self._check_initialization()
                token = self.tokens[self.index_token]
                count_spaces = 0

            graph = self._try_find_graph(token)
            if graph:
                self.check_tokens_by_graph(graph)
                token = self.tokens[self.index_token]
                continue

            # Проверка на пробел в начале
            if symbol_index == 0 and token.kind == KindToken.whiteSpace and token.value != "\\t":
                if token.value == " ":
                    if not skip_first_white_space:
                        self.mismatches.append(self._create_mismatch_by_token(token, "Not white Space",
                                                                              called_from="_check_expression"))
                else:
                    self.mismatches.append(self._create_mismatch_by_token(token, "Not white Space",
                                                                          called_from="_check_expression"))
            # Проверка, нужен ли пробел между элементами
            if self.conditions_for_space():
                self.mismatches.append(self._create_mismatch_by_token(token, "White Space",
                                                                      called_from="_check_expression"))

            # Проверка на исключения, которые не обрабатывает conditions_for_space
            self._check_exceptions(skip_first_white_space)

            if token.value.isspace():
                count_spaces += 1
            elif token.value == "\\n":
                was_enter = True
                enter_count += 1
                if enter_count == 1:
                    self._increment("current_offset", self.current_offset)
                if not self._check_correct_enter():
                    if enter_count == 1:
                        self._decrement("current_offset", self.current_offset)
                    self.mismatches.append(self._create_mismatch_by_token(token, "Not New Line",
                                                                          called_from="_check_expression"))
            elif token.value == "\\t":
                self.mismatches.append(self._create_mismatch_by_token(token, "Not tab",
                                                                      called_from="_check_expression"))
            else:
                count_spaces = 0
            if count_spaces > 1:
                self.mismatches.append(self._create_mismatch_by_token(token, "Not white Space",
                                                                      called_from="_check_expression"))
            self.index_token += 1
            token = self.tokens[self.index_token]
            symbol_index += 1

            if token.value in conditionals and enter_count != 0:
                self._decrement("current_offset", self.current_offset)

            if token.value not in ["\\n", '\\t']:
                was_enter = False

            if token.value == "\\t" and was_enter:
                self._check_offset()
                token = self.tokens[self.index_token]

            if token.value == "(":
                self.index_token += 1
                self._check_expression(")")
                self.index_token += 1
                token = self.tokens[self.index_token]

            # Проверка на пробел в конце
            value = token.value
            if (value == ":" or value == ")" or value == ";") and self.tokens[self.index_token - 1].value.isspace():
                self.mismatches.append(
                    self._create_mismatch_by_token(self.tokens[self.index_token - 1], "Not white Space",
                                                   called_from="_check_expression"))

    def _check_correct_enter(self):
        """
        Проверяет, можно ли в этом случае сделать \n
        :return:
        """
        allowed_enter_symbols = ["||", "|", "&&", "&", ","]
        current_index = self.index_token

        # Проверка предыдущего токена
        while self.index_token > 0:
            if self.tokens[self.index_token].value not in [" ", "\\n", "\\t"]:
                break
            self.index_token -= 1

        prev_token = self.tokens[self.index_token]
        self.index_token = current_index

        if prev_token.value in allowed_enter_symbols:
            return True

        # Проверка следующего токена
        while self.index_token < len(self.tokens):
            if self.tokens[self.index_token].value not in [" ", "\\n", "\\t"]:
                break
            self.index_token += 1

        next_token = self.tokens[self.index_token]
        self.index_token = current_index

        if next_token.value in allowed_enter_symbols:
            return True

        return False

    def conditions_for_space(self):
        """
        Условие для постановки пробела в expression(строке)
        """
        current_token = self.tokens[self.index_token]
        next_token = self.tokens[self.index_token + 1] if self.index_token + 1 < len(self.tokens) else None

        if current_token and next_token:
            current_kind = current_token.kind
            next_kind = next_token.kind

            if (current_kind == KindToken.operator and next_kind == KindToken.identifier
                and current_token.value != "!" and current_token.value != "--" and
                current_token.value != "++") or \
                    (current_kind == KindToken.operator and next_kind == KindToken.keyword) or \
                    (current_kind == KindToken.keyword and next_kind == KindToken.operator) or \
                    (current_token.value == "]" and next_kind == KindToken.operator) or \
                    (current_kind == KindToken.identifier and next_kind == KindToken.operator and
                     (next_token.value != "++" and next_token.value != "--")) or \
                    (current_kind == KindToken.literal and next_kind == KindToken.operator) or \
                    (current_kind == KindToken.operator and next_kind == KindToken.literal):
                if current_token.value == '-' and self._check_unary():
                    return False

                return True
            return False

    def _check_unary(self):
        """
        Проверяет, является ли "-" унарным
        """
        current_index = self.index_token
        while self.index_token > 0:
            if self.tokens[self.index_token].value != ' ':
                break
            self.index_token -= 1
        prev_token = self.tokens[self.index_token]
        self.index_token = current_index
        if prev_token.kind == KindToken.identifier:
            return False
        else:
            return True

    def _check_line(self, conditions=[";"]):
        """
        Проверяет строчку, если ни один из графов не подошел. Метод по мере проверки на пробелы распознает, это строка
        вызова функции, её объявления или просто строки
        :return:
        """
        token = self.tokens[self.index_token]  # type: Token
        was_equal = False
        if token.value == "\\n":
            self.is_current_line_empty = True
            self.index_token += 1
            self._check_offset()
            return

        count_spaces = 0
        token_identifier_after_modifiers_id = -1
        was_class = False
        was_attribute = False
        open_square_bracket_id = -1
        while token.value not in conditions:
            if token.value == "{":
                first_n_tokens = [x.value for x in self._get_first_n_not_white_space_tokens(4)]
                if "get" in first_n_tokens or "set" in first_n_tokens:
                    self._check_get_set_block()
                    return

            if token.value in ["get", "set"]:
                self._check_get_set()
                return

            graph = self._try_find_graph(token)
            if graph:
                self.check_tokens_by_graph(graph)
                token = self.tokens.at(self.index_token)
                if not token or graph in [self.graphs[Graphs.while_], self.graphs[Graphs.for_],
                                          self.graphs[Graphs.foreach_],
                                          self.graphs[Graphs.if_],
                                          self.graphs[Graphs.just_block_]]:
                    return
                if token.value in conditions:
                    break

            if token.value == "=":
                was_equal = True

            if token.value == "class" or token.value == "struct" or token.value == "interface":
                was_class = True

            if self.was_private_in_line and self.tokens[self.index_token].kind == KindToken.identifier:
                token_identifier_after_modifiers_id = self.index_token

            if token.value == "[":
                open_square_bracket_id = self.index_token

            if token.value == "]":
                was_attribute = self._check_attributes(open_square_bracket_id)
                open_square_bracket_id = -1

            # Проверка на пробел между элементами
            if self.conditions_for_space():
                self.mismatches.append(
                    self._create_mismatch_by_token(token, "White Space", called_from="_check_line"))

            self._check_exceptions(skip_first_white_space=None)

            if token.value.isspace():
                count_spaces += 1
            elif token.value == "\\n" and not was_class and not was_attribute:
                count_spaces = 0
                self.mismatches.append(self._create_mismatch_by_token(token, "Not New Line", called_from="_check_line"))
            elif token.value == "\\t":
                self.mismatches.append(self._create_mismatch_by_token(token, "Not tab",
                                                                      called_from="_check_line"))
                count_spaces = 0
            else:
                count_spaces = 0
            if count_spaces > 1:
                self.mismatches.append(
                    self._create_mismatch_by_token(token, "Not white Space", called_from="_check_line"))

            self.check_naming(token_identifier_after_modifiers_id)
            self.index_token += 1
            token = self.tokens.at(self.index_token)
            if token is None:
                return

            if token.kind == KindToken.whiteSpace and self.tokens[self.index_token - 1].value == "\\n":
                self._check_offset()
                token = self.tokens.at(self.index_token)

            if token.value == "{" and was_equal:
                self._check_initialization()
                token = self.tokens[self.index_token]

            if token.value == "(":
                self.index_token += 1
                self._check_expression(")")
                count_spaces = 0
                self.index_token += 1
                token = self.tokens[self.index_token]
                index_first_not_whitespace_token = self.first_next_not_whitespace_index()
                first_not_whitespace_token = self.tokens[index_first_not_whitespace_token]
                if first_not_whitespace_token.value == ";":
                    self._add_mismatches_in_range(index_first_not_whitespace_token, "Not white space")
                    self._check_new_line_after_semicolon()
                    return
                if first_not_whitespace_token.value == "{":
                    self.check_tokens_by_graph(self.extension_graphs[Graphs.just_block_for_func_])
                    return

        self.check_naming(token_identifier_after_modifiers_id)
        self.index_token += 1
        if conditions == [";"]:
            self._check_new_line_after_semicolon()

    def _check_attributes(self, open_square_bracket_id):
        """
        Проверяет являются ли [] атрибутом
        :param open_square_bracket_id: id [
        :return:
        """
        was_attribute = True
        open_square_bracket_id -= 1
        while open_square_bracket_id > 0 and self.tokens[open_square_bracket_id].value != "\\n":
            if self.tokens[open_square_bracket_id].value != " " and self.tokens[open_square_bracket_id].value != "\\t":
                was_attribute = False
                break
            open_square_bracket_id -= 1
        return was_attribute

    def _check_exceptions(self, skip_first_white_space: bool):
        """
        Проверяет на наличие пробелов (исключения)
        :param skip_first_white_space: Флаг: нужно ли пропускать первый пробел
        :return:
        """
        if skip_first_white_space is None:
            skip_first_white_space = False
        if (self.tokens[self.index_token - 1].kind == KindToken.identifier and self.tokens[
            self.index_token].value.isspace()
                and self.tokens[self.index_token].value == "(" or
                self.tokens[self.index_token - 1].value == "." and self.tokens[self.index_token].value.isspace() or
                self.tokens[self.index_token].value.isspace() and self.tokens[self.index_token + 1].value == '.' or
                self.tokens[self.index_token].value.isspace() and (
                        self.tokens[self.index_token + 1].value == '++' or
                        self.tokens[self.index_token + 1].value == '--')):
            if not skip_first_white_space:
                self.mismatches.append(self._create_mismatch_by_token(self.tokens[self.index_token], "Not white Space",
                                                                      called_from="_check_expression"))

    def _check_get_set_block(self):
        close_bracket = self.tokens[self._find_index_first_token_forward("}")]  # type: Token
        if close_bracket.line_index == self.tokens[self.index_token].line_index:
            self.index_token += 1
            self._check_expression(conditionals=["}"], skip_first_white_space=True)
            self.index_token += 1
            return
        self._roll_back(kind_token=KindToken.identifier, token_value=None)
        self.index_token += 1
        self._check_order_token_by_array(["\\n", "{"])
        self.index_token -= 1
        self.check_tokens_by_graph(self.graphs[Graphs.just_block_])
        return

    def _check_get_set(self):
        self.index_token += 1
        index_first_not_whitespace_token = self.first_next_not_whitespace_index()
        token = self.tokens[index_first_not_whitespace_token]
        if token.value == ";":
            self._add_mismatches_in_range(index_first_not_whitespace_token, "not white space")
            self._check_new_line_after_semicolon()
            return
            # Возможно лишний
            # self._check_offset()
        order_tokens = ["\\n"]
        # if self.setts.indent_style == "tab":
        #    order_tokens += ["\\t"] * self.current_offset
        # else:
        #    order_tokens += [""] * self.current_offset * 4
        order_tokens += ["{"]
        self._check_order_token_by_array(order_tokens)
        self.index_token -= 1
        self.check_tokens_by_graph(self.graphs[Graphs.just_block_])

    def _add_mismatches_in_range(self, index_end: int, expected: str):
        """
        Добавляет несовпадения с индекса self.index_token до index_end. Применяется, если между двумя не пробельными
        токенами есть пробельные, которых не должно быть.
        Сам указатель смещает на index_end
        :param index_end: индекс конца, после которого ошибки не будут включаться. Сам индекс не входит
        :param expected: ожидаемый токен
        """
        while self.index_token < index_end:
            self.mismatches.append(
                self._create_mismatch_by_token(token=self.tokens[self.index_token], expected=expected,
                                               called_from="_add_mismatches_in_range"))
            self.index_token += 1
        self.index_token += 1

    def _try_find_graph(self, token: Token) -> nx.DiGraph:
        """
        Пытается найти граф по первому токену. Если не находит, то возвращает None
        :param token: первый токен в графе
        """
        for graph in self.graphs.values():  # type: nx.DiGraph
            for start_node_index in self._get_start_nodes(graph):
                if graph.nodes[start_node_index]["data"] == token.value:
                    return graph
        return None

    def _check_new_line_after_semicolon(self):
        """
        Вызвать, когда указатель стоит после токена ";" чтобы проверить,
        что следом за ним сразу идет символ новой строки
        """
        token = self.tokens.at(self.index_token)
        if not token:
            return
        while token.kind == KindToken.whiteSpace:
            if token.value != r'\n':
                self.mismatches.append(self._create_mismatch_by_token(token, expected="new line",
                                                                      called_from="_check_new_line_after_semicolon"))
                self.index_token += 1
                token = self.tokens.at(self.index_token)
                if token is None:
                    return
            else:
                return
        self.mismatches.append(
            self._create_mismatch_by_token(token, expected="new line", called_from="_check_new_line_after_semicolon"))

    def _check_offset(self):
        """
        Проверяет количество отступов в строчке. Для выбора отступа, нужно установить флаг UseTabs в самом линтере
        """

        count_tabs = 0
        count_spaces = 0
        token = self.tokens.at(self.index_token)  # type: Token
        if token is None:
            return

        mismatches = []
        index_next_not_white_space_token = self.first_next_not_whitespace_index()
        if index_next_not_white_space_token is None:
            return
        next_nws_token = self.tokens[index_next_not_white_space_token]

        # FLAGS
        indent_style = self.setts.indent_style.value
        indent_size = self.setts.indent_size.value

        while token.value == '\\t' or token.value == ' ':
            if token.value == '\\t':
                count_tabs += 1
                if indent_style == "space":
                    mismatches.append(
                        self._create_mismatch_by_token(token, "Should use spaces", called_from="_check_offset"))
            if token.value == ' ':
                count_spaces += 1
                if indent_style == "tab":
                    mismatches.append(
                        self._create_mismatch_by_token(token, "Should use tabs", called_from="_check_offset"))
            if (indent_style == "tab" and count_tabs > self.current_offset
                    or indent_style == "space" and count_spaces / indent_size > self.current_offset):
                mismatches.append(self._create_mismatch_by_token(token, "less offset", called_from="_check_offset"))
            self.index_token += 1
            token = self.tokens[self.index_token]

        if token.value == r"\n":
            return
        self.mismatches += mismatches
        if token.value == '}':
            self.current_offset -= 1
        if indent_style == "tab" and count_tabs < self.current_offset:
            self.mismatches.append(self._create_mismatch_by_token(token, "more offset", called_from="_check_offset"))
        if indent_style == "space" and count_spaces / indent_size < self.current_offset:
            self.mismatches.append(self._create_mismatch_by_token(token, "more offset", called_from="_check_offset"))
        if count_spaces * count_tabs != 0:
            self._append_mismatch(token.line_index, "Mixed spaces in offsets.", "_check_offset")
        if token.value == '}':
            self.current_offset += 1

    def _create_mismatch_by_token(self, token: Token, expected: str, called_from: str,
                                  qutie_expected=False) -> Mismatch:
        """
        Создает объект
        :param token:
        :param expected:
        :param called_from:
        :param qutie_expected:
        :return:
        """
        if qutie_expected:
            expected = f"'{expected}'"
        return Mismatch(CategoryStyleRule.CR, self.file.lines[token.line_index - 1], token.start_index,
                        token.line_index, f"Expected {expected}, but was '{token.value}'. Created by {called_from}\n",
                        None, expected=expected)

    def _append_mismatch(self, index_line: int, message: str, called_from: str):
        self.mismatches.append(
            Mismatch(CategoryStyleRule.CR, self.file.lines[index_line - 1], 0, index_line,
                     message + f" Created by {called_from}\n", None, expected=""))

    def _check_switch_block(self):
        while self.index_token < len(self.tokens):
            token = self.tokens[self.index_token]
            if token.value == "case" or token.value == "default":
                self.check_tokens_by_graph(self.graphs[Graphs.case_])
            if token.value == "}":
                break
            self.index_token += 1

    def _roll_back(self, token_value: str, kind_token: KindToken):
        """
        Откатывает указатель назад
        :param token_value: значение токена
        :param kind_token: тип токена
        :return:
        """
        while self.index_token > 0:
            if token_value:
                if self.tokens[self.index_token].value == token_value:
                    return
            if kind_token:
                if self.tokens[self.index_token].kind == kind_token:
                    return
            self.index_token -= 1

    def _roll_back_first_not_white_space_token(self):
        """
        Откатывает указатель назад
        """
        while self.index_token > 0:
            if self.tokens[self.index_token].kind != KindToken.whiteSpace:
                return
            self.index_token -= 1

    def _find_index_first_token_forward(self, token_value: str) -> int:
        """
        Находит индекс первого токена спереди, который совпадает со значением
        Не изменяет сам указатель
        :param token_value:
        :return: индекс найденного токена
        """
        index = self.index_token
        while index < len(self.tokens):
            if self.tokens[index].value == token_value:
                return index
            index += 1

    def first_next_not_whitespace_index(self) -> int:
        """
        Возвращает индекс первого токена не пробельного типа впереди указателя.
        Не меняет текущий указатель.
        :return: Индекс первого не пробельного типа впереди указателя
        """
        index = self.index_token
        while index < len(self.tokens):
            if self.tokens[index].kind != KindToken.whiteSpace:
                return index
            index += 1

    def _get_first_n_not_white_space_tokens(self, count_tokens: int) -> list:
        """
        Возвращает список из первых n не пробельных символов. Начинает набор с self.index_token
        :param count_tokens: количество требуемых токенов
        :return: список из первых n не пробельных символов
        """
        res = []
        i_t = self.index_token
        while len(res) < count_tokens and i_t < len(self.tokens):
            if self.tokens[i_t].kind != KindToken.whiteSpace:
                res.append(self.tokens[i_t])
            i_t += 1
        return res


def main():
    """ Main program """
    parser = argparse.ArgumentParser(description='Linter для C#')

    parser.add_argument("-f", "--file",
                        help="Путь до одного или нескольких CS файлов (разделите запятыми)", type=str, nargs='+')
    parser.add_argument("-conf", "--config", help="Путь до файла c флагами. По умолчанию в файл flags.txt", type=str, nargs='?',
                        default="flags.txt")
    parser.add_argument("-sf", "--save_file", help="Путь, куда сохранять. По умолчанию в файл mismatches.txt", type=str,
                        nargs='?',
                        default="mismatches.txt")
    parser.add_argument("-p", "--print", help="Вывести результат в консоль", action="store_true")

    args = parser.parse_args()

    settings = Settings()
    settings.read_flags_from_file(args.config)

    linter = Linter(settings, args.save_file, args.print)

    testing = False

    if args.file:
        linter.analyze_files(args.file, args.print)
    else:
        linter.analyze_files([cs_file_path], True)

    if testing:
        print("Run on file:///" + os.path.abspath(cs_file_path).replace("\\", "/"))

    return 0


if __name__ == "__main__":
    main()
