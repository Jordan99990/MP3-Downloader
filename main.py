import customtkinter
import constants as const
from download import download_yt
from PIL import Image
from sys import platform
import sys, os
from tkinter import PhotoImage
from tkinter import Listbox
from threading import *

SAVE_LOCATION = ""


class Page(customtkinter.CTkFrame):
    def __init__(self, *args, **kwargs):
        customtkinter.CTkFrame.__init__(self, *args, **kwargs)

    def show(self):
        self.lift()
    

def list_string(arr):
    if len(arr) == 1:
        return arr[0]

    joined_arr = ", ".join(arr[:-1])
    return "%s & %s" % (joined_arr, arr[-1])


class HomePage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.rowconfigure((0, 1, 2), weight=1)
        self.columnconfigure(0, weight=1)

        title = customtkinter.CTkLabel(
            self, justify="center", text="MP3 Downloader", bg_color="transparent", font=("arial bold", 20))
        title.grid(row=0, column=0, sticky="N", padx=0)

        desc = customtkinter.CTkLabel(
            self, justify="center", text="Save YouTube videos and Soundcloud music as MP3 files", font=("arial", 14))
        desc.grid(row=0, column=0, sticky="S")

        urlDesc = customtkinter.CTkLabel(
            self, justify="left", text="URL: ", font=("arial", 14))
        urlDesc.grid(row=1, column=0, sticky="WS", padx=50)

        self.inputBox = customtkinter.CTkEntry(self, height=2, width=300)
        self.inputBox.grid(row=1, column=0, sticky="S", padx=80)

        downloadBtn = customtkinter.CTkButton(
            self, text="Download", width=112, command=self.threading)
        downloadBtn.grid(row=2, column=0, sticky="N", pady=30)

    def threading(self):
        t1 = Thread(target = self.download)
        t1.start()
    
    def download(self):
        url = self.inputBox.get()
        # print(check_url(url))
        download_yt(url, SAVE_LOCATION)


class SettingsPage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.rowconfigure((0, 1, 2), weight=1)
        self.columnconfigure(0, weight=1)

        title = customtkinter.CTkLabel(
            self, justify="center", text="Settings", bg_color="transparent", font=("arial bold", 20))
        title.grid(row=0, column=0, sticky="N", padx=0)

        desc = customtkinter.CTkLabel(
            self, justify="center", text="Configure MP3 Downloader", font=("arial", 14))
        desc.grid(row=0, column=0, sticky="S")

        saveDesc = customtkinter.CTkLabel(
            self, justify="left", text="Save location: ", font=("arial", 14))
        saveDesc.grid(row=1, column=0, sticky="WS", padx=50)

        self.inputBox = customtkinter.CTkEntry(self, height=2, width=300)
        self.inputBox.grid(row=1, column=0, sticky="S", padx=80)

        with open("settings.txt", "r") as settingsFile:
            save = settingsFile.read()
            global SAVE_LOCATION
            SAVE_LOCATION = save
            self.inputBox.insert(0, save)

        downloadBtn = customtkinter.CTkButton(
            self, text="Save", width=112, command=self.update_save)
        downloadBtn.grid(row=2, column=0, sticky="N", pady=30)

    def update_save(self):
        with open("settings.txt", "w") as settingsFile:
            settingsFile.write(self.inputBox.get())
            global SAVE_LOCATION
            SAVE_LOCATION = self.inputBox.get()
            print(SAVE_LOCATION)
            
class DownloadHistory(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.rowconfigure((0, 1, 2), weight=1)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        title = customtkinter.CTkLabel(
            self, justify="center", text="Download History", font=("arial bold", 20))
        title.grid(row=0, column=0, sticky="N")

        self.listbox = Listbox (
            self, bg = '#e8e7e6',
            width = 85 
        )
        
        self.update_history()
        
        
    def update_history(self):
        self.listbox.delete(0, 'end')
        
        with open('history.txt', 'r') as file:
            pos = 0
            for line in file:
                self.listbox.insert(pos, line[:len(line) - 1])
                pos += 1
        
        self.listbox.grid(row=1, column=0, sticky="N")
    
    def show(self): # metoda da override la apelul update_history()
        # de fiecare data cand ii accesata prin DownloadHistory
        # metoda e apelata
        super().show()
        self.update_history()
        
class AboutPage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.rowconfigure((0, 1, 2), weight=1)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        title = customtkinter.CTkLabel(
            self, justify="center", text="About", font=("arial bold", 20))
        title.grid(row=0, column=0, sticky="N")

        desc = customtkinter.CTkLabel(self, justify="center", text="%s by %s" % (
            const.TITLE, list_string(const.AUTHORS)), font=("arial", 14))
        desc.grid(row=1, column=0, sticky="N")

        

class App(customtkinter.CTk):

    def __init__(self):
        super().__init__()
        self.configure_window()
        sidebar_frame = customtkinter.CTkFrame(
            self, fg_color="#ccc", corner_radius=0)
        sidebar_frame.pack(side="left", fill="both")
        page_frame = customtkinter.CTkFrame(self, corner_radius=0)
        page_frame.pack(side="left", fill="both", expand=True)
        self.load_pages(page_frame)

        sidebar_frame.rowconfigure((0, 1, 2, 3, 4), weight=1)
        sidebar_frame.columnconfigure(1, weight=1)

        mp3downloader_png = customtkinter.CTkImage(
            light_image=Image.open("assets/light/mp3downloader_lightmode.png"),
            dark_image=Image.open("assets/dark/mp3downloader_darkmode.png"),
            size=(64, 64)
        )
        mp3downloader_logo = customtkinter.CTkLabel(
            sidebar_frame, text="", image=mp3downloader_png)
        mp3downloader_logo.grid(row=0, column=0, ipady=10, pady=0, padx=14)

        btnHome = customtkinter.CTkButton(
            sidebar_frame, text="MP3 Downloader", width=112)
        btnHome.grid(row=1, column=0, ipady=10, pady=0, padx=12)
        btnHome.bind("<Button-1>", lambda e: self.homePage.show())

        btnSettings = customtkinter.CTkButton(
            sidebar_frame, text="Settings", width=112)
        btnSettings.grid(row=2, column=0, ipady=10, pady=0, padx=12)
        btnSettings.bind("<Button-1>", lambda e: self.settingsPage.show())

        btnDownloadHistory = customtkinter.CTkButton(
            sidebar_frame, text="History Download", width=112)
        btnDownloadHistory.grid(row=3, column=0, ipady=10, pady=0, padx=12)
        btnDownloadHistory.bind("<Button-1>", lambda e: self.downloadHistory.show())
        
        btnAbout = customtkinter.CTkButton(
            sidebar_frame, text="About", width=112)
        btnAbout.grid(row=4, column=0, ipady=10, pady=0, padx=12)
        btnAbout.bind("<Button-1>", lambda e: self.aboutPage.show())

    def configure_window(self):
        window_title = "MP3 Downloader by %s" % (list_string(const.AUTHORS))
        self.title(window_title)
        
        if platform == 'linux' or platform == 'linux2':
            self.iconphoto(True, PhotoImage(file=os.path.join(sys.path[0], 'assets/light/mp3downloader_lightmode.png')))
        else:
            self.iconbitmap("assets/light/mp3downloader_lightmode.ico")

        self.geometry("%dx%d" % const.WINDOW_SIZE)
        self.resizable(True, False)

    def load_pages(self, pageframe):
        self.homePage = HomePage(self)
        self.homePage.place(in_=pageframe, x=0, y=0, relwidth=1, relheight=1)

        self.settingsPage = SettingsPage(self)
        self.settingsPage.place(in_=pageframe, x=0, y=0,
                                relwidth=1, relheight=1)

        self.downloadHistory = DownloadHistory(self)
        self.downloadHistory.place(in_=pageframe, x=0, y=0, relwidth=1, relheight=1)
        
        self.aboutPage = AboutPage(self)
        self.aboutPage.place(in_=pageframe, x=0, y=0, relwidth=1, relheight=1)

        self.homePage.show()

    def update_appearance_mode(self, mode):
        if not mode in ["light", "dark", "system"]:
            return

        super()._set_appearance_mode(mode)


if __name__ == "__main__":
    app = App()
    app.mainloop()