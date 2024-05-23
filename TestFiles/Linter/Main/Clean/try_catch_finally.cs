try
{
	try
	{
		Console.WriteLine("Ошибка деления на ноль");
	}
	catch
	{
		try
		{
		}
	}
	finally
	{
		try
		{
		}
	}
}
catch (DivideByZeroException ex)
{
	Console.WriteLine("Ошибка деления на ноль");
}
catch (ArgumentException ex)
{
	Console.WriteLine("Ошибка аргумента");
}
catch
{
	Console.WriteLine($"Необработанное исключение: {ex.Message}");
}
finally
{
	Console.WriteLine("Завершение программы");
}
