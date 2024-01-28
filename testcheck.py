from ultralytics import YOLO
import cv2
import math


# start webcam
cap = cv2.VideoCapture(0)

width = 1280
height = 720

cap.set(3, width)
cap.set(4, height)

# model
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
while True:
    success, img = cap.read()
    results = model(img, stream=True)
    # vertical lines
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

                # Class name and details
                org = [x1, y1]
                font = cv2.FONT_HERSHEY_SIMPLEX
                fontScale = 1
                color = (255, 0, 0)
                thickness = 2

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
                                    
                cv2.putText(img, f"{quadrant_num}", org, font, fontScale, color, thickness)
                # if roation_follow == 0 and quadrant_num != 5:
                
    cv2.imshow('Webcam', img)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
