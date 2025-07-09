import os
import tkinter
import tkinter.colorchooser
import customtkinter
from PIL import ImageGrab, Image, ImageColor
import numpy as np
import Model_Connector

class Draw(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color='gray')
        self.pack(fill='both', expand=True)

        self.old_x = self.old_y = None
        self.ToolsColor = {'Pencil':'black','Eraser':'white','CanvasBG':'white'}
        self.Width = {'Pencil':30,'Eraser':100}
        self.InHand='Pencil'

        self.Tools_Frame = customtkinter.CTkFrame(self)
        self.Tools_Frame.pack(side='top', fill='x')
        self.Colors_Frame = customtkinter.CTkFrame(self)
        self.Colors_Frame.pack(side='top', fill='x')

        self.ScanCanvas = tkinter.Canvas(self, bg='white')
        self.ScanCanvas.pack(side='left', fill='both', expand=True)
        self.ScanCanvas.bind('<B1-Motion>', self.on_paint)
        self.ScanCanvas.bind('<ButtonRelease-1>', self.on_reset)

        self.ColorPicked_Button = customtkinter.CTkButton(self.Tools_Frame, width=50, height=50,
                                        fg_color=self.ToolsColor['Pencil'], border_width=2,
                                        corner_radius=25, text='', command=self.pick_color)
        self.ColorPicked_Button.pack(side='right', padx=5)

        for tool, cmd in [('Pencil', self.set_pencil), ('Eraser', self.set_eraser), ('Clear', self.clear_canvas)]:
            customtkinter.CTkButton(self.Tools_Frame, text=tool, command=cmd).pack(side='left', padx=5, pady=5)

        colors=['black','gray','red','orange','yellow','white','green','cyan','magenta','lime']
        for i, c in enumerate(colors):
            customtkinter.CTkButton(self.Colors_Frame, fg_color=c, text='', command=lambda col=c: self.set_color(col),
                                    width=30, height=30).pack(side='left', padx=2, pady=2)

        self.ScreenShot_Button = customtkinter.CTkButton(self.Tools_Frame, text='Screenshot', command=self.take_screenshot)
        self.ScreenShot_Button.pack(side='right', padx=5)
        self.Predict_Button = customtkinter.CTkButton(self.Tools_Frame, text='Predict', command=self.predict, state='disabled')
        self.Predict_Button.pack(side='right', padx=5)

    def on_paint(self, e):
        if self.old_x is not None:
            self.ScanCanvas.create_line(self.old_x, self.old_y, e.x, e.y,
                                      width=self.Width[self.InHand], fill=self.ToolsColor[self.InHand], capstyle='round')
        self.old_x, self.old_y = e.x, e.y

    def on_reset(self, e):
        self.old_x = self.old_y = None

    def set_pencil(self):
        self.InHand='Pencil'

    def set_eraser(self):
        self.InHand='Eraser'

    def clear_canvas(self):
        self.ScanCanvas.delete('all')

    def pick_color(self):
        _, hexc = tkinter.colorchooser.askcolor(color=self.ToolsColor[self.InHand])
        if hexc:
            self.set_color(hexc)

    def set_color(self, col):
        self.ToolsColor['Pencil'] = self.ToolsColor['CanvasBG'] = col
        self.ColorPicked_Button.configure(fg_color=col)

    def take_screenshot(self):
        self.update_idletasks()
        x = self.ScanCanvas.winfo_rootx()
        y = self.ScanCanvas.winfo_rooty()
        w = self.ScanCanvas.winfo_width()
        h = self.ScanCanvas.winfo_height()

        img = ImageGrab.grab(bbox=(x, y, x + w, y + h))

        bg_rgb = ImageColor.getcolor(self.ScanCanvas['bg'], 'RGB')
        fg_rgb = ImageColor.getcolor(self.ToolsColor['Pencil'], 'RGB')

        arr = np.array(img)[...,:3]  # Discard alpha channel if exists

        mask_bg = np.all(arr == bg_rgb, axis=-1)
        mask_fg = np.all(arr == fg_rgb, axis=-1)

        arr[mask_bg] = [0, 0, 0]
        arr[mask_fg] = [255, 255, 255]

        img = Image.fromarray(arr).convert('L')  # Grayscale
        img28 = img.resize((28, 28), Image.Resampling.LANCZOS)

        folder = os.path.dirname(__file__)
        img28.save(os.path.join(folder, 'ScreenShot.png'))
        img.save(os.path.join(folder, 'Preview.png'))

        self.Predict_Button.configure(state='normal')

    def predict(self):
        folder = os.path.dirname(__file__)
        img_path = os.path.join(folder, 'ScreenShot.png')

        try:
            pred = Model_Connector.PredictImage(img_path)
        except Exception as e:
            pred = f"Error: {str(e)}"

        popup = customtkinter.CTkToplevel()
        popup.title("Prediction Result")
        popup.geometry("300x100")
        customtkinter.CTkLabel(popup, text=f"Prediction: {pred}", font=(None, 20)).pack(padx=20, pady=20)

        self.Predict_Button.configure(state='disabled')
