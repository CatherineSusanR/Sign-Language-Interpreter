import os
import cv2
import time
import numpy as np

ASSETS_DIR = './assets'

def text_to_sign(text):
    text = text.upper()
    
    for char in text:
        if char == ' ':
            img = np.zeros((500, 500, 3), np.uint8)
            cv2.putText(img, "SPACE", (150, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        else:
            image_path = os.path.join(ASSETS_DIR, f'{char}.jpg')
            folder_path = os.path.join(ASSETS_DIR, char)
            
            final_path = None
            if os.path.exists(folder_path) and os.path.isdir(folder_path):
                files = os.listdir(folder_path)
                if files:
                    final_path = os.path.join(folder_path, files[0])
            elif os.path.exists(image_path):
                final_path = image_path
                
            if final_path:
                img = cv2.imread(final_path)
            else:
                img = np.zeros((500, 500, 3), np.uint8)
                cv2.text = f"Image for {char} not found"
                cv2.putText(img, text, (50, 250), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        
        if img is not None:
             cv2.imshow('Text to Sign', img)
             cv2.waitKey(1000)
    
    cv2.destroyAllWindows()

if __name__ == "__main__":
    text_input = input("Enter text: ")
    text_to_sign(text_input)
