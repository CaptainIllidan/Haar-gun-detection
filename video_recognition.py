import numpy as np
import cv2
import imutils
import datetime

gun_cascade = cv2.CascadeClassifier('cascade.xml')
camera = cv2.VideoCapture('data/gun4_2.mp4')
outputFile = "out.avi"

# initialize the first frame in the video stream
firstFrame = None

# loop over the frames of the video

gun_exist = False

vid_writer = cv2.VideoWriter(outputFile, cv2.VideoWriter_fourcc('M','J','P','G'), 30, (round(camera.get(cv2.CAP_PROP_FRAME_WIDTH)),round(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))))

while True:
    (grabbed, frame) = camera.read()

    # if the frame could not be grabbed, then we have reached the end of the video
    if not grabbed:
        break

    # resize the frame, convert it to grayscale, and blur it
    frame = imutils.resize(frame, width=500)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
    
    gun = gun_cascade.detectMultiScale(gray, 1.3, 5, minSize = (100, 100))
    
    if len(gun) > 0:
        gun_exist = True
        
    for (x,y,w,h) in gun:
        frame = cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]    

    # if the first frame is None, initialize it
    if firstFrame is None:
        firstFrame = gray
        continue

    # draw the text and timestamp on the frame
    cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                    (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

					
    vid_writer.write(frame.astype(np.uint8))
    # show the frame and record if the user presses a key
    cv2.imshow("Security Feed", frame)
    key = cv2.waitKey(1) & 0xFF

if gun_exist:
    print("guns detected")
else:
    print("guns NOT detected")

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()






