import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from database import ImageDatabase


class ImageGalleryApp:
    THUMB_SIZE = (140, 140)
    PREVIEW_SIZE = (600, 400)

    def __init__(self, root):
        self.root = root
        self.root.title("Image Gallery (DB Powered)")
        self.root.geometry("900x600")

        self.db = ImageDatabase()
        self.images = []
        self.index = 0
        self.thumb_refs = []

        self._ui()
        self._load_from_db()

    def _ui(self):
        top = tk.Frame(self.root)
        top.pack(fill=tk.X)

        tk.Button(top, text="Add Folder", command=self.add_folder).pack(padx=10, pady=10)

        self.preview = tk.Label(self.root)
        self.preview.pack(pady=10)

        nav = tk.Frame(self.root)
        nav.pack()

        tk.Button(nav, text="◀ Prev", command=self.prev_image).pack(side=tk.LEFT, padx=10)
        tk.Button(nav, text="Next ▶", command=self.next_image).pack(side=tk.LEFT, padx=10)

        self.canvas = tk.Canvas(self.root, height=200)
        self.canvas.pack(fill=tk.X)

        self.thumb_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.thumb_frame, anchor="nw")
        self.thumb_frame.bind("<Configure>", self._update_scroll)

    def _update_scroll(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def add_folder(self):
        folder = filedialog.askdirectory()
        if not folder:
            return

        for file in os.listdir(folder):
            if file.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif")):
                path = os.path.join(folder, file)
                self.db.add_image(file, path)

        self._load_from_db()

    def _load_from_db(self):
        self.images = self.db.get_all_images()
        if not self.images:
            return
        self.index = 0
        self._load_thumbnails()
        self._show_image()

    def _load_thumbnails(self):
        for w in self.thumb_frame.winfo_children():
            w.destroy()

        self.thumb_refs.clear()

        for i, path in enumerate(self.images):
            img = Image.open(path)
            img.thumbnail(self.THUMB_SIZE)
            tk_img = ImageTk.PhotoImage(img)
            self.thumb_refs.append(tk_img)

            btn = tk.Button(
                self.thumb_frame,
                image=tk_img,
                command=lambda idx=i: self._select(idx),
                relief=tk.FLAT
            )
            btn.grid(row=0, column=i, padx=5)

    def _select(self, i):
        self.index = i
        self._show_image()

    def _show_image(self):
        img = Image.open(self.images[self.index])
        img.thumbnail(self.PREVIEW_SIZE)
        self.preview_img = ImageTk.PhotoImage(img)
        self.preview.config(image=self.preview_img)

    def next_image(self):
        if not self.images:
            return
        self.index = (self.index + 1) % len(self.images)
        self._show_image()

    def prev_image(self):
        if not self.images:
            return
        self.index = (self.index - 1) % len(self.images)
        self._show_image()


if __name__ == "__main__":
    root = tk.Tk()
    ImageGalleryApp(root)
    root.mainloop()
