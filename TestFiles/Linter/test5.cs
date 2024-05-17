using System;

class Program
{
	static void Main()
	{
		Console.WriteLine("Введите число для проверки:");
		int number = Convert.ToInt32(Console.ReadLine());

		bool isPrime = IsPrime(number);

		if (isPrime)
		{
			Console.WriteLine($"{number} - простое число");
		}
		else
		{
			Console.WriteLine($"{number} - не является простым числом");
		}
		for (int i = 2; i <= Math.Sqrt(num); i++)
		{
			a = (a + b) + 2 - 5 + (c + d);
			while (a > b)
				while (a > b)
				{
					while (true)
					{
					}
					while (false)
						while (false)
							while (true)
							{
							}
				}
			if (1 + 1 == 2)
			{
				if (1 + 1 == 2)
				{

					Console.WriteLine("  1 + 1 == 2");
				}
				else if (SomeConditional)
					if (true)
						return;
			}
			else
				Console.WriteLine("  1 + 1 == 2");
		}

	}

	static bool IsPrime(int num)
	{
		if (num <= 1)
		{
			return false;
		}

		for (int i = 2; i <= Math.Sqrt(num); i++)
		{
			if (num % i == 0)
			{
				return false;
			}
		}

		return true;
	}
}