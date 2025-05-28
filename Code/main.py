import cv2      
import mediapipe
import serial

cap = cv2.VideoCapture(0)
initHand = mediapipe.solutions.hands  # Initializing mediapipe
# Object of mediapipe with "arguments for the hands module"
mainHand = initHand.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.8)
# Object to draw the connections between each finger index
draw = mediapipe.solutions.drawing_utils
# Outputs the hight and width of the screen (1920 x 1080)


def handLandmarks(colorImg):
    landmarkList = []  # Default values if no landmarks are tracked

    # Object for processing the video input
    landmarkPositions = mainHand.process(colorImg)
    # Stores the out of the processing object (returns False on empty)
    landmarkCheck = landmarkPositions.multi_hand_landmarks
    if landmarkCheck:  # Checks if landmarks are tracked
        for hand in landmarkCheck:  # Landmarks for each hand
            # Loops through the 21 indexes and outputs their landmark coordinates (x, y, & z)
            for index, landmark in enumerate(hand.landmark):
                # Draws each individual index on the hand with connections
                draw.draw_landmarks(img, hand, initHand.HAND_CONNECTIONS)
                h, w, c = img.shape  # Height, width and channel on the image
                # Converts the decimal coordinates relative to the image for each index
                centerX, centerY = int(landmark.x * w), int(landmark.y * h)
                # Adding index and its coordinates to a list
                landmarkList.append([index, centerX, centerY])

    return landmarkList

def fingers(landmarks):
    fingerTips = []  # To store 4 sets of 1s or 0s
    tipIds = [4, 8, 12, 16, 20]  # Indexes for the tips of each finger

    # Check if thumb is up
    if landmarks[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
        fingerTips.append(1)
    else:
        fingerTips.append(0)

    # Check if fingers are up except the thumb
    for id in range(1, 5):
        # Checks to see if the tip of the finger is higher than the joint
        if landmarks[tipIds[id]][2] < landmarks[tipIds[id] - 3][2]:
            fingerTips.append(1)
        else:
            fingerTips.append(0)

    return fingerTips

def connectToRobot(portNo):
    global ser
    try:
        ser = serial.Serial(portNo, 9600)
        print("Robot Connected ")
    except:
        print("Not Connected To Robot ")
        pass

def sendData(fingers):

    string = "$"+str(int(fingers[0]))+str(int(fingers[1]))+str(int(fingers[2]))+str(int(fingers[3]))+str(int(fingers[4]))
    print(string)
    try:
       ser.write(string.encode())
    except:
        pass

portNo = "COM4"
connectToRobot(portNo)

while True:
    check, img = cap.read()  # Reads frames from the camera
    # Changes the format of the frames from BGR to RGB
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    lmList = handLandmarks(imgRGB)
    # cv2.rectangle(img, (75, 75), (640 - 75, 480 - 75), (255, 0, 255), 2)

    if len(lmList) != 0:
        # Gets index 8s x and y values (skips index value because it starts from 1)
        x1, y1 = lmList[5][1:]
        # Gets index 12s x and y values (skips index value because it starts from 1)
        x2, y2 = lmList[12][1:]
        # Calling the fingers function to check which fingers are up
        finger = fingers(lmList)

        # finger 0 = thumb
        # finger 1 = index
        # finger 2 = middle finger
        # print(finger)
        sendData(finger)
        

        cv2.imshow("Webcam", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
