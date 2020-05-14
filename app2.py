import glob

from flask.json import jsonify
import brain_tumor_detection as tumor
import os
import cv2
from flask import Flask, render_template, redirect, url_for, request, send_from_directory
import os
import time
import base64
app2 = Flask(__name__)
imageArr=[]
app2.config['SECRET_KEY'] = 'Thisissupposedtobesecret'
# Bootstrap(app)
LIST=[]
count1=1
TUMOR = []
CLASSIFY = []
NOTUMOR = []
def Decode_image(image_64_encode):
    global count1
    #image = open(r'132.png', 'rb')
    #image_read = image.read()
    #image_64_encode = base64.encodestring(image_read)
    encode_64 = bytes(image_64_encode,'utf-8')
    image_64_decode = base64.decodestring(encode_64)
    image_result = open('New_Images/'+str(count1)+'.png', 'wb')
    # create a writable image and write the decoding result
    image_result.write(image_64_decode)
    img = cv2.imread('New_Images/'+str(count1)+'.png')
    image_result.close()
    try:
        os.remove('New_Images/' + str(count1) + '.png')
    except:
        print("Exception")
    count1 = count1 + 1
    return img
def BASE64(image):
    my_string = base64.b64encode(image)
    return my_string
@app2.route('/')
def index():
    return render_template('index.html')
count=1
Folder="IMAGES"
Path=os.listdir(Folder)
def Load_Images():
    global TUMOR
    global CLASSIFY
    global NOTUMOR
    tumor_='Detection_Images'
    classify_='New_Images'
    No_tumor_='No_Tumor'
    DATA1=os.listdir(tumor_)
    for Image in DATA1:
        TUMOR.append(Image)
    DATA2 = os.listdir(classify_)
    for Image in DATA2:
        CLASSIFY.append(Image)
    DATA3 = os.listdir(No_tumor_)
    for Image in DATA3:
        NOTUMOR.append(Image)

    return TUMOR,CLASSIFY,NOTUMOR

@app2.route('/tumor/<name>', methods=['GET'])
def download1(name):
    app2.config['CLIENT_PNG'] = 'Detection_Images'
    response = send_from_directory(directory=app2.config['CLIENT_PNG'], filename=name, as_attachment=True)
    response.headers['my-custom-header'] = 'my-custom-status-0'
    return response

@app2.route('/classify/<name>', methods=['GET'])
def download2(name):
    app2.config['CLIENT_PNG'] = 'New_Images'
    response = send_from_directory(directory=app2.config['CLIENT_PNG'], filename=name, as_attachment=True)
    response.headers['my-custom-header'] = 'my-custom-status-0'
    return response


@app2.route('/notumor/<name>', methods=['GET'])
def download3(name):
    app2.config['CLIENT_PNG'] = 'No_Tumor'
    response = send_from_directory(directory=app2.config['CLIENT_PNG'], filename=name, as_attachment=True)
    response.headers['my-custom-header'] = 'my-custom-status-0'
    return response

@app2.route('/classify/' , methods=['POST'])
def dashboard():
    global count
    global imageArr
    Detection_Images=glob.glob('Detection_Images/*')
    New_image = glob.glob('New_Images/*')
    No_Tumor = glob.glob('No_Tumor/*')
    for i in range(len(Detection_Images)):
        os.remove(Detection_Images[i])
    for i in range(len(New_image)):
        os.remove(New_image[i])
    for i in range(len(No_Tumor)):
        os.remove(No_Tumor[i])
    recieveImages=str(request.form['image'])
    imageArr = recieveImages.split(',')
    for Image in range(len(imageArr)):
        if len(imageArr[Image])>5:
            New_image = Decode_image(imageArr[Image])
            image=New_image
            ########################################################################################
            Read_Image = image.copy()
            Tumor_Image = image.copy()
            Bool, TUMOR_IMAGE = tumor.Detection_Tumor(image)
            tumorKey=''
            claasify=''
            notumor=''
            if Bool == False:
                font = cv2.FONT_HERSHEY_SIMPLEX
                org = (50, 50)
                fontScale = 1
                color = (102, 205, 0)
                thickness = 2
                cv2.putText(TUMOR_IMAGE, 'Tumor not found', org, font,
                          fontScale, color, thickness, cv2.LINE_AA)
                cv2.imwrite(("No_Tumor/" + (str(count) + '.png')), TUMOR_IMAGE)
                count = count + 1
            elif Bool == True:
                font = cv2.FONT_HERSHEY_SIMPLEX
                org = (50, 50)
                fontScale = 1
                color = (0, 0, 255)
                thickness = 2
                cv2.putText(TUMOR_IMAGE, 'Tumor  Exist', org, font,
                          fontScale, color, thickness, cv2.LINE_AA)
                cv2.imwrite(("Detection_Images/" + (str(count)+'.png')), TUMOR_IMAGE)
                Bool_updated,updated = tumor.Tumor_Detection(Tumor_Image)
                if Bool_updated==True:
                    cv2.imwrite(("New_Images/" + (str(count)+'.png')), updated)
                count = count + 1
    TUMOR1,CLASSIFY1,NOTUMOR1=Load_Images()
    RESPONSE=dict(tumor=TUMOR1, claasify=CLASSIFY1, notumor=NOTUMOR1)
    return jsonify({'response': RESPONSE})
if __name__ == "_main_":

    app2.debug=True
    app2.run(host='0.0.0.0', port=80)
    #Decode_image()