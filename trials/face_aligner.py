from imutils.face_utils import FaceAligner
from imutils.face_utils import rect_to_bb
import imutils
import dlib
import cv2

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
fa = FaceAligner(predictor, desiredFaceWidth=256)

cap = cv2.VideoCapture(0)

while True:
    _, image = cap.read()

    image = cv2.flip(image, 1)
    image = imutils.resize(image, width=250)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    cv2.imshow("Input", image)

    rects = detector(gray, 2)

    for rect in rects:
        (x, y, w, h) = rect_to_bb(rect)
        faceOrig = imutils.resize(image[y : y + h, x : x + w], width=250)
        faceAligned = fa.align(image, gray, rect)
        # display the output images
        cv2.imshow("Original", faceOrig)
        cv2.imshow("Aligned", faceAligned)

    k = cv2.waitKey(1)
    if k == 27:  # Check for the 'Esc' key
        break

cv2.destroyAllWindows()
cap.release()
