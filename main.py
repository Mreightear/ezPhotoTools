import cv2
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

class ImageProcessor:
    def __init__(self, root):
        self.root = root
        self.root.title("ezPhotoTools")
        self.input_image = None
        self.select_button = tk.Button(root, text="Dosya Seç", command=self.select_file)
        self.select_button.pack(pady=20)
        self.effects_var = tk.StringVar(root)
        self.effects_var.set("Orjinal")
        self.effects_menu = tk.OptionMenu(root, self.effects_var, "Orjinal", "Gri Ton", "Blurlama", "Canny")
        self.effects_menu.pack(pady=10)
        self.apply_button = tk.Button(root, text="Efekt Uygula", command=self.apply_effect)
        self.apply_button.pack(pady=10)
    def select_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("JPEG files", "*.jpg;*.jpeg")])
        if file_path:
            self.input_image = cv2.imread(file_path)
            img = Image.open(file_path)
            img = img.resize((300, 300))
            img = ImageTk.PhotoImage(img)
            panel = tk.Label(self.root, image=img)
            panel.image = img
            panel.pack()
    def apply_effect(self):
        if self.input_image is not None:
            selected_effect = self.effects_var.get()
            if selected_effect == "Orjinal":
                output_image = self.input_image
            elif selected_effect == "Gri Ton":
                output_image = cv2.cvtColor(self.input_image, cv2.COLOR_BGR2GRAY)
            elif selected_effect == "Blurlama":
                output_image = cv2.GaussianBlur(self.input_image, (15, 15), 0)
            elif selected_effect == "Canny":
                output_image = cv2.Canny(self.input_image, 100, 200)
            output_file = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg;*.jpeg")])
            cv2.imwrite(output_file, output_image)
            tk.messagebox.showinfo("Başarılı", "Efekt uygulama işlemi tamamlandı.")
        else:
            tk.messagebox.showwarning("Hata", "Lütfen önce bir dosya seçin.")
if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessor(root)
    root.mainloop()
