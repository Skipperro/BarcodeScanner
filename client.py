import cv2
import time
import os
from pyzbar import pyzbar
import simplejson as json
import requests
import threading
import random

cap = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_PLAIN
cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
cap.set(cv2.CAP_PROP_FOCUS, 100)
cap.set(3, 1280)
cap.set(4, 1024)

def update_detection():
    pass

lastprinted = time.time()

current_frame = None
response = None
updater = threading.Thread(target=update_detection)

def process_frame():
    global current_frame, response
    start = time.time()
    _, frame = cap.read()
    current_frame = frame
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    fileID = str(random.randint(0, 100000)) + ".jpg"
    cv2.imwrite(fileID, image, [cv2.IMWRITE_JPEG_QUALITY, 50])
    with open(fileID, 'rb') as f:
        r = requests.post('http://52.29.176.28:5000/barcode', files={'image': f})
    response = json.loads(r.content)
    os.remove(fileID)
    for obj in response['barcodes']:
        x = obj['rect']['left']
        y = obj['rect']['top']
        w = obj['rect']['width']
        h = obj['rect']['height']
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 5)
        text = "{} ( {} )".format(obj['data'], obj['type'])
        cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_DUPLEX, 0.8, (0, 0, 255), 2)

    cv2.putText(frame,
                "Server-side: " + str(response['time_ms']) + " ms",
                (0, 50), cv2.FONT_HERSHEY_DUPLEX, 0.8, (0, 0, 0), 2)
    timems = int((time.time() - start) * 1000)
    cv2.putText(frame, "FPS: " + str(int(1000 / timems)), (0, 25), cv2.FONT_HERSHEY_DUPLEX, 0.8, (0, 0, 0),
                2)
    current_frame = frame

def main():
    while True:
        #time.sleep(0.05)
        #th = threading.Thread(target=process_frame)
        #th.start()
        process_frame()
        if not current_frame is None:
            cv2.imshow("Webcam Preview", current_frame)
        #os.remove('frame.jpg')
        #print(json.loads(r.content))

        #print(timems)

        key = cv2.waitKey(1)
        if key == 27:
            break

main()

cap.release()
cv2.destroyAllWindows()