using System;
using System.Collections.Generic;

namespace yield;

public static class MovingAverageTask
{
    private static Queue<double> queueDataPoint;

    public static IEnumerable<DataPoint> MovingAverage(this IEnumerable<DataPoint> data, int windowWidth)
    {
        var sum = 0.0;
        queueDataPoint = new Queue<double>();
        foreach (var dataPoint in data)
        {
            sum += dataPoint.OriginalY;
            queueDataPoint.Enqueue(dataPoint.OriginalY);
            if (queueDataPoint.Count > windowWidth)
                sum -= queueDataPoint.Dequeue();
            yield return dataPoint.WithAvgSmoothedY(sum / queueDataPoint.Count);
        }

    }
}
