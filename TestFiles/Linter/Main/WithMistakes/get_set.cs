public T Value
{
	get

{
		asasas();
		}
	set ;
}

public int A
{
	get	{
		var current = root;
		var currentIndex = index;
		while (true)
		{
			if (current.CountLeftNodes == currentIndex)
				return current.Value;
			if (current.CountLeftNodes > currentIndex)
				current = current.Left;
			else
			{
				currentIndex -= current.CountLeftNodes + 1;
				current = current.Right;
			}
		}
	}
}