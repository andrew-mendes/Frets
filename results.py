import customtkinter as ctk

class ResultsWindow(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.geometry("260x400")
        self.maxsize(260, 400)
        self.resizable(0,0)
        self.grid_columnconfigure(0, weight=1)
        self.title("Results")

        # Dealing with customtkinter's TopLevel Window's default icon bug:
        # https://stackoverflow.com/questions/75825190/how-to-put-iconbitmap-on-a-customtkinter-toplevel
        self.after(200, lambda: self.iconbitmap("frets.ico"))