using System;

class Program
{
    static void Main()
    {
        try
        {
            int[] numbers = { 1, 2, 3, 4, 5 };
            int sum = CalculateSum(numbers);
            Console.WriteLine($"Сумма чисел в массиве: {sum}");
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Произошла ошибка: {ex.Message}");
        }
    }

    static int CalculateSum(int[] numbers)
    {
        if (numbers == null)
        {
            throw new ArgumentNullException("Массив чисел не может быть пустым");
        }

        int sum = 0;
        foreach (int num in numbers)
        {
            sum += num;
        }

        return sum;
    }
}
