int a = 10, b = 5;
string result;
if (a > b)
	result = "a больше b";
else
	result = "a меньше или равно b";
Console.WriteLine(result);

if (true)
	if (false)
	{
		if (true)
			Write();
		else if (false)
		{
			Write();
		}
		else
			a = 1;
	}
