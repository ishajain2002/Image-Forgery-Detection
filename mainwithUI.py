import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk
import cv2
import hashlib
import os

def calculate_md5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def detect_forgery(original_path, test_path):
    original_image = cv2.imread(original_path)
    test_image = cv2.imread(test_path)

    original_image = cv2.resize(original_image, (256, 256))
    test_image = cv2.resize(test_image, (256, 256))

    original_hash = calculate_md5(original_path)
    test_hash = calculate_md5(test_path)

    return original_hash == test_hash

class ForgeryDetectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Forgery Detection")

        # Set a themed style
        self.style = ttk.Style()
        self.style.theme_use("clam")  # Choose from "clam", "alt", "default", etc.

        # Configure background color
        self.style.configure("TFrame", background="#FFD700")  # Golden Yellow
        self.style.configure("TLabel", background="#FFD700", font=("Arial", 12))
        self.style.configure("TButton", background="#32CD32", font=("Arial", 12))  # Lime Green
        self.style.configure("TLabelResult.TLabel", background="#FFD700", font=("Arial", 12, "bold"), foreground="#FF4500")  # Orange Red

        # Variables
        self.original_image_path = ""
        self.test_image_path = ""

        # UI Components
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.grid(row=0, column=0, padx=50, pady=50, sticky="nsew")

        self.original_image_label = ttk.Label(self.main_frame, text="Original Image:")
        self.original_image_label.grid(row=0, column=0, pady=(10, 5))

        self.original_image_button = ttk.Button(self.main_frame, text="Upload Original Image", command=self.upload_original_image)
        self.original_image_button.grid(row=0, column=1, pady=(10, 5))

        self.test_image_label = ttk.Label(self.main_frame, text="Test Image:")
        self.test_image_label.grid(row=1, column=0, pady=(5, 5))

        self.test_image_button = ttk.Button(self.main_frame, text="Upload Test Image", command=self.upload_test_image)
        self.test_image_button.grid(row=1, column=1, pady=(5, 5))

        self.detect_button = ttk.Button(self.main_frame, text="Detect Forgery", command=self.detect_forgery)
        self.detect_button.grid(row=2, column=0, columnspan=2, pady=(15, 5))

        self.result_label = ttk.Label(self.main_frame, text="", style="TLabelResult.TLabel")
        self.result_label.grid(row=3, column=0, columnspan=2, pady=(5, 10))

        # Center the content
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)

    def upload_original_image(self):
        self.original_image_path = filedialog.askopenfilename()
        self.display_image(self.original_image_path, row=0, col=2)

    def upload_test_image(self):
        self.test_image_path = filedialog.askopenfilename()
        self.display_image(self.test_image_path, row=1, col=2)

    def detect_forgery(self):
        if self.original_image_path and self.test_image_path:
            result = detect_forgery(self.original_image_path, self.test_image_path)
            if result:
                self.result_label.config(text="Forgery Detected: Yes", foreground="#FF4500")  # Orange Red
            else:
                self.result_label.config(text="Forgery Detected: No", foreground="#32CD32")  # Lime Green
        else:
            self.result_label.config(text="Please upload both original and test images.", foreground="orange")

    def display_image(self, image_path, row, col):
        img = Image.open(image_path)
        img = img.resize((150, 150), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        panel = ttk.Label(self.main_frame, image=img)
        panel.image = img
        panel.grid(row=row, column=col, padx=10, pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = ForgeryDetectionApp(root)
    root.mainloop()

