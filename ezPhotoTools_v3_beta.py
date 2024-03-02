import cv2
import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser, simpledialog
from PIL import Image, ImageTk
import numpy as np

class ImageProcessor:
    def __init__(self, root):
        self.root = root
        self.root.title("ezPhotoTools")
        self.input_image = None
        self.preview_image = None
        self.text_entries = []
        self.text_color = (255, 255, 255)
        self.text_font = None

        self.select_button = tk.Button(root, text="Dosya Seç", command=self.select_file)
        self.select_button.pack(pady=20)

        self.effects_var = tk.StringVar(root)
        self.effects_var.set("Orjinal")

        effects_list = ["Orjinal", "Gri Ton", "Blurlama", "Canny", "Negatif", "Döndür", "Aynala", "Sepya"]
        self.effects_menu = tk.OptionMenu(root, self.effects_var, *effects_list)
        self.effects_menu.pack(pady=10)

        self.apply_button = tk.Button(root, text="Efekt Uygula", command=self.apply_effect)
        self.apply_button.pack(pady=10)

        self.text_entry = tk.Entry(root, width=30)
        self.text_entry.pack(pady=10)

        self.color_button = tk.Button(root, text="Renk Seç", command=self.select_color)
        self.color_button.pack(pady=10)

        self.font_button = tk.Button(root, text="Yazı Tipi Seç", command=self.select_font)
        self.font_button.pack(pady=10)

        self.preview_label = tk.Label(root, text="Önizleme:")
        self.preview_label.pack(pady=10)

        self.canvas = tk.Canvas(root, bg="white", width=300, height=300)
        self.canvas.pack()

        self.canvas.bind("<Button-1>", self.click_to_add_text)

        self.update_preview()

    def select_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("JPEG files", "*.jpg;*.jpeg")])
        if file_path:
            self.input_image = cv2.imread(file_path)
            self.display_image(file_path)

    def display_image(self, file_path):
        img = Image.open(file_path)
        img = img.resize((300, 300))
        img = ImageTk.PhotoImage(img)
        if hasattr(self, 'panel'):
            self.panel.destroy()
        self.panel = tk.Label(self.root, image=img)
        self.panel.image = img
        self.panel.pack()

    def apply_effect(self):
        if self.input_image is not None:
            selected_effect = self.effects_var.get()
            if selected_effect == "Orjinal":
                self.preview_image = self.input_image.copy()
            elif selected_effect == "Gri Ton":
                self.preview_image = cv2.cvtColor(self.input_image, cv2.COLOR_BGR2GRAY)
            elif selected_effect == "Blurlama":
                self.preview_image = cv2.GaussianBlur(self.input_image, (15, 15), 0)
            elif selected_effect == "Canny":
                self.preview_image = cv2.Canny(self.input_image, 100, 200)
            elif selected_effect == "Negatif":
                self.preview_image = 255 - self.input_image
            elif selected_effect == "Döndür":
                self.preview_image = cv2.rotate(self.input_image, cv2.ROTATE_90_CLOCKWISE)
            elif selected_effect == "Aynala":
                self.preview_image = cv2.flip(self.input_image, 1)
            elif selected_effect == "Sepya":
                self.preview_image = self.apply_sepia(self.input_image)

            self.update_preview()
        else:
            tk.messagebox.showwarning("Hata", "Lütfen önce bir dosya seçin.")

    def apply_sepia(self, image):
        sepia = cv2.cvtColor(image, cv2.COLOR_BGR2RGB).astype(np.float32)

        sepia_filter = np.array([[0.393, 0.769, 0.189],
                                 [0.349, 0.686, 0.168],
                                 [0.272, 0.534, 0.131]])

        sepia = cv2.transform(sepia, sepia_filter)

        sepia = np.clip(sepia, 0, 255).astype(np.uint8)

        return sepia

    def select_color(self):
        color = colorchooser.askcolor(initialcolor=self.text_color)
        if color[1] is not None:
            self.text_color = tuple(map(int, color[0]))  # Renk değerlerini tam sayıya çevirme

    def select_font(self):
        font_name = simpledialog.askstring("Yazı Tipi Seç", "Yazı tipi adını girin:")
        if font_name:
            self.text_font = font_name

    def click_to_add_text(self, event):
        text = self.text_entry.get()
        if text and self.text_font and self.text_color:
            x, y = event.x, event.y
            self.text_entries.append({"text": text, "font": self.text_font, "color": self.text_color, "position": (x, y)})
            self.display_image(file_path)  # Burada display_image fonksiyonunu çağırıyoruz
            self.update_preview()

    def update_preview(self):
        if self.preview_image is not None:
            img = self.preview_image.copy()
            for entry in self.text_entries:
                text = entry["text"]
                font_scale = 1
                font_thickness = 2
                color = entry["color"]
                position = entry.get("position", (50, 50))

                cv2.putText(img, text, position, cv2.FONT_HERSHEY_SIMPLEX, font_scale, color, font_thickness, cv2.LINE_AA)

            img = Image.fromarray(img)
            img = img.resize((300, 300))
            img = ImageTk.PhotoImage(img)

            if hasattr(self, 'preview_panel'):
                self.preview_panel.destroy()
            self.preview_panel = tk.Label(self.root, image=img)
            self.preview_panel.image = img
            self.preview_panel.pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessor(root)
    root.mainloop()
