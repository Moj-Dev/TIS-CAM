
# Add path to python-common/TIS.py to the import path
import sys
sys.path.append("../python-common")

import cv2
import numpy as np
import os
import TIS
import time
from collections import namedtuple


# This sample shows, how to get an image in a callback and use trigger or software trigger
# needed packages:
# pyhton-opencv
# pyhton-gst-1.0
# tiscamera

class CustomData:
        ''' Example class for user data passed to the on new image callback function
        '''

        def __init__(self, newImageReceived, image):
                self.newImageReceived = newImageReceived
                self.image = image
                self.busy = False

CD = CustomData(False, None)

def on_new_image(tis, userdata):
        '''
        Callback function, which will be called by the TIS class
        :param tis: the camera TIS class, that calls this callback
        :param userdata: This is a class with user data, filled by this call.
        :return:
        '''
        # Avoid being called, while the callback is busy
        if userdata.busy is True:
                return

        userdata.busy = True
        userdata.newImageReceived = True
        userdata.image = tis.Get_image()
        userdata.busy = False

Tis = TIS.TIS()
height = 2160
width  = 3840
#3840x2160 
# The following line opens and configures the video capture device.
Tis.openDevice("06020009", width, height, "15/1","rggb16", False)

# The next line is for selecting a device, video format and frame rate.
#if not Tis.selectDevice():
#        quit(0)

#Tis.List_Properties()
Tis.Set_Image_Callback(on_new_image, CD)

# Tis.Set_Property("Trigger Mode", "Off") # Use this line for GigE cameras
Tis.Set_Property("Trigger Mode", False)
CD.busy = True # Avoid, that we handle image, while we are in the pipeline start phase
# Start the pipeline
Tis.Start_pipeline()

# Tis.Set_Property("Trigger Mode", "On") # Use this line for GigE cameras
Tis.Set_Property("Trigger Mode", True)
cv2.waitKey(1000)

CD.busy = False  # Now the callback function does something on a trigger

# Remove comment below in oder to get a propety list.
# Tis.List_Properties()

# In case a color camera is used, the white balance automatic must be
# disabled, because this does not work good in trigger mode
Tis.Set_Property("Whitebalance Auto", True)
Tis.Set_Property("Whitebalance Auto", False)
Tis.Set_Property("Whitebalance Auto", True)

# Query the gain auto and current value :
print("Gain Auto : %s " % Tis.Get_Property("Gain Auto").value)
print("Gain : %d" % Tis.Get_Property("Gain").value)

# Check, whether gain auto is enabled. If so, disable it.
Tis.Set_Property("Gain Auto",False)
Tis.Set_Property("Gain Auto",True)
Tis.Set_Property("Gain Auto",False)

if Tis.Get_Property("Gain Auto").value :
        Tis.Set_Property("Gain Auto",False)
        print("Gain Auto now : %s " % Tis.Get_Property("Gain Auto").value)

Tis.Set_Property("Gain",0)

# Now do the same with exposure. Disable automatic if it was enabled
# then set an exposure time.
if Tis.Get_Property("Exposure Auto").value :
        Tis.Set_Property("Exposure Auto", False)
        print("Exposure Auto now : %s " % Tis.Get_Property("Exposure Auto").value)
        
Tis.Set_Property("Exposure Auto", False)
Tis.Set_Property("Exposure Auto", True)
Tis.Set_Property("Exposure Auto", False)

#Tis.Set_Property("Exposure Auto Upper Limit Auto", 200000)

Tis.Set_Property("Exposure Time (us)", 66000)

Tis.Set_Property("Tonemapping", True)
Tis.Set_Property("Tonemapping", False)
Tis.Set_Property("Tonemapping", True)

Tis.Set_Property("Sharpness", 8)
Tis.Set_Property("Sharpness", 8)

error = 0
print('Press Esc to stop')
lastkey = 0
cv2.namedWindow('opencv',cv2.WINDOW_NORMAL)
fourcc = cv2.VideoWriter_fourcc(*'DIVX')  # 'x264' doesn't work

#out = cv2.VideoWriter('output.avi', -1, 15.0, (640,480))

out = cv2.VideoWriter('output.avi',  cv2.VideoWriter_fourcc(*'M', 'J', 'P', 'G'), 15.0, (width, height)) 
try:
        while lastkey != 27 and error < 5:
                #Tis.Set_Property("Tonemapping", True)
                #Tis.Set_Property("Sharpness", 8)
                #print(Tis.Get_Property("Exposure Time (us)"))
                #print(Tis.Get_Property("Sharpness"))


                time.sleep(0.01)
                Tis.Set_Property("Software Trigger",1) # Send a software trigger

                # Wait for a new image. Use 10 tries.
                tries = 10
                while CD.newImageReceived is False and tries > 0:
                        time.sleep(0.01)
                        tries -= 1

                # Check, whether there is a new image and handle it.
                if CD.newImageReceived is True:
                        CD.newImageReceived = False
                        #frame = CD.image
                        #print(frame.shape)

                        #cv2.imshow('opencv', CD.image)

                        img= CD.image#cv2.cvtColor(CD.image, cv2.COLOR_BGR2RGB)
                        #cv2.imshow('opencv', img)

                        out.write(img)

                else:
                        print("No image received")

                lastkey = cv2.waitKey(10)

except KeyboardInterrupt:
        cv2.destroyWindow('opencv')

# Stop the pipeline and clean ip
Tis.Stop_pipeline()
out.release()
cv2.destroyAllWindows()
print('Program ends')

import cv2
vidcap = cv2.VideoCapture('output.avi')
success,image = vidcap.read()
count = 0
while success:
    image_ = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    cv2.imwrite("frames/frame%d.jpg" % count, image_)     # save frame as JPEG file
    success,image = vidcap.read()
    print('Read a new frame: ', success)
    count += 1


