# -*- coding: utf-8 -*-

DEBUG_MODE = 1
def myprint(color,mes):
    """
0  All attributes off 默认值
1  Bold (or Bright) 粗体 or 高亮
4  Underline 下划线
5  Blink 闪烁
7  Invert 反显
30 Black text
31 Red text
32 Green text
33 Yellow text
34 Blue text
35 Purple text
36 Cyan text
37 White text
40 Black background
41 Red background
42 Green background
43 Yellow background
44 Blue background
45 Purple background
46 Cyan background
47 White background
"""
    if color == 'r':
        fore = 31
    elif color == 'g':
        fore = 32
    elif color == 'b':
        fore = 36
    elif color == 'y':
        fore = 33
    else:
        fore = 37
    color = "\x1B[%d;%dm" % (1,fore)
    print "%s %s\x1B[0m" % (color,mes)

#debug mode
def d( mes ):
    if DEBUG_MODE:
        myprint("r", mes)

#log
def l( mes ):
    myprint("g", mes)
