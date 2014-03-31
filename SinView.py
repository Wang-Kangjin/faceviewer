#! /usr/bin/env python

#coding=utf-8
from PyQt4 import QtCore, QtGui
import cv2.cv as cv
import sys, os
from main2_ui import Ui_Form
from debug import d, l
from Picture import *
from funs import *
from Global.g_vars import *


class SingleView(QtGui.QWidget):
	current_image_item = 0

	def __init__(self, image_path, parent=None):
		QtGui.QWidget.__init__(self, parent)
		self.ui = Ui_Form()
		self.ui.setupUi(self)
		self.init_image_list( image_path )
		self.current_image_item = None
		self.face_list = []
		self.show_image()
		QtCore.QObject.connect(self.ui.pushButton, QtCore.SIGNAL("clicked()"), self.click_next)
		QtCore.QObject.connect(self.ui.pushButton_3, QtCore.SIGNAL("clicked()"), self.click_previous)
		QtCore.QObject.connect(self.ui.pushButton_5, QtCore.SIGNAL("clicked()"), self.click_detect)

	def show_image(self):
		d(g_image_list[g_image_index].abspath)
		self.photo = QtGui.QPixmap( g_image_list[g_image_index].abspath )
		if self.photo :
			l('load image success')
		else:
			l('load image faild: check file '+image_path+' exist.')
			exit(1)
		if SingleView.current_image_item:
			image_size = self.photo.size()
			#step 1: remove before image and face rectangle
			self.ui.scene.removeItem(SingleView.current_image_item)
			for face in self.face_list:
				self.ui.scene.removeItem(face)
	 		self.ui.scene.setSceneRect(0, 0, image_size.width(), image_size.height())
			SingleView.current_image_item = self.ui.scene.addPixmap(self.photo)
		else:
			SingleView.current_image_item = self.ui.scene.addPixmap(self.photo)

	def click_next(self):
		global g_image_index
		d("print next pushButton")
		d("total:"+str(len(g_image_list)))
		d("current:"+str(g_image_index + 1))
		if g_image_index + 1 < len( g_image_list ):
			g_image_index = g_image_index + 1
			self.show_image()

	def click_previous(self):
		global g_image_index
		d("print next pushButton")
		d("total:"+str(len(g_image_list)))
		d("current:"+str(g_image_index + 1))
		if g_image_index > 0:
			g_image_index = g_image_index - 1
			self.show_image()

	def click_detect(self):
		current_img_path = g_image_list[g_image_index].abspath
		cv_image = cv.LoadImage(current_img_path, 1)
		cascade = cv.Load("./haarcascade_frontalface_alt.xml")
		self.detect_and_draw(cv_image, cascade)

	def init_image_list(self, image_path):
		floder_name = os.path.dirname(os.path.abspath(image_path))
		target_name = os.path.basename( image_path )
		l("opening:"+ floder_name)
		#clear the link list of image
		del g_image_list[:]
		g_image_index = 0
		for filename in os.listdir(floder_name):
			#find all image
			if self.isimage( filename ):
				g_image_list.append(Picture( floder_name , filename))
				if filename == target_name:
					g_image_index += 1
		l("this floder has "+str(len(g_image_list))+" photos")

	def detect_and_draw(self, img, cascade):
	# allocate temporary images
		gray = cv.CreateImage((img.width,img.height), 8, 1)
		small_img = cv.CreateImage((cv.Round(img.width / image_scale), cv.Round (img.height / image_scale)), 8, 1)

		# convert color input image to grayscale
		cv.CvtColor(img, gray, cv.CV_BGR2GRAY)

		# scale input image for faster processing
		cv.Resize(gray, small_img, cv.CV_INTER_LINEAR)

		cv.EqualizeHist(small_img, small_img)

		if(cascade):
			t = cv.GetTickCount()
			faces = cv.HaarDetectObjects(small_img, cascade, cv.CreateMemStorage(0),haar_scale, min_neighbors, haar_flags, min_size)
			t = cv.GetTickCount() - t
			print "detection time = %gms" % (t/(cv.GetTickFrequency()*1000.))
			if faces:
				for ((x, y, w, h), n) in faces:
					# the input to cv.HaarDetectObjects was resized, so scale the
					# bounding box of each face and convert it to two CvPoints
					#pt1 = (int(x * image_scale), int(y * image_scale))
					#pt2 = (int((x + w) * image_scale), int((y + h) * image_scale))
					draw_color = QtGui.QColor(127, 255, 0)
					pen = QtGui.QPen(draw_color)
					pen.setWidth(2)
					aface = self.ui.scene.addRect(
						int(x * image_scale),
						int(y * image_scale),
						int(w * image_scale),
						int(h * image_scale),
						pen
						)
					self.face_list.append(aface)
					#cv.Rectangle(img, pt1, pt2, cv.RGB(255, 0, 0), 3, 8, 0)

		#cv.ShowImage("result", img)
