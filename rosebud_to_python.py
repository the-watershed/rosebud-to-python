import os
import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox, ttk
from translator import translate_to_python  # Import the translate_to_python function

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Rosebud to Python Translator")
        self.geometry("800x500")

        self.top_frame = tk.Frame(self)
        self.top_frame.pack(pady=10, fill=tk.X)

        self.select_button = tk.Button(self.top_frame, text="Select File", command=self.select_file)
        self.select_button.pack(side=tk.LEFT, padx=10)

        self.file_name_box = tk.Entry(self.top_frame, bg="black", fg="#00FF00", width=50)
        self.file_name_box.pack(side=tk.LEFT, padx=10)

        self.translate_button = tk.Button(self.top_frame, text="Translate", command=self.translate_file)
        self.translate_button.pack(side=tk.LEFT, padx=10)

        self.text_area = scrolledtext.ScrolledText(self, wrap=tk.WORD, width=70, height=20, bg="black", fg="white")
        self.text_area.pack(pady=10)

        self.progress = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self, orient="horizontal", length=400, mode="determinate", variable=self.progress)
        self.progress_bar.pack(pady=10)

        self.text_area.tag_configure("filename", foreground="#00FF00")
        self.text_area.tag_configure("path", foreground="#FFFF00")

    def select_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.file_name_box.delete(0, tk.END)
            self.file_name_box.insert(0, file_path)
            self.text_area.insert(tk.END, "Selected file: ", "path")
            self.text_area.insert(tk.END, f"{file_path}\n", "filename")

    def read_file(self, file_path):
        try:
            with open(file_path, 'r') as file:
                return file.read()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read file: {e}")
            return None

    def save_to_file(self, filename, code):
        try:
            with open(filename, 'w') as file:
                file.write(code)
            self.text_area.insert(tk.END, "Translated program saved to ", "path")
            self.text_area.insert(tk.END, f"{filename}\n", "filename")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file: {e}")

    def translate_file(self):
        file_path = self.file_name_box.get()
        if not file_path:
            messagebox.showwarning("Warning", "Please select a file first.")
            return

        rosebud_code = self.read_file(file_path)
        if rosebud_code is None:
            return

        self.text_area.insert(tk.END, "Translating...\n")
        self.progress.set(0)
        self.update_idletasks()

        def log_callback(message):
            self.text_area.insert(tk.END, message)
            self.update_idletasks()

        python_code = translate_to_python(rosebud_code, log_callback)

        output_filename = os.path.splitext(file_path)[0] + '.py'
        self.save_to_file(output_filename, python_code)

        self.progress.set(100)
        self.update_idletasks()
        self.text_area.insert(tk.END, "Translation complete.\n")

if __name__ == "__main__":
    app = Application()
    app.mainloop()