import cv2
import pickle
import numpy as np
from img_preprocessing import preprocess_images


with open("models/eigenface_recognizer.pkl", "rb") as f:
    eigenface_recognizer = pickle.load(f)
    print(dir(eigenface_recognizer))


face_classifier = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

video_capture = cv2.VideoCapture(0)


def detect_bounding_box(vid):
    gray_image = cv2.cvtColor(vid, cv2.COLOR_BGR2GRAY)

    faces = face_classifier.detectMultiScale(
        gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(40, 40)
    )

    for x, y, w, h in faces:
        cv2.rectangle(vid, (x, y), (x + w, y + h), (0, 255, 0), 4)

    return faces


while True:
    result, video_frame = video_capture.read()

    if result is False:
        break

    video_frame = cv2.flip(video_frame, 1)

    faces = detect_bounding_box(video_frame)

    if len(faces):
        x, y, w, h = faces[0]

        face = video_frame[y : y + h, x : x + w]
        face = cv2.resize(face, (250, 250))
        face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)

        preprocessed_image = preprocess_images([face])
        cv2.imshow("Face", preprocessed_image[0].reshape((250, 250)))

        label = eigenface_recognizer.predict(preprocessed_image)

        cv2.putText(
            video_frame,
            "Name: " + str(label[0]),
            (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2,
        )

    cv2.imshow("Face Detection Project", video_frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

video_capture.release()
cv2.destroyAllWindows()
