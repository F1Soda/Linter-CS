using System;

public class MyClass
{
	public MyClass(int value)
	{
		Value = value;
	}

	public void DisplayValue()
	{
		Console.WriteLine("Текущее значение: " + Value);
	}
}

class Program
{
	static void Main()
	{
		MyClass myObject = new MyClass(0);

		do
		{
			myObject.DisplayValue();
			myObject.Value++;
		} while (myObject.Value < 5);

		Console.WriteLine("Цикл завершен.");
	}
}