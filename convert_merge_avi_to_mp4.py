import moviepy.editor as mp
import tkinter as tk
from tkinter import filedialog, messagebox
import os

class VideoConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AVI to MP4 Converter and Merger")
        self.root.geometry("600x400")
        self.video_files = []

        # GUI elements
        self.label = tk.Label(root, text="Select AVI files to convert and merge")
        self.label.pack(pady=10)

        self.file_listbox = tk.Listbox(root, width=80, height=10)
        self.file_listbox.pack(pady=10)

        self.select_button = tk.Button(root, text="Select AVI Files", command=self.select_files)
        self.select_button.pack(pady=5)

        self.output_button = tk.Button(root, text="Select Output File", command=self.select_output)
        self.output_button.pack(pady=5)

        self.convert_button = tk.Button(root, text="Convert and Merge", command=self.convert_and_merge)
        self.convert_button.pack(pady=10)

        self.status_label = tk.Label(root, text="", wraplength=500)
        self.status_label.pack(pady=10)

        self.output_path = ""

    def select_files(self):
        files = filedialog.askopenfilenames(filetypes=[("AVI files", "*.avi")])
        self.video_files = list(files)
        self.file_listbox.delete(0, tk.END)
        for file in self.video_files:
            self.file_listbox.insert(tk.END, file)

    def select_output(self):
        self.output_path = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 files", "*.mp4")])
        if self.output_path:
            self.status_label.config(text=f"Output file: {self.output_path}")

    def convert_and_merge(self):
        if not self.video_files:
            messagebox.showerror("Error", "Please select at least one AVI file.")
            return
        if not self.output_path:
            messagebox.showerror("Error", "Please select an output file path.")
            return

        try:
            self.status_label.config(text="Processing... Please wait.")
            self.root.update()

            # Convert and load all videos
            video_clips = []
            for input_path in self.video_files:
                if not os.path.exists(input_path):
                    messagebox.showerror("Error", f"File not found: {input_path}")
                    return
                clip = mp.VideoFileClip(input_path)
                video_clips.append(clip)

            # Merge videos in order
            final_clip = mp.concatenate_videoclips(video_clips, method="compose")

            # Write to MP4
            final_clip.write_videofile(self.output_path, codec="libx264", audio_codec="aac", verbose=False)

            # Close all clips
            for clip in video_clips:
                clip.close()
            final_clip.close()

            self.status_label.config(text=f"Successfully converted and merged to {self.output_path}")
            messagebox.showinfo("Success", "Conversion and merging completed!")
        except Exception as e:
            self.status_label.config(text=f"Error: {str(e)}")
            messagebox.showerror("Error", f"Failed to process videos: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoConverterApp(root)
    root.mainloop()