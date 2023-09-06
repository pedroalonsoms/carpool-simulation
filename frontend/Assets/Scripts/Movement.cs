using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class NewBehaviourScript : MonoBehaviour
{
    public List<GameObject> waypoints = new List<GameObject>();
    private Transform targetWaypoint;
    private int targetWaypointIndex = 0;
    private float minDistance = 0.1f;

    // Start is called before the first frame update
    void Start()
    {
        targetWaypoint = waypoints[targetWaypointIndex].transform;
    }

    // Update is called once per frame
    void Update()
    {

        if (targetWaypointIndex == 0)
        {
            transform.position = targetWaypoint.position;
        }
        else
        {
            transform.LookAt(2 * transform.position - targetWaypoint.position);
            transform.position = Vector3.MoveTowards(transform.position, targetWaypoint.position, Time.deltaTime * 250);
        }
        // Si llegamos a ese punto, nomás actualizamos el target
        if (Vector3.Distance(targetWaypoint.position, transform.position) < minDistance && targetWaypointIndex < waypoints.Count - 1)
        {
            targetWaypointIndex = (targetWaypointIndex + 1);
            targetWaypoint = waypoints[targetWaypointIndex].transform;
        }
    }
}