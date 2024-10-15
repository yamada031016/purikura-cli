import mediapipe as mp
import cv2
import numpy as np
from stegano import lsb

def decorate(src_name, output_path):
    frame_width = 20
    pre_purikura_img = cv2.copyMakeBorder((cv2.imread(src_name)),  frame_width,frame_width,frame_width,frame_width, cv2.BORDER_CONSTANT, (255, 255, 255) )
    pre_purikura_img = cv2.bilateralFilter(pre_purikura_img,10,30,30)

    size = 516
    pre_purikura_img = cv2.resize(pre_purikura_img,dsize=(size,size))

    pre_purikura_img = cv2.cvtColor(pre_purikura_img, cv2.COLOR_BGR2HSV)
    pre_purikura_img[:,:,(1)] = pre_purikura_img[:,:,(1)]*0.65 # 彩度の変更
    pre_purikura_img = cv2.cvtColor(pre_purikura_img, cv2.COLOR_HSV2BGR)

    pre_purikura_img = add_lipstick(pre_purikura_img)

    frame = cv2.resize(cv2.imread("frames/heart-zuttomo.png", -1), dsize=(size, size))
    frame_mask = frame[:, :, 3]
    mask=cv2.merge((frame_mask,frame_mask,frame_mask))

    output = cv2.bitwise_and(pre_purikura_img,cv2.bitwise_not(mask))
    output = cv2.bitwise_or(cv2.cvtColor(output, cv2.COLOR_BGR2BGRA), frame)

    cv2.imwrite(output_path,output)

def add_lipstick(img):
    drawing = mp.solutions.drawing_utils
    drawing_spec = drawing.DrawingSpec(thickness=1, circle_radius=1, color=(0, 255, 0))
    drawing_styles = mp.solutions.drawing_styles
    face_mesh = mp.solutions.face_mesh
    face_detector = face_mesh.FaceMesh(min_detection_confidence=0.6, min_tracking_confidence=0.9)
# 検知処理
    results = face_detector.process(img)
    face_landmarks = results.multi_face_landmarks

# 入力画像と同じサイズの黒マスクを作成
    gray = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)

# 検知した顔における「唇」に関するINDEXを抽出する
    lips_idx = list(face_mesh.FACEMESH_LIPS)
    lips = np.ravel(lips_idx)

# 唇のINDEXを用いてピクセル座標に戻し、リストを作成する
    empty_lip = []
    for i in lips:
        pt1 = face_landmarks[0].landmark[i]
        x = int(pt1.x * img.shape[1])
        y = int(pt1.y * img.shape[0])
        empty_lip.append((x, y))

        # ピクセル座標をもとに唇の凸包を作成
    convexhull  = cv2.convexHull(np.array(empty_lip))

# 作成した凸包に対して色を塗る
    mask = cv2.fillConvexPoly(gray, convexhull, ((70, 10, 255)))

# 見た目をより円滑化するため、ガウシアンブラーをかける
    mask = cv2.GaussianBlur(mask, (7, 7), 20)
    return cv2.addWeighted(mask, 0.5, img, 1, 0.)

def hide_save_message(img_path, msg):
    img =  lsb.hide(img_path, msg)
    img.save(img_path)

def reveal_message(img_path):
    return lsb.reveal(img_path)

def help_message():
    print("""
    purikura <src-img-path> <command> <command-options..>

    commands:
        help: show this help message.
        deco: decorate your src-image
            need 1 argument <output-path>
        hide: hide secret message on your src-image
            need 1 argument <message>
        reveal: reveal secret message on your src-image
    """)
