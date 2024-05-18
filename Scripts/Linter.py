import argparse
import networkx as nx
import enum
import os

from Settings import Settings
from Utils import CustomList
from CSFile import CSFile
from Tokenizer import Token, KindToken
from Flag import CategoryStyleRule

# temporary
config_file_path = r'data/.EditorConfig'  # не используется
cs_file_path = r'TestFiles/Linter/Main/WithMistakes/for.cs'
modifiers = [['public', 'private', 'protected', 'internal', 'protected internal', 'private protected', 'file'],
             ['abstract', 'virtual'],
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
    case_ = "case"
    while_ = "while.cs"
    for_ = "for.cs"
    foreach_ = "foreach"
    namespace_ = "namespace"
    do_while_ = "do_while"
    class_ = "class"
    enum_ = "enum"


class Mismatch:
    """
    Класс описания несовпадения в коде. Содержит категорию ошибку, строку, индекс в строке, сообщение
    """

    def __init__(self, category: CategoryStyleRule, line: str, index: int, index_line: int, message: str,
                 mismatched_flag):
        self.category = category
        self.line = line
        self.index = index
        self.index_line = index_line
        self.message = message
        self.mismatched_flag = mismatched_flag

    def __str__(self):
        first_part = f"index = {self.index} Line {self.index_line}: "
        offset = len(first_part)
        return first_part + self.line + "\n" + " " * (offset + self.index) + "^" + "\n" + self.message

    def __repr__(self):
        return self.__str__()


class Linter:
    def __init__(self, settings: Settings):
        self.setts = settings
        self.mismatches = []
        self.graphs = {}
        self.extension_graphs = {}
        self._parse_graphs()
        self.index_token = 0
        self.tokens = CustomList()
        self.current_offset = 0
        self.prev_modifier_id = -1
        self.was_public_in_line = False
        self.was_private_in_line = False
        # TODO: Я сейчас написал специальный класс для хранения данных о файле, который возможно можно просто сократить
        #  до списка токенов
        self.file = None  # type: CSFile|None

        # Пока вместо флагов будет вот такая штуковина, так как ну очень нужна
        self.UseTabs = True

        self._keywords_to_func = {
            "expression_)": lambda: self._check_expression(conditionals=[")"]),
            "expression_;": lambda: self._check_expression(conditionals=[";"]),
            "expression_:": lambda: self._check_expression(conditionals=[":"]),
            "switch_block": lambda: self._check_switch_block(),
            "identifier": lambda: self._increment("index_token", self.index_token),
            "line": lambda: self._check_line(),
            "block": lambda: self.analyze(conditionals=["}"]),
            "case_block": lambda: self.analyze(conditionals=["break", "return"]),  # TODO: еще нужно рассмотреть case
            "increase_offset": lambda: self._increment("current_offset", self.current_offset),
            "decrease_offset": lambda: self._decrement("current_offset", self.current_offset),
            "line_or_block": lambda: self._line_or_block(),
            "just_block": lambda: self.check_tokens_by_graph(graph=self.graphs[Graphs.just_block_]),
        }

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
        directory = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Graphs\\Standards")

        for filename in os.listdir(directory):
            if filename.endswith(".gml"):
                graph_name = os.path.splitext(filename)[0] + "_"
                graph_path = os.path.join(directory, filename)
                graph = nx.DiGraph(nx.convert_node_labels_to_integers(nx.read_gml(graph_path)))
                self.graphs[Graphs[graph_name]] = graph
        directory = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Graphs\\Extensions")
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
                self.mismatches.append(self._create_mismatch_by_token(self.tokens[self.index_token], "Wrong modifiers order", "check_modifiers"))

        self.prev_modifier_id = curr_id

        if self.tokens[self.index_token].value == "public":
            self.was_public_in_line = True
        if self.tokens[self.index_token].value == "private":
            self.was_private_in_line = True

        # Проверка на пробелы
        space_count = 0
        while self.tokens[self.index_token + 1].value.isspace():
            self.index_token += 1
            space_count += 1
            if space_count > 1:
                self.mismatches.append(self._create_mismatch_by_token(self.tokens[self.index_token], "Not white Space", "check_modifiers"))

        if space_count == 0:
            self.mismatches.append(self._create_mismatch_by_token(self.tokens[self.index_token], "White space", "check_modifiers"))

    def analyze_file(self, file_path):
        """
        Анализирует весь файл
        :param file_path: путь до файла
        :return:
        """
        with open(file_path, mode='r', encoding='utf8') as f:
            self.file = CSFile(f.read())
        self.tokens = self.file.tokenizer.tokens
        self.analyze()

    def analyze(self, conditionals=None):
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
                continue
            if token.value == r"\t" or token.value == " ":
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

            graph = self._try_find_graph(token)
            if graph:
                self.check_tokens_by_graph(graph)
                found = True
                self.index_token += 1

            if not found:
                self._check_line(conditionals=conditionals + ["{"])

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
                    self._create_mismatch_by_token(self.tokens[token_identifier_after_modifiers_id], "Lowercase first letter",
                                                   "analyze"))
            if (self.tokens[token_identifier_after_modifiers_id].value[0].islower()
                    and self.tokens[self.index_token].value == "("):
                self.mismatches.append(
                    self._create_mismatch_by_token(self.tokens[token_identifier_after_modifiers_id], "Uppercase first letter",
                                                   "analyze"))

    def _check_empty_line(self):
        """
        Проверяет, что если есть пустая строчка, то она должна быть пустой 
        Пример :
        \t\t  \t\n -- выдасть ошибку
        \n -- то что надо
        :return: 
        """
        index = self.index_token - 1
        if self.tokens[index].value == r"\n":
            return
        while index >= 0:
            if self.tokens[index].kind != KindToken.whiteSpace:
                return
            if self.tokens[index].value == r"\n":
                self.mismatches.append(
                    self._create_mismatch_by_token(self.tokens[index + 1], expected="Remove useless white spaces"),
                    called_from="_check_empty_line")
                return
            index -= 1

    def _line_or_block(self) -> bool:
        """
        Метод, который вызывает check_tokens_by_graph. Используется для ветвления и циклов, когда тело может быть 
        из одной строчки или целого блока
        :return: если была строка, вернёт True
        """
        index = self.index_token
        is_line = False
        while index < len(self.tokens):
            token = self.tokens[index]
            if token.value == "{":
                break
            if token.kind != KindToken.whiteSpace:
                self.current_offset += 1
                is_line = True
                break
            index += 1

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
        index_node = 0
        for index_start_node in self._get_start_nodes(graph):
            if self.tokens[self.index_token].value == graph.nodes[index_start_node]["data"]:
                index_node = index_start_node
                break

        # колхоз, но так надо -- этот флаг для того, чтобы первый токен граф все же проверил
        # В прошлой версии граф скипал первый токен, считая что раз его вызвали, то уже есть совпадение
        # Сделал это для одного графа из Extensions
        first_time = True

        # Некоторые функции могут возвращать True или False, которые будут определять выбор следующей ноды
        # Потому результат нужно куда то сохранять
        res_of_keyword_func = None

        while self.index_token < len(self.tokens):
            found = False
            next_nodes = self._direct_successors(graph, index_node)
            if first_time:
                next_nodes = [index_node]
                first_time = False
            if not next_nodes:
                return
            token_to_check = self.tokens[self.index_token]
            for next_node_id in next_nodes:
                # Тоже колхоз, связанный с тем, что мне нужно для перехода из 0 -> 0 использовать default
                if index_node == next_node_id:
                    condition = "default"
                else:
                    condition = graph[index_node][next_node_id]['condition']

                if condition == "True" and (res_of_keyword_func is not None and res_of_keyword_func != True):
                    res_of_keyword_func = None
                    continue
                if condition == "False" and (res_of_keyword_func is not None and res_of_keyword_func != False):
                    res_of_keyword_func = None
                    continue

                neighbor = graph.nodes[next_node_id]
                data = neighbor["data"]
                should_check_offset = neighbor["should_check_offset"]
                if data in self._keywords_to_func:
                    res_of_keyword_func = self._keywords_to_func[data]()
                    found = True
                    index_node = next_node_id
                    if should_check_offset == "true":
                        self._check_offset()
                    break
                elif token_to_check.value == data:
                    index_node = next_node_id
                    checked = False
                    if should_check_offset == "true":
                        self._check_offset()
                        checked = True
                    self.index_token += 1
                    if data == "\\n":
                        self._check_empty_line()
                        if not checked and (should_check_offset == "default" or should_check_offset == "true"):
                            self._check_offset()
                    found = True
                    break

            if not found and token_to_check.value == r"\n":
                self._check_empty_line()
                found = True
                self.index_token += 1
                self._check_offset()

            if not found:
                expected = graph.nodes[next_nodes[0]]["data"]
                self.mismatches.append(self._create_mismatch_by_token(token=token_to_check, expected=expected,
                                                                      called_from="check_tokens_by_graph"))
                if token_to_check.kind == KindToken.whiteSpace:
                    self.index_token += 1
                else:
                    self.index_token += 1
                    index_node = next_nodes[0]

    def _check_expression(self, conditionals=None):
        """
        Проверяет, что выражение соответствует правилам.
        Пока правило одно: больше двух пробелов между токенами быть не может,
        устанавливает метку на первый токен из conditionals
        Указатель должен быть на выражение, а не на скобки!
        :param conditionals: условие для остановки работы метода
        :return:
        """

        token = self.tokens[self.index_token]  # type: Token
        count_spaces = 0
        symbol_index = 0
        while not (token.value in conditionals):
            graph = self._try_find_graph(token)
            if graph:
                self.check_tokens_by_graph(graph)
                token = self.tokens[self.index_token]
                continue

            # Проверка на пробел в начале
            if symbol_index == 0 and token.value.isspace():
                self.mismatches.append(self._create_mismatch_by_token(token, "Not white Space",
                                                                      called_from="_check_expression"))
            # Проверка, нужен ли пробел между элементами
            if self.conditions_for_space():
                self.mismatches.append(self._create_mismatch_by_token(token, "White Space",
                                                                      called_from="_check_expression"))

            # Проверка на исключения, которые не обрабатывает conditions_for_space
            if (self.tokens[self.index_token - 1].kind == KindToken.identifier and self.tokens[self.index_token].value.isspace()
                and self.tokens[self.index_token].value == "(" or
                self.tokens[self.index_token - 1].value == "." and self.tokens[self.index_token].value.isspace() or
                self.tokens[self.index_token].value.isspace() and self.tokens[self.index_token + 1].value == '.' or
                self.tokens[self.index_token].value.isspace() and (self.tokens[self.index_token + 1].value == '++' or
                                                                 self.tokens[self.index_token + 1].value == '--')):
                self.mismatches.append(self._create_mismatch_by_token(token, "Not white Space",
                                                                      called_from="_check_expression"))

            if token.value.isspace() or token.value == "\\t":
                count_spaces += 1
            elif token.value == "\\n":
                self.mismatches.append(self._create_mismatch_by_token(token, "Not New Line",
                                                                      called_from="_check_expression"))
            else:
                count_spaces = 0
            if count_spaces > 1:
                self.mismatches.append(self._create_mismatch_by_token(token, "Not white Space",
                                                                      called_from="_check_expression"))
            self.index_token += 1
            token = self.tokens[self.index_token]
            symbol_index += 1
            if token.value == "(":
                self._check_expression(conditionals=')')
                self.index_token += 1
                token = self.tokens[self.index_token]

            # Проверка на пробел в конце
            value = token.value
            if (value == ":" or value == ")" or value == ";") and self.tokens[self.index_token - 1].value.isspace():
                self.mismatches.append(
                    self._create_mismatch_by_token(self.tokens[self.index_token - 1], "Not white Space",
                                                   called_from="_check_expression"))

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
                    and current_token.value != "!") or \
                    (current_kind == KindToken.operator and next_kind == KindToken.keyword) or \
                    (current_kind == KindToken.keyword and next_kind == KindToken.operator) or \
                    (current_token.value == "]" and next_kind == KindToken.operator) or \
                    (current_kind == KindToken.identifier and next_kind == KindToken.operator and
                     (next_token.value != "++" and next_token.value != "--")) or \
                    (current_kind == KindToken.literal and next_kind == KindToken.operator) or \
                    (current_kind == KindToken.operator and next_kind == KindToken.literal):
                return True
        return False

    def _check_line(self, conditionals=None):
        """
        Проверяет строчку, если ни один из графов не подошел. Метод по мере проверки на пробелы распознает, это строка
        вызова функции, её объявления или просто строки
        :return:
        """

        token = self.tokens[self.index_token]  # type: Token

        if token.value == "\\n":
            self.is_current_line_empty = True
            self.index_token += 1
            self._check_offset()
            return

        count_spaces = 0
        token_identifier_after_modifiers_id = -1;
        was_symbol_equal = False
        while token.value != ";":
            graph = self._try_find_graph(token)
            if graph:
                self.check_tokens_by_graph(graph)
                token = self.tokens.at(self.index_token)
                if not token or graph in [self.graphs[Graphs.while_], self.graphs[Graphs.for_],
                                          self.graphs[Graphs.foreach_],
                                          self.graphs[Graphs.if_]]:
                    return

            if self.was_private_in_line and self.tokens[self.index_token].kind == KindToken.identifier:
                token_identifier_after_modifiers_id = self.index_token

            # Проверка на пробел между элементами
            if self.conditions_for_space():
                self.mismatches.append(
                    self._create_mismatch_by_token(token, "White Space", called_from="_check_line"))

            if ((self.tokens[self.index_token - 1].kind == KindToken.identifier and self.tokens[self.index_token].value.isspace()
                and self.tokens[self.index_token + 1].value == "(") or
                self.tokens[self.index_token - 1].value == "." and self.tokens[self.index_token].value.isspace() or
                self.tokens[self.index_token].value.isspace() and self.tokens[self.index_token + 1].value == '.' or
                self.tokens[self.index_token].value.isspace() and (self.tokens[self.index_token + 1].value == '++' or
                                                                 self.tokens[self.index_token + 1].value == '--')):
                self.mismatches.append(self._create_mismatch_by_token(token, "Not white Space",
                                                                      called_from="_check_expression"))

            if token.value.isspace() or token.value == "\\t":
                count_spaces += 1
            elif token.value == "\\n":
                self.mismatches.append(self._create_mismatch_by_token(token, "Not New Line", called_from="_check_line"))
            else:
                count_spaces = 0
            if count_spaces > 1:
                self.mismatches.append(
                    self._create_mismatch_by_token(token, "Not white Space", called_from="_check_line"))

            self.check_naming(token_identifier_after_modifiers_id)
            self.index_token += 1
            token = self.tokens[self.index_token]

            if token.value == "(":
                self.index_token += 1
                self._check_expression(")")
                self.index_token += 1
                index_first_not_whitespace_token = self.first_next_not_whitespace_index()
                first_not_whitespace_token = self.tokens[index_first_not_whitespace_token]
                if first_not_whitespace_token.value == ";":
                    self._add_mismatches_in_range(index_first_not_whitespace_token, "Not white space")
                    self._check_new_line_after_semicolon()
                    return
                if first_not_whitespace_token.value == "{":
                    self.check_tokens_by_graph(self.extension_graphs[Graphs.just_block_for_func_])
                    return

            if token.value == "=":
                was_symbol_equal = True

        self.check_naming(token_identifier_after_modifiers_id)
        self.index_token += 1
        self._check_new_line_after_semicolon()

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

    def _try_find_graph(self, token: Token) -> nx.DiGraph | None:
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
                token = self.tokens[self.index_token]
            else:
                return
        self.mismatches.append(
            self._create_mismatch_by_token(token, expected="new line", called_from="_check_new_line_after_semicolon"))

    def _check_offset(self):
        """
        Проверяет количество отступов в строчке. Для выбора отсупа, нужно установить флаг UseTabs в самом линтере
        """

        count_tabs = 0
        count_spaces = 0
        token = self.tokens[self.index_token]  # type: Token

        mismatches = []
        index_next_not_white_space_token = self.first_next_not_whitespace_index()
        next_nws_token = self.tokens[index_next_not_white_space_token]
        if next_nws_token.value == "}":
            self.current_offset -= 1
        while token.value == '\\t' or token.value == ' ':
            if token.value == '\\t':
                count_tabs += 1
                if not self.UseTabs:
                    mismatches.append(
                        self._create_mismatch_by_token(token, "Should use spaces", called_from="_check_offset"))
            if token.value == ' ':
                count_spaces += 1
                if self.UseTabs:
                    mismatches.append(
                        self._create_mismatch_by_token(token, "Should use only tabs", called_from="_check_offset"))
            if self.UseTabs and count_tabs > self.current_offset or (
                    not self.UseTabs) and count_spaces / 4 > self.current_offset:
                mismatches.append(self._create_mismatch_by_token(token, "less offset", called_from="_check_offset"))
            self.index_token += 1
            token = self.tokens[self.index_token]
        if next_nws_token.value == "}":
            self.current_offset += 1
        if token.value == r"\n":
            return
        self.mismatches += mismatches
        if token.value == '}':
            self.current_offset -= 1
        if self.UseTabs and count_tabs < self.current_offset:
            self.mismatches.append(self._create_mismatch_by_token(token, "more offset", called_from="_check_offset"))
        if not self.UseTabs and count_tabs < self.current_offset:
            self.mismatches.append(self._create_mismatch_by_token(token, "more offset", called_from="_check_offset"))
        if count_spaces * count_tabs != 0:
            self._append_mismatch(token.line_index, "not mixed spaces in offsets", called_from="_check_offset")
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
                        None)

    def _append_mismatch(self, index_line: int, called_from: str, message: str):
        self.mismatches.append(
            Mismatch(CategoryStyleRule.CR, self.file.lines[index_line], 0, index_line,
                     message + f"\nCreated by{called_from}", None))

    def _check_switch_block(self):
        while self.index_token < len(self.tokens):
            token = self.tokens[self.index_token]
            if token.value == "case" or token.value == "default":
                # self._roll_back(r'\n')
                # self.index_token += 1
                # self._check_offset()
                self.check_tokens_by_graph(self.graphs[Graphs.case_])
            if token.value == "}":
                break
            self.index_token += 1

    def _roll_back(self, token_value: str):
        """
        Откатывает указатель назад
        :param token_value:
        :return:
        """
        while self.index_token > 0:
            if self.tokens[self.index_token].value == token_value:
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
        :return: индекс первого не пробельного типа впереди указателя
        """
        index = self.index_token
        while index < len(self.tokens):
            if self.tokens[index].kind != KindToken.whiteSpace:
                return index
            index += 1


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
        print("Run on file:///" + os.path.abspath(cs_file_path).replace("\\", "/"))

    return 0


if __name__ == "__main__":
    main()
