from flask import Flask, render_template, request
import cv2
import os
from pyzbar import pyzbar
import simplejson as json
import time

app = Flask(__name__)
GlobalFileID = 0

def get_objects_from_image(filename):
    image = cv2.imread(str(filename))
    decodedObjects = pyzbar.decode(image)
    return decodedObjects #json.dumps({"code": 200, decodedObjects})

@app.route('/', methods=['GET','POST'])
def index():
    return render_template('index.html')

@app.route('/test', methods=['GET','POST'])
def test():
    start = time.time()
    objects = get_objects_from_image("test.jpg")
    timems = int((time.time() - start) * 1000)
    return json.dumps({"code": 200, "time_ms": timems, "barcodes": objects})

@app.route('/barcode', methods=['POST'])
def process_post():
    start = time.time()
    global GlobalFileID
    if request.method == 'POST':
        f = request.files['image']
        if GlobalFileID > 100000:
            GlobalFileID = 0
        FileID = GlobalFileID
        f.save(str(FileID))
        objects = get_objects_from_image(str(FileID))
        os.remove(str(FileID))
        timems = int((time.time() - start)*1000)
        return json.dumps({"code":200, "time_ms": timems, "barcodes": objects})


if __name__ == '__main__':
    from waitress import serve
    serve(app, host="0.0.0.0", port=5000)
    #app.run(debug=True)
