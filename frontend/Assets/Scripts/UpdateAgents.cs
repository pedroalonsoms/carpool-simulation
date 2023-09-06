using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;
using System.IO;
using System.Diagnostics;
using System;

// This is a class for the JSON Car object
[System.Serializable]
public class Car
{
    public string id;
    public int x;
    public int y;
}

// This is a class for the JSON Person object
[System.Serializable]
public class Person
{
    public string id;
    public int x;
    public int y;
}

// This is a class for the JSON object that holds all the agents during a step
[System.Serializable]
public class StepData
{
    public Car[] cars;
    public Person[] people;
}

// This is a class for the JSON object that holds all the steps of the simulation
[System.Serializable]
public class Root
{
    public StepData[] simulationData;
}

public class UpdateAgents : MonoBehaviour
{
    // These gameObjects are instantiated from the Unity Editor
    // They reference the prefabs of the car and person objects that will be instantiated
    public GameObject carPrefab;
    public GameObject personPrefab;

    // Spawn rates that will be later initialized
    float carSpawnRate;
    float personSpawnRate;

    // We need to keep track of the game objects that are already on the simulation
    Dictionary<string, GameObject> carGameObjects = new Dictionary<string, GameObject>();
    Dictionary<string, GameObject> personGameObjects = new Dictionary<string, GameObject>();
    
    // The root object for the JSON we'll read
    Root root;
    // The index of the JSON step we're reading 
    int currentStepIndex = 0;
        // The iteration count of the Update() loop
    int iterationCount = 0;
    // The maximum number of iterations to read the next step
    int ITERATIONS_BEFORE_NEXT_STEP = 75;

    // Keeping track of whether we've completed the web request or not
    bool startFinished = false;

    // We retrieve the spawn rates once we load the scene
    void OnEnable() {
        carSpawnRate = PlayerPrefs.GetFloat("carSpawnRate");
        personSpawnRate = PlayerPrefs.GetFloat("personSpawnRate");
    }

    // We need to do a web request
    IEnumerator fetch() {
        // Encoding URL parameters
        string URL = "http://127.0.0.1:5000/";
        URL += "?car_spawn_rate=" + carSpawnRate.ToString();
        URL += "&person_spawn_rate=" + personSpawnRate.ToString();

        UnityWebRequest unityWebRequest = UnityWebRequest.Get(URL);
        yield return unityWebRequest.SendWebRequest();
        if (unityWebRequest.result == UnityWebRequest.Result.ConnectionError)
        {
            UnityEngine.Debug.LogError(unityWebRequest.error);
            yield break;
        }
        // Parse JSON
        root = JsonUtility.FromJson<Root>(unityWebRequest.downloadHandler.text);
        startFinished = true;
    }

    // Start is called before the first frame update
    void Start() {
        StartCoroutine(fetch());
    }

    // Update is called once per frame
    void Update() {
        // We should not start Update() if we haven't finished Start()
        if (!startFinished) return;

        // We iterate on the cars of our current step data
        foreach (Car car in root.simulationData[currentStepIndex].cars) {
            // If that car already exists on the simulation
            if (carGameObjects.ContainsKey(car.id)) {
                // Then we retrieve it from our dictionary
                GameObject carGameObject = carGameObjects[car.id];

                // And move it to its new position
                Vector3 targetPosition = new Vector3(car.x, 0, car.y);
                float step = 10 * Time.deltaTime;
                carGameObject.transform.position = Vector3.MoveTowards(carGameObject.transform.position, targetPosition, step);
            } else {
                // If it doesn't exist, then we need to instantiate it
                GameObject carGameObject = Instantiate(carPrefab, new Vector3(car.x, 0, car.y), Quaternion.identity);
                // And save it in the dictionary
                carGameObjects.Add(car.id, carGameObject);
            }
        }

        // We iterate on the people of our current step data
        foreach (Person person in root.simulationData[currentStepIndex].people) {
            // If the person doesn't exist, then we need to instantiate it
            if (!personGameObjects.ContainsKey(person.id)) {
                // We give them an offset so they don't overlap in the scene
                float offsetX = UnityEngine.Random.Range(-0.75f, 0.75f);
                float offsetY = UnityEngine.Random.Range(-0.75f, 0.75f);
                // Instatiating them
                GameObject personGameObject = Instantiate(personPrefab, new Vector3(person.x + offsetX, 0, person.y + offsetY), Quaternion.identity);
                // Add to the dictionary
                personGameObjects.Add(person.id, personGameObject);
            }
        }

        // We need to destroy the cars which are no longer in the simulation
        List<string> carIdsToDestroy = new List<string>(); 
        // We iterate in our dictionary of existing cars
        foreach (string carId in carGameObjects.Keys) {
            bool found = false;
            
            // We check if they're also present in the current step
            foreach (Car car in root.simulationData[currentStepIndex].cars) {
                if (carId == car.id) {
                    found = true;
                }
            }

            // If they were in our dictionary, but they're no longer in the simulation
            if (!found) {
                // Then we must destroy them
                carIdsToDestroy.Add(carId);
            }
        }

        // Iterate trough the list and remove them
        foreach (string carId in carIdsToDestroy) {
            Destroy(carGameObjects[carId]);
            carGameObjects.Remove(carId);
        }

        // We need to destroy the people who are no longer in the simulation
        List<string> personIdsToDestroy = new List<string>();
        // We iterate in our dictionary of existing people
        foreach (string personId in personGameObjects.Keys) {
            bool found = false;
            
            // We check if they're also present in the current step
            foreach (Person person in root.simulationData[currentStepIndex].people) {
                if (person.id == personId) {
                    found = true;
                }
            }

            // If they were in our dictionary, but they're no longer in the simulation
            if (!found) {
                // Then we must destroy them
                personIdsToDestroy.Add(personId);
            }
        }

        // Iterate trough the list and remove them
        foreach (string personId in personIdsToDestroy) {
            Destroy(personGameObjects[personId]);
            personGameObjects.Remove(personId);
        }

        // If we've reached the determined iteration count
        if (iterationCount == ITERATIONS_BEFORE_NEXT_STEP) {
            // If we've not reached the simulation limit yet
            if (currentStepIndex < root.simulationData.Length - 1) {
                // Increase the current step
                currentStepIndex++;
            }
            // Reset iteration count
            iterationCount = 0;
        } else {
            // Add 1 to keep track of the total iterations
            iterationCount++;
        }
    }
}
