from djitellopy import Tello
from ultralytics import YOLO
from tarck import track
from threading import Thread
import cv2
import math
import time

# Image size
width = 1280
height = 720

model = YOLO("yolo-Weights/yolov8n-face.pt")

# object classes
classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
              "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
              "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
              "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
              "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
              "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
              "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
              "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
              "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
              "teddy bear", "hair drier", "toothbrush"
              ]

# 0 means fly and 1 for testing
fight = 0
rotate = 1

me = Tello()
me.connect(wait_for_state=True)

me.for_back_velocity = 0
me.left_right_velocity = 0
me.up_down_velocity = 0
me.yaw_velocity = 0
me.speed = 0

print(me.get_battery)

if fight == 0:
        me.takeoff()
        time.sleep(2)
        me.send_rc_control(0,0,30,0)
        time.sleep(3)
        me.send_rc_control(0,0,0,0)
        fight == 0

me.streamoff()   
me.streamon()
while True:
    img = me.get_frame_read()
    img = img.frame
    img = cv2.resize(img, (width, height))
    
    results = model(img, stream=True)
    
    cv2.line(img, (width//3, 0), (width//3, height), (0, 255, 0), 2)
    cv2.line(img, (2*(width//3), 0), (2*(width//3), height), (0, 255, 0), 2)
    
    cv2.line(img, (0, height//3), (width, height//3), (0, 255, 0), 2)
    cv2.line(img, (0, 2*(height//3)), (width, 2*(height//3)), (0, 255, 0), 2)

    # Check for person detection
    for r in results:
        boxes = r.boxes

        for box in boxes:
            cls = int(box.cls[0])

            # Check if the detected object is a person
            if classNames[cls] == "person":
                # Bounding box
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

                # Calculate center coordinates of the person
                center_person_x = (x1 + x2) // 2
                center_person_y = (y1 + y2) // 2

                # Calculate center coordinates of the screen
                center_screen_x = 1280 // 2
                center_screen_y = 720 // 2

                # Draw a line from the center of the screen to the center of the person
                cv2.line(img, (center_screen_x, center_screen_y), (center_person_x, center_person_y), (0, 255, 0), 2)

                # Confidence
                confidence = math.ceil((box.conf[0] * 100)) / 100

                # Print the quadrant information
                quadrant_num = 0
                
                # 0 means it will rotate to follow you and 1 mean to will fly to follow you
                roation_follow = 0
                
                if(center_person_x <= width//3 and center_person_y >= (height//3)*2):
                    quadrant_num = 1
                elif(center_person_x > width//3 and  center_person_x < 2*(width//3) and center_person_y >= (height//3)*2):
                    quadrant_num = 2
                elif(center_person_x >= 2*(width//3) and center_person_y >= (height//3)*2):
                    quadrant_num = 3
                elif(center_person_x <= width//3 and center_person_y >= (height//3) and center_person_y < (height//3)*2):
                    quadrant_num = 4
                elif(center_person_x > width//3 and  center_person_x < 2*(width//3) and center_person_y >= (height//3) and center_person_y < (height//3)*2):
                    quadrant_num = 5
                elif(center_person_x >= 2*(width//3) and center_person_y >= (height//3) and center_person_y < (height//3)*2):
                    quadrant_num = 6
                elif(center_person_x <= width//3 and center_person_y < (height//3)):
                    quadrant_num = 7
                elif(center_person_x > width//3 and  center_person_x < 2*(width//3) and center_person_y < (height//3)):
                    quadrant_num = 8
                else:
                    quadrant_num = 9
                    
                
                if quadrant_num !=5 and quadrant_num != None and rotate == 0:
                    track.rotate(me = me, qudrant = quadrant_num)
                elif quadrant_num !=5 and quadrant_num != None and rotate == 1:
                    track.follow(me = me, qudrant = quadrant_num)
                else:
                    track.sling_shot(me = me, qudrant = quadrant_num)
                
    cv2.imshow('MyResult', img)
    
        
    if cv2.waitKey(1) & 0xFF == ord('q'):
        me.land()
        break
    
cv2.destroyAllWindows()