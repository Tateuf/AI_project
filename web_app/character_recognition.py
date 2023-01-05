import numpy as np
import cv2
from skimage import img_as_ubyte		
from skimage.color import rgb2gray
from keras.models import load_model
import pandas as pd
import text_detection
import os

def characterRecognition(img) :
    boxes = text_detection.text_detection(img)
    model = load_model('web_app/emnist_model.h5')
    answer = ""
    i = 0
    for box in boxes:
        img_original = cv2.imread(img)
        x = box[0]
        y = box[1]
        w = box[2]
        h = box[3]
        cropped_image = img_original[y:y+h, x:x+w]
        img_gray = rgb2gray(cropped_image)
        img_gray_u8 = img_as_ubyte(img_gray)
    
        (thresh, im_binary) = cv2.threshold(img_gray_u8, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        img_resized = cv2.resize(im_binary,(28,28), interpolation=cv2.INTER_AREA)

        im_gray_invert = 255 - img_resized

        im_final = im_gray_invert.reshape(1,28,28,1)

        ans = model.predict(im_final)
        ans = np.argmax(ans,axis=1)[0]
        
        label_map = pd.read_csv("web_app/emnist-balanced-mapping.txt", 
                                delimiter = ' ', 
                                index_col=0, 
                                header=None, 
                                squeeze=True)
        
        label_dictionary = {}
        
        for index, label in enumerate(label_map):
            label_dictionary[index] = chr(label)

        answer += "BOX "+ str(i) +" => " + label_dictionary[ans] + ", "
        i += 1
    return answer[:-2]
