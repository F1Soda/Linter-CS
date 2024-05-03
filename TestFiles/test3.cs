using System;

namespace AnotherExample
{
    class Program
    {
        static void Main()
        {
            int x = 10;
            int y = 5;

            if (x > y)
            {
                Console.WriteLine("x больше y");
            }
            else
            {
                Console.WriteLine("x меньше или равно y");
            }

            for (int i = 0; i < x; i++)
            {
                if (i % 2 == 0)
                {
                    Console.WriteLine($"Число {i} - четное");
                }
                else
                {
                    Console.WriteLine($"Число {i} - нечетное");
                }
            }

            int result = AddNumbers(x, y);
            Console.WriteLine($"Сумма чисел x и y: {result}");

            string s = "Пример строки";
            Console.WriteLine($"Длина строки: {s.Length}");

            PrintMessage();

            var student = new { Name = "Александр", Age = 25 };
            Console.WriteLine($"Студент: {student.Name}, возраст {student.Age}");
        }

        static int AddNumbers(int a, int b)
        {
            return a + b;
        }

        static void PrintMessage()
        {
            Console.WriteLine("Привет, мир!");
        }
    }
}
