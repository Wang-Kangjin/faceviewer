#! /usr/bin/env python

#coding=utf-8

import sys, os, time
from PyQt4 import QtCore, QtGui
from PreView import PreviewView
from SinView import SingleView
from debug import *
from Global.g_vars import *

def analysis( param ):
	if param.startswith("--"):
		option = param[2:]
		if option == "version":
			print "FacePhoto "+VERSION
		elif option == "help":
			print_help()
		else :
			print_help()
	elif param.startswith("-"):
		option = param[1:]
		if option == "V":
			print "FacePhoto "+VERSION
		elif option == "h":
			print_help()
		else:
			print_help()


def print_help():
	print helpString.__doc__

def helpString():
	'''
FacePhoto is a photo view wrote by QtPy4.
Usage:
 	python main.py [OPTION...] [FILE...]

	Help Options:
	  -h, --help                        Show help options

	Application Options:
	  -V, --version                     Show the application's version
	'''

#MAIN
if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	app.setStyle("windows")
	if len(sys.argv) is 1:
		#TODO:show unitary view
		myapp = PreviewView(".")
	elif len(sys.argv) is 2:
		if sys.argv[1].startswith('-'):
			analysis(sys.argv[1])
			exit(0)
		else:
			if os.path.isdir(sys.argv[1]):
				myapp = PreviewView(sys.argv[1])
			elif os.path.isfile(sys.argv[1]):
				myapp = SingleView(sys.argv[1])
	elif len(sys.argv) > 2:
		print_help()
	myapp.show()
	sys.exit(app.exec_())
