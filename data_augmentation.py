import cv2
import numpy as np
import glob
import re

def keyFunc(afilename):
    nondigits = re.compile("\D")
    return int(nondigits.sub("", afilename))
person=1
random=6
room=['3','5','6','12','13','14','15','19','21','23','25','27','30']
for i in room:
    file = glob.glob('/home/user/Desktop/coord/Make coffee_'+str(i)+'_'+str(person)+'_'+str(random)+'/*.jpg')

    img_array = []
    for x in sorted(file, key=keyFunc):
        img = cv2.imread(x)
        height, width, layers = img.shape
        size = (width, height)
        img_array.append(img)
    out = cv2.VideoWriter('/home/user/Desktop/coord/video_1/Make coffee'+'_'+str(i)+'_'+str(random)+'.avi', cv2.VideoWriter_fourcc(*'DIVX'), 5, size)

    for i in range(len(img_array)):
        out.write(img_array[i])
    out.release()