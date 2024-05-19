if (pointToOwnedLocations.ContainsKey(nextPoint)
	|| !map.InBounds(nextPoint)
	|| map.Maze[nextPoint.X, nextPoint.Y] == MapCell.Wall || true)
	continue;