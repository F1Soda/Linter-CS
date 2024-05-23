import enum


class CategoryStyleRule(enum.Enum):
    LanguageAndUnnecessaryCodeRules = CR = 0
    FormattingRules = FR = 1
    NamingRules = NR = 2
    OtherRules = OR = 3


class Flag:
    def __init__(self, value, category: CategoryStyleRule, message=""):
        """
        :param value: Значение флага. Если значение равно None, флаг будет использовать значение по умолчанию.
        :param category: Категория правила стиля, с которой связан флаг.
        :param message:  Необязательное сообщение, связанное с флагом.
        """
        self.value = value
        self.category = category
        self.message = message
