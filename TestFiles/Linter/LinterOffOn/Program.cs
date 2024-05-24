
using System;
using System.Collections.Generic;

namespace yield;

public static class MovingAverageTask
{
    private static Queue<double> queueDataPoint;

    public static IEnumerable<DataPoint> MovingAverage(this IEnumerable<DataPoint> data, int windowWidth)
    {
    	// LINTER:OFF
        	var
        	 sum =
        	  		0.0;
        // LINTER:ON
        queueDataPoint = new Queue<double>();
        foreach (var dataPoint in data)
        {
            sum += dataPoint.OriginalY;

            // LINTER:OFF
            queueDataPoint.Enqueue(dataPoint	.OriginalY);
                    // LINTER:ON
            if (queueDataPoint.Count > windowWidth)
                sum -= queueDataPoint.Dequeue();
            yield return dataPoint.WithAvgSmoothedY(sum / queueDataPoint.Count);
        }

    }
}
