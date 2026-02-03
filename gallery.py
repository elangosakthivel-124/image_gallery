import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk


class ImageGalleryApp:
    THUMBNAIL_SIZE = (150, 150)
    PREVIEW_SIZE = (600, 400)

    def __init__(self, root):
        self.root = root
        self.root.title("Python Image Gallery")
        self.root.geometry("900x600")
        self.root.configure(bg="#1e1e1e")

        self.image_paths = []
        self.current_index = 0
        self.thumbnail_refs = []

        self._build_ui()

    def _build_ui(self):
        top_bar = tk.Frame(self.root, bg="#2b2b2b", height=50)
        top_bar.pack(fill=tk.X)

        load_btn = tk.Button(
            top_bar, text="Load Folder", command=self.load_folder,
            bg="#4CAF50", fg="white", relief=tk.FLAT
        )
        load_btn.pack(padx=10, pady=10, side=tk.LEFT)

        self.preview_label = tk.Label(self.root, bg="#1e1e1e")
        self.preview_label.pack(pady=10)

        nav_frame = tk.Frame(self.root, bg="#1e1e1e")
        nav_frame.pack()

        tk.Button(nav_frame, text="◀ Prev", command=self.prev_image).pack(side=tk.LEFT, padx=10)
        tk.Button(nav_frame, text="Next ▶", command=self.next_image).pack(side=tk.LEFT, padx=10)

        self.canvas = tk.Canvas(self.root, bg="#1e1e1e", height=200)
        self.canvas.pack(fill=tk.X, pady=10)

        self.thumb_frame = tk.Frame(self.canvas, bg="#1e1e1e")
        self.canvas.create_window((0, 0), window=self.thumb_frame, anchor="nw")

        self.thumb_frame.bind("<Configure>", self._update_scrollregion)

    def _update_scrollregion(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def load_folder(self):
        folder = filedialog.askdirectory()
        if not folder:
            return

        self.image_paths = [
            os.path.join(folder, f)
            for f in os.listdir(folder)
            if f.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".bmp"))
        ]

        if not self.image_paths:
            messagebox.showwarning("No Images", "No supported image files found.")
            return

        self.current_index = 0
        self._load_thumbnails()
        self._show_preview()

    def _load_thumbnails(self):
        for widget in self.thumb_frame.winfo_children():
            widget.destroy()

        self.thumbnail_refs.clear()

        for index, path in enumerate(self.image_paths):
            img = Image.open(path)
            img.thumbnail(self.THUMBNAIL_SIZE)
            tk_img = ImageTk.PhotoImage(img)
            self.thumbnail_refs.append(tk_img)

            btn = tk.Button(
                self.thumb_frame, image=tk_img, relief=tk.FLAT,
                command=lambda i=index: self._select_image(i)
            )
            btn.grid(row=0, column=index, padx=5, pady=5)

    def _select_image(self, index):
        self.current_index = index
        self._show_preview()

    def _show_preview(self):
        img = Image.open(self.image_paths[self.current_index])
        img.thumbnail(self.PREVIEW_SIZE)
        self.preview_img = ImageTk.PhotoImage(img)
        self.preview_label.config(image=self.preview_img)

    def next_image(self):
        if not self.image_paths:
            return
        self.current_index = (self.current_index + 1) % len(self.image_paths)
        self._show_preview()

    def prev_image(self):
        if not self.image_paths:
            return
        self.current_index = (self.current_index - 1) % len(self.image_paths)
        self._show_preview()


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageGalleryApp(root)
    root.mainloop()
