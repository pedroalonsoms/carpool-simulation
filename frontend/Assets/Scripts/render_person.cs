using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class render_person : MonoBehaviour
{
    public GameObject prefabPerson;
    public int clones = 0;
    public float x = 0, y = 1.5f, z = 0;
    public int scale = 1;
    public int xMultiplicator = 1, zMultiplicator = 1;
    public float rotation = 0;
    GameObject[] total_clones;
    // Start is called before the first frame update
    void Start()
    {
        total_clones = new GameObject[clones];

        for (int i = 0; i < clones; i++)
        {
            total_clones[i] = Instantiate(prefabPerson, new Vector3(x + (i * xMultiplicator), y, z + (i * zMultiplicator)), Quaternion.Euler(0, rotation, 0));
            total_clones[i].transform.localScale = new Vector3(scale, scale, scale);
            // total_clones[i].transform.localRotation = new Vector3(0, rotation, 0);
        }
    }

    // Update is called once per frame
    void Update()
    {

    }
}
