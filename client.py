import cv2
import time
import os
from pyzbar import pyzbar
import simplejson as json
import requests

cap = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_PLAIN
cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
cap.set(cv2.CAP_PROP_FOCUS, 100)
cap.set(3, 1280)
cap.set(4, 1024)
cap.set(cv2.CAP_PROP_FPS, 60)

lastprinted = time.time()

while True:
    start = time.time()
    _, frame = cap.read()

    cv2.imwrite('frame.jpg', frame)
    with open('frame.jpg', 'rb') as f:
        r = requests.post('http://localhost:5000/barcode', files={'image': f})
    response = json.loads(r.content)
    for obj in response['barcodes']:
        x = obj['rect']['left']
        y= obj['rect']['top']
        w = obj['rect']['width']
        h = obj['rect']['height']
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 5)
        text = "{} ( {} )".format(obj['data'], obj['type'])
        cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_DUPLEX, 0.8, (0, 0, 255), 2)

    cv2.putText(frame,
                "Server-side: " + str(response['time_ms']) + " ms",
                (0, 50), cv2.FONT_HERSHEY_DUPLEX, 0.8, (0, 0, 0), 2)
    timems = int((time.time() - start) * 1000)
    cv2.putText(frame, "FPS: " + str(int(1000/timems)), (0, 25), cv2.FONT_HERSHEY_DUPLEX, 0.8, (0, 0, 0),
                2)
    cv2.imshow("Webcam Preview", frame)
    os.remove('frame.jpg')
    #print(json.loads(r.content))

    #print(timems)

    key = cv2.waitKey(1)
    if key == 27:
        break
cap.release()
cv2.destroyAllWindows()