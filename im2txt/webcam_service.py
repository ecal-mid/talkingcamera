from __future__ import print_function

import serial
import grpc
import threading

from im2txt.im2txt import im2txt_pb2
from im2txt.im2txt import im2txt_pb2_grpc

import cv2
from gtts import gTTS
import subprocess
import glob
import sys




btn_clicked = False

# class SerialThread(threading.Thread):
#     def __init__(self):
#         threading.Thread.__init__(self)

#     def run(self):
#         ser = serial.Serial("/dev/ttyACM0")
#         while 1:
#             ser.readline()
#             btn_clicked = True

#SerialThread().start()

ser = serial.Serial("/dev/ttyACM1")

def run():
    running = 1
    cam = cv2.VideoCapture(0)
    cv2.namedWindow("test")

    channel = grpc.insecure_channel('localhost:50051')
    stub = im2txt_pb2_grpc.Im2TxtStub(channel)

    tmp_jpg_filename = '_img_tmp.jpg'
    tmp_mp3_filename = '_mp3_tmp.wav'

    while running == 1:
        try :
            ret, frame = cam.read()
            cv2.imshow("test", frame)

            if not ret:
                break


            k = cv2.waitKey(1)
           

            if ser.inWaiting()>0:
                line = ser.read(ser.inWaiting()).decode('ascii')
            #line = ser.readline()
            
                print(line, end='')
                if len(line) > 0:
                    print("Started recognition")


                    cv2.imwrite(tmp_jpg_filename, frame)
                    with open(tmp_jpg_filename, "r") as f:
                         imageTo = f.read()
                    response = stub.Run(im2txt_pb2.Im2TxtRequest(image=imageTo))
                    print("Response received: " + response.text)

                    tts = gTTS(text=response.text, lang='en')
                    tts.save(tmp_mp3_filename)
                    subprocess.Popen(['mpg123', tmp_mp3_filename]).wait()



    #        if k % 256 == 27:
                # ESC pressed
    #            print("Escape hit, closing...")
    #            break
    #        elif k % 256 == 32:
            #if btn_clicked:
                # SPACE pressed
                # TODO: remove temp storage on harddrive (BytesIO)
               
            
        except KeyboardInterrupt:
            running = 0
            print("Session ended")
            #ser.close()

    

        
    cam.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    print("hi")
    run()



