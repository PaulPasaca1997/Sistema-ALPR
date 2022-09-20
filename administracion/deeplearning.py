from imutils.video import VideoStream
import imutils
import cv2
import os
import urllib.request
import numpy as np
from django.conf import settings
from tensorflow.keras.preprocessing.image import load_img,load_img, img_to_array
import tensorflow as tf
import pytesseract as pt

model = tf.keras.models.load_model(
    'D:/ALPR/administracion/cnn.h5')

class VideoCamera(object):
	def __init__(self):
		self.video = cv2.VideoCapture(0)

	def __del__(self):
		self.video.release()

	def get_frame(self):
		cap = cv2.VideoCapture(0)
		cap.set(cv2.CAP_PROP_FRAME_WIDTH,2560)
		cap.set(cv2.CAP_PROP_FRAME_HEIGHT,1440)
  
		ret,frame = cap.read()
		cv2.imwrite ('D:/ALPR/administracion/static/upload/fotoPrueba.jpg', frame)
		cap.release()
        
        
"""
        success, image = self.video.read()
        frame_flip = cv2.flip(image, 1)
        cv2.imwrite("D:ALPR/administracion/static/upload/lenaGuardada.jpeg",image)
        cv2.waitKey(0)
        ret, jpeg = cv2.imencode('.jpg', frame_flip)
        return jpeg.tobytes()
"""


class IPWebCam(object):
    def __init__(self):
        self.url = "http://192.168.100.3:8080/shot.jpg"


    def __del__(self):
        cv2.destroyAllWindows()

    def get_frame(self):
        imgResp = urllib.request.urlopen(self.url)
        imgNp = np.array(bytearray(imgResp.read()), dtype=np.uint8)
        img = cv2.imdecode(imgNp, -1)
        img =cv2.resize(img, (640, 480))
        frame_flip = cv2.flip(img, 1)
        ret, jpeg = cv2.imencode('.jpg', frame_flip)
        return jpeg.tobytes()

def object_detection(path, filename):
    # Read image
    image = load_img(path)  # PIL object
    image = np.array(image, dtype=np.uint8)  # 8 bit array (0,255)
    image1 = load_img(path, target_size=(224, 224))
    # Data preprocessing
    # Convert into array and get the normalized output
    image_arr_224 = img_to_array(image1)/255.0
    h, w, d = image.shape
    test_arr = image_arr_224.reshape(1, 224, 224, 3)
    # Make predictions
    coords = model.predict(test_arr)
    # Denormalize the values
    denorm = np.array([w, w, h, h])
    coords = coords * denorm
    coords = coords.astype(np.int32)
    # Draw bounding on top the image
    xmin, xmax, ymin, ymax = coords[0]
    pt1 = (xmin, ymin)
    pt2 = (xmax, ymax)
    print(pt1, pt2)
    cv2.rectangle(image, pt1, pt2, (0, 255, 0), 3)
    # Convert into bgr
    image_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    cv2.imwrite(
        'D:/ALPR/administracion/static/predict/{}'.format(filename), image_bgr)
    return coords

def save_text(filename, text):
    name, ext = os.path.splitext(filename)
    with open('D:/ALPR/administracion/static/predict/{}.txt'.format(name), mode='w') as f:
        f.write(text)
    f.close()


def OCR(path, filename):
    img = np.array(load_img(path))
    cods = object_detection(path, filename)
    xmin, xmax, ymin, ymax = cods[0]
    roi = img[ymin:ymax, xmin:xmax]
    roi_bgr = cv2.cvtColor(roi, cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(roi_bgr, cv2.COLOR_BGR2GRAY)
    magic_color = apply_brightness_contrast(gray, brightness=40, contrast=70)
    cv2.imwrite('D:/ALPR/administracion/static/roi/{}'.format(filename), roi_bgr)
    
    text = pt.image_to_string(magic_color, lang='eng', config='--psm 6')
    print(text)
    save_text(filename, text)
    return text

def apply_brightness_contrast(input_img, brightness=0, contrast=0):

    if brightness != 0:
        if brightness > 0:
            shadow = brightness
            highlight = 255
        else:
            shadow = 0
            highlight = 255 + brightness
        alpha_b = (highlight - shadow)/255
        gamma_b = shadow

        buf = cv2.addWeighted(input_img, alpha_b, input_img, 0, gamma_b)
    else:
        buf = input_img.copy()

    if contrast != 0:
        f = 131*(contrast + 127)/(127*(131-contrast))
        alpha_c = f
        gamma_c = 127*(1-f)

        buf = cv2.addWeighted(buf, alpha_c, buf, 0, gamma_c)

    return buf
