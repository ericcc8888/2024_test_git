import time
import cv2

def put_cv2_text(image, text, org):
    cv2.putText(
        img=image,
        text=text, 
        org=org, #圖片的像素坐標系,Y軸是反過來的(向下變大)
        fontFace=cv2.FONT_HERSHEY_SIMPLEX, 
        fontScale=1,
        color=(0, 255, 255), 
        thickness=1, 
        lineType=cv2.LINE_AA
    )

def collect_image(folder_path,category_name,camara_id):
    camera = cv2.VideoCapture(camara_id)
    is_collection_start = False #預設不會一開始就蒐集
    while True:
        is_success, frame = camera.read()  # 從camera取得資料
        if is_success:
            # 我想要在這邊可以透過camera蒐集圖片
            show_frame = frame.copy() #copy frame for display
            put_cv2_text(show_frame , f"Collecting:{is_collection_start}" , (30,50))
            put_cv2_text(show_frame , f"Collecting:{category_name}" , (30,100))
            cv2.imshow("Collector", show_frame)
            if is_collection_start:
                image_name = f"{time.time()}.jpg" #我用timestamp
                filename = f"{folder_path}/{category_name}/{image_name}" #組合檔名
                cv2.imwrite(filename, frame)
                key = cv2.waitKey(1000)
            else:
                key = cv2.waitKey(1)
        else:
            print("Wait for camera ready......")
            key = cv2.waitKey(1000)

        if key == ord('q') or key == ord("Q"): # 如果按下'q' or 'Q'
            break
        elif key == ord('a') or key == ord('A'): #開始
            is_collection_start = True
        elif key == ord('z') or key == ord('Z'): #暫停
            is_collection_start = False

cv2.destroyAllWindows() # close all window

if __name__ == "__main__":
    folder_path = 'images/gesture'
    camara_id = 0
    categories_name = ['open_palm' , 'thumb' , 'victory']

    for category_name in categories_name:
        collect_image(folder_path , category_name , camara_id)
    