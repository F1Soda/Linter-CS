public  	void AddItem(TItem item)
{
	Items.Add(item);
	stackOperations.Push((item, null));
}