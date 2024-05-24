using System;
using System.Collections;
using System.Collections.Generic;

namespace BinaryTrees;

public class BinaryTree<T> : IEnumerable<T> where T : IComparable
{
	private class Node
	{
		public T Value { get; }
		public Node Left { get; set; }
		public Node Right { get; set; }

		public int CountLeftNodes { get; set; }

		public int CountRightNodes { get; set; }

		public Node(T value)
		{
			Value = value;
		}
	}


	private Node root;

	public void Add(T value)
	{
		var newNode = new Node(value);
		if (root is null)
		{
			root = newNode;
			return;
		}
		var current = root;
		while (current is { } parent)
		{
			if (value.CompareTo(current.Value) < 0)
			{
				current.CountLeftNodes += 1;
				current = current.Left;
				if (current is null) parent.Left = newNode;
			}
			else
			{
				current.CountRightNodes += 1;
				current = current.Right;
				if (current is null) parent.Right = newNode;
			}
		}
	}

	public bool Contains(T value)
	{
		var current = root;
		while (current != null)
		{
			if (current.Value.CompareTo(value) == 0)
				return true;
			current = value.CompareTo(current.Value) < 0 ? current.Left : current.Right;
		}
		return false;
	}

	public IEnumerator<T> GetEnumerator()
	{
		if (root is null)
			yield break;

		if (root.Left is not null)
		{
			foreach (var node in GetRecursiveNodes(root.Left))
				yield return node.Value;
		}

		yield return root.Value;

		if (root.Right is not null)
		{
			foreach (var node in GetRecursiveNodes(root.Right))
				yield return node.Value;
		}
	}

	public T this[int index]
	{
		get
		{
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

	private IEnumerable<Node> GetRecursiveNodes(Node currentNode)
	{
		if (currentNode is null)
			yield break;

		foreach (var node in GetRecursiveNodes(currentNode.Left))
			yield return node;

		yield return currentNode;

		foreach (var node in GetRecursiveNodes(currentNode.Right))
			yield return node;
	}

	IEnumerator IEnumerable.GetEnumerator() => GetEnumerator();
}
