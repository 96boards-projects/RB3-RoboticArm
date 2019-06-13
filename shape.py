import cv2
import imutils
from imutils.video import VideoStream
from collections import deque
import numpy as np
import json
from pymemcache.client import base

client = base.Client(('localhost', 11211))

class ShapeDetector:
	def __init__(self):
		pass
 
	def detect(self, c):
		# initialize the shape name and approximate the contour
		shape = "unidentified"
		peri = cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, 0.04 * peri, True)
		# if the shape is a triangle, it will have 3 vertices
		if len(approx) == 3:
			shape = "triangle"
 
		# if the shape has 4 vertices, it is either a square or
		# a rectangle
		elif len(approx) == 4:
			# compute the bounding box of the contour and use the
			# bounding box to compute the aspect ratio
			#(x, y, w, h) = cv2.boundingRect(approx)
			#ar = float(w / h)
 
			# a square will have an aspect ratio that is approximately
			# equal to one, otherwise, the shape is a rectangle
			# shape = "square" if ar >= 0.9 and ar <= 1.1 else "rectangle"
			shape = "rectangle"

		# if the shape is a pentagon, it will have 5 vertices
		elif len(approx) == 5:
			shape = "pentagon"
 
		# otherwise, we assume the shape is a circle
		else:
			shape = "circle"
 
		# return the name of the shape
		return shape


# WebCam Streaming using imutils
vs = VideoStream(src=0).start()

greenLower = (10, 140, 100)
greenUpper = (30, 255, 255)

redLower = (0, 80, 80)
redUpper = (10, 255, 190)

blueLower = (100, 60, 40)
blueUpper = (120, 255, 200)

pts=deque(maxlen=64)

def detects(frame, lower, upper):
		# resize the frame, blur it, and convert it to the HSV
		# color space
		blurred = cv2.GaussianBlur(frame, (11, 11), 0)
		hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

		# construct a mask for the color "green", then perform
		# a series of dilations and erosions to remove any small
		# blobs left in the mask
		mask = cv2.inRange(hsv, lower, upper)
		mask = cv2.erode(mask, None, iterations=2)
		mask = cv2.dilate(mask, None, iterations=2)

		# find contours in the mask and initialize the current
		# (x, y) center of the ball
		cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
			cv2.CHAIN_APPROX_SIMPLE)
		cnts = imutils.grab_contours(cnts)

		
		data = [0,0,0,0]
		data_arr=[data]

		if len(cnts) > 0:
			c = max(cnts, key=cv2.contourArea)
			sd = ShapeDetector()
			i = 0
			for c in cnts:
				((x, y), radius) = cv2.minEnclosingCircle(c)
				M = cv2.moments(c)
				cX = int((M["m10"] / M["m00"]))
				cY = int((M["m01"] / M["m00"]))
				shape = sd.detect(c)
				data = [c, cX, cY, shape]
				data_arr.insert(i, data)
				i = i + 1
		
		return data_arr


def overlay(frame, data, overlay_col, num):
	try:
		cv2.drawContours(frame, [data[0]], -1, overlay_col, 2)
		cv2.putText(frame, str(data[3]) + " " + str(num) + ": " + str(data[1]) + "x" + str(data[2]), (data[1], data[2]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
	except:
		print("An exception occurred")



def main():
	while True:
		# compute the center of the contour, then detect the name of the
		# shape using only the contour
		# grab the current frame

		# Incase of stream using cv2.VideoCapture
		#ret, frame = vs.read()

		# incase of stream using imutils
		frame = vs.read()
		frame = imutils.resize(frame, width=640)

		shape_blue = detects(frame, blueLower, blueUpper)
		shape_green = detects(frame, greenLower, greenUpper)		
		shape_red = detects(frame, redLower, redUpper)

		shape_blue_data = [10]
		shape_green_data = [10]
		shape_red_data = [10]

		for i in range(len(shape_blue)-1):
			overlay(frame, shape_blue[i], (0,0,255), i)
			try:
				shape_blue_data[i] = [shape_blue[i][1],shape_blue[i][2],shape_blue[i][3]]
			except:
				pass

		for i in range(len(shape_green)-1):
			overlay(frame, shape_green[i], (255,0,0), i)
			try:
				shape_green_data[i] = [shape_green[i][1],shape_green[i][2],shape_green[i][3]]
			except:
				pass

		for i in range(len(shape_red)-1):
			overlay(frame, shape_red[i], (0,255,0), i)
			try:
				shape_red_data[i] = [shape_red[i][1],shape_red[i][2],shape_red[i][3]]
			except:
				pass

		cv2.imshow("Frame", frame)

		shape_data = [shape_blue_data, shape_green_data, shape_red_data]
		shape_data_str = json.dumps(shape_data)
		client.set('vision_data', shape_data_str)

		#cv2.imshow("Frame1", framer)
		key = cv2.waitKey(1) & 0xFF

		# if the 'q' key is pressed, stop the loop
		if key == ord("q"):
			break

	vs.stop()
	cv2.destroyAllWindows()

main()
