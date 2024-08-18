import cv2
import numpy as np
from pyzbar.pyzbar import decode
import webbrowser
import time

# 定義解碼器函數
def decoder(image):
    gray_img = cv2.cvtColor(image, 0)       # 將圖像轉換為灰度圖像
    barcode = decode(gray_img)              # 解碼圖像中的條形碼或二維碼

                                            # 遍歷所有解碼出的條形碼或二維碼
    for obj in barcode:
        points = obj.polygon                # 獲取條碼的多邊形頂點坐標
        (x, y, w, h) = obj.rect             # 獲取條碼的矩形區域
        pts = np.array(points, np.int32)    # 將頂點轉換為 numpy 數組
        pts = pts.reshape((-1, 1, 2))       # 調整數組形狀以適應 cv2.polylines
        cv2.polylines(image, [pts], True, (0, 255, 0), 3)  # 在圖像上繪製多邊形，用綠色表示
        barcodeData = obj.data.decode("utf-8")  # 將條形碼數據解碼為字符串
        barcodeType = obj.type                  # 獲取條碼的類型
        string = "Data " + str(barcodeData) + " || Type " + str(barcodeType)  # 創建顯示的字符串
        cv2.putText(frame, string, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)  # 在圖像上顯示數據和類型
        print("barcode: " + barcodeData + " | Type: " + barcodeType)  # 打印條碼數據和類型到控制台
        if barcodeData:                     # 如果成功讀取到條碼數據
            webbrowser.open(barcodeData)    # 打開條碼數據指向的網頁
            time.sleep(3) 

# 開始視頻捕捉
cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()  # 讀取攝像頭的一幀
    decoder(frame)  # 調用解碼器函數
    cv2.imshow("Image", frame)  # 顯示圖像
    code = cv2.waitKey(10)  # 等待按鍵輸入
    if code == ord('q') or cv2.getWindowProperty('Image', cv2.WND_PROP_VISIBLE) < 1:  # 如果按下 'q' 或者窗口關閉
        break  

cap.release()
cv2.destroyAllWindows()