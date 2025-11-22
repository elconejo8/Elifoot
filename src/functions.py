import cv2
import os
from PIL import Image

def save_video_frames(vid, save_to_path, n, transform=None):
    video_capture = cv2.VideoCapture(vid)
    v_len = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
    for j in range(v_len):
        _, vframe = video_capture.read()
        if j % n == 0:
            vframe = cv2.cvtColor(vframe, cv2.COLOR_BGR2RGB)
            Image.fromarray(vframe).save(os.path.join(save_to_path, str(j) + '.png'))
    return 1