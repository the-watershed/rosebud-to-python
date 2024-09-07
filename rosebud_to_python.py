import os
import tkinter as tk
from tkinter import filedialog, scrolledtext

# Step 1: Create the main application window
class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Rosebud to Python Translator")
        self.geometry("600x400")

        # Create a button to select a file
        self.select_button = tk.Button(self, text="Select File", command=self.select_file)
        self.select_button.pack(pady=10)

        # Create a scrolled text widget to display the translation process
        self.text_area = scrolledtext.ScrolledText(self, wrap=tk.WORD, width=70, height=20, bg="black", fg="white")
        self.text_area.pack(pady=10)

        # Configure tags for different text styles
        self.text_area.tag_configure("filename", foreground="#00FF00")  # Bright green
        self.text_area.tag_configure("path", foreground="#FFFF00")      # Yellow

    # Step 2: File selection dialog
    def select_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.text_area.insert(tk.END, "Selected file: ", "path")
            self.text_area.insert(tk.END, f"{file_path}\n", "filename")
            self.translate_file(file_path)

    # Step 3: Read the selected file
    def read_file(self, file_path):
        with open(file_path, 'r') as file:
            return file.read()

    # Step 4: Translate the program (this is a placeholder function)
    def translate_to_python(self, rosebud_code):
        # Implement your translation logic here
        # For now, we'll just return the original code as a placeholder
        return rosebud_code

    # Step 5: Save the translated program locally
    def save_to_file(self, filename, code):
        with open(filename, 'w') as file:
            file.write(code)
        self.text_area.insert(tk.END, "Translated program saved to ", "path")
        self.text_area.insert(tk.END, f"{filename}\n", "filename")

    # Step 6: Translate the selected file and display the process
    def translate_file(self, file_path):
        rosebud_code = self.read_file(file_path)
        self.text_area.insert(tk.END, "Translating...\n")
        python_code = self.translate_to_python(rosebud_code)
        output_filename = os.path.splitext(file_path)[0] + '.py'
        self.save_to_file(output_filename, python_code)
        self.text_area.insert(tk.END, "Translation complete.\n")

# Run the application
if __name__ == "__main__":
    app = Application()
    app.mainloop()