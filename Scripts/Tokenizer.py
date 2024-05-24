from Settings import Settings
from exceptions import UnexpectedChar
from Utils import *


class Tokenizer:
    """
    Класс для лексического анализа (токенеризации) исходного кода.
    """

    def __init__(self, rfile: CustomList, settings: Settings, lines: list):
        """
        Инициализирует объект класса `Tokenizer` с заданным параметром `rfile` - списком символов исходного кода.
        """
        self.tokens = CustomList([])
        self.settings = settings
        self.lines = lines
        self.rfile = rfile
        self.abs_index_char = 0
        self.index_line = 1
        self.index_char = 0
        self.current_char = ""
        self.next_char = ""
        self.lines_with_comments = []
        self.too_long_lines = []
        self.line_lengths = []
        self._tokenize()

    def __str__(self):
        return str([token.value for token in self.tokens])

    def __repr__(self):
        return self.__str__()

    def _tokenize(self):
        """
        Выполняет лексический анализ (токенеризацию) исходного кода.
        """
        token = ""
        while self.abs_index_char < len(self.rfile):
            self._update_data()
            # Token
            if self.current_char.isalpha() or self.current_char == "_":
                token += self.current_char
                continue
            elif token != '':
                self.tokens.append(Token(self.index_char, self.index_line, token))
                self.index_char += len(token)
                token = ""

            if (self._check_comments() or
                    self._check_white_spaces() or
                    self._check_punctuation() or
                    self._check_operators() or
                    self._check_string_literal() or
                    self._check_integer_literal()):
                continue

            raise UnexpectedChar(self.current_char,
                                 ''.join(self.rfile[self.abs_index_char - 10:self.abs_index_char + 10]))
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
            if self.current_char == '<':
                if self.next_char is not None and self.next_char == '<':
                    self.tokens.append(Token(self.index_char, self.index_line, '<<'))
                    self.abs_index_char += 1
                    self.index_char += 2
                    return True

            elif self.current_char == '>':
                if self._check_punctuation_angle_bracket(len(self.tokens) - 1):
                    self.tokens.append(
                        Token(self.index_char, self.index_line, self.current_char, KindToken.punctuation))
                    self.index_char += 1
                    return True
                if self.next_char is not None and self.next_char == '>':
                    self.tokens.append(Token(self.index_char, self.index_line, '>>'))
                    self.abs_index_char += 1
                    self.index_char += 2
                    return True
                return False

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
                self._processing_new_line()
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
        if self.next_char and self.current_char + self.next_char == "//":
            self.lines_with_comments.append(self.index_line)
            if "LINTER:OFF" in self.lines[self.index_line-1]:
                self.abs_index_char += len(self.lines[self.index_line-1][(self.index_char+2):]) + 3
                self.index_char = 0
                self.index_line += 1
                while "LINTER:ON" not in self.lines[self.index_line-1]:
                    self.abs_index_char += len(self.lines[self.index_line-1]) + 2
                    self.index_line += 1
                self.abs_index_char += len(self.lines[self.index_line-1])
            else:
                while self.next_char is not None and self.current_char + self.next_char != r"\n":
                    self._update_data()
                self.tokens.append(Token(self.index_char, self.index_line, r'\n'))
                self.abs_index_char += 1
                self.index_line += 1
                self.index_char = 0
            return True

        if self.next_char and self.current_char + self.next_char == "/*":
            self.lines_with_comments.append(self.index_line)
            while self.next_char is not None and self.current_char + self.next_char != r"*/":
                if self.current_char + self.next_char == r"\n":
                    self._processing_new_line()
                    self.lines_with_comments.append(self.index_line)
                self._update_data()
                self.index_char += 1
            self.tokens.append(Token(self.index_char, self.index_line, r'\n'))
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
        while self.abs_index_char < len(self.rfile):
            self.current_char = self.rfile[self.abs_index_char]
            if self.current_char == quote:
                self.abs_index_char += 1
                return literal + quote
            literal += self.current_char
            self.abs_index_char += 1
        return literal

    def _get_integer_literal(self) -> str:
        """
        Возвращает первый в списке токен, который не является пробельным.
        :return: True, если удалось прочесть и False в противном случае
        """
        literal = self.rfile[self.abs_index_char - 1]
        while self.abs_index_char < len(self.rfile):
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
        return literal

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

    def _check_punctuation_angle_bracket(self, start_index_token: int) -> bool:
        """
        Осуществляет проверку, для токена >. Суть заключается в том, что < парсится как оператор, а когда токенайзер
        встречает >, то запускается проверка, которая при удачном исходе изменяет тип < и возвращает индекс токена <
        :param start_index_token: Функция может вызываться рекурсивно, для вложенных generic типов.
        С этого токена начинается проверка на <
        :return: True если пунктуация, и False если оператор
        """
        index_token = start_index_token
        token = self.tokens[start_index_token]  # type: Token
        while token is not None and token.value != ";":
            if token.value == "<" and token.kind != KindToken.punctuation:
                index_first_not_whitespace_token_back = self._get_index_first_not_whitespace_token_back(index_token - 1)
                back_token = self.tokens[index_first_not_whitespace_token_back]
                if back_token.value == ",":
                    token.kind = KindToken.punctuation
                    return True
                if back_token.kind == KindToken.identifier:
                    # next_token = self._get_next_not_space_token_value(self.abs_index_char - 1)
                    # if next_token.kind == KindToken.identifier:
                    #     return False
                    # else:
                    token.kind = KindToken.punctuation
                    return True

                return False

            if token.value == ">" and token.kind != KindToken.punctuation:
                if self._check_punctuation_angle_bracket(index_token - 1):
                    token.kind = KindToken.punctuation

            if token.kind == KindToken.operator:
                return False

            index_token -= 1
            token = self.tokens.at(index_token)

    def _get_index_first_not_whitespace_token_back(self, start_index_token: int) -> int:
        """
        Возвращает индекс первого не пробельного токена в списке существующих токенов
        :param start_index_token: индекс токена, с которого начинается поиск
        :return: индекс токена или None, если не нашел
        """
        index = start_index_token
        token = self.tokens[start_index_token]
        while index >= 0:
            if token.kind != KindToken.whiteSpace:
                return index
            index -= 1
            token = self.tokens[index]
        return -1

    def _get_next_not_space_token_value(self, start_index: int) -> Token:
        """
        Получает первый не пробельный токен, начиная поиск с индекса start_index
        :param start_index: абсолютный индекс символа, с которого начинается поиск.
        :return: Возвращает токен или None, если не удалось найти.
        """
        token = ""
        index = start_index + 1
        while index < len(self.rfile):
            current_char = self.rfile[index]
            if current_char == " ":
                index += 1
                continue
            if current_char == "\\" and (self.rfile[index + 1] == "n" or self.rfile[index + 1] == "t"):
                index += 2
                continue
            if current_char.isalpha() or current_char == "_":
                token += current_char
                index += 1
                continue
            elif token != '':
                return Token(start_index, self.index_line, token)
            return Token(index, self.index_line, current_char)
        return None

    def _processing_new_line(self):
        count_chars = self.index_char + 1 + self.lines[self.index_line - 1].count("\t") * (
                self.settings.indent_size.value - 2)
        self.line_lengths.append(count_chars)
        if count_chars > self.settings.hard_wrap_at.value:
            self.too_long_lines.append((self.index_line, count_chars))
        self.index_line += 1
        self.index_char = 0


if __name__ == "__main__":
    # TODO: Убрать потом
    with open("TestFiles/Linter/Program.cs", mode='r') as f:
        tokenizer = Tokenizer(CustomList(repr(f.read())[1:-1]))
        print(tokenizer.print())
