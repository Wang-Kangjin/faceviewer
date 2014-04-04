#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
from PyQt4 import QtCore, QtGui
from Global.g_vars import *
import cv2.cv as cv

def isimage( filename):
    '''TODO: FIXBUG:
    a floder named fuckyou.jpg '''
    filetype = os.path.splitext( filename )[1]
    return filetype in g_support_type

def ispath( pathname):
    filetype = os.path.splitext( pathname )[1]
    if filetype:
        return False
    else:
        return True

def QPixmapToIplImage( pixmap ):
    pixmap = pixmap.toImage()
    width = pixmap.width();
    height = pixmap.height()
    size = (width, height)
    IplImageBuffer = cv.CreateImage(size, 8, 3)
    for y in range(0, height):
        for x in range(0, width):
            rgb = pixmap.pixel(x, y)
            cv.Set2D(IplImageBuffer, y, x, cv.CV_RGB(QtGui.qRed(rgb), QtGui.qGreen(rgb), QtGui.qBlue(rgb)))
    return IplImageBuffer;
