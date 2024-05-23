foreach (var color in colors)
{
	Console.WriteLine("Цвет: " + color);
}

Console.WriteLine("Цикл завершен.");

foreach (var number in numbers)
	Console.WriteLine(number);

foreach (var number in numbers)
	foreach (var number in numbers)
	{
		foreach (var number in numbers)
			Console.WriteLine(number);
	}
