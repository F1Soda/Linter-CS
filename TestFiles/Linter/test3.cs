string option = "case2";

switch (option)
{
	case "case1":
		a = a + 4;
		break;
	case "case2":
		Console.WriteLine("Вы выбрали Case 2");
		break;
	default:
		Console.WriteLine("Ни один из вариантов не соответствует");
		break;
}
