#!/usr/bin/env python
# a simple script to check HSV values for OpenCV

import cv
import time

y_co = 0
x_co = 0

def on_mouse(event, x, y, flag, param):
    global x_co
    global y_co
    if (event == cv.CV_EVENT_MOUSEMOVE):
        x_co = x
        y_co = y

cv.NamedWindow("camera", 1)
capture = cv.CaptureFromCAM(0)
font = cv.InitFont(cv.CV_FONT_HERSHEY_SIMPLEX, 0.55, 1, 0, 2, 8)

while True:
    src = cv.QueryFrame(capture)
    cv.Smooth(src, src, cv.CV_BLUR, 3)
    hsv = cv.CreateImage(cv.GetSize(src), 8, 3)
    thr = cv.CreateImage(cv.GetSize(src), 8, 1)
    cv.CvtColor(src, hsv, cv.CV_BGR2HSV)
    cv.SetMouseCallback("camera", on_mouse, 0);
    s = cv.Get2D(hsv, y_co, x_co)
    cv.PutText(src,str(s[0])+","+str(s[1])+","+str(s[2]), (x_co,y_co),font, (55,25,255))
    cv.ShowImage("camera", src)

    if cv.WaitKey(10) == 27:
        break
