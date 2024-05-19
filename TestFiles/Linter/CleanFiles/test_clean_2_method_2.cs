private static void ProcessPath(string path, Node root, Dictionary<string, Node> nodes)
{
	var parts = path.Split('\\');
	var currentNode = root;
	var currentPath = "";

	foreach (var part in parts)
	{
		currentPath += part + '\\';
		if (!nodes.TryGetValue(currentPath, out var node))
		{
			currentNode.Children.Add(node);
			nodes[currentPath] = node;
		}

		currentNode = node;
	}
}