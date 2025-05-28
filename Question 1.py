import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2

class ImageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Crop App")

        self.canvas = tk.Canvas(self.root, bg="gray")
        self.canvas.pack()

        self.load_button = tk.Button(self.root, text="Load Image", command=self.load_image)
        self.load_button.pack(pady=5)

        self.cv_image = None
        self.tk_image = None
        self.scale = 1

    def load_image(self):
        path = filedialog.askopenfilename()
        if not path:
            return

        self.cv_image = cv2.cvtColor(cv2.imread(path), cv2.COLOR_BGR2RGB)
        self.display_image(self.cv_image)

    def display_image(self, img_array):
        max_w, max_h = 800, 600
        h, w = img_array.shape[:2]
        self.scale = min(max_w / w, max_h / h)
        new_w, new_h = int(w * self.scale), int(h * self.scale)
        resized = cv2.resize(img_array, (new_w, new_h))
        self.tk_image = ImageTk.PhotoImage(Image.fromarray(resized))
        self.canvas.config(width=new_w, height=new_h)
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageApp(root)
    root.mainloop()
