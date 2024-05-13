from Flag import Flag, CategoryStyleRule


class Settings:
	def __init__(self, flags):
		# GENERAL
		types = CategoryStyleRule
		self.indent_style = Flag("tab", types.FR, "spaces")
		self.indent_size = Flag(4, types.FR, 4)
		self.trim_trailing_whitespace = Flag(True, types.FR, True)
		self.insert_final_newline = Flag(True, types.FR, True)

		# CUSTOM
		self.remove_whitespaces_between_tokens = Flag(True, types.FR, True)
		self.end_line_with_semicolon = Flag(True, types.FR, True)
		self.after_if_whitespace = Flag(True, types.FR, True)

		# USING AND NAMESPACESk
		self.csharp_using_directive_placement = Flag("outside_namespace", types.CR, "outside_namespace")
		self.csharp_prefer_simple_using_statement = Flag(True, types.LanguageAndUnnecessaryCodeRules, True)
