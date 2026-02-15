import subprocess
import time
import pygetwindow as gw
import pyautogui
from PIL import ImageGrab, Image
import numpy as np
import torch
from torchvision.transforms import v2
from torch import nn

transforms = v2.Compose([
    v2.ToTensor(),
    v2.RandomHorizontalFlip(p=0.5),
    v2.ToDtype(torch.float32, scale=True),
    v2.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    v2.RandomResizedCrop(size=(120, 120), antialias=True),
])

def make_single_pred(img, model, transform):
    img_transform = transform(img)
    
    softmax = nn.Softmax(dim=1)
    return softmax(model(img_transform.unsqueeze(0))).max(axis=1).indices.tolist()[0]


class EliBot:
    def __init__(self, game_path, dosbox_folder_path, model_path, classes_label_conversion):

        self.game_path = game_path
        self.dosbox_folder_path = dosbox_folder_path
        self.model = torch.load(model_path, weights_only=False)
        self.classes_label_conversion = classes_label_conversion

        """
        Launch game in DOSBox (DOS emulator)
        """
        # Start DOSBox with the game
        self.process = subprocess.Popen(
            self.game_path,
            cwd=self.dosbox_folder_path,
            stdin=subprocess.PIPE
        )
        time.sleep(3)  # Wait for game to load
        
        # Get game window position
        self.find_game_window()
    
    def find_game_window(self):
        """Find DOSBox window coordinates"""
        
        elifoot_windows = [title for title in gw.getAllTitles() if 'ELIFOOT2' in title]
        if len(elifoot_windows) > 1:
            raise ValueError('Multiple Elifoot windows found, exiting')
        if len(elifoot_windows) == 0:
            raise ValueError('No Elifoot window found, exiting')
        windows = gw.getWindowsWithTitle('DOSBox')
        self.game_window = windows[0]
        self.game_window.activate()
        
    def capture_screen(self):
        """Capture game screen"""
        if hasattr(self, 'game_window'):
            bbox = (
                self.game_window.left,
                self.game_window.top,
                self.game_window.right,
                self.game_window.bottom
            )
            screenshot = ImageGrab.grab(bbox)
            return np.array(screenshot)
        else:
            # Fallback: capture full screen
            screenshot = ImageGrab.grab()
            return np.array(screenshot)


    def send_key(self, key):
        """Send keyboard input to game"""
        print(f">>> Bot pressing: {key}")
        pyautogui.press(key)

    def start_game(self):
        """Start game with a single player (G)"""
        self.send_key('n')
        time.sleep(25)
        self.send_key('G')
        time.sleep(2)
        self.send_key('enter')
        time.sleep(2)
        self.send_key('enter')

    def random_play(self, save_screens=True):
        """Play game randomly saving screen before pressing keys"""
        while True:
            for key_name in ['enter', 'f1', 'f3', 'f6', 'f8', 'n', 'esc']:
                print(key_name, save_screens)
                time.sleep(5)
                if save_screens:
                    screen = self.capture_screen()
                    screen_img = Image.fromarray(screen)
                    pred_class = make_single_pred(screen_img, model=self.model, transform=transforms)
                    screen_img.save("Data\Screenshots\{}_{}.jpeg".format(time.time(), pred_class))
                self.send_key(key_name)

    def random_play(self, save_screens=True):
        """Play game randomly saving screen before pressing keys"""
        while True:
            for key_name in ['enter', 'f1', 'f3', 'f6', 'f8', 'n', 'esc']:
                print(key_name, save_screens)
                time.sleep(5)
                if save_screens:
                    screen = self.capture_screen()
                    screen_img = Image.fromarray(screen)
                    pred_class = make_single_pred(screen_img, model=self.model, transform=transforms)
                    pred_class = self.classes_label_conversion.loc[self.classes_label_conversion['Label'] == pred_class, 'Class'].item()
                    if pred_class in ['Class_tables', 'Cup_draw', 'Cup_game', 'Game', 'Game_extra_time', 'Manager_changes', 'Top_scorers']:
                        time.sleep(3)
                    else: 
                        screen_img.save("Data\Screenshots\{}_{}.jpeg".format(time.time(), pred_class))
                self.send_key(key_name)




#Simulating decisions and saving the images each step