# BarcodeScanner

## Server installation

For installation on standard Ubuntu AWS Server with "ubuntu" user.

1. Clone repository.
2. Copy service script and make it executable.
3. Update service config.
4. Start service.
5. Check if service is running.

```
git clone https://github.com/Skipperro/BarcodeScanner.git
sudo cp /home/ubuntu/BarcodeScanner/barcodes /etc/init.d/barcodes
sudo chmod +x /etc/init.d/barcodes
sudo update-rc.d barcodes defaults
sudo service barcodes start
sudo service barcodes status
```

## Example of HTML page for sending a request

Important! File input must have "image" set as its name!
```html
<html>
   <body>
      <form action = "/barcode" method = "POST"
         enctype = "multipart/form-data">
         <input type = "file" name = "image" />
         <input type = "submit"/>
      </form>   
   </body>
</html>
```

## Example of JSON response
```json
{
   "code":200,
   "time_ms":126,
   "barcodes":[
      {
         "data":"HTTP://QR.NESTLE.DE/THOMY39",
         "type":"QRCODE",
         "rect":{
            "left":604,
            "top":239,
            "width":248,
            "height":223
         },
         "polygon":[
            {
               "x":604,
               "y":460
            },
            {
               "x":836,
               "y":462
            },
            {
               "x":852,
               "y":239
            },
            {
               "x":607,
               "y":240
            }
         ]
      },
      {
         "data":"4005500087052",
         "type":"EAN13",
         "rect":{
            "left":201,
            "top":240,
            "width":330,
            "height":157
         },
         "polygon":[
            {
               "x":201,
               "y":241
            },
            {
               "x":202,
               "y":293
            },
            {
               "x":203,
               "y":317
            },
            {
               "x":204,
               "y":339
            },
            {
               "x":205,
               "y":355
            },
            {
               "x":207,
               "y":385
            },
            {
               "x":208,
               "y":395
            },
            {
               "x":209,
               "y":397
            },
            {
               "x":364,
               "y":397
            },
            {
               "x":531,
               "y":396
            },
            {
               "x":531,
               "y":240
            }
         ]
      }
   ]
}
```
