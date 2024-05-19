	// Тут вообще какое то комбо -- замечает только пробел, а на \t пофег
	public  	void AddItem(TItem item)
	{
		Items.Add(item);
		stackOperations.Push((item, null));
	}