using System;
using System.Collections.Generic;

namespace Antiplagiarism;

public static class LongestCommonSubsequenceCalculator
{
	public static List<string> Calculate(List<string> first, List<string> second)
	{
		var opt = CreateOptimizationTable(first, second);
		return RestoreAnswer(opt, first, second);
	}

	private static int[,] CreateOptimizationTable(List<string> first, List<string> second)
	{
		var (lenFirst, lenSecond) = (first.Count, second.Count);
		var opt = new int[lenFirst + 1, lenSecond + 1];
		for (var i = 0; i <= lenFirst; ++i)
			opt[i, 0] = 0;
		for (var i = 0; i <= lenSecond; ++i)
			opt[0, i] = 0;
		for (var i = 1; i <= lenFirst; ++i)
			for (var j = 1; j <= lenSecond; ++j)
			{
				if (first[i - 1] == second[j - 1])
					opt[i, j] = opt[i - 1, j - 1] + 1;
				else
					opt[i, j] = Math.Max(opt[i - 1, j], opt[i, j - 1]);
			}
		return opt;
	}

	private static List<string> RestoreAnswer(int[,] opt, List<string> first, List<string> second)
	{
		var res = new List<string>();
		var (x, y) = (first.Count, second.Count);
		do
		{
			if (first[x - 1] == second[y - 1])
			{
				res.Add(first[x - 1]);
				x--;
				y--;
			}
			else if (opt[x - 1, y] > opt[x, y - 1])
				x--;
			else
				y--;
		} while (x >= 1 && y >= 1);
		res.Reverse();
		return res;
	}
}
