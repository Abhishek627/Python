import zlib,base64

with open('/Users/shabhishek/Desktop/oc-device_bkp.json','r') as f:
    data=f.read()
S = zlib.compress(base64.b64encode(zlib.compress(data,9)))

with open("/Users/shabhishek/Desktop/temp.zlib", "wb") as myfile:
    myfile.write(S)

# with open("/Users/shabhishek/Desktop/temp.json", "wb") as myfile:
#     myfile.write(base64.b64encode(zlib.compress(data,9)))