using System;
using System.Numerics;

namespace Tickets;

class TicketsTask
{
	public static BigInteger Solve(int halfLen, int totalSum)
	{
		if (totalSum % 2 != 0 || totalSum > halfLen * 18)
			return 0;

		var halfSum = totalSum / 2;
		var opt = MakeTable(halfLen, halfSum);

		return BigInteger.Pow(opt[halfLen, halfSum], 2);
	}

	private static BigInteger[,] MakeTable(int halfLen, int halfSum)
	{
		var opt = new BigInteger[halfLen + 1, halfSum + 1];

		PrepareOpt(opt, halfLen, halfSum);

		for (var i = 2; i <= halfLen; ++i)
		{
			for (var j = 1; j <= halfSum; ++j)
			{
				var sum = BigInteger.Zero;
				for (int k = 0; k < 10; k++)
				{
					if (k <= j)
						sum += opt[i - 1, j - k];
					else
						break;
				}

				opt[i, j] = sum;
			}
		}

		return opt;
	}

	private static void PrepareOpt(BigInteger[,] opt, int halfLen, int halfSum)
	{
		for (var i = 0; i <= halfLen; ++i)
			opt[i, 0] = 1;

		for (var i = 0; i <= halfSum; ++i)
		{
			if (i >= 10)
				break;
			opt[1, i] = 1;
		}

		opt[0, 0] = 0;
	}
}