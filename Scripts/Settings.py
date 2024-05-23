from Flag import Flag, CategoryStyleRule


class Settings:
    def __init__(self):
        # GENERAL
        types = CategoryStyleRule
        self.indent_style = Flag("tab", types.FR)
        self.indent_size = Flag(4, types.FR)
        self.insert_final_newline = Flag(True, types.FR)
        self.hard_wrap_at = Flag(120, types.FR)

    def read_flags_from_file(self, file):
        with open(file, 'r') as f:
            for line in f:
                if "#" in line or line == "\n":
                    continue
                name, value = line.strip().split(' = ')
                if value.isdigit():
                    value = int(value)
                elif value in ["True", "true"]:
                    value = True
                elif value in ["False", "false"]:
                    value = False
                if hasattr(self, name):
                    flag = getattr(self, name)
                    flag.value = value
