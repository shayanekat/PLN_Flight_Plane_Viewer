"""
Shayane Katchera
Main script making the GUI with python tkinter
"""

from tkinter import *
import pln_parser as pln
#%% BACKEND
# init variables
methods = (
    "from image (lowest resolution)",
    "cartopy (low resolution)",
    "file for google earth"
)

# functions
def main():
    """
    main function that is run when clicking on the button on first page
    """
    pass


#%% FRONTEND
root = Tk()
root.title("PLN file Viewer")

# firt row : pln file path
l00 = Label(root, text="pln file complete path : ")
l00.grid(row=0, column=0, padx=5, pady=5)

e01 = Entry(root)
e01.grid(row=0, column=1, padx=5, pady=5)

# second row : display method choice
l10 = Label(root, text="choose the method of display : ")
l10.grid(row=1, column=0, padx=5, pady=5)

s11 = Spinbox(root, values=methods)
s11.grid(row=1, column=1, padx=5, pady=5)

# blank space
bs0 = Label(root, text=" ")
bs0.grid(row=2, column=0)


# third row : information text
txt =  "from image : more useful for liner flights than short flight\r\n"
txt += "cartopy : same as 'from image' \r\n"
txt += "file for google earth : you need will need to enter a file name for a kml file that you will open with google earth"
l2 = Label(root, text=txt, borderwidth=2, relief=SOLID, wraplength=400)
l2.grid(row=3, columnspan=2, padx=5, pady=5)

# blank space
bs1 = Label(root, text=" ")
bs1.grid(row=4, column=0)

# fourth row : button
b31 = Button(root, text="run selected method", command=main)
b31.grid(row=5, column=1, padx=5, pady=5)

root.mainloop()