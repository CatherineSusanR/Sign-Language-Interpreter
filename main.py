import tkinter as tk
from tkinter import simpledialog, messagebox
import os
import threading
import sys
import subprocess

def run_sign_to_text():
    if not os.path.exists('model.p'):
        messagebox.showerror("Error", "Model not found! Please train the model first.")
        return

    try:
        subprocess.Popen([sys.executable, 'inference_classifier.py'])
    except Exception as e:
        messagebox.showerror("Error", f"Failed to start Sign to Text: {e}")

def run_text_to_sign():
    text = simpledialog.askstring("Input", "Enter text to convert:")
    if text:
        try:
            import text_to_sign
            threading.Thread(target=text_to_sign.text_to_sign, args=(text,), daemon=True).start()
        except ImportError:
             messagebox.showerror("Error", "Could not import text_to_sign module.")
        except Exception as e:
             messagebox.showerror("Error", f"An error occurred: {e}")

root = tk.Tk()
root.title("Sign Language Converter")
root.geometry("400x250")
root.resizable(False, False)

label = tk.Label(root, text="Sign Language Converter", font=("Arial", 20, "bold"))
label.pack(pady=30)

subtitle = tk.Label(root, text="Choose an option:", font=("Arial", 12))
subtitle.pack(pady=(0, 15))

btn_frame = tk.Frame(root)
btn_frame.pack(pady=5)

btn_s2t = tk.Button(btn_frame, text="Sign to Text (Camera)", command=run_sign_to_text,
                    width=20, font=("Arial", 11), bg="lightblue", cursor="hand2")
btn_s2t.pack(side=tk.LEFT, padx=10)

btn_t2s = tk.Button(btn_frame, text="Text to Sign", command=run_text_to_sign,
                    width=20, font=("Arial", 11), bg="lightgreen", cursor="hand2")
btn_t2s.pack(side=tk.LEFT, padx=10)

root.mainloop()
