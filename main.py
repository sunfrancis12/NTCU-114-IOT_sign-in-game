import cv2
import mediapipe as mp
import math
import time
import threading
from memory_game import MemoryGame

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

# pyinstaller --add-data "C:\Users\USER\AppData\Local\Programs\Python\Python310\Lib\site-packages\mediapipe;mediapipe/" YOURSCRIPT.py
#pyinstaller --add-data "C:\Users\sunfr\OneDrive\文件\GitHub\NTCU-114-IOT_sign-in-game\NTCU-114-IOT\Lib\site-packages\mediapipe/main.py"

# 根據兩點的座標，計算角度
def vector_2d_angle(v1, v2):
    v1_x = v1[0]
    v1_y = v1[1]
    v2_x = v2[0]
    v2_y = v2[1]
    try:
        angle_= math.degrees(math.acos((v1_x*v2_x+v1_y*v2_y)/(((v1_x**2+v1_y**2)**0.5)*((v2_x**2+v2_y**2)**0.5))))
    except:
        angle_ = 180
    return angle_

# 根據傳入的 21 個節點座標，得到該手指的角度
def hand_angle(hand_):
    angle_list = []
    # thumb 大拇指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0])- int(hand_[2][0])),(int(hand_[0][1])-int(hand_[2][1]))),
        ((int(hand_[3][0])- int(hand_[4][0])),(int(hand_[3][1])- int(hand_[4][1])))
        )
    angle_list.append(angle_)
    # index 食指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0])-int(hand_[6][0])),(int(hand_[0][1])- int(hand_[6][1]))),
        ((int(hand_[7][0])- int(hand_[8][0])),(int(hand_[7][1])- int(hand_[8][1])))
        )
    angle_list.append(angle_)
    # middle 中指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0])- int(hand_[10][0])),(int(hand_[0][1])- int(hand_[10][1]))),
        ((int(hand_[11][0])- int(hand_[12][0])),(int(hand_[11][1])- int(hand_[12][1])))
        )
    angle_list.append(angle_)
    # ring 無名指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0])- int(hand_[14][0])),(int(hand_[0][1])- int(hand_[14][1]))),
        ((int(hand_[15][0])- int(hand_[16][0])),(int(hand_[15][1])- int(hand_[16][1])))
        )
    angle_list.append(angle_)
    # pink 小拇指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0])- int(hand_[18][0])),(int(hand_[0][1])- int(hand_[18][1]))),
        ((int(hand_[19][0])- int(hand_[20][0])),(int(hand_[19][1])- int(hand_[20][1])))
        )
    angle_list.append(angle_)
    return angle_list

# 根據手指角度的串列內容，返回對應的手勢名稱
def hand_pos(finger_angle):
    f1 = finger_angle[0]   # 大拇指角度
    f2 = finger_angle[1]   # 食指角度
    f3 = finger_angle[2]   # 中指角度
    f4 = finger_angle[3]   # 無名指角度
    f5 = finger_angle[4]   # 小拇指角度

    # 小於 50 表示手指伸直，大於等於 50 表示手指捲縮
    if f1<50 and f2>=50 and f3>=50 and f4>=50 and f5>=50:
        return 'good'
    elif f1>=50 and f2>=50 and f3<50 and f4>=50 and f5>=50:
        return 'no!!!'
    elif f1<50 and f2<50 and f3>=50 and f4>=50 and f5<50:
        return 'ROCK!'
    elif f1>=50 and f2>=50 and f3>=50 and f4>=50 and f5>=50:
        return '0'
    elif f1>=50 and f2>=50 and f3>=50 and f4>=50 and f5<50:
        return 'pink'
    elif f1>=50 and f2<50 and f3>=50 and f4>=50 and f5>=50:
        return '1'
    elif f1>=50 and f2<50 and f3<50 and f4>=50 and f5>=50:
        return '2'
    elif f1>=50 and f2>=50 and f3<50 and f4<50 and f5<50:
        return 'ok'
    elif f1<50 and f2>=50 and f3<50 and f4<50 and f5<50:
        return 'ok'
    elif f1>=50 and f2<50 and f3<50 and f4<50 and f5>50:
        return '3'
    elif f1>=50 and f2<50 and f3<50 and f4<50 and f5<50:
        return '4'
    elif f1<50 and f2<50 and f3<50 and f4<50 and f5<50:
        return '5'
    elif f1<50 and f2>=50 and f3>=50 and f4>=50 and f5<50:
        return '6'
    elif f1<50 and f2<50 and f3>=50 and f4>=50 and f5>=50:
        return '7'
    elif f1<50 and f2<50 and f3<50 and f4>=50 and f5>=50:
        return '8'
    elif f1<50 and f2<50 and f3<50 and f4<50 and f5>=50:
        return '9'
    else:
        return ''



cap = cv2.VideoCapture(0)            # 讀取攝影機
fontFace = cv2.FONT_HERSHEY_SIMPLEX  # 印出文字的字型
lineType = cv2.LINE_AA               # 印出文字的邊框
font = cv2.FONT_HERSHEY_SIMPLEX

# 引入遊戲
game = MemoryGame()
text = "" #當前的手勢

#每隔一秒鐘，讀取使用者手勢並輸入
last_gesture = None
last_change_time = time.time()
handled_gesture = False
input_interval = 1.0  # 每 1 秒讀取一次穩定手勢

def process_gesture(gesture):
    global last_gesture, last_change_time, handled_gesture

    now = time.time()
    cv2.putText(frame, f"Next input comes in:{(now - last_change_time):.1f}", (50, 150), font, 0.9, (200, 200, 255), 2)
    if(now - last_change_time >= input_interval): #not handled_gesture and 
        print(f"✅ 輸入手勢：{gesture}")
        game.handle_input(int(text))
        last_change_time = now
    # if gesture != last_gesture:
    #     last_gesture = gesture
    #     last_change_time = now
    #     handled_gesture = False
    # else:
    #     if(now - last_change_time >= input_interval): #not handled_gesture and 
    #         print(f"✅ 輸入手勢：{gesture}")
    #         game.handle_input(int(text))
    #         handled_gesture = True  # 不再重複讀取同個手勢


# mediapipe 啟用偵測手掌
with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:

    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    w, h = 1080, 720                                  # 影像尺寸
    while True:
        ret, frame = cap.read()
        frame = cv2.resize(frame, (w,h))                 # 縮小尺寸，加快處理效率
        if not ret:
            print("Cannot receive frame")
            break
        
        game.update()

        img2 = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # 轉換成 RGB 色彩
        results = hands.process(img2)                # 偵測手勢
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                finger_points = []                   # 記錄手指節點座標的串列
                for i in hand_landmarks.landmark:
                    # 將 21 個節點換算成座標，記錄到 finger_points
                    x = i.x*w
                    y = i.y*h
                    finger_points.append((x,y))
                if finger_points:
                    finger_angle = hand_angle(finger_points) # 計算手指角度，回傳長度為 5 的串列
                    #print(finger_angle)                     # 印出角度 ( 有需要就開啟註解 )
                    
                    text = hand_pos(finger_angle)            # 取得手勢所回傳的內容
        
        cv2.putText(frame, text, (800,120), fontFace, 5, (0,0,255), 10, lineType) # 印出當前手勢
        
        #比OK即開始遊戲
        if game.status == 'waiting':
            cv2.putText(frame, "Waiting the game to start", (50, 50), font, 0.9, (0, 255, 255), 2)
            cv2.putText(frame, f"Show ok to start the game", (50, 100), font, 0.9, (255, 255, 0), 2)
            if text == "ok":
                game.start()
                
        if game.status == 'showing':
            cv2.putText(frame, "remember this five number:", (50, 50), font, 0.9, (0, 255, 255), 2)
            cv2.putText(frame, ' '.join(map(str, game.answer)), (50, 100), font, 1.2, (0, 255, 0), 3)
            sec = 3 - int(time.time() - game.display_start)
            cv2.putText(frame, f"You still have {sec} second to remember...", (50, 150), font, 0.8, (255, 0, 0), 2)

        elif game.status == 'playing':
            cv2.putText(frame, f"Time left: {game.time_left():.1f}s", (50, 50), font, 0.9, (0, 255, 0), 2)
            cv2.putText(frame, f"Your input: {' '.join(map(str, game.user_input))}", (50, 100), font, 0.9, (255, 255, 0), 2)

        elif game.status == 'win':
            cv2.putText(frame, "You win", (100, 100), font, 1.0, (0, 255, 0), 3)
            cv2.putText(frame, f"User has successfully sign-in", (50, 150), font, 0.9, (200, 200, 255), 2)

        elif game.status == 'fail':
            cv2.putText(frame, "You lose", (50, 100), font, 1.0, (0, 0, 255), 3)
            cv2.putText(frame, f"Answer: {' '.join(map(str, game.answer))}", (50, 150), font, 0.8, (0, 255, 255), 2)
        
        
        key = cv2.waitKey(30) & 0xFF
        if key == ord('q'):
            break
        elif game.status == 'playing':
            if text in ['1','2','3','4','5']:
                process_gesture(text)
                #game.handle_input(int(text)
        
        cv2.imshow('sign-in-game', frame)
cap.release()
cv2.destroyAllWindows()