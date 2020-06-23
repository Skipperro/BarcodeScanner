from flask import Flask, render_template, request
import cv2
import os
from pyzbar import pyzbar
import simplejson as json
import time
import numpy as np
import uuid

app = Flask(__name__)

def get_objects_from_image(filename):
    try:
        image = cv2.imread(str(filename))
        if len(image.shape) > 2:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        if image.min() > 0 or image.max() < 255:
            image -= image.min()
            image = np.array(image * 255.0 / image.max(), dtype='uint8')
        decodedObjects = pyzbar.decode(image,
                                       [pyzbar.ZBarSymbol.CODE128, pyzbar.ZBarSymbol.EAN13, pyzbar.ZBarSymbol.QRCODE])
        return decodedObjects  # json.dumps({"code": 200, decodedObjects})
    except Exception as e:
        print(e)
        return None


@app.route('/', methods=['GET','POST'])
def index():
    return render_template('index.html')

@app.route('/test', methods=['GET','POST'])
def test():
    try:
        start = time.time()
        objects = get_objects_from_image("test.jpg")
        if objects is None:
            return "[]"
        timems = int((time.time() - start) * 1000)
        return json.dumps({"code": 200, "time_ms": timems, "barcodes": objects})
    except Exception as e:
        print(e)
        return "[]"

@app.route('/barcode', methods=['POST'])
def process_post():
    try:
        start = time.time()
        if request.method == 'POST':
            f = list(request.files.values())[0]
            FileID = str(uuid.uuid4())
            f.save('/dev/shm/' + str(FileID))
            objects = get_objects_from_image('/dev/shm/' + str(FileID))
            if objects is None:
                return "[]"
            os.remove('/dev/shm/' + str(FileID))
            timems = int((time.time() - start) * 1000)
            return json.dumps({"uuid": FileID, "time_ms": timems, "barcodes": objects})
    except Exception as e:
        print(e)
        return "[]"



if __name__ == '__main__':
    from waitress import serve
    serve(app, host="0.0.0.0", port=5000)
    #app.run(host='0.0.0.0', debug=True)
