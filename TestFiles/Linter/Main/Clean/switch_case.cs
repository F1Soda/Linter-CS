int number = 3;
string message;

switch (number)
{
	case 1:
		message = "Число равно 1";
		break;
	case 2:
		message = "Число равно 2";
		break;
	case 3:
		message = "Число равно 3";
		break;
	default:
		message = "Число не равно 1, 2 или 3";
		break;
}

Console.WriteLine(message);
