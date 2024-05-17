import enum
from Utils import CustomList

keywords = ['abstract', 'as', 'base', 'bool', 'break', 'byte', 'case', 'catch', 'char', 'checked', 'class', 'const',
            'continue', 'decimal', 'default', 'delegate', 'do', 'double', 'else', 'enum', 'event', 'explicit', 'extern',
            'false', 'finally', 'fixed', 'float', 'for.cs', 'foreach', 'goto', 'if', 'implicit', 'in', 'int',
            'interface',
            'internal', 'is', 'lock', 'long', 'namespace', 'new', 'null', 'object', 'operator', 'out', 'override',
            'params', 'private', 'protected', 'public', 'readonly', 'ref', 'return', 'sbyte', 'sealed', 'short',
            'sizeof', 'stackalloc', 'static', 'string', 'struct', 'switch', 'this', 'throw', 'true', 'try', 'typeof',
            'uint', 'ulong', 'unchecked', 'unsafe', 'ushort', 'using', 'virtual', 'void', 'volatile', 'while']

punctuations = [';', ':', ',', '.', '(', ')', '[', ']', '{', '}', '?']

operators = ['+', '-', '*', '/', '%', '=', '>>', '<<', '&', '&&', '|', '||', '!', '^', '>', '>=', '<', '<=', '==', '!=',
             '~', '+=', '-=', '/=', '*=', '%=', '++', '--']

backslash_character_literals = [r'\n', r'\r', r'\f', r'\t', r'\a', r'\b', r'\o', r'\v', r'\\', r"\'", r'\"']

number_postfixes = ['f', 'l', 'd']


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
        if self.value in punctuations:
            return KindToken.punctuation
        if self.value in operators:
            return KindToken.operator
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


class Tokenizer:
    """
    Класс для лексического анализа (токенеризации) исходного кода.
    """

    def __init__(self, rfile: CustomList):
        """
        Инициализирует объект класса `Tokenizer` с заданным параметром `rfile` - списком символов исходного кода.
        """
        self.tokens = CustomList([])
        self.rfile = rfile
        self.abs_index_char = 0
        self.index_line = 1
        self.index_char = 0
        self.current_char = ""
        self.next_char = ""
        self._tokenize()

    def _tokenize(self):
        """
        Выполняет лексический анализ (токенеризацию) исходного кода.
        """
        token = ""
        while self.abs_index_char < len(self.rfile):
            self._update_data()
            # Token
            if self.current_char.isalpha():
                token += self.current_char
                continue
            elif token != '':
                self.tokens.append(Token(self.index_char, self.index_line, token))
                self.index_char += len(token)
                token = ""

            if (self._check_comments() or
                    self._check_white_spaces() or
                    self._check_operators() or
                    self._check_punctuation() or
                    self._check_string_literal() or
                    self._check_integer_literal()):
                continue

            raise Exception(
                "Undefined char = " +
                f'"{self.current_char}"\nLine was:' +
                f"...{''.join(self.rfile[self.abs_index_char - 10:self.abs_index_char + 10])}...")
        if token != "":
            self.tokens.append(Token(self.index_char, self.index_line, token))

    def _update_data(self):
        """
        Обновляет значения current_char, next_char и abs_index_char.
        """
        self.current_char = self.rfile[self.abs_index_char]
        self.next_char = self.rfile.at(self.abs_index_char + 1)
        self.abs_index_char += 1

    def _check_string_literal(self, nested=False):
        """
        Проверяет, является ли текущий символ началом строковой константы, и выполняет ее чтение. Может сама себя
        вызывать для обрабатывания случаев @$ и $@
        :param nested: при вложении поведение другое
        """
        if self.current_char == '"' or self.current_char == "'":
            res = self._get_string_literal(self.current_char)
            if nested:
                return res
            self.tokens.append(Token(self.index_char, self.index_line, res))
            self.index_char += len(res)
            return True

        elif self.current_char == '$':
            index = self.index_char
            self._update_data()
            res = "$" + self._check_string_literal(nested=True)
            if nested:
                return res
            self.tokens.append(Token(index, self.index_line, res))
            self.index_char += len(res)
            return True

        elif self.current_char == '@':
            index = self.index_char
            self._update_data()
            res = "@" + self._check_string_literal(nested=True)
            if nested:
                return res
            self.tokens.append(Token(index, self.index_line, res))
            self.index_char += len(res)
            return True

        return False

    def _check_integer_literal(self) -> bool:
        """
        Проверяет, является ли текущий символ началом целочисленной константы, и выполняет ее чтение.
        :return: True, если удалось прочесть и False в противном случае
        """
        if self.current_char.isdigit():
            self.tokens.append(Token(self.index_char, self.index_line, self._get_integer_literal()))
            return True
        return False

    def _check_operators(self) -> bool:
        """
        Проверяет, является ли текущий символ оператором, и выполняет его чтение.
        :return: True, если удалось прочесть и False в противном случае
        """
        if self.next_char is not None and self.current_char + self.next_char in operators:
            self.tokens.append(Token(self.index_char, self.index_line, self.current_char + self.next_char))
            self.abs_index_char += 1
            self.index_char += 2
            return True

        elif self.current_char in operators:
            self.tokens.append(Token(self.index_char, self.index_line, self.current_char))
            self.index_char += 1
            return True

        return False

    def _check_punctuation(self) -> bool:
        """
        Проверяет, является ли текущий символ знаком препинания, и выполняет его чтение.
        :return: True, если удалось прочесть и False в противном случае
        """
        if self.current_char in punctuations:
            if self.current_char == '<' and self.next_char is not None and self.next_char == '<':
                self.tokens.append(Token(self.index_char, self.index_line, '<<'))
                self.abs_index_char += 1
                self.index_char += 2
                return True
            elif self.current_char == '>' and self.next_char is not None and self.next_char == '>':
                self.tokens.append(Token(self.index_char, self.index_line, '>>'))
                self.abs_index_char += 1
                self.index_char += 2
                return True
            else:
                self.tokens.append(Token(self.index_char, self.index_line, self.current_char))
                self.index_char += 1
                return True
        return False

    def _check_white_spaces(self) -> bool:
        """
        Проверяет, является ли текущий символ пробельным, и выполняет его чтение.
        :return: True, если удалось прочесть и False в противном случае
        """
        if self.current_char.isspace():
            self.tokens.append(Token(self.index_char, self.index_line, self.current_char))
            self.index_char += 1
            return True
        elif self.next_char is not None:
            if self.current_char + self.next_char == r'\n':
                self.tokens.append(Token(self.index_char, self.index_line, self.current_char + self.next_char))
                self.index_line += 1
                self.index_char = 0
                self.abs_index_char += 1
                return True
            elif self.current_char + self.next_char in backslash_character_literals:
                self.tokens.append(Token(self.index_char, self.index_line, self.current_char + self.next_char))
                self.abs_index_char += 1
                self.index_char += 2
                return True
        return False

    def _check_comments(self) -> bool:
        """
        Проверяет, является ли текущий символ началом комментария, и выполняет его чтение.
        :return: True, если удалось прочесть и False в противном случае
        """
        if self.next_char and self.current_char + self.next_char == r"//":
            while self.next_char is not None and self.current_char + self.next_char != r"\n":
                self.abs_index_char += 1
                self._update_data()
            self.abs_index_char += 1
            self.index_line += 1
            return True

        if self.next_char and self.current_char + self.next_char == "/*":
            while self.next_char is not None and self.current_char + self.next_char != r"*/":
                if self.current_char + self.next_char != r"\n":
                    self.index_line += 1
                self.abs_index_char += 1
                self._update_data()
            self.abs_index_char += 1
            return True

        return False

    def _get_string_literal(self, quote='"') -> str:
        """
        Выполняет чтение строковой константы, заключенной в кавычки `quote`.
        :param quote: Тип кавычек
        :return: True, если удалось прочесть и False в противном случае
        """
        literal = quote
        while True:
            self.current_char = self.rfile[self.abs_index_char]
            if self.current_char == quote:
                self.abs_index_char += 1
                return literal + quote
            literal += self.current_char
            self.abs_index_char += 1

    def _get_integer_literal(self) -> str:
        """
        Возвращает первый в списке токен, который не является пробельным.
        :return: True, если удалось прочесть и False в противном случае
        """
        literal = self.rfile[self.abs_index_char - 1]
        while True:
            char = self.rfile[self.abs_index_char]  # type: str
            next_char = self.rfile.at(self.abs_index_char + 1)
            if char.isspace() or next_char is not None and char + next_char in backslash_character_literals:
                self.index_char += len(literal)
                return literal
            if not char.isdigit() and char not in number_postfixes + ['E', 'e', '.']:
                self.index_char += len(literal)
                return literal
            literal += char
            self.abs_index_char += 1

    def print(self) -> str:
        """
        Красиво в виде строчки возвращает затокенезированный файл
        :return: строка со всеми токенами в том же самом порядке, как и в файле
        """
        res = ""
        for token in self.tokens:  # type: Token
            if token.value == r'\n':
                res += token.value
                res += '\n'
            elif token.value == ' ':
                res += " "
            else:
                res += token.value
        return res


if __name__ == "__main__":
    # TODO: Убрать потом
    with open("TestFiles/Tokenizer/test_white_spaces_after_new_line.cs", mode='r') as f:
        tokenizer = Tokenizer(CustomList(repr(f.read())[1:-1]))
        print(tokenizer.print())
