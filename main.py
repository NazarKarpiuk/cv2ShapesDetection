import cv2
import numpy as np
import Stack_im

def getContours(img):
    contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        print(area)
        if area>500:
            cv2.drawContours(imgContour, cnt, -1, (255, 100, 0), 3)
            peri = cv2.arcLength(cnt,True)
            #print(peri)
            approx = cv2.approxPolyDP(cnt,0.02*peri,True)
            #print(len(approx))
            objCor = len(approx)
            x,y,w,h = cv2.boundingRect(approx)

            if objCor == 3:
                OBJtype = "triangle"
            elif objCor == 4:
                aspRatio = w/float(h)
                if aspRatio > 0.95 and aspRatio < 1.05:
                    OBJtype = "Square"
                else:
                    OBJtype = "Rectangle"
            elif objCor >4:
                OBJtype = "Circle"

            cv2.rectangle(imgContour,(x,y),(x+w,y+h),(0,255,0),2)
            cv2.putText(imgContour,OBJtype,(x+(w//2)-10,y+(h//2)-10),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0),2)
img = cv2.imread("Resources/shapes.jpg")
imgShapes = cv2.resize(img,(370,300))

imgContour = imgShapes.copy()

imgShapesGray = cv2.cvtColor(imgShapes,cv2.COLOR_BGR2GRAY)
imgBlur = cv2.GaussianBlur(imgShapesGray,(7,7),1)
imgCanny = cv2.Canny(imgBlur,50,50)
getContours(imgCanny)
imgBlank = np.zeros_like(imgShapes)
stackImg = Stack_im.stackImages(0.8,([imgShapes,imgShapesGray,imgBlur],[imgCanny,imgContour,imgBlank ]))

#cv2.imshow("Shapes", imgShapes)
#cv2.imshow("ShapesGray", imgShapesGray)
#cv2.imshow("ShapesBlur", imgBlur)
cv2.imshow("Stack",stackImg )
cv2.waitKey(0)