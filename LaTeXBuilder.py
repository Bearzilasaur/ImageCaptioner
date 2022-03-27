# TODO:
# [ ] - 4 pictures per page (arranged nicely)
# [ ] - better temp orary files and definitely better output location

from distutils.command.clean import clean
import pathlib
from tkinter import filedialog
import csv
import tkinter as tk
import pathlib
from os import listdir, path, system, makedirs
from pylatex import Document, Figure, Package


class LaTeXBuilder:
    def __init__(self):
        # the initial document setup
        self.document = Document("basic")

        # this is required for the occlusion of 'Figure X. ...' from the document
        self.document.packages.append(Package("Caption", options=["labelformat=empty"]))

    # Construct the latext document by iteratively calling self.build for each row in the supplied
    # captions file
    def construct(self):
        with open(self.captionfile, "r") as captions:
            reader = csv.reader(captions)
            for i, row in enumerate(reader):
                if row:  # filter our falsy rows
                    print(f"i: {i}\n")
                    print(row[0], "\n", row[1], "\n", row[2])
                    self.build(row[0], row[2])

    # used to build individual images/figures with captions
    def build(self, imagepath, caption):
        with self.document.create(Figure(position="h")) as included_image:
            included_image.add_image(imagepath)
            included_image.add_caption(caption)

    # User select image folder to build pdf for (Must have captions.csv in it)
    def getDir(self):
        directory = filedialog.askdirectory(initialdir="./")
        if "captions.csv" not in listdir(directory):
            usr_select = tk.messagebox.askyesno(
                Title="File Error",
                message="Couldn't find captions.csv file, would you like to select one?",
            )
            if usr_select:
                captionsfile = filedialog.askopenfilename(
                    initialdir="./",
                    filetypes=(
                        ("Comma Separated Values", "*.csv"),
                        ("All Files", "*.*"),
                    ),
                )
        else:
            captionsfile = path.join(directory, "captions.csv")
        self.captionfile = captionsfile
        self.directorypath = directory

    def generate(self):
        if not path.isdir("./latex"):
            makedirs("./latex")
        self.document.generate_pdf(
            "./latex/temp", compiler="pdflatex", clean=True, clean_tex=False
        )


if __name__ == "__main__":
    tex = LaTeXBuilder()
    tex.getDir()
    tex.construct()
    tex.generate()

    # user select output path
# outfile = path.basename(filedialog.asksaveasfilename(title='Save PDF', initialdir='./', filetypes=(('PDF Files', '*.pdf'), ('All Files', '*.*')) ))
# # system call to generate pdf form tex document
# system(f"pdflatex ./latex/temp.tex -jobname={outfile}")
