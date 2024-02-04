from flask import Flask, request, jsonify
from PIL import Image
from io import BytesIO
import cv2
import numpy as np
import pickle

from img_preprocessing import preprocess_images

app = Flask(__name__)

with open("models/eigenface_recognizer.pkl", "rb") as f:
    eigenface_recognizer = pickle.load(f)


face_classifier = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)


def detect_bounding_box(vid):
    gray_image = cv2.cvtColor(vid, cv2.COLOR_BGR2GRAY)

    faces = face_classifier.detectMultiScale(
        gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(40, 40)
    )

    for x, y, w, h in faces:
        cv2.rectangle(vid, (x, y), (x + w, y + h), (0, 255, 0), 4)

    return faces


@app.route("/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        return jsonify({"error": "No file part"})

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No selected file"})

    if file:
        try:

            image_stream = BytesIO(file.read())

            image = Image.open(image_stream)

            opencv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

            faces = detect_bounding_box(opencv_image)

            if len(faces):
                x, y, w, h = faces[0]

                face = opencv_image[y : y + h, x : x + w]
                face = cv2.resize(face, (250, 250))
                face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)

                preprocessed_image = preprocess_images([face])
                cv2.imshow("Face", preprocessed_image[0].reshape((250, 250)))

                label = eigenface_recognizer.predict(preprocessed_image)

                return jsonify({"result": str(label[0])})

            return jsonify({"result": "No face detected"})

        except Exception as e:
            return jsonify({"error": str(e)})

    return jsonify({"error": "No selected file"})


if __name__ == "__main__":
    # Run the Flask app
    app.run(debug=True, host="0.0.0.0")
