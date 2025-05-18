import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import os
import numpy as np
from utils import filters

class IMPEGApp:
    def __init__(self, master):
        self.master = master
        self.master.title("IMPEG")
        self.master.geometry("1000x600")
        self.master.configure(bg="#d0f0f7")

        self.create_top_buttons()
        self.build_homepage()
        self.logout_btn = tk.Button(self.top_frame, text="🚪 Logout", command=self.logout)
        self.logout_btn.pack(side="right", padx=5)
        self.master.protocol("WM_DELETE_WINDOW", self.logout)

    def logout(self):
        confirm = messagebox.askyesno("Konfirmasi Keluar", "Apakah Anda yakin ingin keluar dari aplikasi?")
        if confirm:
            self.master.quit()

    def create_top_buttons(self):
        self.top_frame = tk.Frame(self.master, bg="#e0f7fa")
        self.top_frame.pack(side="top", fill="x", pady=5)

        btn_style = {
            "font": ("Helvetica", 10, "bold"),
            "bg": "#004d40",
            "fg": "white",
            "activebackground": "#00796b",
            "activeforeground": "white",
            "bd": 0,
            "padx": 20,
            "pady": 5,
            "relief": "raised",
        }

        self.home_btn = tk.Button(self.top_frame, text="🏠 Home", command=self.build_homepage, **btn_style)
        self.effect_btn = tk.Button(self.top_frame, text="✨ Effect", command=self.start_editor, **btn_style)
        self.about_btn = tk.Button(self.top_frame, text="ℹ️ About", command=self.show_about, **btn_style)

        self.home_btn.pack(side="left", padx=5)
        self.effect_btn.pack(side="left", padx=5)
        self.about_btn.pack(side="left", padx=5)

        self.image_path = None
        self.original_image = None
        self.processed_image = None

        self.menubar = None
        self.content_frame = None
        self.before_label = None
        self.after_label = None

        self.build_menu()
        self.build_homepage()

    def build_menu(self):
        self.menubar = tk.Frame(self.master, bg="#dcdcdc", height=40)
        self.menubar.pack(fill=tk.X)

        tk.Button(self.menubar, text="Home", width=10, command=self.build_homepage).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(self.menubar, text="Effect", width=10, command=self.start_editor).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(self.menubar, text="About", width=10, command=self.show_about).pack(side=tk.LEFT, padx=5, pady=5)

    def clear_widgets(self):
        for widget in self.master.winfo_children():
            if widget != self.top_frame:
                widget.destroy()

    def build_homepage(self):
        self.clear_widgets()
        self.content_frame = tk.Frame(self.master, bg="#e0f7fa")
        self.content_frame.pack(fill="both", expand=True)

        logo_path = os.path.join("assets", "logo.png")
        if os.path.exists(logo_path):
            logo_img = Image.open(logo_path).resize((180, 180))
            logo_img_tk = ImageTk.PhotoImage(logo_img)
            logo_label = tk.Label(self.content_frame, image=logo_img_tk, bg="#e0f7fa", bd=2, relief="groove")
            logo_label.image = logo_img_tk
            logo_label.pack(pady=20)

        title_label = tk.Label(
            self.content_frame,
            text="IMPEG",
            font=("Helvetica", 32, "bold"),
            bg="#e0f7fa",
            fg="#00796b"
        )
        title_label.pack()

        subtitle_label = tk.Label(
            self.content_frame,
            text="Image Processing Editor GUI",
            font=("Helvetica", 14),
            bg="#e0f7fa",
            fg="#004d40"
        )
        subtitle_label.pack(pady=5)

        start_button = tk.Button(
            self.content_frame,
            text="Start",
            font=("Helvetica", 12, "bold"),
            bg="#00796b",
            fg="white",
            activebackground="#004d40",
            activeforeground="white",
            padx=20,
            pady=5,
            relief="raised",
            command=self.start_editor
        )
        start_button.pack(pady=20)

    def show_about(self):
        self.clear_widgets()
        self.content_frame = tk.Frame(self.master, bg="#e0f7fa")
        self.content_frame.pack(fill="both", expand=True)

        title = tk.Label(
            self.content_frame,
            text="Tentang Aplikasi IMPEG",
            font=("Helvetica", 20, "bold"),
            fg="#004d40",
            bg="#e0f7fa"
        )
        title.pack(pady=20)

        description = tk.Label(
            self.content_frame,
            text=(
                "IMPEG v1.0\n"
                "Aplikasi Pengolahan Citra berbasis GUI\n"
                "Dikembangkan oleh Mutia dan Tim\n\n"
                "Fitur-fitur termasuk efek negatif, rotasi, blending,\n"
                "penyesuaian kontras, kecerahan, ketajaman, dan lainnya.\n\n"
                "Gunakan aplikasi ini untuk eksplorasi dan pembelajaran\n"
                "tentang pemrosesan citra digital."
            ),
            font=("Arial", 13),
            fg="#00695c",
            bg="#e0f7fa",
            justify="center"
        )
        description.pack(pady=10)

        back_btn = tk.Button(
            self.content_frame,
            text="⬅ Kembali ke Beranda",
            font=("Helvetica", 12, "bold"),
            bg="#00796b",
            fg="white",
            activebackground="#004d40",
            activeforeground="white",
            padx=10,
            pady=5,
            command=self.build_homepage
        )
        back_btn.pack(pady=20)

    def start_editor(self):
        self.clear_widgets()
        self.content_frame = tk.Frame(self.master, bg="#f0f0f0")
        self.content_frame.pack(fill="both", expand=True)

        control_frame = tk.Frame(self.content_frame, bg="#f0f0f0")
        control_frame.pack(pady=10)

        filter_frame = tk.LabelFrame(self.content_frame, text="Filter dan Efek", bg="#ffffff", padx=10, pady=10, font=("Helvetica", 12, "bold"), fg="#004d40")
        filter_frame.pack(pady=10)

        filter_buttons = [
            ("Negative", self.apply_negative),
            ("Thresholding", self.apply_threshold),
            ("Rotate 90°", lambda: self.rotate_image(90)),
            ("Rotate 180°", lambda: self.rotate_image(180)),
            ("Flip Horizontal", lambda: self.flip_image('horizontal')),
            ("Flip Vertical", lambda: self.flip_image('vertical')),
            ("Zoom In", self.zoom_in),
            ("Shrink", self.shrink),
            ("Log Transform", self.log_transform),
            ("Translate", self.translate_image),
            ("Blending", self.blend_image),
        ]

        for text, command in filter_buttons:
            btn = tk.Button(filter_frame, text=text, command=command,
                            bg="#004d40", fg="white", activebackground="#00796b", activeforeground="white",
                            relief="raised", padx=10, pady=5, font=("Helvetica", 10, "bold"))
            btn.pack(side=tk.LEFT, padx=5, pady=5)

        tk.Button(control_frame, text="📤 Upload Gambar", command=self.upload_image,
                  bg="#0288d1", fg="white", font=("Helvetica", 10, "bold"), padx=10, pady=5).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="🔄 Reset", command=self.reset_image,
                  bg="#ffa000", fg="white", font=("Helvetica", 10, "bold"), padx=10, pady=5).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="💾 Simpan Gambar", command=self.save_image,
                  bg="#43a047", fg="white", font=("Helvetica", 10, "bold"), padx=10, pady=5).pack(side=tk.LEFT, padx=5)

        image_frame = tk.Frame(self.content_frame, bg="#f0f0f0")
        image_frame.pack(pady=10, expand=True)

        self.before_label = tk.Label(image_frame, text="Before", bg="#f0f0f0")
        self.before_label.pack(side=tk.LEFT, padx=10)

        self.after_label = tk.Label(image_frame, text="After", bg="#f0f0f0")
        self.after_label.pack(side=tk.RIGHT, padx=10)

        slider_frame = tk.Frame(self.content_frame, bg="#f0f0f0")
        slider_frame.pack(side=tk.BOTTOM, pady=10)

        self.build_slider(slider_frame, "Contrast", self.adjust_contrast)
        self.build_slider(slider_frame, "Brightness", self.adjust_brightness)
        self.build_slider(slider_frame, "Sharpness", self.sharpen_image)
        self.build_slider(slider_frame, "Saturation", self.adjust_saturation)
        self.build_slider(slider_frame, "Noise Reduction", self.reduce_noise)

    def effect_page(self):
        self.clear_widgets()

        label = tk.Label(self.master, text="Halaman Effect", font=("Helvetica", 16), bg="#d0f0f7")
        label.pack(pady=50)

    def build_slider(self, frame, label, command):
        subframe = tk.Frame(frame, bg="#f0f0f0")
        subframe.pack(side=tk.LEFT, padx=10)
        tk.Label(subframe, text=label, bg="#f0f0f0").pack()
        scale = tk.Scale(subframe, from_=0, to=2, resolution=0.1, orient=tk.HORIZONTAL,
                         command=lambda val, cmd=command: cmd(float(val)))
        scale.set(1)
        scale.pack()

    def upload_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.image_path = file_path
            image = Image.open(file_path).convert("RGB")
            self.original_image = image
            self.processed_image = image.copy()
            self.show_images()

    def reset_image(self):
        if self.original_image:
            self.processed_image = self.original_image.copy()
            self.show_images()

    def save_image(self):
        if self.processed_image:
            path = filedialog.asksaveasfilename(defaultextension=".png")
            if path:
                self.processed_image.save(path)
                messagebox.showinfo("Success", "Gambar berhasil disimpan!")

    def show_images(self):
        if self.original_image and self.processed_image:
            ori = self.original_image.resize((400, 300))
            out = self.processed_image.resize((400, 300))
            ori_tk = ImageTk.PhotoImage(ori)
            out_tk = ImageTk.PhotoImage(out)

            self.before_label.config(image=ori_tk)
            self.before_label.image = ori_tk
            self.after_label.config(image=out_tk)
            self.after_label.image = out_tk

    def pil_to_cv(self, image):
        return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    def cv_to_pil(self, image):
        return Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    def apply_negative(self):
        if self.original_image:
            img_cv = self.pil_to_cv(self.original_image)
            result = filters.image_negative(img_cv)
            self.processed_image = self.cv_to_pil(result)
            self.show_images()

    def apply_threshold(self):
        if self.original_image:
            img_cv = self.pil_to_cv(self.original_image)
            result = filters.image_thresholding(img_cv)
            self.processed_image = self.cv_to_pil(result)
            self.show_images()

    def rotate_image(self, angle):
        if self.original_image:
            img_cv = self.pil_to_cv(self.original_image)
            result = filters.image_rotating(img_cv, angle)
            self.processed_image = self.cv_to_pil(result)
            self.show_images()

    def flip_image(self, direction):
        if self.original_image:
            img_cv = self.pil_to_cv(self.original_image)
            result = filters.image_flipping(img_cv, direction)
            self.processed_image = self.cv_to_pil(result)
            self.show_images()

    def zoom_in(self):
        if self.original_image:
            img_cv = self.pil_to_cv(self.original_image)
            result = filters.image_zooming(img_cv, scale=1.5)
            self.processed_image = self.cv_to_pil(result)
            self.show_images()

    def shrink(self):
        if self.original_image:
            img_cv = self.pil_to_cv(self.original_image)
            result = filters.image_shrinking(img_cv, scale=0.5)
            self.processed_image = self.cv_to_pil(result)
            self.show_images()

    def log_transform(self):
        if self.original_image:
            img_cv = self.pil_to_cv(self.original_image)
            result = filters.image_logarithmic(img_cv)
            self.processed_image = self.cv_to_pil(result)
            self.show_images()

    def translate_image(self):
        if self.original_image:
            img_cv = self.pil_to_cv(self.original_image)
            result = filters.image_translation(img_cv, tx=50, ty=50)
            self.processed_image = self.cv_to_pil(result)
            self.show_images()

    def blend_image(self):
        if self.original_image:
            image_path2 = filedialog.askopenfilename(title="Pilih Gambar Kedua untuk Blending")
            if not image_path2:
                return
            img1 = self.pil_to_cv(self.original_image)
            img2 = cv2.imread(image_path2)
            result = filters.image_blending(img1, img2, alpha=0.5)
            self.processed_image = self.cv_to_pil(result)
            self.show_images()

    def adjust_contrast(self, val):
        if self.original_image:
            img_cv = self.pil_to_cv(self.original_image)
            result = filters.adjust_contrast(img_cv, val)
            self.processed_image = self.cv_to_pil(result)
            self.show_images()

    def adjust_brightness(self, val):
        if self.original_image:
            img_cv = self.pil_to_cv(self.original_image)
            value = int((val - 1) * 100)
            result = filters.adjust_brightness(img_cv, value)
            self.processed_image = self.cv_to_pil(result)
            self.show_images()

    def sharpen_image(self, val):
        if self.original_image and val != 1.0:
            img_cv = self.pil_to_cv(self.original_image)
            result = filters.sharpen_image(img_cv)
            self.processed_image = self.cv_to_pil(result)
            self.show_images()

    def adjust_saturation(self, val):
        if self.original_image:
            img_cv = self.pil_to_cv(self.original_image)
            result = filters.adjust_saturation(img_cv, val)
            self.processed_image = self.cv_to_pil(result)
            self.show_images()

    def reduce_noise(self, val):
        if self.original_image and val != 1.0:
            img_cv = self.pil_to_cv(self.original_image)
            result = filters.reduce_noise(img_cv)
            self.processed_image = self.cv_to_pil(result)
            self.show_images()

if __name__ == "__main__":
    root = tk.Tk()
    app = IMPEGApp(root)
    root.mainloop()
