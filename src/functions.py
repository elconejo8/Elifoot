import cv2
import os
from PIL import Image
import numpy as np
from skimage.metrics import structural_similarity as ssim
import shutil
from pathlib import Path

def frame_similarity(frame1, frame2, thr=0.99):
    gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

    frame_sim = ssim(gray1, gray2)

    return frame_sim > thr


def save_video_frames(vid, save_to_path, n, transform=None):
    video_capture = cv2.VideoCapture(vid)
    v_len = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))

    last_frame = None
    for j in range(v_len):
        _, vframe = video_capture.read()
        if j % n == 0:
            vframe = cv2.cvtColor(vframe, cv2.COLOR_BGR2RGB)
            if frame_similarity(last_frame, vframe):
                continue
            else:
                last_frame = vframe
            Image.fromarray(vframe).save(os.path.join(save_to_path, str(j) + '.png'))
    return 1


FRAMES_CLASSES = {
    'o': 'Data/Frames_Categories/Other',
    'tm': 'Data/Frames_Categories/Team_menu',
    's': 'Data/Frames_Categories/Salary_auction',
    'g': 'Data/Frames_Categories/Game',
    'cg': 'Data/Frames_Categories/Cup_game',
    'ge': 'Data/Frames_Categories/Game_extra_time',
    'gi': 'Data/Frames_Categories/Game_Interval',
    't': 'Data/Frames_Categories/Class_tables',
    'sq': 'Data/Frames_Categories/Squad',
    'cd': 'Data/Frames_Categories/Cup_draw',
    'ts': 'Data/Frames_Categories/Top_scorers',
    'mc': 'Data/Frames_Categories/Manager_changes',
    'pd': 'Data/Frames_Categories/Player_demand',
}

def copy_frame_to_folder(img, class_short):
    if class_short not in FRAMES_CLASSES.keys():
        raise ValueError("Class chosen doesn't exist: {}".format(class_short))
    else:
        frame_name = Path(img).name
        dest_folder = Path(FRAMES_CLASSES[class_short])
        dest_folder.mkdir(parents=True, exist_ok=True)

        dest_path = os.path.join(dest_folder, frame_name)
        shutil.move(img, dest_path)

    return 1
#Copies frame to the correct folder and deletes the original image"