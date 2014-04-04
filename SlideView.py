#! /usr/bin/env python

#coding=utf-8
from ui.slideshow_ui import Ui_SlideShow
from Global.g_vars import *
from PyQt4 import QtCore, QtGui
from debug import d, l
from funs import *
import os, time, thread

class SlideView(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self,parent)
        self.ui = Ui_SlideShow()
        self.ui.setupUi(self)
        thread.start_new_thread(play, (self,))

def play(self):
    time.sleep(1)
    l("enter ppt mode")
    self.setWindowFlags(QtCore.Qt.Window)
    self.showFullScreen()
    tmp_image_index = g_image_index
    while tmp_image_index+1 <= len(g_image_list):
        image = QtGui.QPixmap( g_image_list[tmp_image_index].abspath )
        label_width = self.ui.image_label.width()
        label_height = self.ui.image_label.height()
        if image.width() > label_width :
            image = image.scaledToWidth(label_width)
            if image.height() > label_height:
                image = image.scaledToHeight(label_height)
        elif image.height() > label_height:
            image = image.scaledToHeight(label_height)
            if image.width() > label_width:
                image = image.scaledToWidth(label_width)
        d("showing "+str(tmp_image_index)+":"+g_image_list[tmp_image_index].abspath)
        self.ui.image_label.setPixmap(image)
        time.sleep(3)
        tmp_image_index = tmp_image_index + 1
    thread.exit_thread()
