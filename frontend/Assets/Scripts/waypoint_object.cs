using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class waypoint_object : MonoBehaviour
{

    public string wpName = "NoName";
    public Vector3 wpPosition = new Vector3(0, 0, 0);
    public int rotation = 0;
    public bool isBase = false;
    // Start is called before the first frame update
    void Start()
    {
        wpName = gameObject.name;
        wpPosition = GameObject.Find(wpName).transform.position;
    }

    // Update is called once per frame
    void Update()
    {

    }
}
