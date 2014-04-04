#! /usr/bin/env python

#coding=utf-8
from PyQt4 import QtCore, QtGui
from ui.preui import Ui_Preview
from SinView import SingleView
from debug import d, l
from funs import *
import os, time

class PreviewView(QtGui.QDialog):
	def __init__(self, show_path, parent=None):
		QtGui.QDialog.__init__(self,parent)
		self.ui = Ui_Preview()
		self.ui.setupUi(self)
		self.path = show_path
		self.openfolder(show_path)
		self.ui.listWidget.setIconSize(QtCore.QSize(80, 80))
		QtCore.QObject.connect(self.ui.listWidget, QtCore.SIGNAL("itemDoubleClicked(QListWidgetItem*)"), self.on_item_double_clicked)

	def openfolder(self, floder_path):
		self.ui.listWidget.clear()
		self.path = floder_path+"/"
		p_floder_icon_pixmap = QtGui.QPixmap("res/10.png")
		floder_icon_pixmap = QtGui.QPixmap("res/Black.png")
		if floder_icon_pixmap:
			l("load floder icon success!")
		floder_icon = QtGui.QIcon(floder_icon_pixmap)
		p_floder_icon = QtGui.QIcon(p_floder_icon_pixmap)
		p_floder_item = QtGui.QListWidgetItem(p_floder_icon, "..")
		self.ui.listWidget.addItem(p_floder_item)
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

	def on_item_double_clicked(self, item):
		l("open item: " + item.text())
		if self.item_is_floder(item):
			self.openfolder(self.path + item.text())
		elif self.item_is_image(item):
			self.hide()
			d("path :"+self.path + item.text())
			sinview = SingleView(self.path + item.text())
			sinview.exec_()
			self.show()

	def item_is_floder(self, item):
		return ispath(str(item.text()))

	def item_is_image(self, item):
		return isimage(str(item.text()))
