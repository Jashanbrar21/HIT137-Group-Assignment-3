# Adds cropping result preview beside original image

import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2

class ImageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Crop App")

        self.image_frame = tk.Frame(self.root)
        self.image_frame.pack()

        self.canvas = tk.Canvas(self.image_frame, bg="gray")
        self.canvas.grid(row=0, column=0)

        self.preview = tk.Label(self.image_frame, bg="lightgray")
        self.preview.grid(row=0, column=1, padx=10)

        tk.Button(self.root, text="Load Image", command=self.load_image).pack(pady=5)

        self.cv_image = None
        self.clone_image = None
        self.tk_image = None
        self.scale = 1
        self.start_x = self.start_y = 0
        self.rect_id = None
        self.cropped = None

    def load_image(self):
        path = filedialog.askopenfilename()
        if not path:
            return

        self.cv_image = cv2.cvtColor(cv2.imread(path), cv2.COLOR_BGR2RGB)
        self.clone_image = self.cv_image.copy()
        self.display_image(self.cv_image)

        self.canvas.bind("<ButtonPress-1>", self.start_crop)
        self.canvas.bind("<B1-Motion>", self.draw_crop)
        self.canvas.bind("<ButtonRelease-1>", self.end_crop)

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

    def start_crop(self, event):
        self.start_x, self.start_y = event.x, event.y
        if self.rect_id:
            self.canvas.delete(self.rect_id)
        self.rect_id = None

    def draw_crop(self, event):
        if self.rect_id:
            self.canvas.delete(self.rect_id)
        self.rect_id = self.canvas.create_rectangle(
            self.start_x, self.start_y, event.x, event.y, outline="red", width=2
        )

    def end_crop(self, event):
        x1, x2 = sorted([self.start_x, event.x])
        y1, y2 = sorted([self.start_y, event.y])
        scale = 1 / self.scale
        x1, x2 = int(x1 * scale), int(x2 * scale)
        y1, y2 = int(y1 * scale), int(y2 * scale)

        if x2 > x1 and y2 > y1:
            self.cropped = self.clone_image[y1:y2, x1:x2]
            self.show_preview()

        if self.rect_id:
            self.canvas.delete(self.rect_id)
            self.rect_id = None

    def show_preview(self):
        img = Image.fromarray(self.cropped)
        tk_img = ImageTk.PhotoImage(img)
        self.preview.config(image=tk_img)
        self.preview.image = tk_img

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageApp(root)
    root.mainloop()
