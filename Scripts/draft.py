import argparse


def main():
	parser = argparse.ArgumentParser(description='Простое консольное приложение')

	parser.add_argument("file", help="Путь до файла", type=str, nargs='?')
	parser.add_argument("-v", "--verbose", help="Вывести подробный вывод", action="store_true")
	parser.add_argument("-n", "--name", help="Указать имя")

	args = parser.parse_args()

	if args.verbose:
		print("Подробный вывод")

	if args.name:
		print(f"Привет, {args.name}!")

	if args.file:
		print(f"Путь до файла: {args.file}")


if __name__ == '__main__':
	main()
