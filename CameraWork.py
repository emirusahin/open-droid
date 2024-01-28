import tkinter as tk
from tkinter import messagebox
import cv2
from PIL import Image, ImageTk
from djitellopy import Tello
import threading

class DroneCameraApp:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)

        # Initialize drone
        self.me = Tello()
        self.me.connect(wait_for_state=True)
        self.me.for_back_velocity = 0
        self.me.left_right_velocity = 0
        self.me.up_down_velocity = 0
        self.me.yaw_velocity = 0
        self.me.speed = 0
        self.me.streamoff()
        self.me.streamon()

        # Initialize camera and canvas for video feed
        self.vid = self.me.get_frame_read()
        self.vid = self.vid.frame
        self.canvas = tk.Canvas(self.window)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Create buttons frame
        self.buttons_frame = tk.Frame(self.window)
        self.buttons_frame.pack(side=tk.BOTTOM, pady=10)

        # Start video stream thread
        self.video_thread = threading.Thread(target=self.update_camera)
        self.video_thread.daemon = True
        self.video_thread.start()

        # Create buttons
        self.create_buttons()

        self.window.protocol("WM_DELETE_WINDOW", self.on_close)  # Handle window close event
        self.window.mainloop()

    def create_buttons(self):
        # Create five buttons labeled Button One through Button Five
        for i in range(1, 6):
            button_text = f"Button {i}"
            button = tk.Button(self.buttons_frame, text=button_text, width=10, command=lambda idx=i: self.button_click(idx))
            button.grid(row=0, column=i, padx=5, pady=5, sticky='ew')
            button.bind("<Enter>", lambda event, button=button: self.on_enter(event, button))
            button.bind("<Leave>", lambda event, button=button: self.on_leave(event, button))

        # Create a settings button
        settings_button = tk.Button(self.buttons_frame, text="Settings", width=10, command=self.open_settings_menu)
        settings_button.grid(row=0, column=0, padx=5, pady=5, sticky='ew')
        settings_button.bind("<Enter>", lambda event, button=settings_button: self.on_enter(event, button))
        settings_button.bind("<Leave>", lambda event, button=settings_button: self.on_leave(event, button))

    def on_enter(self, event, button):
        button.config(bg='darkblue', width=12)  # Change background color and increase width

    def on_leave(self, event, button):
        button.config(bg='blue', width=10)  # Restore original background color and width

    def button_click(self, idx):
        print(f"Button {idx} clicked!")

    def update_camera(self):
        while True:
            frame = cv2.cvtColor(self.vid, cv2.COLOR_BGR2RGB)
            photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
            self.canvas.config(width=frame.shape[1], height=frame.shape[0])
            self.canvas.create_image(0, 0, image=photo, anchor=tk.NW)
            self.window.photo = photo

    def open_settings_menu(self):
        # Add settings menu functionality here
        pass

    def on_close(self):
        self.vid.release()
        self.me.streamoff()
        self.me.land()
        self.window.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = DroneCameraApp(root, "Drone Camera App")
    root.mainloop()
