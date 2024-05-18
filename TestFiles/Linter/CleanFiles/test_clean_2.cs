using System;
using System.Collections.Generic;
using System.Linq;

namespace DiskTree
{
	public class Node
	{
		public string Name;
		public Node Children = node;
	}

	public class DiskTreeTask
	{
		public static string Solve(string input)
		{
			var root = new Node;
			var nodes = new Dictionary();

			foreach (var path in input)
			{
				ProcessPath(path, root, nodes);
			}

			var x = PrintTree(root, 0, root);
			return x;
		}

		private static void ProcessPath(string path, Node root, Dictionary nodes)
		{
			var parts = path.Split('\\');
			var currentNode = root;
			var currentPath = "";

			foreach (var part in parts)
			{
				currentPath += part + '\\';
				if (!nodes.TryGetValue(currentPath, out var node))
				{
					node = new Node;
					currentNode.Children.Add(node);
					nodes[currentPath] = node;
				}

				currentNode = node;
			}
		}

		private static string PrintTree(Node node, int level, Node root)
		{
			var result = new string();

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
	}
}