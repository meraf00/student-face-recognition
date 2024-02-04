from imutils.face_utils import FaceAligner
from imutils.face_utils import rect_to_bb
import dlib
import cv2
import pickle
import preproc

with open("models/eigenface_recognizer.pkl", "rb") as f:
    eigenface_recognizer = pickle.load(f)

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
fa = FaceAligner(predictor, desiredFaceWidth=250, desiredFaceHeight=250)

cap = cv2.VideoCapture(0)

while True:
    _, video_frame = cap.read()

    video_frame = cv2.flip(video_frame, 1)

    gray = cv2.cvtColor(video_frame, cv2.COLOR_BGR2GRAY)

    faces = detector(gray, 0)
    print(faces)

    if len(faces):
        x, y, w, h = rect_to_bb(faces[0])

        face = cv2.resize(video_frame[y : y + h, x : x + w], (250, 250))

        faceAligned = fa.align(video_frame, gray, faces[0])

        faceAligned = cv2.cvtColor(faceAligned, cv2.COLOR_BGR2GRAY)

        preprocessed_image = preproc.preprocess_images([faceAligned])

        cv2.imshow("Aligned", preprocessed_image[0].reshape((250, 250)))

        label = eigenface_recognizer.transform(preprocessed_image)

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

    k = cv2.waitKey(1)
    if k == 27:  # Check for the 'Esc' key
        break

cv2.destroyAllWindows()
cap.release()
