import cv2
import time
import numpy as np
from numpy.core.defchararray import upper

fourcc= cv2.VideoWriter_fourcc(*'XVID')
outputFile= cv2.VideoWriter('output.avi',fourcc,20.0,(640,480))
camera=cv2.VideoCapture(0)
time.sleep(2)
background=0

for i in range(60):
    ret,background=camera.read()
    
background=np.flip(background,axis=1)

while (camera.isOpened()):
    ret,image=camera.read()
    if not ret:
        break
    image=np.flip(image,axis=1)
    hsv=cv2.cvtColor(image,cv2.COLOR_BGR2HSV)

    lowerBlack=np.array([10,255,255])
    upperBlack=np.array([0,120,50])
    mask1=cv2.inRange(hsv,lowerBlack,upperBlack)

    lowerBlack=np.array([10,255,255])
    upperBlack=np.array([0,120,50])
    mask2=cv2.inRange(hsv,lowerBlack,upperBlack)

    mask1=mask1+mask2

    mask1=cv2.morphologyEx(mask1,cv2.MORPH_OPEN,np.ones((3,3),np.uint8))
    mask1=cv2.morphologyEx(mask1,cv2.MORPH_DILATE,np.ones((3,3),np.uint8))

# In line 38 here we are selecting the part which dooes not have red color
    mask2=cv2.bitwise_not(mask1)
    result1=cv2.bitwise_and(image,image,mask=mask2)
    result2=cv2.bitwise_and(background,background,mask=mask1)

    final_output=cv2.addWeighted(result1,1,result2,1,0)
    outputFile.write(final_output)
    cv2.imshow('COUNTRIES',final_output)
    cv2.waitKey(1)


camera.release()
cv2.destroyAllWindows()

