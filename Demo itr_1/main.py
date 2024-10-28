import tkinter as tk
import threading # threading ka kaam krr cz button phir memory aur cpu le rhe h 

class DrawApp:
    def __init__(self, master):
        self.master = master
        
        self.canvas = tk.Canvas(master, width=980, height=680, bg="white")
        self.canvas.pack()

        self.canvas.bind("<B1-Motion>", self.paint)

        self.button_frame = tk.Frame(master)
        self.button_frame.pack(pady=10)

        #  buttons
        self.clear_button = tk.Button(self.button_frame, text="Clear", command=self.clear, width=10, height=2, padx=5)
        self.clear_button.pack(side=tk.LEFT, padx=5)

        self.predict_button = tk.Button(self.button_frame, text="Predict", command=self.predict, width=10, height=2, padx=5)
        self.predict_button.pack(side=tk.LEFT, padx=5)

    def paint(self, event):
        x, y = event.x, event.y
        self.canvas.create_oval(x-5, y-5, x+5, y+5, fill="black", outline="black")

    def clear(self):
        self.canvas.delete("all")

    def predict(self):
        pass 
    # image yha call krr skte h, ek baar pura structure discuss krr lu mei 

root = tk.Tk()
app = DrawApp(root)
root.mainloop()