#! /usr/bin/env python

#coding=utf-8
import os

class Picture(object):
    def __init__(self, floder_name, name):
        self.floder = floder_name
        self.filename = os.path.splitext( name )[0]
        #drop '.' in type name
        self.type = os.path.splitext( name )[1][1:]
        self.abspath = floder_name +'/'+ name
