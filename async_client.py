import cv2
import time
import simplejson as json
import requests
import threading
import os

cap = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_PLAIN
cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
cap.set(cv2.CAP_PROP_FOCUS, 100)
cap.set(3, 1280)
cap.set(4, 720)

serverIP = "52.29.176.28"
#serverIP = "127.0.0.1"

def update_detection():
    global original_frame, response
    if original_frame is None:
        return
    image = cv2.cvtColor(original_frame, cv2.COLOR_BGR2GRAY)
    fileID = "frame.jpg"
    cv2.imwrite(fileID, image, [cv2.IMWRITE_JPEG_QUALITY, 80])
    with open(fileID, 'rb') as f:
        r = requests.post('http://' + serverIP + ':5000/barcode', files={'image': f})
    response = json.loads(r.content)
    if len(response['barcodes']) > 0:
        for code in response['barcodes']:
            print("Information : \n Found Type : {} Barcode : {}".format(code['type'], code['data']))
        time.sleep(2)

lastprinted = time.time()

original_frame = None
current_frame = None
response = None
updater = threading.Thread(target=update_detection)

def process_frame():
    global current_frame, original_frame, response
    start = time.time()
    _, current_frame = cap.read()
    _, original_frame = cap.read()
    if not response is None:
        for obj in response['barcodes']:
            x = obj['rect']['left']
            y = obj['rect']['top']
            w = obj['rect']['width']
            h = obj['rect']['height']
            cv2.rectangle(current_frame, (x, y), (x + w, y + h), (0, 0, 255), 5)
            text = "{} ( {} )".format(obj['data'], obj['type'])
            cv2.putText(current_frame, text, (x, y - 10), cv2.FONT_HERSHEY_DUPLEX, 0.8, (0, 0, 255), 2)

        cv2.rectangle(current_frame, (0, 0), (0 + 280, 0 + 40), (0, 0, 0), 50)

        cv2.putText(current_frame,
                    "Server-side: " + str(response['time_ms']) + " ms",
                    (3, 50), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 2)
        timems = int((time.time() - start) * 1000)

        cv2.putText(current_frame, "Webcam FPS: " + str(int(1000 / timems)), (3, 25), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255),
                    2)

def main():
    global updater
    while True:
        if updater.is_alive():
            pass
        else:
            updater = threading.Thread(target=update_detection)
            updater.start()
        process_frame()
        if not current_frame is None:
            cv2.imshow("Webcam Preview", current_frame)

        key = cv2.waitKey(1)
        if key == 27:
            break

main()

cap.release()
cv2.destroyAllWindows()