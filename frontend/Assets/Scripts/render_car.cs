using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class render_car : MonoBehaviour
{
    public GameObject prefabCar;
    public int clones = 0;
    public float x = 0, y = 1.5f, z = 0;
    public int scale = 1;
    public int xMultiplicator = 1, zMultiplicator = 1;
    public float rotation = 0;
    GameObject[] total_clones;

    public string prefixCarName;
    public string carName;
    private int contador = 0;

    // timer properties *Temporal
    public float delay = 3;
    float timer;
    // Start is called before the first frame update
    void Start()
    {
        total_clones = new GameObject[clones];

        // for (int i = 0; i < clones; i++)
        // {
        //     carName = "CAR_" + i.ToString();
        //     total_clones[i] = Instantiate(prefabCar, new Vector3(x + (i * xMultiplicator), y, z + (i * zMultiplicator)), Quaternion.Euler(0, rotation, 0));
        //     total_clones[i].transform.localScale = new Vector3(scale, scale, scale);
        //     total_clones[i].name = carName;
        //     // total_clones[i].transform.localRotation = new Vector3(0, rotation, 0);
        // }
    }

    // Update is called once per frame
    void Update()
    {
        if (contador < clones)
        {
            carName = prefixCarName + "CAR_" + contador.ToString();
            total_clones[contador] = Instantiate(prefabCar, new Vector3(x + (contador * xMultiplicator), y, z + (contador * zMultiplicator)), Quaternion.Euler(0, rotation, 0));
            total_clones[contador].transform.localScale = new Vector3(scale, scale, scale);
            total_clones[contador].name = carName;
            contador++;
        }
    }
}
