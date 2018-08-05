# py-facedetection-stream

A framework written in Python3 to fetch a server-side video input, detect the position of a face and stream it via a webserver written with Flask.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

1. You need to have Python3 installed in order to to let the audio stream work propably.
2. Make sure to install the required 3rd party modules. In our case we need:

```
numpy
OpenCV (cv2)*
pyaudio
flask
```
* since the cv2-module is under some circumstances quite a struggle, feel free to send me a message, in case you need some help with the setup.
3. Launch the [server.py](server.py)

```
python3 server.py
```

### Check the result

The webserver will be launched under the socket [http://0.0.0.0:5000/](http://0.0.0.0:5000/).
By default the server will stream gray frames with the guidelines of the detected faces + COI as well as a static threshold rectangle.
![Alt text](/github/screenshot.png?raw=true "Screenshow of Website")

I use the threshold rectangle to only make a camera gimbal moving when the COI is out of those boundaries.
Note, that the Python script will output relative correction angles once the threshold is exceeded.

## Things to adjust

If you want to use the framework for some realworld projects, I highly recommend tweaking a few things.
In case you want to use some servomotors or a dedicated gimbal to make a sort of facefollowing system then you first have to lookup or calculate the correct FOV of your webcam. The angles (seperated in horzontaly and verticaly) could be easily changed in the [facedetection.py](facedetection.py) file. Change the following lines:
```
camHFOV = 66.0
camVFOV = 26.0
```

Furthermore you might want to adjust the threshold range. Therefore you only have to make a slight change in the [server.py](server.py) file.
```
# Parameters: video, sensX-treshold(0.0-1.0), sensY-treshold(0.0-1.0)
# 0.0 = agressive movement, 1.0 = not movement
frame_face_detected = facedetection.fnc(frame, 0.3, 0.25)
```
The second and third parameter of the `facedetection.fnc` are the percentage of captured frame width/height. Choosing the value `1.0` (100%) will basicly disable the moving of the camera, while a value of `0.0` will make the camera very sensitive the every movement on the frame.

Finaly, using the facedetection and camera moving capabilities while returning the original but still processed image to via the Flask webserver you just have to just have to change the following line in the [server.py](server.py) file from `frame_face_detected` to `frame`:
```
cv2.imwrite('signals/currFrame.jpg', frame_face_detected)
```

## Note

Keep in mind that the project is more in a proof of concept state then a performant one.
