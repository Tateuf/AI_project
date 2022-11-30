import numpy as np
import cv2
from skimage import img_as_ubyte		
from skimage.color import rgb2gray
from keras.models import load_model
import os

model = load_model('testPseudoBestModel.h5')

dico = {}
test_data_dir = "test_images"
sample_dir = "hdig_3-split"
full_dir = test_data_dir +"/"+ sample_dir +"/imageonline/"

for image in os.listdir(full_dir):
    full_path = full_dir + image
    img_original = cv2.imread(test_data_dir +"/"+ sample_dir + "/imageonline/" + image)
    img_gray = rgb2gray(img_original)
    img_gray_u8 = img_as_ubyte(img_gray)
    #cv2.imshow("Window", img_gray_u8)

    #Convert grayscale image to binary
    (thresh, im_binary) = cv2.threshold(img_gray_u8, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    # cv2.imshow("Window", im_binary)
    # cv2.waitKey(0)


    img_resized = cv2.resize(im_binary,(28,28), interpolation=cv2.INTER_AREA)
    # cv2.imshow("Window", img_resized)
    # cv2.waitKey(0)

    #invert image
    im_gray_invert = 255 - img_resized
    #cv2.imshow("invert image", im_gray_invert)

    im_final = im_gray_invert.reshape(1,28,28,1)

    ans = model.predict(im_final)
    ans = np.argmax(ans,axis=1)[0]

    keyform = image.split(".")[0]
    #dico[image] = ans
    dico[keyform] = ans

print(dico)