import glob
from flask.json import jsonify
import brain_tumor_detection as tumor
import os
import cv2
from flask import Flask, render_template, redirect, url_for, request, send_from_directory
import os
import time
import base64
#from flask_talisman import Talisman
#from flask_ssl import *
#from flask_sslify import SSLify
import uuid
app = Flask(__name__)
#sslify = SSLify(app)
#Talisman(app, content_security_policy=None)
imageArr=[]
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret'
# Bootstrap(app)
LIST=[]
count1=1

def Decode_image(image_64_encode):
    global count1
    encode_64 = bytes(image_64_encode,'utf-8')
    image_64_decode = base64.decodestring(encode_64)
    a=image_64_encode
    image_result = open('Images_New/'+str(count1)+'.jpg', 'wb')
    a=image_result
    b=image_64_encode
    # create a writable image and write the decoding result
    image_result.write(image_64_decode)
    img = cv2.imread('Images_New/'+str(count1)+'.jpg')
    image_result.close()
    try:
        os.remove('Images_New/' + str(count1) + '.jpg')
    except:
        print("Exception")
    count1 = count1 + 1
    return img

def BASE64(image):
    my_string = base64.b64encode(image)
    return my_string
#@ssl_redirect
@app.route('/')
def index():
    return "Its Working well"
count=1
Folder="IMAGES"
Path=os.listdir(Folder)
TUMOR_=[]
CLASSIFY_=[]
NoTumor_=[]
TUMOR_PERCENT=[]
def Load_Images():
    TUMOR = []
    CLASSIFY = []
    NOTUMOR = []
    bilal=0
    is_true="false"
    print("working with the best case")
    tumor_='Detection_Images'
    classify_='New_Images'
    No_tumor_='No_Tumor'
    DATA1=os.listdir(tumor_)
    for Image in DATA1:
        for i in range(len(TUMOR_)):
            if Image==TUMOR_[i]:
              TUMOR.append(Image)
    DATA2 = os.listdir(classify_)
    for Image in DATA2:
        for i in range(len(CLASSIFY_)):
            if Image==CLASSIFY_[i]:
                CLASSIFY.append(Image)
    DATA3 = os.listdir(No_tumor_)
    for Image in DATA3:
        for i in range(len(NoTumor_)):
            if Image == NoTumor_[i]:
                NOTUMOR.append(Image)
    return TUMOR,CLASSIFY,NOTUMOR
#@ssl_redirect
@app.route('/tumor/<name>', methods=['GET'])
def download1(name):
    app.config['CLIENT_PNG'] = 'Detection_Images'
    response = send_from_directory(directory=app.config['CLIENT_PNG'], filename=name, as_attachment=True)
    response.headers['my-custom-header'] = 'my-custom-status-0'
    return response
#@ssl_redirect
@app.route('/classify/<name>', methods=['GET'])
def download2(name):
    app.config['CLIENT_PNG'] = 'New_Images'
    response = send_from_directory(directory=app.config['CLIENT_PNG'], filename=name, as_attachment=True)
    response.headers['my-custom-header'] = 'my-custom-status-0'
    return response
#@ssl_redirect
@app.route('/notumor/<name>', methods=['GET'])
def download3(name):
    app.config['CLIENT_PNG'] = 'No_Tumor'
    response = send_from_directory(directory=app.config['CLIENT_PNG'], filename=name, as_attachment=True)
    response.headers['my-custom-header'] = 'my-custom-status-0'
    return response
#@ssl_redirect
@app.route('/main/' , methods=['POST'])
def dashboard():
    TUMOR_PERCENT=[]
    #global count
    count=1
    global imageArr
    Detection_Images=glob.glob('Detection_Images/*')
    New_image = glob.glob('New_Images/*')
    No_Tumor = glob.glob('No_Tumor/*')
    # for i in range(len(Detection_Images)):
    #     os.remove(Detection_Images[i])
    # for i in range(len(New_image)):
    #     os.remove(New_image[i])
    # for i in range(len(No_Tumor)):
    #     os.remove(No_Tumor[i])
    recieveImages=str(request.form['image'])
    imageArr = recieveImages.split(',')
    for Image in range(len(imageArr)):
        if len(imageArr[Image])>5:
            New_image = Decode_image(imageArr[Image])
            image=New_image
            ########################################################################################
            #Read_Image = image.copy()
            Tumor_Image = image.copy()
            Bool, TUMOR_IMAGE,NAME = tumor.Detection_Tumor(image)
            if len(NAME) > 0:
                LIST_PERCENT_SAVE = []
                for k in range(0, len(NAME)):
                    PERCENT = str(NAME[k])
                    Percent_save = PERCENT.split(":")
                    Tumor_percent = str(Percent_save[1])
                    Tumor_percent_new = Tumor_percent.split("%")
                    LIST_PERCENT_SAVE.append(int(Tumor_percent_new[0]))
                Percent_save_1 = str(max(LIST_PERCENT_SAVE))
                TUMOR_PERCENT.append(Percent_save_1)
            else:
                Percent_save_1 = ""
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
                NUM=uuid.uuid1()
                NoTumor_.append(str(NUM)+'.png')
                cv2.imwrite(("No_Tumor/" + (str(NUM) + '.png')), TUMOR_IMAGE)
                count = count + 1
            elif Bool == True:
                font = cv2.FONT_HERSHEY_SIMPLEX
                org = (50, 50)
                fontScale = 1
                color = (0, 0, 255)
                thickness = 2
                cv2.putText(TUMOR_IMAGE, 'Tumor  Exist', org, font,
                          fontScale, color, thickness, cv2.LINE_AA)
                NUM = uuid.uuid1()
                TUMOR_.append(str(NUM)+'.png')
                cv2.imwrite(("Detection_Images/" + (str(NUM)+'.png')), TUMOR_IMAGE)
                Bool_updated,updated = tumor.Tumor_Detection(Tumor_Image)
                if Bool_updated==True:
                    NUM = uuid.uuid1()
                    CLASSIFY_.append(str(NUM)+'.png')
                    cv2.imwrite(("New_Images/" + (str(NUM)+'.png')), updated)
                count = count + 1
    TUMOR1,CLASSIFY1,NOTUMOR1=Load_Images()
    RESPONSE=dict(tumor=TUMOR1, claasify=CLASSIFY1, notumor=NOTUMOR1,tumorpercent=TUMOR_PERCENT)
    TUMOR_PERCENT = []
    TUMOR_.clear()
    CLASSIFY_.clear()
    NoTumor_.clear()
    return jsonify({'response': RESPONSE})
@app.route('/Breast_Cancer/' , methods=['POST'])
def dashboard1():
    #global count
    count=1
    global imageArr
    global TUMOR_PERCENT_1
    # Detection_Images=glob.glob('/home/tecbeck/mysite/Detection_Images/*')
    # New_image = glob.glob('/home/tecbeck/mysite/New_Images/*')
    # No_Tumor = glob.glob('/home/tecbeck/mysite/No_Tumor/*')
    recieveImages=str(request.form['image'])
    imageArr = recieveImages.split(',')
    for Image in range(len(imageArr)):
        if len(imageArr[Image])>5:
            New_image = Decode_image(imageArr[Image])
            image=New_image
            ########################################################################################
            #Read_Image = image.copy()
            Tumor_Image = image.copy()
            # Bool, TUMOR_IMAGE = tumor.Detection_Tumor(image)
            Bool, TUMOR_IMAGE,NAME = b_tumor.Detection_Tumor(image)
            if len(NAME) > 0 and Bool == True:
                LIST_PERCENT_SAVE = []
                for k in range(0, len(NAME)):
                    PERCENT = str(NAME[k])
                    Percent_save = PERCENT.split(":")
                    Tumor_percent = str(Percent_save[1])
                    Tumor_percent_new = Tumor_percent.split("%")
                    LIST_PERCENT_SAVE.append(int(Tumor_percent_new[0]))
                Percent_save_1 = str(max(LIST_PERCENT_SAVE))
                TUMOR_PERCENT_1.append(Percent_save_1)
            else:
                Percent_save_1 = ""
            tumorKey=''
            claasify=''
            notumor=''
            if Bool == False:
                font = cv2.FONT_HERSHEY_SIMPLEX
                org = (50, 50)
                fontScale = 1
                color = (102, 205, 0)
                thickness = 2
                # cv2.putText(TUMOR_IMAGE, 'Tumor not found', org, font,
                #           fontScale, color, thickness, cv2.LINE_AA)
                NUM=uuid.uuid1()
                NoTumor_.append(str(NUM)+'.png')
                cv2.imwrite(("No_Tumor/" + (str(NUM) + '.png')), TUMOR_IMAGE)
                count = count + 1
            elif Bool == True:
                font = cv2.FONT_HERSHEY_SIMPLEX
                org = (50, 50)
                fontScale = 1
                color = (0, 0, 255)
                thickness = 2
                # cv2.putText(TUMOR_IMAGE, 'Tumor Found', org, font,
                #           fontScale, color, thickness, cv2.LINE_AA)
                NUM = uuid.uuid1()
                TUMOR_.append(str(NUM)+'.png')
                cv2.imwrite(("Detection_Images/" + (str(NUM)+'.png')), TUMOR_IMAGE)
                Bool_updated,updated = b_tumor.Tumor_Detection(Tumor_Image)
                if Bool_updated==True:
                    NUM = uuid.uuid1()
                    CLASSIFY_.append(str(NUM)+'.png')
                     cv2.imwrite(("New_Images/" + (str(NUM)+'.png')), updated)
                count = count + 1
    TUMOR1,CLASSIFY1,NOTUMOR1=Load_Images()
    # RESPONSE=dict(tumor=TUMOR1, claasify=CLASSIFY1, notumor=NOTUMOR1)
    RESPONSE=dict(Cancer=TUMOR1, cancer_claasify=CLASSIFY1, nocancer=NOTUMOR1,cancerpercent=TUMOR_PERCENT_1)
    TUMOR_.clear()
    CLASSIFY_.clear()
    #TUMOR_PERCENT.clear()
    NoTumor_.clear()
    #TUMOR_PERCENT_1.clear()
    return jsonify({'response': RESPONSE})

if __name__ == "__main__":
    app.debug=True
    app.run(host='0.0.0.0', port=80)
    #Decode_image()