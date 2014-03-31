#! /usr/bin/env python

#coding=utf-8
from PyQt4 import QtCore, QtGui
from main2_ui import Ui_Form
from debug import d, l
import os

class PreviewView(QtGui.QWidget):
	def __init__(self, show_path, parent=None):
		QtGui.QWidget.__init__(self,parent)
		self.ui = Ui_Form()
		self.ui.setupUi(self)


