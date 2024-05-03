import enum

class CategoryStyleRule(enum.Enum):
	LanguageAndUnnecessaryCodeRules = CR = 0
	FormattingRules = FR = 1
	NamingRules = NR = 2
	OtherRules = OR = 3

class Flag:
	def __init__(self, value, category: CategoryStyleRule, default_value, message=""):
		self._value = value
		self.category = category
		self.default_value = default_value
		self.message = message

	def get_value(self):
		return self.default_value if self._value is None else self._value
