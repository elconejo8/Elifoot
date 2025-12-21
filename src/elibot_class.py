import subprocess
import time
import pygetwindow as gw
import pyautogui
from PIL import ImageGrab, Image
import numpy as np

class EliBot:
    def __init__(self, game_path, dosbox_folder_path):

        self.game_path = game_path
        self.dosbox_folder_path = dosbox_folder_path

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
    
    def analyze_screen(self, screen):
        """Analyze screen to extract game state"""
        # Convert to grayscale for analysis
        from PIL import Image
        img = Image.fromarray(screen)
        gray = img.convert('L')
        

        state = {}
        
        return state


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
        for key_name in ['enter', 'f1', 'f3', 'f6', 'f8', 'n', 'esc']:
            time.sleep(5)
            if save_screens:
                screen = self.capture_screen()
                screen = Image.fromarray(screen)
                screen.save("Data\Screenshots\{}_enter.jpeg".format(time.time()))
            self.send_key(key_name)


#Simulating decisions and saving the images each step