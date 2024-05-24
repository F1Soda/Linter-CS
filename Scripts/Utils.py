import enum

keywords = ['abstract', 'as', 'base', 'bool', 'break', 'byte', 'case', 'catch', 'char', 'checked', 'class', 'const',
            'continue', 'decimal', 'default', 'delegate', 'do', 'double', 'else', 'enum', 'event', 'explicit', 'extern',
            'false', 'finally', 'fixed', 'float', 'for.cs', 'foreach', 'goto', 'if', 'implicit', 'in', 'int',
            'interface',
            'internal', 'is', 'lock', 'long', 'namespace', 'new', 'null', 'object', 'operator', 'out', 'override',
            'params', 'private', 'protected', 'public', 'readonly', 'ref', 'return', 'sbyte', 'sealed', 'short',
            'sizeof', 'stackalloc', 'static', 'string', 'struct', 'switch', 'this', 'throw', 'true', 'try', 'typeof',
            'uint', 'ulong', 'unchecked', 'unsafe', 'ushort', 'using', 'virtual', 'void', 'volatile', 'while']

punctuations = [';', ':', ',', '.', '(', ')', '[', ']', '{', '}', '?', '<', '>', '#']

operators = ['+', '-', '*', '/', '%', '=', '>>', '<<', '&', '&&', '|', '||', '!', '^', '>', '>=', '<', '<=', '==', '!=',
             '~', '+=', '-=', '/=', '*=', '%=', '++', '--']

backslash_character_literals = [r'\n', r'\r', r'\f', r'\t', r'\a', r'\b', r'\o', r'\v', r'\\', r"\'", r'\"']

number_postfixes = ['f', 'l', 'd']


class CustomList(list):
    def at(self, index):
        if 0 <= index < len(self):
            return self[index]
        else:
            return None


class CustomStr(str):
    def at(self, index):
        if 0 <= index < len(self):
            return self[index]
        else:
            return None


class KindToken(enum.Enum):
    """
    Класс для представления типов токенов.
    """
    identifier = 0
    keyword = 1
    literal = 2  # Аналог expression
    operator = 3
    punctuation = 4
    whiteSpace = 5
    none = None


class Token:
    """
    Класс для представления отдельных лексем (токенов) в исходном коде.
    """

    def __init__(self, start_index: int, line_index: int, value: str, kind=KindToken.none):
        """
        Инициализирует объект класса `Token` с заданными параметрами: `start_index`, `line_index`, `value` и `kind`.
        Если `kind` не задан или равен `KindToken.none`, то вызывается метод `_define_kind_token()` для определения типа
         токена.
        :param start_index: Индекс символа начала токена
        :param line_index: индекс строки
        :param value: значение
        :param kind: тип
        """
        self.start_index = start_index
        self.line_index = line_index
        self.value = value
        self.kind = kind if kind is not KindToken.none else self._define_kind_token()

    def _define_kind_token(self) -> KindToken:
        """
        :return: Определяет тип токена на основе его значения.
        """
        if self.value in keywords:
            return KindToken.keyword
        if self.value in operators:
            return KindToken.operator
        if self.value in punctuations:
            return KindToken.punctuation
        if '\'' in self.value or '"' in self.value or any(oper in self.value for oper in operators):
            return KindToken.literal
        if self.value.isspace() or self.value == r"\n" or self.value == r"\t":
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
