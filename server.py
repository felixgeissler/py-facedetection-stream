#!/usr/bin/env python
from flask import Flask, render_template, Response
import sys
sys.path.insert(0, "/usr/local/lib/python3.7/site-packages/")
import cv2
import facedetection
import pyaudio
import numpy as np

FORMAT = pyaudio.paInt16
CHUNK = 1024
sampleRate = 44100
bitsPerSample = 16
channels = 1
#samples = 200000000

app = Flask(__name__)


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


# Stream routing
@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(generateVideo(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route("/audio_feed")
def audio_feed():
    """Audio streaming route. Put this in the src attribute of an audio tag."""
    return Response(generateAudio(),
                    mimetype="audio/x-wav")


# Stream generating
def generateVideo():
    """Video streaming generator function."""
    cap = cv2.VideoCapture(0)
    while (cap.isOpened()):
        ret, frame = cap.read()

        # Parameters: video, sensX-treshold(0.0-1.0), sensY-treshold(0.0-1.0)
        # 0.0 = agressive movement, 1.0 = not movement
        frame_face_detected = facedetection.fnc(frame, 0.3, 0.25)

        cv2.imwrite('signals/currFrame.jpg', frame_face_detected)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + open('signals/currFrame.jpg', 'rb').read() + b'\r\n')


@app.route('/audiofeed')
def audiofeed():
    def gen_audio():

        audio = pyaudio.PyAudio()
        stream = audio.open(format=FORMAT, channels=channels,
                rate=sampleRate, input=True,
                frames_per_buffer=CHUNK)
        wav_header = genHeader(sampleRate, bitsPerSample, channels)

        data = stream.read(CHUNK)
        chunck = wav_header + data
        while True:
            yield (chunck)
            data = stream.read(CHUNK)
            chunck = data

    return Response(gen_audio(),
                    mimetype="audio/x-wav")

def genHeader(sampleRate, bitsPerSample, channels):
    datasize = 2000*10**6
    o = bytes("RIFF", 'ascii')                                               # (4byte) Marks file as RIFF
    o += (datasize + 36).to_bytes(4, 'little')                               # (4byte) File size in bytes excluding this and RIFF marker
    o += bytes("WAVE", 'ascii')                                              # (4byte) File type
    o += bytes("fmt ", 'ascii')                                              # (4byte) Format Chunk Marker
    o += (16).to_bytes(4, 'little')                                          # (4byte) Length of above format data
    o += (1).to_bytes(2, 'little')                                           # (2byte) Format type (1 - PCM)
    o += (channels).to_bytes(2, 'little')                                    # (2byte)
    o += (sampleRate).to_bytes(4, 'little')                                  # (4byte)
    o += (sampleRate * channels * bitsPerSample // 8).to_bytes(4, 'little')  # (4byte)
    o += (channels * bitsPerSample // 8).to_bytes(2, 'little')               # (2byte)
    o += (bitsPerSample).to_bytes(2, 'little')                               # (2byte)
    o += bytes("data", 'ascii')                                              # (4byte) Data Chunk Marker
    o += (datasize).to_bytes(4,'little')                                    # (4byte) Data size in bytes
    return o


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True)
