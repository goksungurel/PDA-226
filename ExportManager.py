import json
import os
from tkinter import filedialog, messagebox
from PIL import Image

class ExportManager:
    def __init__(self, app):
        self.app = app
    def export_album(self, album_data, tracks, cover_image):
        if not album_data or not tracks:
            messagebox.showwarning(
                "Export Error",
                "No album data to save. Please generate an album first.",
                parent=self.app
            )
            return False
        raw_name = album_data.get("album_name", "fictional_album")
        clean_name = "".join([c for c in raw_name if c.isalnum() or c in " ._-"]).strip()
        default_filename = clean_name.replace(" ", "_").lower()
        file_path = filedialog.asksaveasfilename(
            parent=self.app,
            title="Save Album Files",
            initialfile=default_filename,
            defaultextension=".json",
            filetypes=[("JSON Files", "*.json")]
        )
        if not file_path:
            return False
        base_path, _ = os.path.splitext(file_path)
        json_path = base_path + ".json"
        png_path = base_path + ".png"
        try:
            export_data = album_data.copy()
            export_data["tracks"] = tracks
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=4, ensure_ascii=False)
            if cover_image and isinstance(cover_image, Image.Image):
                cover_image.save(png_path, "PNG")
            messagebox.showinfo(
                "Success",
                f"Album saved successfully!\n\n1. {os.path.basename(json_path)}\n2. {os.path.basename(png_path)}",
                parent=self.app
            )
            return True
        except Exception as e:
            messagebox.showerror("System Error", f"Failed to save files:\n{e}", parent=self.app)
            return False