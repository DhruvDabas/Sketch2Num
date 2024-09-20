import tkinter
import customtkinter
from PIL import Image
import Draw_GUI

customtkinter.set_appearance_mode('dark')

# This is the Main Window of the App Everything else is built on it or in it.
class MainWindow(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sketch-2-Num")  # Title Of the Main Window.
        self.geometry("1280x720")   # Dimensionality of the Main Window.
        #self.minsize(width=1280, height=720)   # Min Dimensionality.
        self.maxsize(width=1280, height=720)    # Max Dimensionality.
        self.iconbitmap(r'Images\Sketch_2_Num Icon.ico')

    # Don't mess with these two commented code. :)
        #self.grid_columnconfigure(0, weight=1) 
        #self.grid_rowconfigure(0, weight=1)

    # For Easy Padding size changing.
        self.padx = 10
        self.pady = 10

    # For Deleting The Frames.
        self.Index = 0

    # NavBar Frame (Sketch-2-Num, Documentation, Creators, ..., GitHub)
        self.NavBar_Frame = customtkinter.CTkFrame(self, height=45, fg_color='#252525')
        self.NavBar_Frame.pack(
            side = 'top',
            anchor = 'w',
            padx = self.padx,
            pady = (self.pady, 0),
            fill = 'x',
            expand = False,
        )

    # The Second Frame Where Everything will Appear.
        self.Content_Frame = customtkinter.CTkFrame(self)
        self.Content_Frame.pack(
            side = 'top',
            anchor = 'w',
            padx = self.padx,
            pady = self.pady,
            fill = 'both',
            expand = True
        )

# Images for all the Buttons

    # 1. Sketch-2-Num Button's Image
        self.Sketch2Num_Image = customtkinter.CTkImage(
            light_image = Image.open(r'Images\Sketch_2_Num_Light.png'),
            dark_image = Image.open(r'Images\Sketch_2_Num_Dark.png'),
            size=(35, 35)
        )

    # 2. GitHub Button's Image
        self.GitHub_Image = customtkinter.CTkImage(
            light_image = Image.open(r'Images\GitHub_Light.png'),
            dark_image = Image.open(r'Images\GitHub_Dark.png'),
            size=(35, 35)
        )

        
# NavBar Buttons.

    # 1. Sketch-2-Num Button.
        self.Sketch2Num_Button = customtkinter.CTkButton(
            master = self.NavBar_Frame,
            width = 0,
            height = 0,
            image = self.Sketch2Num_Image,
            text = 'Sketch-2-Num',
            font = (None, 20),
            command = lambda: self.Delete_Create_Frame(index=0),
            compound = 'left',
            fg_color='#252525'
        )
        self.Sketch2Num_Button.pack(side='left')

    # 2. Dark/Light (Theme) Toggle Button.
        self.Theme_Button = customtkinter.CTkButton(
            master = self.NavBar_Frame,
            width = 0,
            height = 0,
            image = None,
            text = 'Theme',
            font = (None, 20),
            command = self.Theme_Mode(),
            compound = 'right',
            fg_color='#252525'
        )
        self.Theme_Button.pack(side='right')

    # 3. GitHub Button.
        self.GitHub_Button = customtkinter.CTkButton(
            master = self.NavBar_Frame,
            width = 0,
            height = 0,
            image = self.GitHub_Image,
            text = '| GitHub',
            font = (None, 20),
            command = self.GitHub(),
            compound = 'right',
            fg_color='#252525'
        )
        self.GitHub_Button.pack(side='right')

    # 4. About Us Button.
        self.About_Us_Button = customtkinter.CTkButton(
            master = self.NavBar_Frame,
            width = 0,
            height = 0,
            image = None,
            text = 'About Us',
            font = (None, 20),
            command = lambda: self.Delete_Create_Frame(index=1),
            compound = 'left',
            fg_color='#252525'
        )
        self.About_Us_Button.pack(side='right')

    # 5. Documentation Button.
        self.Documentation_Button = customtkinter.CTkButton(
            master = self.NavBar_Frame,
            width = 0,
            height = 0,
            image = None,
            text = 'Documentation |',
            font = (None, 20),
            command = lambda: self.Delete_Create_Frame(index=2),
            compound = 'left',
            fg_color='#252525'
        )
        self.Documentation_Button.pack(side='right')
       
        self.Content_Frame.forget()
        self.Mnist_Model()

# NavBar Buttons On Click
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

        self.button = customtkinter.CTkButton(self.tab1, text='Mnist Model Tab 1!', command=lambda: Draw_GUI.Start("__name__"))
        self.button.pack(side='top')

        self.button = customtkinter.CTkButton(self.tab2, text='Mnist Model Tab 2!')
        self.button.pack(side='top')

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
    
    def GitHub(self):
        pass

    def Theme_Mode(self):
        pass

    def Delete_Create_Frame(self, index):
        # Delete The Old Frame On Screen.
        if self.Index == 0:
            self.Sketch_Camera_Frame.forget()

        elif self.Index == 1:
            self.About_Us_Frame.forget()

        elif self.Index == 2:
            self.Documentation_Frame.forget()

        # Create New Frame On Screen.
        if index == 0:
            self.Mnist_Model()

        elif index == 1:
            self.Documentation()

        elif index == 2:
            self.About_Us()

        self.Index = index

        

        


# Very Important Piece of code.

        #self.Content_Frame.forget()
        #self.Content_Frame.pack()


if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
