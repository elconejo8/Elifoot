import cv2
import os
from PIL import Image
import numpy as np
from skimage.metrics import structural_similarity as ssim

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