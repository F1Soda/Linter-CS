namespace ProjectZero
{
	private int OverlapSphere(Vector3 position) => Physics.OverlapSphereNonAlloc(position, _sphereRadiusAttackZone, _overlapResults, layerEnemy.value);
}
