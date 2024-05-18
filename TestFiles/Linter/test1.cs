using System;

namespace KeywordsExample
{
    class Program
    {
        static void Main()
        {
            int a = 10;
            int b = 20;

            if (a + b > 15)
            {
                Console.WriteLine(@"Результат больше 15!");
            }
            else
            {
                Console.WriteLine(@"Результат меньше или равен 15.");
            }

            for (int i = 0; i < 5; i++)
            {
                Console.WriteLine($@"Цикл #{i + 1}");
            }

            string[] fruits = { "яблоко", "груша", "банан" };
            foreach (string fruit in fruits)
            {
                Console.WriteLine($@"Фрукт: {fruit}");
            }

            switch (a)
            {
                case 10:
                    Console.WriteLine(@"a равно 10");
                    break;
                default:
                    Console.WriteLine(@"a не равно 10");
                    break;
            }

            while (b > 15)
            {
                b--;
            }

            do
            {
                b++;
            }
            while (b < 20);

            var obj = new { Name = "John", Age = 30 };
            Console.WriteLine($@"Name: {obj.Name}, Age: {obj.Age}");
        }
    }
}
