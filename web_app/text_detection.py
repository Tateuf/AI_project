import cv2
import numpy as np


def text_detection(img):
    image = cv2.imread("web_app/static/"+img)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (7,7), 0)
    thresh = cv2.threshold(blur, 200, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Create rectangular structuring element and dilate
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (4,4))
    dilate = cv2.dilate(thresh, kernel, iterations=5)

    # Find contours and draw rectangle
    cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    i = 0
    for c in cnts:
        x,y,w,h = cv2.boundingRect(c)
        cropped_image = image[y:y+h, x:x+w]
        cv2.imwrite("web_app/static/cropped/"+str(i)+"_cropped_"+img, cropped_image)
        cv2.rectangle(image, (x, y), (x + w, y + h), (36,255,12), 2)
        cv2.putText(image, str(i), (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
        i += 1
    cv2.imwrite("web_app/labeled/labeled_"+img)
