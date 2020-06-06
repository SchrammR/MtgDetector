import glob

import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt


query = cv.imread("images/capturedCard.png")
#query = cv.blur(query,(7,7))
#query = cv.resize(query,(int(query.shape[1]*20/100), int(query.shape[0]*20/100)))


def searchImage(query):
    #load images
    filenames = glob.glob("images/cardReferences/*")
    filenames.sort()
    bagOfImages = [cv.imread(img) for img in filenames]
    bagOfKeypoints = []
    bagOfDescriptors = []

    #bagOfImages[5] = cv.blur(bagOfImages[5],(5,5))
    #bagOfImages[5] = cv.resize(bagOfImages[5],(int(bagOfImages[5].shape[1]*20/100), int(bagOfImages[5].shape[0]*20/100)))

    for i in range(len(bagOfImages)):
        bagOfImages[i] = cv.blur(bagOfImages[i], (7, 7))
        bagOfImages[i] = cv.resize(bagOfImages[i],(int(bagOfImages[i].shape[1]*20/100), int(bagOfImages[i].shape[0]*20/100)))


    #get ORB features
    orb = cv.ORB_create()

    for image in bagOfImages:
        keypoints, descriptors = orb.detectAndCompute(image, None)
        bagOfKeypoints.append(keypoints)
        bagOfDescriptors.append(descriptors)

    queryKp, queryDes = orb.detectAndCompute(query, None)

    lowe_ratio = 0.85

    bf = cv.BFMatcher()
    good = []
    maxMatches = 0
    bestMatch = 0
    what = 0

    for i in range(len(bagOfImages)):
        matches = bf.knnMatch(queryDes,bagOfDescriptors[i], k=3)

        for m,n, l in matches:
            if m.distance < lowe_ratio*n.distance:
                good.append([m])

        msg1 = 'using %s with lowe_ratio %.2f' % ("ORB", lowe_ratio)
        msg2 = 'there are %d good matches' % (len(good))

        #print(i, " Good: ", len(good))
        if len(good) > maxMatches:
            maxMatches = len(good)
            bestMatch = i
            what = good.copy()

        good.clear()

    '''
    font = cv.FONT_HERSHEY_SIMPLEX
    cv.putText(img3,msg1,(10, 250), font, 0.5,(255,255,255),1,cv.LINE_AA)
    cv.putText(img3,msg2,(10, 270), font, 0.5,(255,255,255),1,cv.LINE_AA)
    fname = 'output_%s_%.2f.png' % ("ORB", lowe_ratio)
    cv.imwrite(fname, img3)'''
    print("Good Matches: ", maxMatches)
    img3 = cv.drawMatchesKnn(query,queryKp,bagOfImages[bestMatch],bagOfKeypoints[bestMatch],what, None, flags=2)

    cv.imshow("ImageSearch Result",img3)
    #cv.waitKey()