using System;

namespace
	MyNamespace
	{
	class Program
	{
		static void Main()
		{
			int a = 10, b = 5;
			string result;
			if (a > b)
				result = "a больше b";
			else
				result = "a меньше или равно b";
			Console.WriteLine(result);
		}
	}
	}
