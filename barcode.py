from pyzbar import pyzbar
import cv2

for i in range(24):
    image = cv2.imread('imgs/'+ str(i+1) +'.jpg')
    barcodes = pyzbar.decode(image)
    for barcode in barcodes:
        (x, y, w, h) = barcode.rect
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 5)

        barcodeData = barcode.data.decode('utf-8')
        barcodeType = barcode.type
        text = "{} ( {} )".format(barcodeData, barcodeType)
        cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_DUPLEX, 0.8, (0, 0, 255), 2)

        print("Information : \n Found Type : {} Barcode : {}".format(barcodeType, barcodeData))

    cv2.imshow("Image", image)
    cv2.waitKey(0)