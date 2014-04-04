#! /usr/bin/env python

#coding=utf-8
from PyQt4 import QtCore, QtGui
import cv2.cv as cv
import sys, os
from ui.main2_ui import Ui_Form
from debug import d, l
from Picture import *
from funs import *
from Global.g_vars import *
from SlideView import *

class SingleView(QtGui.QDialog):

	def __init__(self, image_path, parent=None):
		QtGui.QDialog.__init__(self, parent)
		self.ui = Ui_Form()
		self.ui.setupUi(self)
		self.floder_name = ''
		self.init_image_list( image_path )
		self.current_image_item = None
		self.face_list = []
		self.temp_image = None
		self.show_image()
		QtCore.QObject.connect(self.ui.pushButton, QtCore.SIGNAL("clicked()"), self.click_next)
		QtCore.QObject.connect(self.ui.pushButton_3, QtCore.SIGNAL("clicked()"), self.click_previous)
		QtCore.QObject.connect(self.ui.pushButton_5, QtCore.SIGNAL("clicked()"), self.click_detect)
		QtCore.QObject.connect(self.ui.pushButton_4, QtCore.SIGNAL("clicked()"), self.click_preview)
		QtCore.QObject.connect(self.ui.pushButton_2, QtCore.SIGNAL("clicked()"), self.click_play)
		QtCore.QObject.connect(self.ui.close, QtCore.SIGNAL("clicked()"), self.click_close)

	def show_image(self):
		d("index of image is "+ str(g_image_index))
		d(g_image_list[g_image_index].abspath)
		self.photo = QtGui.QPixmap( g_image_list[g_image_index].abspath )
		self.temp_image = QtGui.QPixmap(self.photo)
		self.zoom_time = 0
		if self.photo :
			l('load image success')
		else:
			l('load image faild: check file '+image_path+' exist.')
			exit(1)
		if self.current_image_item:
			image_size = self.photo.size()
			#step 1: remove before image and face rectangle
			self.ui.scene.removeItem(self.current_image_item)
			self.reomve_face_rects()

	 		self.ui.scene.setSceneRect(0, 0, image_size.width(), image_size.height())
			self.current_image_item = self.ui.scene.addPixmap(self.photo)
		else:
			self.current_image_item = self.ui.scene.addPixmap(self.photo)

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
		cv_image = QPixmapToIplImage(self.current_image_item.pixmap())
		l(type(cv_image))
		self.reomve_face_rects()
		cascade = cv.Load("./haarcascade_frontalface_alt.xml")
		self.detect_and_draw(cv_image, cascade)

	def click_play(self):
		playdlg = SlideView()
		playdlg.exec_()
		d("play end")

	def click_preview(self):
		self.close()
		from PreView import PreviewView
		pre_view = PreviewView(self.floder_name+"/")
		pre_view.exec_()

	def click_close(self):
		self.close
		exit(0)

	def keyPressEvent(self, key_event):
		d(key_event.key())
		#try:
		operator = {
			QtCore.Qt.Key_W:self.turn_left,
			QtCore.Qt.Key_S:self.turn_right,
			QtCore.Qt.Key_A:self.click_previous,
			QtCore.Qt.Key_D:self.click_next,
			QtCore.Qt.Key_Q:self.stretch,
				QtCore.Qt.Key_E:self.reduce}
		operator.get(key_event.key())()
		#except TypeError:
			#print "no function to call"
	def turn_left(self):
		l("turn left")
		curr_image = self.current_image_item.pixmap()
		width = curr_image.width()
		height = curr_image.height()
		matrix = QtGui.QMatrix()
		matrix.rotate(270)
		after_rotate_image = curr_image.transformed(matrix)
		self.current_image_item.setPixmap(after_rotate_image)

		temp_img = self.temp_image
		width = temp_img.width()
		height = temp_img.height()
		matrix = QtGui.QMatrix()
		matrix.rotate(270)
		self.temp_image = temp_img.transformed(matrix)

	def turn_right(self):
		l("turn right")
		curr_image = self.current_image_item.pixmap()
		width = curr_image.width()
		height = curr_image.height()
		matrix = QtGui.QMatrix()
		matrix.rotate(90)
		after_rotate_image = curr_image.transformed(matrix)
		self.current_image_item.setPixmap(after_rotate_image)

		temp_img = self.temp_image
		width = temp_img.width()
		height = temp_img.height()
		matrix = QtGui.QMatrix()
		matrix.rotate(90)
		self.temp_image = temp_img.transformed(matrix)

	def stretch(self):
		curr_pixmap = self.temp_image
		height = curr_pixmap.height()
		zoom_interval = int(height * 0.2)
		self.zoom_time =  self.zoom_time + 1
		d("before:"+str(height))
		l("after: "+str(height*1.2))
		curr_pixmap = curr_pixmap.scaledToHeight(height+self.zoom_time*zoom_interval)
		self.current_image_item.setPixmap(curr_pixmap)

	def reduce(self):
		curr_pixmap = self.temp_image
		height = curr_pixmap.height()
		zoom_interval = int(height * 0.2)
		self.zoom_time = self.zoom_time - 1
		curr_pixmap = curr_pixmap.scaledToHeight(height + self.zoom_time*zoom_interval)
		self.current_image_item.setPixmap(curr_pixmap)

	def init_image_list(self, image_path):
		global g_image_index
		image_path = str(image_path)
		self.floder_name = os.path.dirname(os.path.abspath(image_path))
		target_name = os.path.basename( image_path )
		l("opening floder:"+ self.floder_name)
		l("opening target:"+ target_name)
		#clear the link list of image
		del g_image_list[:]
		g_image_index = 0
		count = 0
		for filename in os.listdir(self.floder_name):
			#find all image
			if isimage( filename ):
				l(filename)
				g_image_list.append(Picture( self.floder_name , filename))
				if filename == target_name:
					d("found!")
					g_image_index = count
				count = count +1
		l("this floder has "+str(len(g_image_list))+" photos")
		d("target index is "+ str(g_image_index))

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
					aface.setZValue(1)
					d("added")
					self.face_list.append(aface)
					#cv.Rectangle(img, pt1, pt2, cv.RGB(255, 0, 0), 3, 8, 0)

		#cv.ShowImage("result", img)
	def reomve_face_rects(self):
		for face in self.face_list:
			d("remove face rect..")
			self.ui.scene.removeItem(face)
		self.face_list = []
