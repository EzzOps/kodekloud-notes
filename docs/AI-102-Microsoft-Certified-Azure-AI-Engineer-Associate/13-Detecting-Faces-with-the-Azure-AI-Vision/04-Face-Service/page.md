# Ref: https://learn.microsoft.com/en-us/python/api/overview/azure/ai-vision-face-readme?view=azure-python-preview
from azure.cognitiveservices.vision.face import FaceClient
from azure.cognitiveservices.vision.face.models import FaceAttributeType
from msrest.authentication import CognitiveServicesCredentials
import json

# Replace with your correct endpoint and key
ENDPOINT = "https://<your-resource-name>.cognitiveservices.azure.com/"
KEY = "<your_key_here>"

# Public image URL (single person)
image_url = "https://azai102imagestore.blob.core.windows.net/images/happy.jpg"

face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))

# Define the face attributes you want to extract
face_attributes = [FaceAttributeType.head_pose]

# Detect faces and attributes
detected_faces = face_client.face.detect_with_url(
    url=image_url,
    return_face_id=False,
    return_face_landmarks=True,
    return_face_attributes=face_attributes
)

print(f"Detected {len(detected_faces)} face(s) in the image.\n")

if not detected_faces:
    print("No face detected.")
else:
    for i, face in enumerate(detected_faces, start=1):
        print(f"Face #{i}")
        # face.face_id may be None when return_face_id=False
        print(f"Face ID: {getattr(face, 'face_id', None)}")
        # Some attributes like glasses or headPose are available when requested
        if face.face_attributes:
            print(f"Head pose: {face.face_attributes.head_pose}")
        # Landmarks (example)
        if face.face_landmarks:
            pl = face.face_landmarks.pupil_left
            nt = face.face_landmarks.nose_tip
            ml = face.face_landmarks.mouth_left
            mr = face.face_landmarks.mouth_right
            print("Landmarks:")
            print(f" - Pupil Left: {pl.x}, {pl.y}")
            print(f" - Nose Tip: {nt.x}, {nt.y}")
            print(f" - Mouth Left: {ml.x}, {ml.y}")
            print(f" - Mouth Right: {mr.x}, {mr.y}")

# Optionally, print the full JSON response for inspection
# NOTE: the SDK objects can be serialized; here we convert to dict via repr/json where useful
print("\nFull JSON-like response for all faces:")
print(json.dumps([face.as_dict() for face in detected_faces], indent=2))
```

Typical cleaned console output (example):

```text theme={null}
Detected 1 face(s) in the image.

Face #1
Face ID: None
Head pose: {'roll': 1.0, 'yaw': 24.3, 'pitch': -4.5}
Landmarks:
 - Pupil Left: 253.9, 145.6
 - Nose Tip: 295.6, 202.2
 - Mouth Left: 258.9, 231.1
 - Mouth Right: 337.8, 230.2

Full JSON-like response for all faces:
[
  {
    "faceRectangle": {
      "width": 189,
      "height": 189,
      "left": 203,
      "top": 95
    },
    "faceLandmarks": {
      "pupilLeft": { "x": 253.9, "y": 145.6 },
      "pupilRight": { "x": 340.6, "y": 145.9 },
      "noseTip": { "x": 295.6, "y": 202.2 },
      ...
    },
    "faceAttributes": {
      "headPose": { "roll": 1.0, "yaw": 24.3, "pitch": -4.5 }
    }
  }
]
```

Group image (multiple faces)

To analyze group images, provide a group image URL. The API response will return one object per detected face in the array.

```python theme={null}
# Public group image URL (multiple people)
image_url = "https://azai102imagestore.blob.core.windows.net/images/group.jpg"

detected_faces = face_client.face.detect_with_url(
    url=image_url,
    return_face_id=False,
    return_face_landmarks=True,
    return_face_attributes=face_attributes
)

print(f"Detected {len(detected_faces)} face(s) in the group image.\n")

for i, face in enumerate(detected_faces, start=1):
    print(f"Face #{i}")
    if face.face_landmarks:
        pl = face.face_landmarks.pupil_left
        nt = face.face_landmarks.nose_tip
        print(f" - Pupil Left: {pl.x}, {pl.y}")
        print(f" - Nose Tip: {nt.x}, {nt.y}")
    print()
```

Tips, notes, and troubleshooting

<Callout icon="lightbulb">
  * If you request face IDs or certain attributes and your subscription lacks approval, the service may return an error—disable those parameters or request access via Azure support.
  * Use returnRecognitionModel for traceability when running experiments across SDK versions.
  * Verify pricing tier and quotas (especially in production) to avoid throttling.
</Callout>

* For persistent matching across images, you need faceId functionality and the appropriate approval.
* If you get permissions errors for sensitive attributes, file an Azure support request to request feature access.
* When debugging, log the recognitionModel and detectionModel returned so you can reproduce results later.

Resources and references

| Resource                                | Description                                                                                                                                                                                                                |
| --------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Face API docs                           | [https://learn.microsoft.com/azure/cognitive-services/face/](https://learn.microsoft.com/azure/cognitive-services/face/)                                                                                                   |
| Azure Cognitive Services Python samples | [https://learn.microsoft.com/en-us/python/api/overview/azure/ai-vision-face-readme?view=azure-python-preview](https://learn.microsoft.com/en-us/python/api/overview/azure/ai-vision-face-readme?view=azure-python-preview) |
| Azure Portal                            | [https://portal.azure.com/](https://portal.azure.com/)                                                                                                                                                                     |

With these steps and examples you can detect faces, extract landmarks, and request face attributes where allowed. Explore the broader Azure Vision documentation for additional capabilities like OCR, object detection, and custom vision scenarios.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/ai-102-microsoft-certified-azure-ai-engineer-associate/module/8d81e205-9362-4870-8c36-5d6b65c3051d/lesson/80654118-eddb-45cc-bf8b-3585edce1309" />
</CardGroup>


# Face Service

Source: https://notes.kodekloud.com/docs/AI-102-Microsoft-Certified-Azure-AI-Engineer-Associate/Detecting-Faces-with-the-Azure-AI-Vision/Face-Service/page

Overview of Azure Face Service features for detecting, analyzing, and recognizing faces including attributes, landmarks, verification, persisted recognition, liveness detection, and privacy and compliance guidance.

The Azure Face Service provides a suite of computer-vision capabilities for extracting meaningful face-related insights from images while helping you meet privacy and compliance obligations. This service supports:

* Face detection (locating faces and returning bounding boxes)
* Face attribute analysis (age, head pose, glasses, blur, occlusion, exposure, etc.)
* Facial landmark detection (precise key points on a face)
* Face comparison and verification
* Persisted face recognition (person groups and enrolled faces)
* Liveness detection (anti-spoofing)

Below we explain each capability, how detected faces are represented, and the concepts you need to train and use persisted recognition models.

## Key capabilities at a glance

| Capability                     | What it does                                                                                                 | Example usage                                                      |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------ |
| Face detection                 | Locates faces in an image and returns bounding boxes (coordinates and sizes)                                 | Draw boxes around faces in a photo gallery                         |
| Face attribute analysis        | Returns attributes such as estimated age, head pose (pitch/yaw/roll), glasses, blur, occlusion, and exposure | Filter photos by blur or detect glasses for accessibility features |
| Facial landmark detection      | Identifies key facial points (eyes, nose tip, mouth corners, chin, etc.)                                     | Align faces for AR filters or facial normalization                 |
| Face comparison / verification | Computes similarity or confidence that two faces are the same person                                         | Match a selfie to an ID photo for verification                     |
| Persisted face recognition     | Recognizes enrolled individuals by comparing faces against person groups                                     | Attendance systems or authorized-access solutions                  |
| Liveness detection             | Detects presentation attacks to ensure a live person is present                                              | Prevent photo/video spoofing during authentication                 |

## Face detection and attribute analysis

Face detection automatically locates faces in images and returns bounding boxes for each face so you can highlight or crop faces in UI. Attribute analysis extracts additional metadata such as approximate age, head pose (pitch/yaw/roll), whether the subject is wearing glasses, blur level, occlusion (e.g., masks), and exposure. These attributes help you determine face quality and suitability for downstream tasks (recognition, verification, or enrollment).

## Facial landmark detection

Facial landmark detection returns precise keypoints (for example, eye centers, nose tip, mouth corners, chin) useful for:

* AR filters and face overlays
* Face normalization and alignment before recognition
* Digital makeup or facial animation pipelines

<Frame>
  <img alt="A dark-themed infographic titled &#x22;The Face Service&#x22; that outlines three functions—face detection, face attribute analysis, and facial landmark detection—alongside cartoon face icons and a list of attributes (head pose, glasses, blur, exposure, etc.). A sample photo, a cloud/AI icon and arrows visually show how the service extracts landmarks and attributes from an image." />
</Frame>

## Face comparison and verification

Face comparison (verification) computes the likelihood that two faces belong to the same person. This is often used for one-to-one checks (e.g., selfie vs. ID). Because verification and identification can reveal sensitive personal data, enabling these features typically requires special approval from Microsoft.

<Callout icon="warning">
  Face-related operations that identify or verify individuals are sensitive and typically require you to request access/approval from Microsoft. Ensure you understand the privacy, legal, and compliance implications before enabling these features.
</Callout>

## Facial recognition and identification

Persisted or “enrolled” recognition compares a detected face against a stored set of persons (person groups). Use cases include attendance, authorized access, and customer verification workflows where faces are matched to labeled identities that you have legally and ethically enrolled.

## Liveness detection

Liveness checks determine whether the presented face is from a live subject (not a printed photo or replayed video). This reduces the risk of spoofing during authentication or verification flows.

## How detected faces are represented

When a face is detected, the Face Service returns a temporary face identifier (faceId). Key points about detected faceIds:

* faceId is ephemeral and available for a limited window (typically up to 24 hours).
* It enables follow-up operations (verification, find-similar, identification) within that timeframe.
* faceId is not tied to a person label unless you persist the face into a person group.

<Frame>
  <img alt="A diagram titled &#x22;Detected Face Identification&#x22; showing three cartoon avatars each linked to an anonymous identifier (e.g., abcd-12345, zyxw-09876, dcba-54321). A highlighted note at the bottom states that Face IDs are stored in the service for up to 24 hours." />
</Frame>

## Operations built on detected-face identification

* Face verification: Compare two detected faceIds to confirm whether they are likely the same person.
* Find similar: Search a collection of detected or persisted faces for faces visually similar to a target face.
* Persisted recognition (identification): Compare a detected face against a trained person group to return one or more candidate matches.

## Persisted face recognition concepts

* Person group / large person group: A container for the people your application will recognize (for example, employees or students).
* Person: An entity within a person group with a human-readable label (for example, "Jan").
* Persisted face: One or more stored face images associated with a Person. Persisted faces are used to train the recognition model.

A typical enrollment workflow stores multiple images per person to capture variation (different angles, expressions, lighting). The service uses those persisted images to build a more robust recognition model—similar to how consumer face enrollment asks for multiple poses.

<Frame>
  <img alt="A diagram titled &#x22;Persisted Face Recognition&#x22; showing how person groups, persons, and persisted face images are stored to train a facial recognition model. Inside an &#x22;Authorized Users&#x22; box are two users (Jan and Jo), each represented by three face icons." />
</Frame>

## Training a persisted-face recognition model

Follow these high-level steps to train a model that recognizes enrolled individuals:

1. Create a person group to contain all people you want to recognize.
2. Register each person in the group (create a Person object with a label).
3. Upload multiple face images for each person (persisted faces) to capture pose, expression, lighting, and occlusion variation.
4. Train the person group—the service processes the persisted faces and builds a recognition model.

After training completes, you can identify or verify people in new images against the trained person group.

<Frame>
  <img alt="An infographic titled &#x22;Persisted Face Recognition: Steps to Train the Model.&#x22; It shows four numbered steps—define a person group, register individuals, store multiple face images, and train the model—each with a short description and icon." />
</Frame>

## Common persisted-face recognition use cases

* Attendance and presence tracking in classrooms or workplaces
* Selfie-to-ID verification for account access or onboarding
* Finding visually similar faces in a database for investigative support or tag suggestions

## Best practices and privacy considerations

* Collect and store persisted faces only when you have a lawful basis and explicit user consent. Comply with local regulations (GDPR, CCPA, or other applicable laws).
* Minimize retention of persisted faces and implement secure access controls and encryption for stored data.
* Remember detected faceIds are temporary (typically up to 24 hours). Use person groups for long-term recognition and prune them according to your data-retention policies.
* Request Microsoft approval (gated access) before enabling identification/verification features where required.

<Callout icon="lightbulb">
  Detected face IDs are temporary (typically up to 24 hours). Persisted faces stored in person groups are the mechanism for long-term recognition — manage them carefully and prune as required by policy.
</Callout>

## Next steps and references

You can call these capabilities via the Azure Face or Azure AI Vision APIs and integrate them into your applications. Start with the official documentation and API reference:

* [Azure Face Service overview](https://learn.microsoft.com/azure/cognitive-services/face/overview)
* [Azure AI Vision documentation](https://learn.microsoft.com/azure/ai-services/vision)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/ai-102-microsoft-certified-azure-ai-engineer-associate/module/8d81e205-9362-4870-8c36-5d6b65c3051d/lesson/342b63d2-5367-4be1-85d5-5bb4eb399e3d" />
</CardGroup>
