# TODO:
# [ ] - 4 pictures per page (arranged nicely)
# [ ] - better temp orary files and definitely better output location


from tkinter import filedialog
import csv
import tkinter as tk
from os import listdir, path, makedirs
from pylatex import Document, Figure, SubFigure, HFill, NoEscape, Command, Package


class LaTeXBuilder:
    def __init__(self):
        self.images = []
        self.imagemax = (500,500)
        self.geometry_options = {'tmargin':"2cm", 'lmargin':"2cm", "rmargin":"2cm", "bmargin":"2cm"}
        # the initial document setup
        self.document = Document("basic", geometry_options=self.geometry_options)

        # this is required for the occlusion of 'Figure X. ...' from the document
        self.document.packages.append(Package("subcaption"))

    # Construct the latext document by iteratively calling self.build for each row in the supplied
    # captions file
    def get_captions(self):
        with open(self.captionfile, "r") as captions:
            reader = csv.reader(captions)
            for row in reader:
                self.images.append(row)        
            # need to pass two images to this with their captions in tuples
            self.construct(self.images)

    
    def construct(self, imgs_and_caps):
        '''
        imgs_and_caps: list
            Comes in the form: [[img1, cap1], [img2, cap2], ... , [img_n, cap_n]]
        '''
        print(imgs_and_caps, '\n'*3)
        # cleaning the input by filtering empty rows
        imgs_and_caps_clean = []
        for row in imgs_and_caps:
            if row:
                imgs_and_caps_clean.append(row)
        
        print(f'Cleaned:{imgs_and_caps_clean}\n\n')

        # making the tuples to iterate through
        evens = imgs_and_caps_clean[0::2] # from element 0 to end, step=2
        odds = imgs_and_caps_clean[1::2]
        imagepairs = [(even,odd) for even,odd in zip(evens,odds)]
        
        # for image combo, create figure/subfigures
        for pair in imagepairs:
            print(pair)
            print('\n'*2)
            print(f'first:{pair[0]}')
            print('\n'*2)
            print(f'second{pair[1]}')
            if len(pair) > 1:
                self.makefigure(pair[0], pair[1])
            else:
                self.makefigure(pair[0])
    
    # used to build individual images/figures with captions
    def makefigure(self, imCap1, imCap2):
        """
        imCap1, imCap2: tuple (path_to_image: str, caption: str)
        """
        with self.document.create(Figure(position="ht")) as included_image:
            self.document.append(Command('centering'))
            self.document.append(NoEscape(r'\captionsetup[subfigure]{labelformat=empty}'))
            with self.document.create(SubFigure(position="t", width=NoEscape(r'0.45\linewidth'))) as subfig1:
                self.document.append(Command('centering'))
                print(f'imgCap1[0]: {imCap1[0][0]}')
                subfig1.add_image(imCap1[0], width=NoEscape(r'0.95\linewidth'))
                subfig1.add_caption(imCap1[1])
            self.document.append(HFill())

            # if a second image was provided for the subfigure
            if imCap2:
                with self.document.create(SubFigure(position="t", width=NoEscape(r'0.45\linewidth'))) as subfig2:
                    self.document.append(Command('centering'))
                    subfig2.add_image(imCap2[0],  width=NoEscape(r'0.95\linewidth'))
                    subfig2.add_caption(imCap2[1])
                self.document.append(HFill())
   
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

    def generate(self, initdir='./', useroutput=None):
        # user select output path
        if useroutput:
            outpath = filedialog.asksaveasfilename(initialdir=initdir, filetypes=(('PDF Documents', '*.pdf'), ("All Files", '*.*')))
            self.document.generate_pdf(
            outpath, compiler="pdflatex", clean=True, clean_tex=False
        )

        # for use without user input
        else:
            if not path.isdir("./latex"):
                makedirs("./latex")
            self.document.generate_pdf(
                "./latex/temp", compiler="pdflatex", clean=True, clean_tex=False
            )


if __name__ == "__main__":
    tex = LaTeXBuilder()
    tex.getDir()
    tex.get_captions()
    tex.generate()

    # user select output path
# outfile = path.basename(filedialog.asksaveasfilename(title='Save PDF', initialdir='./', filetypes=(('PDF Files', '*.pdf'), ('All Files', '*.*')) ))
# # system call to generate pdf form tex document
# system(f"pdflatex ./latex/temp.tex -jobname={outfile}")
