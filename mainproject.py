# -*- coding: utf-8 -*-
"""
Created on Thu Nov 11 19:57:48 2021

@author: abhis
"""

import numpy as np
import cv2
import pyautogui
prev_pos = "neutral"
vid = cv2.VideoCapture(0)
img1=np.zeros((400,400,3),np.uint8)
img2=np.zeros((400,400,3),np.uint8)
def nothing(x):
    pass
def max_contour(contours):
    index=0
    max_area = 0
    for i in range(len(contours)):
        area = cv2.contourArea(contours[i])
        if(area > max_area):
            index = i
            max_area = area
    return index
    
cv2.namedWindow('HAND')
# cv2.namedWindow('URange')
# cv2.namedWindow('LRange')
while 1:
    
    cv2.createTrackbar('UR','HAND',0,255,nothing)
    cv2.createTrackbar('UG','HAND',0,255,nothing)
    cv2.createTrackbar('UB','HAND',0,255,nothing)
    cv2.createTrackbar('LR','HAND',0,255,nothing)
    cv2.createTrackbar('LG','HAND',0,255,nothing)
    cv2.createTrackbar('LB','HAND',0,255,nothing)
    while True:
        _,frame = vid.read()
        frame = cv2.flip(frame,1)
        frame = frame[:300,300:600]
        frame = cv2.GaussianBlur(frame,(5,5),0)
        ur=cv2.getTrackbarPos('UR','HAND')
        ug=cv2.getTrackbarPos('UG','HAND')
        ub=cv2.getTrackbarPos('UB','HAND')
        lr=cv2.getTrackbarPos('LR','HAND')
        lg=cv2.getTrackbarPos('LG','HAND')
        lb=cv2.getTrackbarPos('LB','HAND')
        binary = cv2.inRange(frame,(136,131,130),(240,240,240))
        gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        _,thres = cv2.threshold(gray,127,255,cv2.THRESH_BINARY)
        contours, hierarchy = cv2.findContours(binary,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        index=max_contour(contours)
        cv2.drawContours(frame,contours,index,(0,0,255),2)
        M = cv2.moments(contours[index])
        try:
            x = int(M['m10']/M['m00'])
            y = int(M['m01']/M['m00'])
        except ZeroDivisionError:
            continue
        frame = cv2.circle(frame , (x,y) , 10 , (255,0,0) , 2)
        # frame = cv2.drawContours(frame,contours , index, (0,0,255), 2)

        frame = cv2.line(frame , (75,0) , (75,299) , (255,255,255) , 2)
        frame = cv2.line(frame , (225,0) , (225,299) , (255,255,255) , 2)
        frame = cv2.line(frame , (75,200) , (225,200) , (255,255,255) , 2)
        frame = cv2.line(frame , (75,250) , (225,250) , (255,255,255) , 2)

        cv2.imshow('HAND',frame)
        cv2.imshow('hand2',binary)
        if x < 75:
            curr_pos = "left"
        elif x > 225:
            curr_pos = "right"
        elif y < 200 and x > 75 and x < 225:
            curr_pos = "up"
        elif y > 250 and x > 75 and x < 225:
            curr_pos = "down"
        else:
            curr_pos = "neutral"
        
        if curr_pos!=prev_pos:
            if curr_pos != "neutral":
                pyautogui.press(curr_pos)
            prev_pos = curr_pos
        q = cv2.waitKey(1)
        if q==ord('q'):
            break

    break
vid.release()
cv2.destroyAllWindows()
    
    
    