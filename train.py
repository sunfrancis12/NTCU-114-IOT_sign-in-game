import cv2
import numpy as np

# 使用 OpenCV 提供的內建 Haar XML
xml_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
detector = cv2.CascadeClassifier(xml_path)

#detector = cv2.CascadeClassifier('xml/haarcascade_frontalface_default.xml')  # 載入人臉追蹤模型
recog = cv2.face.LBPHFaceRecognizer_create()      # 啟用訓練人臉模型方法
faces = []   # 儲存人臉位置大小的串列
ids = []     # 記錄該人臉 id 的串列

for i in range(1,31):
    img = cv2.imread(f'./images/{i}.png')         # 依序開啟每一張川普的照片
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 色彩轉換成黑白
    img_np = np.array(gray,'uint8')               # 轉換成指定編碼的 numpy 陣列
    face = detector.detectMultiScale(gray)        # 擷取人臉區域
    for(x,y,w,h) in face:
        faces.append(img_np[y:y+h,x:x+w])         # 記錄川普人臉的位置和大小內像素的數值
        ids.append(1)                             # 記錄川普人臉對應的 id，只能是整數，都是 1 表示川普的 id 為 1
        
for i in range(1,16):
    img = cv2.imread(f'./images/biden_{i}.png')   # 依序開啟每一張拜登的照片
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 色彩轉換成黑白
    img_np = np.array(gray,'uint8')               # 轉換成指定編碼的 numpy 陣列
    face = detector.detectMultiScale(gray)        # 擷取人臉區域
    for(x,y,w,h) in face:
        faces.append(img_np[y:y+h,x:x+w])         # 記錄川普人臉的位置和大小內像素的數值
        ids.append(2)                             # 記錄拜登人臉對應的 id

print('training...')                              # 提示開始訓練
recog.train(faces,np.array(ids))                  # 開始訓練
recog.save('face.yml')                            # 訓練完成儲存為 face.yml
print('ok!')