#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
from Global.g_vars import *

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
