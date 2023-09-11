import customtkinter as ctk
from path import resource_path

class ResultsWindow(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.resizable(1,1)
        self.grid_columnconfigure(0, weight=1)
        self.title("Results")

        # Dealing with customtkinter's TopLevel Window's default icon bug:
        # https://stackoverflow.com/questions/75825190/how-to-put-iconbitmap-on-a-customtkinter-toplevel
        self.after(200, lambda: self.iconbitmap(resource_path("frets.ico")))