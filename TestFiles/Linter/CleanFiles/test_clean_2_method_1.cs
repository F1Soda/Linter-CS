public static List<string> Solve(List<string> input)
{
	var root = new Node { Name = "" };
	var nodes = new Dictionary<string, Node>();

	foreach (var path in input)
	{
		ProcessPath(path, root, nodes);
	}

	var x = PrintTree(root, 0, root);
	return x;
}