using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.SceneManagement;

public class StartScript : MonoBehaviour
{
    // They reference the references of the sliders that will be given from the Unity Editor
    public Slider carProbabilitySlider;
    public Slider personProbabilitySlider;

    // When this scene ends, we pass the parameters to the next scene
    void OnDisable() {
        PlayerPrefs.SetFloat("carSpawnRate", carProbabilitySlider.value);
        PlayerPrefs.SetFloat("personSpawnRate", personProbabilitySlider.value);
    }

    // When user clicks "START", we need to load the new scene
    public void OnStartButtonClick() {
        SceneManager.LoadScene("SimulationScene", LoadSceneMode.Single);
    }

    // Start is called before the first frame update
    void Start()
    {

    }

    // Update is called once per frame
    void Update()
    {
        
    }
}
