import tkinter as tk
from tkinter import filedialog, Scale, Canvas, Scrollbar, Label, Button, Frame
from PIL import Image, ImageTk


class ImageApp:

    def __init__(self, master):
        self.master = master
        self.master.title("Image Editor")
        self.master.geometry('1000x800')

        self.original_image = None
        self.display_image = None
        self.scaled_width = None
        self.scaled_height = None

        # Labels for displaying image dimensions
        self.original_dims_label = Label(self.master, text="Original: - x -")
        self.original_dims_label.pack(pady=10)

        self.scaled_dims_label = Label(self.master, text="Scaled: - x -")
        self.scaled_dims_label.pack(pady=10)

        self.copy_controls_frame = Frame(self.master)
        self.copy_controls_frame.pack(pady=10)

        self.copy_width_button = Button(self.copy_controls_frame, text="Copy Width", command=self.copy_width)
        self.copy_width_button.pack(side=tk.LEFT, padx=5)

        self.copy_height_button = Button(self.copy_controls_frame, text="Copy Height", command=self.copy_height)
        self.copy_height_button.pack(side=tk.LEFT, padx=5)

        self.canvas_frame = tk.Frame(self.master)
        self.canvas_frame.pack(fill=tk.BOTH, expand=tk.YES, padx=20, pady=20)

        self.canvas = Canvas(self.canvas_frame, bg="gray")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.YES)

        self.v_scroll = Scrollbar(self.canvas_frame, orient="vertical", command=self.canvas.yview)
        self.v_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.h_scroll = Scrollbar(self.master, orient="horizontal", command=self.canvas.xview)
        self.h_scroll.pack(side=tk.BOTTOM, fill=tk.X, padx=20)

        self.canvas.configure(yscrollcommand=self.v_scroll.set, xscrollcommand=self.h_scroll.set)
        self.canvas.bind("<Configure>", self.on_canvas_configure)

        self.load_button = tk.Button(self.master, text="Load Image", command=self.load_image)
        self.load_button.pack(pady=10)

        # Adjust the width of the slider and add buttons for scaling
        self.zoom_control_frame = Frame(self.master)
        self.zoom_control_frame.pack(pady=10)

        self.zoom_out_button = Button(self.zoom_control_frame, text="Zoom Out", command=self.zoom_out)
        self.zoom_out_button.pack(side=tk.LEFT, padx=5)

        self.slider = Scale(self.zoom_control_frame, from_=1, to=300, orient="horizontal", label="Image Size in %",
                            length=500, command=self.update_image_size)
        self.slider.pack(side=tk.LEFT, padx=10)

        self.zoom_in_button = Button(self.zoom_control_frame, text="Zoom In", command=self.zoom_in)
        self.zoom_in_button.pack(side=tk.LEFT, padx=5)

    def reset_controls(self):
        self.slider.set(100)
        self.scaled_dims_label.config(text="Scaled: - x -")

    def on_canvas_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def load_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.original_image = Image.open(file_path)
            self.display_image = self.original_image.copy()

            # Reset controls and then set original image dimensions label
            self.reset_controls()
            self.original_dims_label.config(
                text=f"Original: {self.original_image.width} x {self.original_image.height}")
            self.update_image_size(self.slider.get())

    def update_image_size(self, scale_value):
        if self.original_image:
            scale_factor = float(scale_value) / 100.0
            new_width = int(self.original_image.width * scale_factor)
            new_height = int(self.original_image.height * scale_factor)
            self.scaled_width = new_width
            self.scaled_height = new_height
            self.display_image = self.original_image.resize((new_width, new_height))

            # Update the scaled dimensions label
            self.scaled_dims_label.config(text=f"Scaled: {new_width} x {new_height}")
            self.show_image()

    def show_image(self):
        if self.display_image:
            self.canvas.delete("all")  # Clear previous image
            tk_image = ImageTk.PhotoImage(self.display_image)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)
            self.canvas.image = tk_image
            self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def zoom_in(self):
        new_value = min(300, self.slider.get() + 1)  # Increment by 10% but limit to 300%
        self.slider.set(new_value)
        self.update_image_size(new_value)

    def zoom_out(self):
        new_value = max(1, self.slider.get() - 1)  # Decrement by 10% but don't go below 1%
        self.slider.set(new_value)
        self.update_image_size(new_value)

    def copy_width(self):
        self.master.clipboard_clear()
        self.master.clipboard_append(self.scaled_width)

    def copy_height(self):
        self.master.clipboard_clear()
        self.master.clipboard_append(self.scaled_height)


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageApp(root)
    root.mainloop()

