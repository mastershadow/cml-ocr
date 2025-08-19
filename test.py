import cv2
import pytesseract

image_path = "cene.png"
im = cv2.imread(image_path)
im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

(thresh, im_bw) = cv2.threshold(im_gray, 0, 255, cv2.THRESH_OTSU)
h,w = im_bw.shape


splits = []
current_split = None
for x in range(0, w):
  has_content = False
  for y in range(0, h):
    if (im_bw[y, x] < 200):
      has_content = True
      break
    
  if has_content:
    if current_split is None:
      current_split = [x]
  else:
    if current_split is not None:
      current_split.append(x - 1)
      splits.append(current_split)
      current_split = None

if current_split is not None:
      current_split.append(x - 1)
      splits.append(current_split)
      current_split = None
      
# find white spaces
thres = 20
whites = []
if splits[0][0] > thres:
  whites.append([0, splits[0][0] - 1])
  
for idx in range(0, len(splits) - 1):
  a = splits[idx]
  b = splits[idx + 1]
  if (b[0] - a[1] > thres):
    whites.append([a[1] + 1, b[0] - 1])
    
if w - splits[len(splits) - 1][1] > thres:
  whites.append([splits[len(splits) - 1][1] + 1, w])
print(whites)

  


im_temp = im_bw[:, 0:160]
im_humid = im_bw[:, 200:350]
im_dew = im_bw[:, 360:550]
im_rain_tot = im_bw[:, 1100:1200]
im_rain_cur = im_bw[:, w-260:w]

custom_config = '--psm 7 --oem 3 -c tessedit_char_whitelist=0123456789'

imgs = [im_temp, im_humid, im_dew, im_rain_tot, im_rain_cur]
for idx, im in enumerate(imgs):
  cv2.imwrite(str(idx) + ".png", im)
  extracted_text = pytesseract.image_to_string(im, lang="eng", config=custom_config)
  print(extracted_text)