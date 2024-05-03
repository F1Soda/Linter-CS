using System;
namespace S {
	class P {
		static void Main() {
			int x = 10, y = 5;
			if (x > y)
				Console.WriteLine("x > y");
			else {
				Console.WriteLine("x <= y");
			}
			for (int i = 0; i < x; i++)
				Console.WriteLine(i % 2 == 0 ? $"Число {i} - четное" : $"Число {i} - нечетное";
			Console.WriteLine($"Сумма x и y: {x + y}");
		}
	}
}
