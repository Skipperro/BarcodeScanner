import cv2
import time
import simplejson as json
import requests
import threading
import numpy as np

cap = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_PLAIN
cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
cap.set(cv2.CAP_PROP_FOCUS, 100)
cap.set(3, 1280)
cap.set(4, 720)
cap.set(cv2.CAP_PROP_FPS, 60)

serverIP = "52.29.176.28"
#serverIP = "127.0.0.1"

last_update = time.time()
last_time = 0.0

def update_detection():
    global original_frame, response, last_time, last_update
    if original_frame is None:
        return
    image = cv2.cvtColor(original_frame, cv2.COLOR_BGR2GRAY)
    image -= image.min()
    image = np.array(image * 255.0/image.max(), dtype='uint8')
    fileID = "frame.jpg"
    cv2.imwrite(fileID, image, [cv2.IMWRITE_JPEG_QUALITY, 70])
    with open(fileID, 'rb') as f:
        r = requests.post('http://' + serverIP + ':5000/barcode', files={'frame': f})
    response = json.loads(r.content)
    if len(response['barcodes']) > 0:
        for code in response['barcodes']:
            print("Information : \n Found Type : {} Barcode : {}".format(code['type'], code['data']))
        #time.sleep(2)
    last_time = time.time() - last_update
    last_update = time.time()

lastprinted = time.time()

original_frame = None
current_frame = None
response = None
updater = threading.Thread(target=update_detection)
lastframe = 0.0

def process_frame():
    global current_frame, original_frame, response, lastframe, last_time
    _, current_frame = cap.read()
    original_frame = np.array(current_frame)
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
                    "Round-Trip: " + str(int(last_time * 1000)) + " ms",
                    (3, 50), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 2)

        wcfps = cap.get(cv2.CAP_PROP_FPS)
        cv2.putText(current_frame, "Webcam FPS: " + str(wcfps), (3, 25), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255),
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
cap.set(cv2.CAP_PROP_AUTOFOCUS, 1)
cap.set(3, 1920)
cap.set(4, 1080)
cap.release()
cv2.destroyAllWindows()