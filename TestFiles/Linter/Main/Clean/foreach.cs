foreach (string color in colors)
{
	Console.WriteLine("Цвет: " + color);
}

Console.WriteLine("Цикл завершен.");

foreach (int number in numbers)
	Console.WriteLine(number);

foreach (int number in numbers)
	foreach (int number in numbers)
	{
		foreach (int number in numbers)
			Console.WriteLine(number);
	}