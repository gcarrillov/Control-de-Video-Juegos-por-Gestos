import cv2
import imutils
import numpy as np
import time
from control import Control as c
from sklearn.metrics import pairwise

cap = cv2.VideoCapture(0)

def nothing(x):
    pass

cv2.namedWindow('Control Gestos - Videojuegos')
cv2.namedWindow('Mask')

cv2.createTrackbar('H', 'Mask', 0, 255, nothing)
cv2.createTrackbar('S', 'Mask', 0, 255, nothing)
cv2.createTrackbar('V', 'Mask', 0, 255, nothing)
cv2.createTrackbar('Start', 'Mask', 0, 1, nothing)

top, right, bottom, left = 0, 700, 525, 240  # ROI igual al original

ob = c()

while True:
    try:
        _, frame = cap.read()
        frame = imutils.resize(frame, width=700)
        frame = cv2.flip(frame, 1)
        roi = frame[top:bottom, left:right]

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

        # Preprocesamiento optimizado para luz fuerte
        blurred = cv2.GaussianBlur(roi, (7, 7), 0)  # Blur más fuerte para reducir ruido de luz
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

        h = cv2.getTrackbarPos('H', 'Mask')
        s = cv2.getTrackbarPos('S', 'Mask')
        v = cv2.getTrackbarPos('V', 'Mask')
        start = cv2.getTrackbarPos('Start', 'Mask')

        lower_skin = np.array([h, s, v])
        upper_skin = np.array([255, 255, 255])
        mask = cv2.inRange(hsv, lower_skin, upper_skin)

        # Mejora para luz fuerte: más apertura y dilatación
        kernel = np.ones((5,5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=2)
        mask = cv2.dilate(mask, kernel, iterations=3)

        cv2.imshow('Mask', mask)

        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            cnt = max(contours, key=lambda x: cv2.contourArea(x))
            epsilon = 0.0005 * cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, epsilon, True)
            hull = cv2.convexHull(approx)

            cv2.drawContours(roi, [hull], -1, (0, 255, 0), 2)

            extreme_top = tuple(hull[hull[:, :, 1].argmin()][0])
            extreme_bottom = tuple(hull[hull[:, :, 1].argmax()][0])
            extreme_left = tuple(hull[hull[:, :, 0].argmin()][0])
            extreme_right = tuple(hull[hull[:, :, 0].argmax()][0])

            cX = int((extreme_left[0] + extreme_right[0]) / 2)
            cY = int((extreme_top[1] + extreme_bottom[1]) / 2)

            cv2.circle(roi, (cX, cY), 5, (255, 0, 0), 3)
            cv2.circle(roi, extreme_left, 3, (0, 0, 255), 2)
            cv2.circle(roi, extreme_right, 3, (0, 0, 255), 2)

            distances = pairwise.euclidean_distances([(cX, cY)], [extreme_left, extreme_right])[0]
            max_distance = distances.max()

            x1, y1 = extreme_left
            x2, y2 = extreme_right
            if x2 - x1 != 0:
                slope = (y2 - y1) / (x2 - x1)
            else:
                slope = 0

            # Mostrar info
            cv2.putText(frame, f"Distancia: {int(max_distance)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, f"Slope: {slope:.2f}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

            if start > 0:
                direction = "Centro"
                if slope > 0.2:
                    direction = "Derecha"
                elif slope < -0.2:
                    direction = "Izquierda"

                if max_distance > 180:  # Mano abierta → W constante
                    ob.control('W', direction)
                elif max_distance < 120:  # Mano cerrada → S constante
                    ob.control('S', direction)
                elif 140 < max_distance < 180:  # Aprox 2 dedos (paz) → W toque
                    ob.control('W', direction, hold=False)
                elif 120 < max_distance < 140:  # 4 dedos → S toque
                    ob.control('S', direction, hold=False)

        cv2.imshow('Control Gestos - Videojuegos', frame)

    except:
        pass

    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()