#! /usr/bin/env python

#coding=utf-8
from PyQt4 import QtCore, QtGui
from preui import Ui_Preview
from debug import d, l
from funs import *
import os

class PreviewView(QtGui.QWidget):
	def __init__(self, show_path, parent=None):
		QtGui.QWidget.__init__(self,parent)
		self.ui = Ui_Preview()
		self.ui.setupUi(self)
		self.openfolder(show_path)

	def openfolder(self, floder_path):
		self.ui.listWidget.clear()
		floder_icon_pixmap = QtGui.QPixmap("res/Black.png")
		if floder_icon_pixmap:
			l("load floder icon success!")
		floder_icon = QtGui.QIcon(floder_icon_pixmap)
		for item in os.listdir(floder_path):
			print item
			if ispath(item):
				list_item = QtGui.QListWidgetItem(floder_icon, item)
				self.ui.listWidget.addItem(list_item)
			elif isimage(item):
				pixmap = QtGui.QPixmap(floder_path+"/"+item)
				item_icon = QtGui.QIcon(pixmap)
				list_item = QtGui.QListWidgetItem(item_icon, item)
				self.ui.listWidget.addItem(list_item)

		self.ui.listWidget.setViewMode(QtGui.QListView.IconMode)

