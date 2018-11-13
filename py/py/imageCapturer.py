from picamera import PiCamera
from time import sleep
import datetime

class ImageCapturer:

	_camera = ""
	x = 0
	y = 0
	h = 1
	w = 1

	def __init__(self):
		self._camera = PiCamera()


	def setZoom(self, zoom):

		if zoom is None:
			return

		if not isinstance(zoom, list):
			return

		self.x = zoom[0]
		self.y = zoom[1]
		self.h = zoom[2]
		self.w = zoom[3]


	def takeImage(self):

		timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

		try:
			self._camera.resolution = (1024, 1024)
			self._camera.zoom = (self.x, self.y, self.w, self.h)
			self._camera.start_preview()
			self._camera.capture(timestamp+".jpg")
			sleep(0.2)
			self._camera.stop_preview()
		except:
			print("Error taking picture.")
			return False

		return timestamp+".jpg"

	
	def close(self):
		self._camera.close()
