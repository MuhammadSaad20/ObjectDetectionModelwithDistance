import cv2
import numpy as np

def nothing(x):
    pass

cap = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_COMPLEX                ##Font style for writing text on video frame
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)        ##Set camera resolution
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
Kernal = np.ones((3, 3), np.uint8)

while(1):
    ret, frame = cap.read()         ##Read image frame
    frame = cv2.flip(frame, +1)     ##Mirror image frame
    if not ret:                     ##If frame is not read then exit
        break
    if cv2.waitKey(1) == ord('s'):  ##While loop exit condition
        break
    frame2 = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)         ##BGR to HSV
    lb = np.array([28, 79, 120])
    ub = np.array([255, 248, 233])

    mask = cv2.inRange(frame2, lb, ub)                      ##Create Mask
    cv2.imshow('Masked Image', mask)

    opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, Kernal)        ##Morphology
    cv2.imshow('Opening', opening)

    res = cv2.bitwise_and(frame, frame, mask= opening)             ##Apply mask on original image
    cv2.imshow('Resuting Image', res)

    contours, hierarchy = cv2.findContours(opening, cv2.RETR_TREE,      ##Find contours
                                           cv2.CHAIN_APPROX_NONE)

    if len(contours) != 0:
        cnt = contours[0]
        M = cv2.moments(cnt)
        Cx = int(M['m10']/M['m00'])
        Cy = int(M['m01'] / M['m00'])
        area = cv2.contourArea(cnt)

        #y = 1E-09x(square) - 0.0006x + 80.506

        distance = 1 * (10**(-9)) * (area**2) - (0.0006 * area) + 80.506
        S = 'Dist. Of Object: ' + str(distance)
        if distance >= 55:

            S = 'Dist. Of Object: ' + str(distance) + ' No problem have a safe Joureny.'
            #S = 'Location of object:' + '(' + str(Cx) + ',' + str(Cy) + ')'
            cv2.putText(frame, S, (5, 50), font, 1, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.drawContours(frame, cnt, -1, (5, 24, 2), 6)
        elif(distance<55):

            S = 'Dist. Of Object: ' + str(distance) + ' Accident Warning!'
            # S = 'Location of object:' + '(' + str(Cx) + ',' + str(Cy) + ')'
            cv2.putText(frame, S, (5, 50), font, 1, (0, 0, 255), 2, cv2.LINE_AA)
            cv2.drawContours(frame, cnt, -1, (5, 24, 2), 6)

        ##Lets Detect a red ball
    cv2.imshow('Original Image', frame)

cap.release()                   ##Release memory
cv2.destroyAllWindows()         ##Close all the windows