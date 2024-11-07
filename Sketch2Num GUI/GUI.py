import customtkinter
from PIL import Image
import Draw_GUI
import webbrowser

customtkinter.set_appearance_mode('dark')

# This is the Main Window of the App Everything else is built on it or in it.
class MainWindow(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sketch-2-Num")  # Title Of the Main Window.
        self.geometry("1280x720")   # Dimensionality of the Main Window.
        self.minsize(width=1280, height=720)   # Min Dimensionality.
        self.maxsize(width = 1280, height = 720)    # Max Dimensionality.
        self.iconbitmap(r'Images\Sketch2Num_Dark_Icon.ico')

    # For Easy Padding size changing.
        self.padx = 10
        self.pady = 10

    # Appearance Mode Tracker.
        self.Theme = 'dark'
        self.TextColor = ('black', 'white')

    # For Deleting The Frames.
        self.Index = 0

    # NavBar Frame (Sketch-2-Num, Documentation, Creators, ..., GitHub)
        self.NavBar_Frame = customtkinter.CTkFrame(self, height = 45)
        self.NavBar_Frame.pack(
            side = 'top',
            anchor = 'w',
            padx = self.padx,
            pady = (self.pady, 0),
            fill = 'x',
            expand = False,
        )

# Images for all the Buttons

    # 1. Sketch-2-Num Button's Image
        self.Sketch2Num_Image = customtkinter.CTkImage(
            light_image = Image.open(r'Images\Sketch_2_Num_Light.png'),
            dark_image = Image.open(r'Images\Sketch_2_Num_Dark.png'),
            size = (35, 35)
        )

    # 2. GitHub Button's Image
        self.GitHub_Image = customtkinter.CTkImage(
            light_image = Image.open(r'Images\GitHub_Light.png'),
            dark_image = Image.open(r'Images\GitHub_Dark.png'),
            size = (35, 35)
        )

    # 3. Theme Button's Image
        # self.Theme_Image = customtkinter.CTkImage(
        #     light_image = Image.open(r'Images\Theme_Light.png'),
        #     dark_image = Image.open(r'Images\Theme_Dark.png'),
        #     size = (35, 35)
        # )


# NavBar Buttons.

    # 1. Sketch-2-Num Button.
        self.Sketch2Num_Button = customtkinter.CTkButton(
            master = self.NavBar_Frame,
            width = 0,
            height = 0,
            image = self.Sketch2Num_Image,
            text = 'Sketch-2-Num',
            font = (None, 20),
            command = lambda: self.Delete_Create_Frame(NewIndex = 0),
            compound = 'left',
            fg_color = self.NavBar_Frame.cget('fg_color'),
            text_color = self.TextColor
        )

    # 2. Documentation Button.
        self.Documentation_Button = customtkinter.CTkButton(
            master = self.NavBar_Frame,
            width = 0,
            height = 0,
            image = None,
            text = 'Documentation |',
            font = (None, 20),
            command = lambda: self.Delete_Create_Frame(NewIndex = 1),
            compound = 'left',
            fg_color = self.NavBar_Frame.cget('fg_color'),
            text_color = self.TextColor
        )

    # 3. About Us Button.
        self.About_Us_Button = customtkinter.CTkButton(
            master = self.NavBar_Frame,
            width = 0,
            height = 0,
            image = None,
            text = 'About Us |',
            font = (None, 20),
            command = lambda: self.Delete_Create_Frame(NewIndex = 2),
            compound = 'left',
            fg_color = self.NavBar_Frame.cget('fg_color'),
            text_color = self.TextColor
        )

    # 4. GitHub Button.
        self.GitHub_Button = customtkinter.CTkButton(
            master = self.NavBar_Frame,
            width = 0,
            height = 0,
            image = self.GitHub_Image,
            text = '|',
            font = (None, 20),
            command = self.GitHub,
            compound = 'left',
            fg_color = self.NavBar_Frame.cget('fg_color'),
            text_color = self.TextColor
        )

    # 5. Dark/Light (Theme) Toggle Button.
        self.Theme_Button = customtkinter.CTkButton(
            master = self.NavBar_Frame,
            width = 0,
            height = 0,
            image = None,
            text = 'Theme',
            font = (None, 20),
            command = self.Theme_Mode,
            compound = 'right',
            fg_color = self.NavBar_Frame.cget('fg_color'),
            text_color = self.TextColor
        )
    
    # Adding all the Buttons to the MainWindow.
        self.Theme_Button.pack(side = 'right')
        self.GitHub_Button.pack(side = 'right')
        self.About_Us_Button.pack(side = 'right')
        self.Documentation_Button.pack(side = 'right')
        self.Sketch2Num_Button.pack(side = 'left')

# Setting the Application.
        self.Mnist_Model()

# On-Click Action Functions for Buttons.

    # 1. Sketch2Num Button On-Click Action.
    def Mnist_Model(self):
        self.Sketch_Camera_Frame = customtkinter.CTkTabview(self)
        self.Sketch_Camera_Frame.pack(
            side = 'top',
            anchor = 's',
            padx = self.padx,
            pady = self.pady,
            fill = 'both',
            expand = True
        )
        
        self.tab1 = self.Sketch_Camera_Frame.add('Sketch')
        self.tab2 = self.Sketch_Camera_Frame.add('Camera')
        
        Draw_GUI.Draw(self.tab1)
        
    # 2. Documentation Button On-Click Action.
    def Documentation(self):
        self.Documentation_Frame = customtkinter.CTkFrame(self)
        self.Documentation_Frame.pack(
            side = 'top',
            anchor = 'w',
            padx = self.padx,
            pady = self.pady,
            fill = 'both',
            expand = True
        )

        self.button = customtkinter.CTkButton(self.Documentation_Frame, text='Documentation Frame!')
        self.button.pack(side='top')

    # 3. About Us Button On-Click Action.
    def About_Us(self):
        self.About_Us_Frame = customtkinter.CTkFrame(self)
        self.About_Us_Frame.pack(
            side = 'top',
            anchor = 'w',
            padx = self.padx,
            pady = self.pady,
            fill = 'both',
            expand = True
        )

        self.button = customtkinter.CTkButton(self.About_Us_Frame, text='About Us Frame!')
        self.button.pack(side='top')
    
    # 4. GitHub Button On-Click Action.
    def GitHub(self):
        webbrowser.open("https://stackoverflow.com/questions/47926088/how-to-get-webbrowser-module-for-python-3-6-using-pip")
    
    # 5. Theme Mode Button On-Click Action.
    def Theme_Mode(self):
        if self.Theme == 'dark':
            customtkinter.set_appearance_mode('light')
            self.Theme = 'light'
            self.iconbitmap(r'Images\Sketch2Num_Light_Icon.ico')
            
        elif self.Theme == 'light':
            customtkinter.set_appearance_mode('dark')
            self.Theme = 'dark'
            self.iconbitmap(r'Images\Sketch2Num_Dark_Icon.ico')


# Manages Deletion and Creation of Frames when Clicked.

    def Delete_Create_Frame(self, NewIndex):

    # Delete The Old Frame On Screen.
        if self.Index == 0:
            self.Sketch_Camera_Frame.forget()
        elif self.Index == 1:
            self.Documentation_Frame.forget()
        elif self.Index == 2:
            self.About_Us_Frame.forget()

    # Create New Frame On Screen.
        self.Funcs = {          # Dictionary That Contains all the Functions.
            0: self.Mnist_Model,
            1: self.Documentation,
            2: self.About_Us,
        }

        Create_Frame = self.Funcs.get(NewIndex)
        Create_Frame()

        self.Index = NewIndex


if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
