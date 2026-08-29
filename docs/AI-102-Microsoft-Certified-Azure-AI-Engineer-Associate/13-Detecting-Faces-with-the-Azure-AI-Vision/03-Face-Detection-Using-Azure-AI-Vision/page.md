# Face Detection Using Azure AI Vision

Source: https://notes.kodekloud.com/docs/AI-102-Microsoft-Certified-Azure-AI-Engineer-Associate/Detecting-Faces-with-the-Azure-AI-Vision/Face-Detection-Using-Azure-AI-Vision/page

Guide to using Azure AI Vision Face API to detect faces, return bounding boxes, landmarks, and optional attributes, with SDK examples, parameters, and deployment steps.

Face detection with Azure AI Vision (Face API) lets you detect and analyze faces in images. The API locates faces, returns bounding boxes and landmarks (eye centers, nose tip, lip corners), and can optionally return attributes such as head pose, glasses, and more. Note that certain capabilities—like identity matching and some sensitive attributes (age, gender, emotion)—require explicit approval for your Azure subscription.

<Callout icon="warning">
  Some attributes (for example: age, gender, emotions, and identity matching/Face ID) require extra approval from Microsoft before they can be used. You can still retrieve landmarks and basic location data without that approval.
</Callout>

<Frame>
  <img alt="A presentation slide titled &#x22;Face Detection Using Azure AI Vision&#x22; explaining the Face API's ability to detect and analyze faces. It includes a smartphone illustration showing a detected face and two numbered notes about using the Face endpoint and possible extra approval for recognition/identification features." />
</Frame>

What the Face API can return

* Bounding boxes for each detected face.
* Detailed facial landmarks (eyes, nose, mouth, pupils, etc.).
* Optional face attributes (head pose, glasses, and other attributes where allowed).
* Optional unique face identifiers for cross-image matching (subject to approval).

Optional request parameters (quick overview)

| Parameter            | Purpose                                                          | Notes                                                         |
| -------------------- | ---------------------------------------------------------------- | ------------------------------------------------------------- |
| returnFaceId         | Return a unique faceId for each detected face                    | Enables cross-image matching; may require additional approval |
| returnFaceLandmarks  | Return detailed facial keypoints (pupils, nose tip, lip corners) | Useful for overlaying or measuring facial geometry            |
| returnFaceAttributes | Request attributes such as age, emotion, headPose, glasses, etc. | Some attributes require Microsoft approval                    |

<Frame>
  <img alt="A presentation slide titled &#x22;Face Detection Using Azure AI Vision&#x22; that lists three optional request parameters — returnFaceId, returnFaceLandmarks, and returnFaceAttributes — each with a brief description. The slide has a dark teal background with rounded rectangular bullets and a small KodeKloud copyright." />
</Frame>

Additional optional parameters

| Parameter              | Purpose                                                                   | When to use                                                             |
| ---------------------- | ------------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| recognitionModel       | Specify which recognition model version to use                            | Use when identity matching is allowed and multiple models are available |
| returnRecognitionModel | Return the recognition model version used in the response                 | Helpful for auditing and reproducibility                                |
| detectionModel         | Choose the face detection model to control scanning/localization behavior | Useful to balance performance vs. accuracy                              |

<Frame>
  <img alt="A slide titled &#x22;Face Detection Using Azure AI Vision&#x22; listing three optional request parameters—recognitionModel, returnRecognitionModel, and detectionModel—with short descriptions for each." />
</Frame>

API response structure

When faces are detected, the Face API returns a JSON array where each element corresponds to one detected face. Key fields include:

| Field            | Type   | Description                                                             |
| ---------------- | ------ | ----------------------------------------------------------------------- |
| faceId           | string | Unique ID for the detected face (if requested and permitted)            |
| recognitionModel | string | Recognition model name/version used for processing                      |
| faceRectangle    | object | Bounding box with left, top, width, height                              |
| faceLandmarks    | object | Coordinates for facial keypoints (pupilLeft, noseTip, mouthLeft, etc.)  |
| faceAttributes   | object | Requested attributes such as headPose, glasses, emotions (if available) |

<Frame>
  <img alt="A dark-themed presentation slide titled &#x22;Face Detection Using Azure AI Vision&#x22; showing an &#x22;API Response&#x22; button and three icons labeled &#x22;FaceId,&#x22; &#x22;Bounding box coordinates,&#x22; and &#x22;Landmarks&#x22; that illustrate the structured JSON output." />
</Frame>

Example: simplified REST detect request and a trimmed JSON response

```http theme={null}
Request: https://{endpoint}/face/v1.0/detect[?returnFaceId=true|false&returnFaceLandmarks=true|false&returnFaceAttributes=...]
Body: {"url": "http://path-to-image"}

Response:
[
  {
    "faceId": "c5c24a82-6845-4031-9d5d-978df9175426",
    "recognitionModel": "recognition_03",
    "faceRectangle": {
      "width": 78,
      "height": 78,
      "left": 394,
      "top": 54
    },
    "faceLandmarks": {
      "pupilLeft": { "x": 412.7, "y": 78.4 },
      "pupilRight": { "x": 446.8, "y": 74.2 }
    },
    "faceAttributes": {
      "headPose": { "roll": 0.5, "yaw": 10.0, "pitch": -2.1 }
    }
  }
]
```

Create and configure the Face resource in Azure Portal

1. In the Azure Portal, create an Azure AI (Face) resource. Provide subscription, resource group, region, name, and pricing tier. Note: the free tier is limited to one per subscription and may not always be available.
2. After creation, open the resource and copy the service endpoint and subscription keys from the "Keys and Endpoint" blade. You'll use these values in SDKs and REST calls.

<Frame>
  <img alt="A screenshot of the Microsoft Azure portal showing the &#x22;Create Face&#x22; resource form with fields for subscription, resource group, region, instance name, and pricing tier. The page includes navigation tabs and a pricing dropdown open near the bottom." />
</Frame>

<Frame>
  <img alt="A screenshot of the Microsoft Azure portal showing the &#x22;ai900-face-recog | Keys and Endpoint&#x22; page for the Face API, with masked keys, Location/Region set to &#x22;eastus,&#x22; and the service endpoint URL displayed. The Azure left-hand navigation menu and top browser tabs are also visible." />
</Frame>

Python examples (Azure Face SDK)

Below are concise Python examples using the Azure Cognitive Services Face SDK. Replace the endpoint and key placeholders with values from your Azure resource.

Single-image example (detect faces and landmarks, without returning Face ID)

```python theme={null}
