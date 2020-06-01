"""
https://www.youtube.com/watch?v=Fchzk1lDt7Q
"""
import sys
import math
import cv2 as cv
import numpy as np

class boundingBox:
    def __init__(self, x, y, h, w):
        self.x = x
        self.y = y
        self.h = h
        self.w = w

def stackImages(scale, imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv.cvtColor( imgArray[x][y], cv.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv.cvtColor(imgArray[x], cv.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver

def getContours(inputFrame, frameContour):              #gibt auch TREE       #gibt auch simple
    contours, hierarchy = cv.findContours(inputFrame, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)


    for contour in contours:
        area = cv.contourArea(contour)
        if cv.getTrackbarPos("MinArea", "Parameters") < area < cv.getTrackbarPos("MaxArea", "Parameters"):
            cv.drawContours(frameContour, contour, -1, (255, 0, 0), 7)
            #contour lenght - true=contour closed
            perimeter = cv.arcLength(contour, True)
            approx = cv.approxPolyDP(contour, 0.02 * perimeter, True)
            #print(len(approx)) wie viele Ecken

            #bounding Box
            x, y, w, h = cv.boundingRect(approx)
            cv.rectangle(frameContoured, (x, y), (x+w, y+h), (0, 255, 0), 3)
            #cv.putText(frameContoured, "Points: " + str(len(approx)), (x+w+20, y+h+20), cv.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0), 2)
            #cv.putText(frameContoured, "Area: " + str(int(area)), (x+w+20, y+h+45), cv.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0), 2)
            boundingBoxes.append(boundingBox(x, y, h, w))

def clickEventMouseCoordinates(event, x, y, flags, params):
    if event == cv.EVENT_LBUTTONDOWN:
        print(x, ", ", y)
        for box in boundingBoxes:
            if box.x < x < box.x + box.w and box.y < y < box.y + box.h:
                print("Hit")
                saveCard(frameCopy, box)



cap = cv.VideoCapture(0)

def empty(a):
    pass

cv.namedWindow("Parameters")
cv.resizeWindow("Parameters", 640, 240)
cv.createTrackbar("Threshold1", "Parameters", 121, 255, empty)
cv.createTrackbar("Threshold2", "Parameters", 72, 255, empty)
cv.createTrackbar("MinArea", "Parameters", 4000, 50000, empty)
cv.createTrackbar("MaxArea", "Parameters", 20000, 50000, empty)

def saveCard(copy, rectangle:boundingBox):
    card = copy[rectangle.y:rectangle.y+rectangle.h, rectangle.x:rectangle.x+rectangle.w]
    cv.imshow("card", card)
    cv.imwrite("images/capturedCard.png", card)


while True:
    # Capture frame-by-frame
    success, frame = cap.read()

    frameContoured = frame.copy()
    frameCopy = frame.copy()

    boundingBoxes = []


    frameBlur = cv.GaussianBlur(frame, (7,7), 1)
    frameGray = cv.cvtColor(frameBlur, cv.COLOR_BGR2GRAY)

    threshold1 = cv.getTrackbarPos("Threshold1", "Parameters")
    threshold2 = cv.getTrackbarPos("Threshold2", "Parameters")

    #Edge Detection
    frameCanny = cv.Canny(frameGray, threshold1, threshold2)

    #Dilate Image - linen dicker machen
    kernel = np.ones((5,5))
    frameDilated = cv.dilate(frameCanny, kernel, iterations=1)

    #get Contours
    getContours(frameDilated, frameContoured)


    imgStack = stackImages(0.9, ([frame, frameBlur, frameCanny],
                                 [frameDilated, frameContoured, frameContoured]))
    #cv.imshow("Result", imgStack)
    cv.imshow("Result", frameContoured)
    cv.setMouseCallback("Result", clickEventMouseCoordinates)


    #Close Windows
    key = cv.waitKey(1) & 0xFF
    if key ==ord('q'):
        break

# When everything done, release the capture
cap.release()
cv.destroyAllWindows()