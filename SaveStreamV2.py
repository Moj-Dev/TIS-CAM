#!/usr/bin/env python3

# Copyright 2019 The Imaging Source Europe GmbH
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#
# This example will show you how to save a video stream to a file
#
import sys
sys.path.append("../python-common")

import time
import sys
import gi
import TIS


gi.require_version("Tcam", "0.1")
gi.require_version("Gst", "1.0")

from gi.repository import Tcam, Gst




def main():

    '''Tis = TIS.TIS()
    Tis.openDevice("06020009", 4000, 3000, "15/1","rggb16" , False) #1920x1080 3840x2160 TIS.SinkFormats.BGRA
    Tis.Set_Property("Trigger Mode", False)
    Tis.Start_pipeline()

    Tis.Set_Property("Auto Functions ROI Control", False)
    Tis.Set_Property("Auto Functions ROI Preset", "Full Sensor")
    Tis.Set_Property("Highlight Reduction", True)

    Tis.Set_Property("Whitebalance Auto", True)

    Tis.Set_Property("Sharpness", 8)
    #Tis.Set_Property("Gamma", 0.8)
    Tis.Set_Property("Saturation", 1.4)
    #Tis.Set_Property("Contrast", -50)

    Tis.Set_Property("Gain Auto",False)
    Tis.Set_Property("Gain",0)

    Tis.Set_Property("Exposure Auto", False)
    Tis.Set_Property("Exposure", 34000)
    Tis.Set_Property("Tonemapping", True)
    Tis.Set_Property("Tonemapping", False)
    Tis.Set_Property("Tonemapping", True)


    Tis.Stop_pipeline()'''

    Gst.init(sys.argv)  # init gstreamer

    serial = '06020009'


    pipeline = Gst.parse_launch("tcambin name=bin"
                                " ! video/x-raw,format=BGRx,width=3840,height=2160 ,framerate=30/1"
                                #" ! video/x-raw,format=BGRx,width=1920,height=1080 ,framerate=15/1"
                                " ! tee name=t"
                                " ! queue"
                                " ! videoconvert"
                                " ! ximagesink"
                                " t."
                                " ! queue"
                                " ! videoconvert"
                                " ! avimux"
                                " ! filesink name=fsink")

    # to save a video without live view reduce the pipeline to the following:
    #3840x2160    1920x1080
    

    '''pipeline = Gst.parse_launch("tcambin name=bin"
                                " ! video/x-raw,format=BGRx,width=3840,height=2160 ,framerate=30/1"
                                " ! videoconvert"
                                " ! avimux"
                                " ! filesink name=fsink")'''


    camera = Gst.ElementFactory.make("tcambin")

    property_names = camera.get_tcam_property_names()
    print(property_names)

    for name in property_names:
        (ret, value,
         min_value, max_value,
         default_value, step_size,
         value_type, flags,
         category, group) = camera.get_tcam_property(name)
        #print(camera.get_tcam_property(name))
        if not ret:
            print("could not receive value {}".format(name))
            continue
    
    
    
    
    camera = pipeline.get_by_name("bin")
    # serial is defined, thus make the source open that device
    if serial is not None:
        camera.set_property("serial", serial)
        
    time.sleep(0.5)

    file_location = "tiscamera-save-stream.avi"
    fsink = pipeline.get_by_name("fsink")
    fsink.set_property("location", file_location)
    pipeline.set_state(Gst.State.PLAYING)

    time.sleep(0.5)

    #camera = Gst.ElementFactory.make("tcambin")



    #camera.set_tcam_property("Exposure Auto", True)
    camera.set_tcam_property("Exposure Auto", False)
    #camera.set_tcam_property("Exposure Auto", True)

    camera.set_tcam_property("Gain Auto", False)
    camera.set_tcam_property("Gain", 0)
    #camera.set_tcam_property("Exposure", 33000)
    camera.set_tcam_property("Tonemapping", True)
    camera.set_tcam_property("Tonemapping", False)
    camera.set_tcam_property("Tonemapping", True)

    camera.set_tcam_property("Auto Functions ROI Control", False)
    camera.set_tcam_property("Auto Functions ROI Preset", "Full Sensor")
    camera.set_tcam_property("Highlight Reduction", False)
    camera.set_tcam_property("Sharpness", 8)
    #camera.set_tcam_property("Gamma", 0.8)
    camera.set_tcam_property("Saturation", 1.4)
    #camera.set_tcam_property("Contrast", -50)
    #camera.set_tcam_property("Exposure Auto Upper Limit Auto", True)
    camera.set_tcam_property("Exposure Auto Upper Limit Auto", False)
    #camera.set_tcam_property("Exposure Auto Upper Limit Auto", 28000)
    #camera.set_tcam_property("Exposure", 20000)





    #print_properties(camera)




    print("Press Ctrl-C to stop.")

    try:
        while True:
            time.sleep(1)
            #property_names = camera.get_tcam_property_names()
            #print(property_names)
            camera.set_tcam_property("Sharpness", 8)
            camera.set_tcam_property("Tonemapping", True)
            camera.set_tcam_property("Exposure Time (us)", 33000)

            print(camera.get_tcam_property("Exposure Time (us)"))
            print(camera.get_tcam_property("Sharpness"))


            print(camera.get_tcam_property("Tonemapping"))



    except KeyboardInterrupt:
        pass
    finally:
        pipeline.set_state(Gst.State.NULL)



if __name__ == "__main__":
    main()



import cv2
vidcap = cv2.VideoCapture('tiscamera-save-stream.avi')
success,image = vidcap.read()
count = 0
while success:
  cv2.imwrite("frames/frame%d.jpg" % count, image)     # save frame as JPEG file
  success,image = vidcap.read()
  print('Read a new frame: ', success)
  count += 1
