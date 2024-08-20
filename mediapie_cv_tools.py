import mediapipe as mp
import cv2
from image_collector import put_cv2_text

def init_gesture_recognizer(model_path):
    # 實際上工作的類別
    GestureRecognizer = mp.tasks.vision.GestureRecognizer 
    # 不同模型間都有的基礎設定，eg: 模型路徑
    BaseOptions = mp.tasks.BaseOptions 
    # 工作類別的進階設定，每種模型可能會不同
    GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions 
    # 輸入設定，算是進階設定的一個欄位
    VisionRunningMode = mp.tasks.vision.RunningMode

# 組合你的各種設定
    model_path = 'gesture_recognizer.task'
    with open(model_path , 'rb') as model: #建立檔案與程式碼的通道
        model_file = model.read()

    options = GestureRecognizerOptions(
        base_options=BaseOptions(model_asset_buffer=model_file),
        running_mode=VisionRunningMode.IMAGE)

    return GestureRecognizer.create_from_options(options)

def recognize_gesture(cv2_frame):
    # Load the input image from an image file.
    #mp_image = mp.Image.create_from_file('images/victory.jpg')

    #CV2 frame -> mp.Image
    mp_image = mp.Image(image_format = mp.ImageFormat.SRGB, data = cv2_frame)
    
    # 手勢辨識
    gesture_recognition_result = model.recognize(mp_image)

    top_gesture = gesture_recognition_result.gestures

    if top_gesture:
        top_gesture = top_gesture[0][0]
        print("Top Gesture: ", top_gesture.category_name, top_gesture.score)
        return top_gesture.category_name , top_gesture.score
    else:
        return "None" , 1.0

def reconize_gesture_realtime(model , camera_id):
    camera = cv2.VideoCapture(camera_id)
    is_collection_start = False #預設不會一開始就蒐集
    while True:
        is_success, frame = camera.read()  # 從camera取得資料
        if is_success:
            # 我想要在這邊可以透過camera蒐集圖片
            show_frame = frame.copy() #copy frame for display
            put_cv2_text(show_frame , f"Collecting:{is_collection_start}" , (30,50))
            if is_collection_start:
                #辨識手勢
                top_gesture, score = recognize_gesture(frame)
                put_cv2_text(show_frame , f"Collecting:{top_gesture} - {round(score*100,2)}%" , (30,100))
                key = cv2.waitKey(100)
            else:
                key = cv2.waitKey(1)
            cv2.imshow("Collector", show_frame)
        else:
            print("Wait for camera ready......")
            key = cv2.waitKey(1000)

        if key == ord('q') or key == ord("Q"): # 如果按下'q' or 'Q'
            break
        elif key == ord('a') or key == ord('A'): #開始
            is_collection_start = True
        elif key == ord('z') or key == ord('Z'): #暫停
            is_collection_start = False

def init_face_detector(model_path):
# 實際上工作的類別
    FaceDetector = mp.tasks.vision.FaceDetector
    FaceDetectorOptions = mp.tasks.vision.FaceDetectorOptions
    # 不同模型間都有的基礎設定，eg: 模型路徑
    BaseOptions = mp.tasks.BaseOptions 
    # 輸入設定，算是進階設定的一個欄位
    VisionRunningMode = mp.tasks.vision.RunningMode

# 組合你的各種設定
    model_path = 'blaze_face_short_range.tflite'
    with open(model_path , 'rb') as model: #建立檔案與程式碼的通道
        model_file = model.read()

    options = FaceDetectorOptions(
        base_options=BaseOptions(model_asset_buffer=model_file),
        running_mode=VisionRunningMode.IMAGE)

    return FaceDetector.create_from_options(options)

def detect_face(model, cv2_frame):
    mp_image = mp.Image(image_format = mp.ImageFormat.SRGB, data = cv2_frame)
    face_detector_result = model.detect(mp_image)
    return face_detector_result.detections
    
def detect_face_realtime(model, camera_id):
    camera = cv2.VideoCapture(camera_id)
    is_collection_start = False #預設不會一開始就蒐集
    while True:
        is_success, frame = camera.read()  # 從camera取得資料
        if is_success:
            # 我想要在這邊可以透過camera蒐集圖片
            show_frame = frame.copy() #copy frame for display
            put_cv2_text(show_frame , f"Collecting:{is_collection_start}" , (30,50))
            if is_collection_start:
                #辨識手勢
                detections = detect_face(model, frame)
                for detection in detections:
                    # Draw bounding_box
                    bbox = detection.bounding_box
                    start_point = bbox.origin_x, bbox.origin_y # 左上錨點
                    end_point = bbox.origin_x + bbox.width, bbox.origin_y + bbox.height # 右下錨點
                    cv2.rectangle(show_frame, start_point, end_point, (0, 255, 255), 3)
                key = cv2.waitKey(100)
            else:
                key = cv2.waitKey(1)
            cv2.imshow("Collector", show_frame)
        else:
            print("Wait for camera ready......")
            key = cv2.waitKey(1000)

        if key == ord('q') or key == ord("Q"): # 如果按下'q' or 'Q'
            break
        elif key == ord('a') or key == ord('A'): #開始
            is_collection_start = True
        elif key == ord('z') or key == ord('Z'): #暫停
            is_collection_start = False

if __name__ == '__main__':
    camera_id = 0
    model_path = 'blaze_face_short_range.tflite'
    face_detection_model = init_face_detector(model_path)
    detect_face_realtime(face_detection_model , camera_id)