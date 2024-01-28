import tkinter as tk
from tkinter import messagebox
import cv2
from PIL import Image, ImageTk
class CameraApp:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)

        # Flag to indicate if the camera is active
        self.camera_active = False

        # Add an opening animation screen
        self.opening_screen = tk.Canvas(window, bg="white", width=600, height=400)
        self.opening_screen.pack(fill=tk.BOTH, expand=True)

        # Load your logo image
        self.logo_image_path = "drone-logo.png"
        self.logo_alpha = 0
        self.fade_in_speed = 10  # Adjust fading speed

        # Schedule the opening of the camera after 2 seconds
        self.window.after(2000, self.animate_logo)

        self.vid = None  # Initialize vid variable

        self.window.mainloop()

    def animate_logo(self):
        try:
            print("Attempting to load logo image...")
            # Load the logo image
            self.logo_image = Image.open(self.logo_image_path)

            print("Logo image loaded successfully.")

            # Adjust alpha channel if it has one
            if self.logo_image.mode == "RGBA":
                logo_with_alpha = self.logo_image
            else:
                # Convert to RGBA mode (add alpha channel)
                logo_with_alpha = self.logo_image.convert("RGBA")

            # Create a new image with adjusted alpha channel
            logo_with_alpha.putalpha(self.logo_alpha)

            # Create PhotoImage from the modified image
            self.logo_photo_image = ImageTk.PhotoImage(logo_with_alpha)

            # Get the dimensions of the canvas
            canvas_width = self.opening_screen.winfo_width()
            canvas_height = self.opening_screen.winfo_height()

            # Calculate the center coordinates for the logo image
            logo_x = canvas_width // 2
            logo_y = canvas_height // 2

            # Display the logo on the canvas
            self.logo_image_id = self.opening_screen.create_image(logo_x, logo_y, image=self.logo_photo_image,
                                                                   anchor=tk.CENTER)

            # Increase transparency until it's fully visible (alpha = 255)
            if self.logo_alpha < 255:
                self.logo_alpha += self.fade_in_speed
                if self.logo_alpha > 255:
                    self.logo_alpha = 255
                self.window.after(100, self.animate_logo)
            else:
                # Animation complete, proceed to opening the camera
                self.open_camera()
        except Exception as e:
            print("Error:", e)

    def open_camera(self):
        # Remove the opening screen and delete the logo
        self.opening_screen.destroy()
        self.opening_screen.delete(self.logo_image_id)

        # Initialize camera and canvas for video feed
        self.video_source = 0
        self.vid = cv2.VideoCapture(self.video_source)
        self.canvas = tk.Canvas(self.window)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Set camera active flag to True
        self.camera_active = True

        # Create buttons frame
        self.buttons_frame = tk.Frame(self.window)
        self.buttons_frame.pack(side=tk.BOTTOM, pady=10)

        # Create buttons
        self.create_buttons()

        self.update_camera()

    def create_buttons(self):
        # Create five buttons labeled Button One through Button Five
        for i in range(1, 6):
            button_text = f"Button {i}"
            button = tk.Button(self.buttons_frame, text=button_text, width=10, command=lambda idx=i: self.button_click(idx))
            button.grid(row=0, column=i, padx=5, pady=5, sticky='ew')

        # Create a settings button
        settings_button = tk.Button(self.buttons_frame, text="Settings", width=10, command=self.open_settings_menu)
        settings_button.grid(row=0, column=0, padx=5, pady=5, sticky='ew')

    def button_click(self, idx):
        print(f"Button {idx} clicked!")

    def snapshot(self):
        ret, frame = self.vid.read()
        if ret:
            cv2.imwrite("snapshot.png", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
            print("Snapshot saved as snapshot.png")
        else:
            print("Error capturing snapshot")

    def update_camera(self):
        if self.camera_active and self.vid.isOpened():  # Check if video capture is open
            ret, frame = self.vid.read()
            if ret:
                # Resize frame to fit window without black bars
                window_width = self.window.winfo_width()
                window_height = self.window.winfo_height() - self.buttons_frame.winfo_height()

                frame_width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
                frame_height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
                frame_aspect_ratio = frame_width / frame_height
                window_aspect_ratio = window_width / window_height

                if frame_aspect_ratio > window_aspect_ratio:
                    new_width = window_width
                    new_height = int(new_width / frame_aspect_ratio)
                else:
                    new_height = window_height
                    new_width = int(new_height * frame_aspect_ratio)

                resized_frame = cv2.resize(frame, (new_width, new_height))

                photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)))
                self.canvas.config(width=new_width, height=new_height)
                self.canvas.create_image(0, 0, image=photo, anchor=tk.NW)
                self.window.photo = photo

        self.window.after(10, self.update_camera)

    def open_settings_menu(self):
        settings_window = tk.Toplevel(self.window)
        settings_window.title("Settings Menu")

        # Example: Add labels and buttons to the settings menu
        label = tk.Label(settings_window, text="Settings Menu")
        label.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

        # Create text inputs and labels in the settings menu
        tk.Label(settings_window, text="Insert the height from your chin to your forehead in cm:").grid(row=1, column=0, padx=5, pady=5)
        self.height_var = tk.StringVar()
        tk.Entry(settings_window, textvariable=self.height_var).grid(row=1, column=1, padx=5, pady=5)

        tk.Label(settings_window, text="Insert the width from one ear to the next in cm:").grid(row=2, column=0, padx=5, pady=5)
        self.width_var = tk.StringVar()
        tk.Entry(settings_window, textvariable=self.width_var).grid(row=2, column=1, padx=5, pady=5)

        save_button = tk.Button(settings_window, text="Save Settings", command=lambda: self.save_settings(settings_window))
        save_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

    def save_settings(self, settings_window):
        height_value = self.height_var.get()
        width_value = self.width_var.get()

        print("Values before saving:")
        print("Height:", height_value)
        print("Width:", width_value)

        # Check if height and width contain only numbers
        if height_value.replace(".", "", 1).isdigit() and width_value.replace(".", "", 1).isdigit():
            messagebox.showinfo("Settings Saved", "Settings saved successfully!")
        else:
            messagebox.showerror("Invalid Input", "Please enter valid numerical values.")

        # Close the settings window after saving
        settings_window.destroy()


root = tk.Tk()
app = CameraApp(root, "Camera App")
root.mainloop()
