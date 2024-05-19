private static List<string> PrintTree(Node node, int level, Node root)
{
	var result = new List<string>();

	if (node.Name != "" && node != root)
		result.Add(new string(' ', level) + node.Name);

	foreach (var child in node.Children.OrderBy(n => n.Name, StringComparer.Ordinal))
	{
		var nextLevel = level + 1;
		if (node == root)
			nextLevel = 0;
		result.AddRange(PrintTree(child, nextLevel, root));
	}

	return result;
}