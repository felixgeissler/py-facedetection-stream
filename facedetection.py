import sys
sys.path.insert(0, "/usr/local/lib/python3.7/site-packages/")
import cv2

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
# eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')


def fnc(frame, sensX, sensY):

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    # Detection rectangle
    [r, c, d] = frame.shape
    sensX = int(sensX * c)
    sensY = int(sensY * r)
    cv2.rectangle(gray, (int(c/2 - sensX/2), int(r/2 - sensY/2)), (int(c/2 + sensX/2), int(r/2 + sensY/2)), 255, 2)

    # fineSensX = int(sensX * 0.6)
    # fineSensY = int(sensX * 0.6)
    # cv2.rectangle(gray, (c/2 - fineSensX/2, r/2 - fineSensY/2), (c/2 + fineSensX/2, r/2 + fineSensY/2), 200, 2)

    for (x, y, w, h) in faces:

       zv = 150.0/w
       xv =(x-320+w/2)/937.5*zv
       yv = (240-y-h/2)/937.5*zv
       ### print("Virtual World Coordinates of center of faces: ", xv, yv, -zv)

       # Face rectangle
       cv2.rectangle(gray, (x, y), (x+w, y+h), 255, 2)

       # Center
       faceCenter = [int(x+int(w/2)), int(y+int(h/2))]
       cv2.circle(gray, (faceCenter[0], faceCenter[1]), 4, 255, 2)
       ### print("Rought estimation of face angle: ", getCameraAngle(faceCenter[0], faceCenter[1], c, r))

       # Handle camera movement
       handleCamMovement(faceCenter[0], faceCenter[1], sensX, sensY, c, r)

    return gray


def handleCamMovement(poiX, poiY, thresX, thresY, frameW, frameH):
    thresLeft = frameW/2 - thresX/2
    thresRight = frameW/2 + thresX/2
    thresTop = frameH/2 - thresY/2
    thresBottom = frameH/2 + thresY/2

    if (poiX < thresLeft):
        print("Moving Camera %f degrees to left." % getCameraAngle(poiX, poiY, frameW, frameH)[0])
    elif (poiX > thresRight):
        print("Moving Camera %f degrees to right." % getCameraAngle(poiX, poiY, frameW, frameH)[0])

    if (poiY < thresTop):
        print("Moving Camera %f degrees upwards." % getCameraAngle(poiX, poiY, frameW, frameH)[1])
    elif (poiY > thresBottom):
        print("Moving Camera %f degrees downwards." % getCameraAngle(poiX, poiY, frameW, frameH)[1])


def getCameraAngle(poiX, poiY, frameW, frameH):
    # estimated Macbook Pro camera FOV
    camHFOV = 66.0
    camVFOV = 26.0

    diffH = (frameW/2) - poiX
    diffV = (frameH/2) - poiY

    angleH = (diffH*(camHFOV/2))/frameW
    angleV = (diffV*(camVFOV/2))/frameH

    return angleH, angleV
