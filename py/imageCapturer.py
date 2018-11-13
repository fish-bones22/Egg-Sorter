from picamera import PiCamera
from time import sleep
import datetime

class ImageCapturer:

	_camera = ""

	def __init__(self):
		self._camera = PiCamera()

	def takeImage(self):
		timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
		self._camera.resolution = (1024, 768)
		self._camera.start_preview()
		self._camera.capture(timestamp+".jpg")
		self._camera.stop_preview()
