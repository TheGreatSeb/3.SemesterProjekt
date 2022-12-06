import io
import picamera
import logging
import socketserver
from threading import Condition
from http import server
import servo
from datetime import datetime

now = datetime.now()
dt_string = now.strftime("%H%M%S%f")

PAGE="""\
<html>
<head>
<title>Raspberry Pi cam</title>
<link rel='stylesheet' type='text/css' media='screen' href='/home/pi/Desktop/code/main.css'>
</head>
<body style="background-color:azure">
<center><h1>Raspberry Pi cam</h1></center>
<center><img src="stream.mjpg" width="640" height="480"></center>
<center><a href="/button1" style="text-decoration: none;color:black;background-color: #EA4C89;border-radius: 8px;border-style: none;box-sizing: border-box;color: #FFFFFF;cursor: pointer;display: inline-block;font-size: 14px;font-weight: 500;height: 40px;line-height: 20px;list-style: none;margin: auto; outline: black;padding: 10px 16px;position: relative;text-align: center;text-decoration: none;transition: color 100ms;vertical-align: baseline;user-select: none;-webkit-user-select: none;touch-action: manipulation;">Capture</a></center>
</body>
</html>
"""

class StreamingOutput(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # New frame, copy the existing buffer's content and notify all
            # clients it's available
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf)

class StreamingHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            buttonPress = 0
            print(buttonPress)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/button1.html':
            buttonPress = 1
            print(buttonPress)
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            content = PAGE.encode('utf-8')
            self.send_response(200)
            buttonPress = 0
            print(buttonPress)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/stream.mjpg':
            self.send_response(200)
            buttonPress = 1
            print(buttonPress)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                n = 0
                while n < 100000:
                    if buttonPress == 1:
                        print("test")
                        buttonPress = 0
                        n += 1
                        print(f"Button was pushed, taking picture: img:{n}")
                        servo.center()
                        now = datetime.now()
                        dt_string = now.strftime("%H%M%S%f")
                        camera.capture(f"/home/pi/Desktop/pics/img{dt_string}.jpg", use_video_port=False)
                        print(f"Capturing: img{dt_string}.jpg")
                        servo.right()
                        now = datetime.now()
                        dt_string = now.strftime("%H%M%S%f")
                        camera.capture(f"/home/pi/Desktop/pics/img{dt_string}.jpg", use_video_port=False)
                        print(f"Capturing: img{dt_string}.jpg")
                        servo.left()
                        now = datetime.now()
                        dt_string = now.strftime("%H%M%S%f")
                        camera.capture(f"/home/pi/Desktop/pics/img{dt_string}.jpg", use_video_port=False)
                        print(f"Capturing: img{dt_string}.jpg")
                        servo.up()
                        now = datetime.now()
                        dt_string = now.strftime("%H%M%S%f")
                        camera.capture(f"/home/pi/Desktop/pics/img{dt_string}.jpg", use_video_port=False)
                        print(f"Capturing: img{dt_string}.jpg")
                        servo.down()
                        now = datetime.now()
                        dt_string = now.strftime("%H%M%S%f")
                        camera.capture(f"/home/pi/Desktop/pics/img{dt_string}.jpg", use_video_port=False)
                        print(f"Capturing: img{dt_string}.jpg")
                        servo.center()

                    with output.condition:
                        output.condition.wait()
                        frame = output.frame
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
        else:
            self.send_error(404)
            self.end_headers()

class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True

with picamera.PiCamera(resolution='640x480', framerate=24) as camera:
    output = StreamingOutput()
    #Uncomment the next line to change your Pi's Camera rotation (in degrees)
    #camera.rotation = 90
    camera.start_recording(output, format='mjpeg')
    try:
        address = ('', 8000)
        server = StreamingServer(address, StreamingHandler)
        server.serve_forever()
    finally:
        camera.stop_recording()