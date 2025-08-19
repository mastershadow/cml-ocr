import cv2
import pytesseract

image_path = "cene.png"
im = cv2.imread(image_path)
im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
(thresh, im_bw) = cv2.threshold(im_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
print(im_bw.shape)
h = len(im_bw) - 1
w = len(im_bw[0]) - 1

im_temp = im_bw[0:h, 0:160]
im_humid = im_bw[0:h, 200:350]
im_dew = im_bw[0:h, 360:550]
im_rain_tot = im_bw[0:h, 1100:1200]
im_rain_cur = im_bw[0:h, w-260:w]

print(im_rain_cur.shape)

cv2.imwrite("t.png", im_rain_tot)

custom_config = '--psm 13 --oem 3 -c tessedit_char_whitelist=0123456789'

extracted_text = pytesseract.image_to_string(im_rain_tot, lang="eng", config=custom_config)
print(extracted_text)