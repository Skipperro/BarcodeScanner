import cv2
import time
import os
from pyzbar import pyzbar
import simplejson as json

cap = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_PLAIN
cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
cap.set(cv2.CAP_PROP_FOCUS, 100)
cap.set(3, 1280)
cap.set(4, 1024)

lastprinted = time.time()

while True:

    _, frame = cap.read()

    #framegray = frame[500:500+80]
    framegray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #thresh, framegray = cv2.threshold(framegray, 150, 255, cv2.THRESH_BINARY)

    decodedObjects = pyzbar.decode(framegray)

    for obj in decodedObjects:
        #print("Data", obj.data)
        (x, y, w, h) = obj.rect
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 5)
        #cv2.putText(frame, str(obj.data), (50, 50), font, 2, (255, 0, 0), 3)
        barcodeData = obj.data.decode('utf-8')
        barcodeType = obj.type
        text = "{} ( {} )".format(barcodeData, barcodeType)
        cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_DUPLEX, 0.8, (0, 0, 255), 2)
    if lastprinted + 1 < time.time():
        os.system('clear')
        enc = json.dumps(decodedObjects, sort_keys=True, indent=4 * ' ')
        #print("Information : \n Found Type : {} Barcode : {}".format(barcodeType, barcodeData))
        print(enc)
        lastprinted = time.time()

    cv2.imshow("Webcam Preview", frame)

    key = cv2.waitKey(1)
    if key == 27:
        break
cap.release()
cv2.destroyAllWindows()