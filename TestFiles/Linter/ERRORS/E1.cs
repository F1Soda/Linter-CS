foreach (var possibleDir in GetPossibleDirections())
{
  var nextPoint = possibleDir + point;
  if (pointToOwnedLocations.ContainsKey(nextPoint) ||
    !map.InBounds(nextPoint) ||
    map.Maze[nextPoint.X, nextPoint.Y] == MapCell.Wall)
    continue;
  yield return pointToOwnedLocations[nextPoint] = new OwnedLocation(playerIndex, nextPoint, distance + 1);
  queue.Enqueue((nextPoint, playerIndex, distance + 1));
}
