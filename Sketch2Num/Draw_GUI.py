import tkinter
import tkinter.colorchooser
import customtkinter
from PIL import ImageGrab, Image, ImageColor
import numpy as np
import Model_Connector


class Draw(customtkinter.CTkFrame):
    def __init__(self, master):
        self.Master_Frame = master
        self.Master_Frame.configure(fg_color = 'gray')

        # Grid Configuration for the Main Frame.
        self.Master_Frame.grid_columnconfigure(0, weight = 1)
        self.Master_Frame.grid_columnconfigure(1, weight = 3)
        self.Master_Frame.grid_rowconfigure(0, weight = 1)

        # Old Coordinates of Mouse Position (Initially set to None to get the current Location on press)
        self.old_x = None
        self.old_y = None
        
        # Dictionaries (ToolsColor, Width) to Hold Color and Width Value for What's InHand.
        self.ToolsColor = {
            'Pencil' : 'Black',
            'Eraser' : 'White',
            'CanvasBG' : 'Black',
        }
        self.Width = {
            'Pencil' : 30,
            'Eraser' : 100,
        }

        # What is Currently in Use.
        self.InHand = 'Pencil'
        
        # Dictionary to Access Color in the ColorPallet Frame and Variable PrevClicked to change Border Color.
        self.Color_Button_Dict = {}
        self.PrevClicked = False

        # All Images Used.
        self.Pencil = customtkinter.CTkImage(
            light_image = Image.open(r'Images\Pencil_light.png'),
            dark_image = Image.open(r'Images\Pencil_dark.png'),
            size = (40, 40)
        )

        self.Eraser = customtkinter.CTkImage(
            light_image = Image.open(r'Images\Eraser_light.png'),
            dark_image = Image.open(r'Images\Eraser_dark.png'),
            size = (40, 40)
        )

        self.Fill = customtkinter.CTkImage(
            light_image = Image.open(r'Images\Fill_light.png'),
            dark_image = Image.open(r'Images\Fill_dark.png'),
            size = (40, 40)
        )

        self.Trash = customtkinter.CTkImage(
            light_image = Image.open(r'Images\Trash_light.png'),
            dark_image = Image.open(r'Images\Trash_dark.png'),
            size = (40, 40)
        )

        
        # Menu Frame (Where pen, eraser, colorpicker resides).
        self.Menu_Frame = customtkinter.CTkFrame(self.Master_Frame, corner_radius = 0)
        self.Menu_Frame.grid(
            row = 0,
            column = 0,
            sticky = 'news'
        )

        # Canvas Frame (Where we will draw).
        self.Canvas_Frame = customtkinter.CTkFrame(self.Master_Frame, fg_color = 'white')
        self.Canvas_Frame.grid(
            row = 0,
            column = 1,
            sticky = 'news'
        )

        # Create tkinter.Canvas() inside Canvas Frame.
        self.Canvas = tkinter.Canvas(master = self.Canvas_Frame, bg = 'white')
        self.Canvas.pack(fill = 'both', expand = True)

        # KeyBinds to Draw on Mouse Click with Motion.
        self.Canvas.bind('<B1-Motion>', self.Paint)
        self.Canvas.bind('<ButtonRelease-1>', self.Reset)

        # Creating All the Widgets.
        self.MenuWidgets()

 # 1. Handles Painting.       
    def Paint(self, Coordinates):
        # if old_x, old_y are None then skip.
        if self.old_x and self.old_y:
            self.Canvas.create_line(
                self.old_x,
                self.old_y,
                Coordinates.x,
                Coordinates.y,
                width = self.Width.get(self.InHand),
                fill = self.ToolsColor.get(self.InHand),
                capstyle = 'round',
                smooth = True,
                tags = self.InHand
            )

        # Set the Old Mouse Coordinates to New Ones.
        self.old_x = Coordinates.x
        self.old_y = Coordinates.y

    def Reset(self, Coordinates):
        self.old_x = None
        self.old_y = None

# 2. Makes Preparation for the Selected Tool.
    def PencilOnClick(self):
        # UnBind Fill.
        self.Canvas.unbind('<Button-1>')

        # Bind Painting Feature.
        self.Canvas.bind('<B1-Motion>', self.Paint)
        self.Canvas.bind('<ButtonRelease-1>', self.Reset)

        # Specify What's In Hand.
        self.InHand = 'Pencil'

    def EraserOnClick(self):
        # UnBind Fill.
        self.Canvas.unbind('<Button-1>')

        # Bind Painting Feature.
        self.Canvas.bind('<B1-Motion>', self.Paint)
        self.Canvas.bind('<ButtonRelease-1>', self.Reset)
    
        # Specify What's In Hand.
        self.InHand = 'Eraser'
        #self.ColorPicker.configure(state = 'disabled')

    def FillOnClick(self):
        # UnBind Painting Feature.
        self.Canvas.unbind('<B1-Motion>')
        self.Canvas.unbind('<ButtonRelease-1>')

        # Bind Fill.
        self.Canvas.bind('<Button-1>', self.ChangeCanvasBG)

        # Specify What's In Hand.
        self.InHand = 'CanvasBG'

    def ClearOnClick(self):
        self.Canvas.delete('all')

# 3. Change Width and Color of the Tools.
    def ChangeWidth(self, W):
        self.Width[self.InHand] = W

    def ColorPicker(self):
        ChooseColor = tkinter.colorchooser.askcolor(color = self.ToolsColor.get(self.InHand)) [1]     # askcolor return 2 value RGB[0], Hex[1]
        
        self.ToolsColor['Pencil'] = ChooseColor
        self.ToolsColor['CanvasBG'] = ChooseColor

    def ChangeCanvasBG(self, Coordinates):
        self.Canvas['bg'] = self.ToolsColor[self.InHand]
        self.Canvas.itemconfig('Eraser', fill = self.ToolsColor.get('CanvasBG'))

# 4. 
    def ScreenShot(self):
        x = self.Canvas.winfo_rootx()
        y = self.Canvas.winfo_rooty()
        width = self.Canvas.winfo_width()
        height = self.Canvas.winfo_height()

        # Preview Image.
        PreviewImage = ImageGrab.grab((x, y, x + width, y + height))
        PreviewImage.save('Preview.png')
        
        # To Resize the Image into a Square.
        ReSize = round((width - height)/2)

        # Taking ScreenShot of Canvas, Getting Color of Canvas & Pencil in RGB format
        ScreenShot = ImageGrab.grab((x + ReSize, y, x + width - ReSize, y + height))

        CanvasRGB = ImageColor.getcolor(self.Canvas.cget('bg'), "RGB")
        PencilRGB = ImageColor.getcolor(self.Canvas.itemcget('Pencil', 'fill'), "RGB")

        # Turning PIL.Image to np.array.
        ScreenShot = np.array(ScreenShot)

        # Color to Replace From Canvas.
        CanvasReplace = np.array(CanvasRGB) 
        PencilReplace = np.array(PencilRGB)

        # Color to Replace with.
        CanvasNew = np.array([0, 0, 0])
        PencilNew = np.array([255, 255, 255])

        # Mask That contains info on where that Colored Pixel is in the Image.
        CanvasMask = np.all(ScreenShot == CanvasReplace, axis=2)
        PencilMask = np.all(ScreenShot == PencilReplace, axis=2)

        # Replace those data points with the new color.
        ScreenShot[CanvasMask] = CanvasNew
        ScreenShot[PencilMask] = PencilNew

        # Convert the image back to PIL.Image, Resize it and Save.
        ScreenShot = Image.fromarray(ScreenShot)

        ScreenShot = ScreenShot.resize((28, 28), Image.Resampling.LANCZOS)
        ScreenShot.save('ScreenShot.png')  # Saves (28, 28) image in SKetch2Num GUI folder with as ScreenShot.png.

        self.ScreenShot_Button.forget()
        self.Predict_Button.pack(side = 'bottom', padx = 20, pady = 20)
        self.Preview_Frame.pack(side = 'bottom', padx = 20, pady = 20)
        self.Preview()


    def Predict(self):
        image_path = r'C:\Users\aryan\Downloads\Sketch2Num GUI\ScreenShot.png'
        Number_Predicted = Model_Connector.PredictImage(image_path)
        
        new_window = customtkinter.CTkToplevel()
        new_window.title("Prediction")

        label = customtkinter.CTkLabel(new_window, text=f"Predicted Answer is : {Number_Predicted}")
        label.pack(padx=20, pady=20)

        self.Predict_Button.forget()
        self.Preview_Frame.forget()
        
        self.ScreenShot_Button.pack(side = 'bottom', padx = 20, pady = 20)


    def Preview(self):
        PreviewImage = customtkinter.CTkImage(
            Image.open(r'C:\Users\aryan\Downloads\Sketch2Num GUI\Preview.png'),
            size = [250, 200]
        )

        PreviewLabel = customtkinter.CTkLabel(
            self.Preview_Frame,
            text = '',
            image = PreviewImage,
        )
        PreviewLabel.pack(padx = 0, pady = 0, side = 'top')

    def Tools(self):
        # Change Padding etc. in one place.
        padx = 5
        pady = 5
        corner_radius = 5
        border_width = 2
        border_color = 'silver'
        height = 40
        width = 40

        # Pen Icon for selecting Pen.
        self.Pencil_Button = customtkinter.CTkButton(
            master = self.Tools_Frame,
            width = width,
            height = height,
            corner_radius = corner_radius,
            border_width = border_width,
            fg_color = 'transparent',
            border_color = border_color,
            image = self.Pencil,
            text = '',
            command = self.PencilOnClick
        )
        self.Pencil_Button.pack(side = 'left', padx = padx, pady = pady)

        # Eraser Icon for Selecting Eraser.
        self.Eraser_Button = customtkinter.CTkButton(
            master = self.Tools_Frame,
            width = width,
            height = height,
            corner_radius = corner_radius,
            border_width = border_width,
            fg_color = 'transparent',
            border_color = border_color,
            image = self.Eraser,
            text = '',
            command = self.EraserOnClick
        )
        self.Eraser_Button.pack(side = 'left', padx = padx, pady = pady)

        # Fill Icon for Selecting Fill.
        self.Fill_Button = customtkinter.CTkButton(
            master = self.Tools_Frame,
            width = width,
            height = height,
            corner_radius = corner_radius,
            border_width = border_width,
            fg_color = 'transparent',
            border_color = border_color,
            image = self.Fill,
            text = '',
            command = self.FillOnClick
        )
        self.Fill_Button.pack(side = 'left', padx = padx, pady = pady)

        # Clear Icon for Clearing Screen.
        self.Clear_Button = customtkinter.CTkButton(
            master = self.Tools_Frame,
            width = width,
            height = height,
            corner_radius = corner_radius,
            border_width = border_width,
            fg_color = 'transparent',
            border_color = border_color,
            image = self.Trash,
            text = '',
            command = self.ClearOnClick
        )
        self.Clear_Button.pack(side = 'left', padx = padx, pady = pady)

    def ColorPalette(self):
        # Segmented Buttons For Color Selecting.
        Colors = ['#000000', '#7F7F7F', '#ED1C24', '#FF7F27', '#FFF200', '#FFFFFF', '#22B14C', '#00A2E8', '#A349A4', '#B5E61D']
        
        Col = Row = 0

        for Color in Colors:
            Color_Button_Name = f'Button_{Row}_{Col}'

            Color_Button = customtkinter.CTkButton(
                master = self.Colors_Frame,
                width = 50,
                height = 50,
                text = '',
                fg_color = Color,
                border_color = self.Menu_Frame.cget('fg_color'),
                border_width = 4,
                corner_radius = 10,
                hover = False,
                command = lambda color = Color : self.SelectedColorButton(color)                
            )
            Color_Button.grid(row = Row, column = Col, padx = 5, pady = 5)

            Color_Button.bind('<Enter>', lambda Event, ButtonName = Color_Button_Name: self.PaletteOnHover(ButtonName))
            Color_Button.bind('<Leave>', lambda Event, ButtonName = Color_Button_Name: self.PaletteOnLeave(ButtonName))

            self.Color_Button_Dict[Color_Button_Name] = Color_Button

            Col += 1
            if Col == 5:
                Col = 0
                Row = 1

    def MenuWidgets(self):
        # Tools Frame To Store Tool Buttons.
        self.Tools_Frame = customtkinter.CTkFrame(
            self.Menu_Frame,
            fg_color = self.Menu_Frame.cget('fg_color'),
            border_color = 'silver',
            border_width = 1,
        )
        self.Tools_Frame.pack(side = 'top')
        self.Tools()

        # Color Pallet Frame to Store Color Buttons.
        self.Colors_Frame = customtkinter.CTkFrame(
            self.Menu_Frame,
            fg_color = self.Menu_Frame.cget('fg_color'),
            border_color = 'silver',
            border_width = 1,
        )
        self.Colors_Frame.pack(side = 'top')
        self.ColorPalette()

        # Shows The Color Picked By User.
        self.ColorPicked_Button = customtkinter.CTkButton(
            self.Menu_Frame,
            width = 50,
            height = 50,
            text = '',
            fg_color = 'black',
            border_color = '#D3D3D3',
            border_width = 5,
            corner_radius = 25,
            hover = False,
        )
        self.ColorPicked_Button.pack(side = 'top')

        # Click ScreenShot of The Canvas.
        self.ScreenShot_Button = customtkinter.CTkButton(
            self.Menu_Frame,
            width = 0,
            height = 0,
            image = None,
            text = 'ScreenShot',
            font = (None, 20),
            command = self.ScreenShot
        )
        self.ScreenShot_Button.pack(side = 'bottom', padx = 20, pady = 20)

        # Preview Image for the User.
        self.Preview_Frame = customtkinter.CTkFrame(
            self.Menu_Frame,
            width = 0,
            height= 0,
            fg_color = self.Menu_Frame.cget('fg_color'),
        )

        # Run Mnist Model on the ScreenShot.
        self.Predict_Button = customtkinter.CTkButton(
            self.Menu_Frame,
            width = 0,
            height = 0,
            image = None,
            text = 'Predict',
            font = (None, 20),
            command = self.Predict
        )
                
    def SelectedColorButton(self, Color):
        self.ToolsColor['Pencil'] = Color
        self.ToolsColor['CanvasBG'] = Color
        self.ColorPicked_Button.configure(fg_color = Color)
    
    def PaletteOnHover(self, ButtonName):
        Button = self.Color_Button_Dict.get(ButtonName)
        Button.configure(border_color = '#D3D3D3')

    def PaletteOnLeave(self, ButtonName):
        Button = self.Color_Button_Dict.get(ButtonName)
        Button.configure(border_color = self.Menu_Frame.cget('fg_color'))
