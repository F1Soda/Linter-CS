import editorconfig

config_file_path = r'C:\Users\TIm\PycharmProjects\linter\.EditorConfig'
cs_file_path = r'C:\Users\TIm\PycharmProjects\linter\Program.cs'


def get_all_editorconfig_flags(file_path):
    config = editorconfig.get_properties(file_path)

    flags = []
    for key, value in config.items():
        flags.append(f"{key} = {value}")

    return flags


all_flags = get_all_editorconfig_flags(config_file_path)

# for flag in all_flags:
#     print(flag)

with open(cs_file_path, mode='r', encoding='utf8') as f:
    counter = 1
    for line in f:
        print(f"{counter:>{2}} {repr(line)}")
        counter += 1
