using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class render_car : MonoBehaviour
{
    public GameObject prefabCar;
    public int clones = 10;
    public float x = 0, y = 1.5f, z = 0;
    GameObject[] total_clones;
    // Start is called before the first frame update
    void Start()
    {
        total_clones = new GameObject[clones];

        for (int i = 0; i < clones; i++)
        {
            total_clones[i] = Instantiate(prefabCar, new Vector3(x, y, z + (i * 80)), Quaternion.Euler(0, 0, 0));
            total_clones[i].transform.localScale = new Vector3(45, 45, 45);
        }
    }

    // Update is called once per frame
    void Update()
    {

    }
}
