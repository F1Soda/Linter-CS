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