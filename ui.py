from tkinter import ttk
import customtkinter as ctk

import frets, results

import customtkinter as ctk
import webbrowser

from tkinter import ttk, messagebox

import frets, results, pdf

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # System Settings
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        # Main Window
        self.geometry("320x205")
        self.maxsize(320, 205)

        self.geometry("320x220")
        self.maxsize(320, 220)
        self.resizable(0,0)
        
        self.grid_columnconfigure(0, weight=1)
        self.title("Frets Spacing Calculator")
        self.iconbitmap("frets.ico")

        self.create_widgets()

    def create_widgets(self):

        # Unit Selector
        unit_label = ctk.CTkLabel(self, text="Input unit:")
        unit_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")

        def unit_switch_event():
            if unit_switch_var.get() == "mm":
                unit_switch.configure(text="millimetres")
            elif unit_switch_var.get() == "in":
                unit_switch.configure(text="inches")

        unit_switch_var = ctk.StringVar(value="mm")
        unit_switch = ctk.CTkSwitch(
            self,
            text="millimetres",
            progress_color="#d80000",
            fg_color="#0074e0",
            command=unit_switch_event,
            variable=unit_switch_var,
            onvalue="in",
            offvalue="mm"
        )
        unit_switch.grid(row=0, column=1, padx=5, pady=0, sticky="w")

        # Rule Selector
        rule_label = ctk.CTkLabel(self, text="Division rule:")
        rule_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")

        def rule_switch_event():
            if rule_switch_var.get() == 17.817:
                rule_switch.configure(text="17.817")
            elif rule_switch_var.get() == 18:
                rule_switch.configure(text="18")

        rule_switch_var = ctk.DoubleVar(value=17.817)
        rule_switch = ctk.CTkSwitch(
            self,
            text=17.817,
            progress_color="#d80000",
            fg_color="#0074e0",
            command=rule_switch_event,
            variable=rule_switch_var,
            onvalue=18,
            offvalue=17.817
        )
        rule_switch.grid(row=1, column=1, padx=5, pady=0, sticky="w")
        
        # Key inputs validation commands
        # Reference: https://stackoverflow.com/questions/4140437/interactively-validating-entry-widget-content-in-tkinter
        vcmd_scale = (self.register(self.validate_length), '%P')
        vcmd_frets = (self.register(self.validate_frets), '%P')

        # Scale input field
        scale_length_label = ctk.CTkLabel(self, text="Nut to bridge length:")
        scale_length_label.grid(row=3, column=0, padx=5, pady=2)


        scale_length_entry = ctk.CTkEntry(self, validate="key", validatecommand=vcmd_scale)
        scale_length_entry = ctk.CTkEntry(
            self,
            placeholder_text="max",
            validate="key",
            validatecommand=vcmd_scale
        )
        scale_length_entry.grid(
            row=4,
            column=0,
            padx=10,
            pady=5,
            sticky="e",
            columnspan=1
        )

        # Frets input field
        frets_count_label = ctk.CTkLabel(self, text="Frets count:")
        frets_count_label.grid(row=3, column=1, padx=5, pady=2)

        frets_count_entry = ctk.CTkEntry(self, validate="key", validatecommand=vcmd_frets)
        frets_count_entry = ctk.CTkEntry(self, validate="key", validatecommand=vcmd_frets)
        frets_count_entry = ctk.CTkEntry(
            self,
            placeholder_text="Max 100",
            validate="key",
            validatecommand=vcmd_frets
        )
        frets_count_entry.grid(
            row=4,
            column=1,
            padx=10,
            pady=5,
            sticky="e",
            columnspan=1
        )

        # About Hyperlink
        about = ctk.CTkLabel(self, text="About", text_color="blue", cursor="hand2")
        about.grid(row=6, column=1, padx=10, sticky="es")
        about.bind(
            "<Button-1>",
            lambda event:
            webbrowser.open_new("https://github.com/andrew-mendes/frets")
        )


        # Results Window Popup
        self.results_window = None
        def button_event():
            if self.results_window is not None:
                self.results_window.destroy()
            self.results_window = results.ResultsWindow()
            self.results_window.after(100, self.results_window.lift)

            frets_dict = frets.fret_measurer(
                unit_switch_var.get(),
                float(rule_switch_var.get()),
                float(scale_length_entry.get()),
                int(frets_count_entry.get())
            )

            tree_style = ttk.Style()
            tree_style.configure(
                'style.Treeview',
                font=('Segoe UI Variable', 14),
            )
            tree_style.configure(
                'style.Treeview.Heading',
                font=('Segoe UI Variable', 18,'bold'),
                background='yellow'
            )
            # Treeview Setup
            table = ttk.Treeview(
                self.results_window,
                style='style.Treeview',
                columns=('fret', 'mm', 'in'),
                show='headings',
                height=25,
            )

            table.column('fret', width=60, anchor='e')
            table.column('mm', width=100, anchor='center')
            table.column('in', width=100, anchor='center')

            table.heading('fret', text='fret')
            table.heading('mm', text='mm')
            table.heading('in', text='in')
            table.grid(sticky='new')

            # PDF export
            export_button = ctk.CTkButton(
                self.results_window,
                text="Export PDF",
                fg_color="#d80000",
                hover_color="#0074e0",
                text_color="white",
            )
            export_button.grid(sticky="s", pady=8)
            export_button.bind('<Button-1>', lambda event: pdf.export_pdf(frets_dict))
                        
            for item in frets_dict.items():
                table.insert(
                    parent='',
                    index=item[0],
                    values=(item[0], item[1]['mm'], item[1]['in']))

        # Calculate Button
        calculate_button = ctk.CTkButton(
            self,
            text="Calculate",
            fg_color="#d80000",
            hover_color="#0074e0",
            text_color="white",
            command=button_event,
        )
        calculate_button.grid(
            row=5,
            column=0,
            padx=10,
            pady=10,
            columnspan=2
        )
        # Submits input with Enter press regardless of button focus
        self.bind_all('<Return>', lambda event: calculate_button.invoke())

    # Numeric inputs validation
    def validate_length(self, value):
        if len(value) <= 5 and value.isdigit() or \
            (value.count('.') == 1 and value.replace('.', '').isdigit()) or \
                value == "":
            return True
        else:
            return False
    
    def validate_frets(self, value):
        if value.isdigit() or value == "":
            return True
        else:
            return False
        
        

# Handles closing confirmation and prevents errors
def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        app.destroy()

if __name__ == '__main__':
    app = App()
    app.protocol("WM_DELETE_WINDOW", on_closing)
    app.mainloop()