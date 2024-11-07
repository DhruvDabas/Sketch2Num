# import tkinter as tk

# def on_enter(event):
#     label.config(fg="yellow")  # Change color on hover

# def on_leave(event):
#     label.config(fg="black")  # Revert color

# root = tk.Tk()

# button = tk.Button(root)
# button.pack(side='left')

# label = tk.Label(button, text="Hover over me!", font=("Arial", 20))
# label.pack(pady=20)

# label.bind("<Enter>", on_enter)
# label.bind("<Leave>", on_leave)

# root.mainloop()

# import os
# os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"
# from tkinter import *
# import cv2 
# from PIL import Image, ImageTk 
  
# # Define a video capture object 
# vid = cv2.VideoCapture(0) 
  
# # Declare the width and height in variables 
# width, height = 800, 600
  
# # Set the width and height 
# vid.set(cv2.CAP_PROP_FRAME_WIDTH, width) 
# vid.set(cv2.CAP_PROP_FRAME_HEIGHT, height) 
  
# # Create a GUI app 
# app = Tk() 
  
# # Bind the app with Escape keyboard to 
# # quit app whenever pressed 
# app.bind('<Escape>', lambda e: app.quit()) 
  
# # Create a label and display it on app 
# label_widget = Label(app) 
# label_widget.pack() 
  
# # Create a function to open camera and 
# # display it in the label_widget on app 
# def open_camera(): 
  
#     # Capture the video frame by frame 
#     _, frame = vid.read() 
  
#     # Convert image from one color space to other 
#     opencv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA) 
  
#     # Capture the latest frame and transform to image 
#     captured_image = Image.fromarray(opencv_image) 
  
#     # Convert captured image to photoimage 
#     photo_image = ImageTk.PhotoImage(image=captured_image) 
  
#     # Displaying photoimage in the label 
#     label_widget.photo_image = photo_image 
  
#     # Configure image in the label 
#     label_widget.configure(image=photo_image) 
  
#     # Repeat the same process after every 10 seconds 
#     label_widget.after(10, open_camera) 
  
  
# # Create a button to open the camera in GUI app 
# button1 = Button(app, text="Open Camera", command= lambda: open_camera()) 
# button1.pack() 
  
# # Create an infinite loop for displaying app on screen 
# app.mainloop() 

# import os
# os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"

# import cv2

# cap = cv2.VideoCapture(0)

# while True:
#     ret, frame = cap.read()
#     cv2.imshow("Frame", frame)

#     key = cv2.waitKey(1)
#     if key == ord("q"):
#         break

# cap.release()
# cv2.destroyAllWindows()



from PIL import Image, ImageDraw
import customtkinter as ctk

# Load your image and crop it to only include the circular part
def crop_to_circle(image_path):
    img = Image.open(image_path).convert("RGBA")
    size = min(img.size)  # Take the smaller dimension to make it square

    # Center the circle crop
    left = (img.width - size) // 2
    top = (img.height - size) // 2
    right = left + size
    bottom = top + size
    img = img.crop((left, top, right, bottom))

    # Create a mask to make it circular
    mask = Image.new("L", (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size, size), fill=255)

    # Apply mask to make the image circular
    circular_img = Image.new("RGBA", (size, size))
    circular_img.paste(img, (0, 0), mask)
    return circular_img

# Convert the cropped circular image to CTkImage
cropped_image = crop_to_circle("Images\Red.png")
Images = ctk.CTkImage(light_image=cropped_image, size=(80, 80))  # Adjust size as needed

# Set up customtkinter and create the button
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")
app = ctk.CTk()

Color_Button = ctk.CTkButton(
    master=app,
    width=80,  # Set to match image dimensions
    height=10,
    text='',
    image=Images,
    border_color="gray",  # Customize border color
    border_width=4,
    corner_radius=40,  # Half of width/height to make it circular
    fg_color="transparent",
    hover=False
)

Color_Button.pack(pady=20, padx=20)

app.mainloop()


