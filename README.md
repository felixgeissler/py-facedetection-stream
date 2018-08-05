# py-facedetection-stream

A framework written in Python3 to process a server-side video stream, detect face position and stream it via a webserver written with Flask

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
3. Launch the server.py

```
python3 server.py
```

### Check the result

The webserver will be launched under the socket [http://0.0.0.0:5000/](http://0.0.0.0:5000/).
By default the server will stream gray frames with the guidelines of the detected faces + COI as well as a static threshold rectangle.
I use the threshold rectangle to only make a camera gimbal moving when the COI is out of those boundaries.
Note, that the Python script will output relative correction angles once the threshold is exceeded.

## Adjusting the framework

t.b.a