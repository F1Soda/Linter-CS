for (int i = 1				; i < Math.Min(10, totalSum / 2 + 1); i++)
	opt[0, i] = 1;

// Прекол в том, что в форе не работает а в Math.Min(	10, totalSum / 2 + 1); работает
for (int i = 1; i < Math.Min(	10, totalSum / 2 + 1); i++)
	opt[0, i] = 1;

Math.Min(	10, totalSum / 2 + 1)

// Короче, я ещё поковырялся и понял, что линтер не замечает лишние пробелы внутри () for, хотя по отдельности всё ок
// Ты точно рекурсивно вызываешь check_expression?