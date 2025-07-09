import customtkinter
from PIL import Image
import Draw_GUI
import webbrowser
import os

customtkinter.set_appearance_mode('dark')

# resolves image paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(BASE_DIR, 'Images')

def load_img(filename):
    return Image.open(os.path.join(IMAGES_DIR, filename))

class MainWindow(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sketch-2-Num")
        self.geometry("1280x720")
        self.minsize(width=1280, height=720)
        self.maxsize(width=1280, height=720)
        self.iconbitmap(os.path.join(IMAGES_DIR, 'Sketch2Num_Dark_Icon.ico'))

        self.padx = 10
        self.pady = 10
        self.Theme = 'dark'
        self.TextColor = ('black', 'white')
        self.Index = 0

        self.NavBar_Frame = customtkinter.CTkFrame(self, height=45)
        self.NavBar_Frame.pack(side='top', anchor='w', padx=self.padx, pady=(self.pady, 0), fill='x', expand=False)

        self.Sketch2Num_Image = customtkinter.CTkImage(
            light_image=load_img('Sketch_2_Num_Light.png'),
            dark_image=load_img('Sketch_2_Num_Dark.png'),
            size=(35, 35)
        )

        self.GitHub_Image = customtkinter.CTkImage(
            light_image=load_img('GitHub_Light.png'),
            dark_image=load_img('GitHub_Dark.png'),
            size=(35, 35)
        )

        self.Theme_Image = customtkinter.CTkImage(
            light_image=load_img('Theme_Light.png'),
            dark_image=load_img('Theme_Dark.png'),
            size=(35, 35)
        )

        self.Sketch2Num_Button = customtkinter.CTkButton(
            master=self.NavBar_Frame,
            image=self.Sketch2Num_Image,
            text='Sketch-2-Num',
            font=(None, 20),
            command=lambda: self.Delete_Create_Frame(NewIndex=0),
            compound='left',
            fg_color=self.NavBar_Frame.cget('fg_color'),
            text_color=self.TextColor
        )

        self.Documentation_Button = customtkinter.CTkButton(
            master=self.NavBar_Frame,
            text='Documentation |',
            font=(None, 20),
            command=lambda: self.Delete_Create_Frame(NewIndex=1),
            fg_color=self.NavBar_Frame.cget('fg_color'),
            text_color=self.TextColor
        )

        self.About_Us_Button = customtkinter.CTkButton(
            master=self.NavBar_Frame,
            text='About Us |',
            font=(None, 20),
            command=lambda: self.Delete_Create_Frame(NewIndex=2),
            fg_color=self.NavBar_Frame.cget('fg_color'),
            text_color=self.TextColor
        )

        self.GitHub_Button = customtkinter.CTkButton(
            master=self.NavBar_Frame,
            image=self.GitHub_Image,
            text='|',
            font=(None, 20),
            command=self.GitHub,
            compound='left',
            fg_color=self.NavBar_Frame.cget('fg_color'),
            text_color=self.TextColor,
            hover=False
        )

        self.Theme_Button = customtkinter.CTkButton(
            master=self.NavBar_Frame,
            image=self.Theme_Image,
            text='',
            font=(None, 20),
            command=self.Theme_Mode,
            compound='right',
            fg_color=self.NavBar_Frame.cget('fg_color'),
            text_color=self.TextColor,
            hover=False
        )

        self.Theme_Button.pack(side='right')
        self.GitHub_Button.pack(side='right')
        # self.About_Us_Button.pack(side='right')
        # self.Documentation_Button.pack(side='right')
        self.Sketch2Num_Button.pack(side='left')

        self.Mnist_Model()

    def Mnist_Model(self):
        self.Sketch_Camera_Frame = customtkinter.CTkFrame(self)
        self.Sketch_Camera_Frame.pack(
            side='top', anchor='s', padx=self.padx, pady=self.pady, fill='both', expand=True
        )
        Draw_GUI.Draw(self.Sketch_Camera_Frame)

    def Documentation(self):
        self.Documentation_Frame = customtkinter.CTkFrame(self)
        self.Documentation_Frame.pack(
            side='top', anchor='w', padx=self.padx, pady=self.pady, fill='both', expand=True
        )
        self.button = customtkinter.CTkButton(self.Documentation_Frame, text='Documentation Frame!')
        self.button.pack(side='top')

    def About_Us(self):
        self.About_Us_Frame = customtkinter.CTkFrame(self)
        self.About_Us_Frame.pack(
            side='top', anchor='w', padx=self.padx, pady=self.pady, fill='both', expand=True
        )
        self.button = customtkinter.CTkButton(self.About_Us_Frame, text='About Us Frame!')

    def GitHub(self):
        webbrowser.open("https://github.com/DhruvDabas/Sketch2Num/tree/main")

    def Theme_Mode(self):
        if self.Theme == 'dark':
            customtkinter.set_appearance_mode('light')
            self.Theme = 'light'
            self.iconbitmap(os.path.join(IMAGES_DIR, 'Sketch2Num_Light_Icon.ico'))
        else:
            customtkinter.set_appearance_mode('dark')
            self.Theme = 'dark'
            self.iconbitmap(os.path.join(IMAGES_DIR, 'Sketch2Num_Dark_Icon.ico'))

    def Delete_Create_Frame(self, NewIndex):
        if self.Index == 0:
            self.Sketch_Camera_Frame.forget()
        elif self.Index == 1:
            self.Documentation_Frame.forget()
        elif self.Index == 2:
            self.About_Us_Frame.forget()

        self.Funcs = {
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
