import cv2
import tkinter as tk
from tkinter import filedialog, messagebox
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

        effects_list = ["Orjinal", "Gri Ton", "Blurlama", "Canny", "Negatif", "Döndür", "Aynala", "Sepya"]
        self.effects_menu = tk.OptionMenu(root, self.effects_var, *effects_list)
        self.effects_menu.pack(pady=10)

        self.apply_button = tk.Button(root, text="Efekt Uygula", command=self.apply_effect)
        self.apply_button.pack(pady=10)

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
                output_image = self.input_image
            elif selected_effect == "Gri Ton":
                output_image = cv2.cvtColor(self.input_image, cv2.COLOR_BGR2GRAY)
            elif selected_effect == "Blurlama":
                output_image = cv2.GaussianBlur(self.input_image, (15, 15), 0)
            elif selected_effect == "Canny":
                output_image = cv2.Canny(self.input_image, 100, 200)
            elif selected_effect == "Negatif":
                output_image = 255 - self.input_image
            elif selected_effect == "Döndür":
                output_image = cv2.rotate(self.input_image, cv2.ROTATE_90_CLOCKWISE)
            elif selected_effect == "Aynala":
                output_image = cv2.flip(self.input_image, 1)
            elif selected_effect == "Sepya":
                output_image = self.apply_sepia(self.input_image)

            output_file = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg;*.jpeg")])
            cv2.imwrite(output_file, output_image)
            tk.messagebox.showinfo("Başarılı", "Efekt uygulama işlemi tamamlandı.")
        else:
            tk.messagebox.showwarning("Hata", "Lütfen önce bir dosya seçin.")

    def apply_sepia(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        sepia = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        sepia[:, :, 0] = sepia[:, :, 0] * 0.393 + sepia[:, :, 1] * 0.769 + sepia[:, :, 2] * 0.189
        sepia[:, :, 1] = sepia[:, :, 0] * 0.349 + sepia[:, :, 1] * 0.686 + sepia[:, :, 2] * 0.168
        sepia[:, :, 2] = sepia[:, :, 0] * 0.272 + sepia[:, :, 1] * 0.534 + sepia[:, :, 2] * 0.131
        sepia[sepia > 255] = 255
        return sepia

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessor(root)
    root.mainloop()
