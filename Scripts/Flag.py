import enum


class CategoryStyleRule(enum.Enum):
    LanguageAndUnnecessaryCodeRules = CR = 0
    FormattingRules = FR = 1
    NamingRules = NR = 2
    OtherRules = OR = 3


class Flag:
    def __init__(self, value, category: CategoryStyleRule, default_value, message=""):
        """
        :param value: Значение флага. Если значение равно None, флаг будет использовать значение по умолчанию.
        :param category: Категория правила стиля, с которой связан флаг.
        :param default_value: Значение по умолчанию для флага.
        :param message:  Необязательное сообщение, связанное с флагом.
        """
        self._value = value
        self.category = category
        self.default_value = default_value
        self.message = message

    def get_value(self):
        """
        Метод, который возвращает значение флага. Если значение равно None, он вернет значение по умолчанию.
        """
        return self.default_value if self._value is None else self._value
