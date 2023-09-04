import os
import tkinter as tk
from tkinter import filedialog
from fpdf import FPDF
from path import resource_path

def export_pdf(frets_dict):
    pdf = FPDF()
    pdf.add_page()

    # Add icon and title
    icon_width = 30
    x_left = (pdf.w - icon_width) / 2
    pdf.image(resource_path('frets_logo.png'), y=8, w=icon_width, x=x_left)
    pdf.set_font("Times", style="B", size=24)
    pdf.cell(0, 25, txt="Sizes Table", ln=2, align="C")

    # Prepare table
    pdf.set_font("Times", size=16)
    col_width = pdf.w / 4.5
    row_height = pdf.font_size * 1.5

    # Calculate x-coordinate of left edge of table
    table_width = col_width * 3
    x_left = (pdf.w - table_width) / 2
    
    # Add table headers
    pdf.set_xy(x_left, pdf.get_y())
    pdf.cell(col_width, row_height, txt="Fret", border=1)
    pdf.cell(col_width, row_height, txt="mm", border=1)
    pdf.cell(col_width, row_height, txt="in", border=1)
    pdf.ln(row_height)
    
    # Add table data
    for index, data in frets_dict.items():
        pdf.set_xy(x_left, pdf.get_y())
        pdf.cell(col_width, row_height, txt=str(index), border=1)
        pdf.cell(col_width, row_height, txt=data['mm'], border=1)
        pdf.cell(col_width, row_height, txt=data['in'], border=1)
        pdf.ln(row_height)
    pdf.output('Frets_Table.pdf')

    # Prompts user for save location and file name
    root = tk.Tk()
    root.withdraw()
    filename = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("PDF Files", "*.pdf")],
        initialfile="Frets_Table"
    )

    # Open the PDF file using the default application
    if filename:
        pdf.output(filename)
        os.startfile(filename)