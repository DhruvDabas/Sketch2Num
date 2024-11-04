import tkinter as tk
from PIL import Image, ImageDraw
import torch
from torchvision.transforms import ToTensor
from model import ImageClassifier
from ImagePreprocess import preprocess_image
import tkinter.messagebox as messagebox

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Digit Recognition")

        self.canvas_width = 500
        self.canvas_height = 500
        self.canvas = tk.Canvas(root, width=self.canvas_width, height=self.canvas_height, bg='white')
        self.canvas.pack()
        self.canvas.bind("<B1-Motion>", self.paint)

        self.image = Image.new("L", (self.canvas_width, self.canvas_height), 255)  # White canvas
        self.draw = ImageDraw.Draw(self.image)

        self.btn_predict = tk.Button(root, text="Predict", command=self.predict)
        self.btn_predict.pack()

        self.btn_clear = tk.Button(root, text="Clear", command=self.clear_canvas)
        self.btn_clear.pack()

        # Load model
        self.clf = ImageClassifier()
        self.clf.load_state_dict(torch.load('model_state.pt', map_location='cpu'))
        self.clf.eval()

    def paint(self, event):
        x, y = event.x, event.y
        # Increased the pen size
        pen_size = 8
        self.canvas.create_oval(x-pen_size, y-pen_size, x+pen_size, y+pen_size, fill='black', outline='black')
        self.draw.ellipse((x-pen_size, y-pen_size, x+pen_size, y+pen_size), fill='black', outline='black')

    def clear_canvas(self):
        """Clear the drawing canvas."""
        self.canvas.delete("all")
        self.image = Image.new("L", (self.canvas_width, self.canvas_height), 255)  # Reset to a white canvas

    def predict(self):
        # Preprocess the drawn image
        img_tensor = preprocess_image(self.image)

        # Make prediction
        with torch.no_grad():
            prediction = torch.argmax(self.clf(img_tensor)).item()
        
        # Display the prediction
        messagebox.showinfo("Prediction", f'Predicted class: {prediction}')

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
