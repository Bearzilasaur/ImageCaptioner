import tkinter as tk
import csv
from tkinter import filedialog
from PIL import ImageTk, Image
from os import mkdir, path, listdir
from typing import List, Tuple

from LaTeXBuilder import LaTeXBuilder


class ImageCaptioner(tk.Tk):
    def __init__(self, imagemax=(500, 500)):
        super().__init__()
        self.imagemax = imagemax
        self.imageIncrementer = 0
        # =========== LAYOUT ====================#

        # set the window to open to a certain size < screen size
        self.geometry(
            f"{int(self.winfo_screenwidth()*0.75)}x{int(self.winfo_screenheight()*0.75)}"
        )

        # create background and set self.canvas size to screen size
        self.canvas = tk.Canvas(
            self,
            height=self.winfo_screenheight(),
            width=self.winfo_screenwidth(),
            bg="red",
        )
        self.canvas.pack()

        # list of images iterating through
        self.dirframe = tk.Frame(self.canvas, bg="blue", padx=10, pady=5)
        self.dirframe.place(relwidth=0.2, relheight=0.8, relx=0.1, rely=0.1)

        # insert the working frame into the self.canvas (it is adaptable)
        self.iframe = tk.Frame(self.canvas, bg="green", padx=10, pady=5)
        self.iframe.place(relwidth=0.6, relheight=0.8, relx=0.325, rely=0.1)

        self.imgframe = tk.Frame(self.iframe, bg="grey", padx=10, pady=5)
        self.imgframe.place(relwidth=0.8, relheight=0.7, relx=0.1, rely=0.1)

        # add button to select files
        filebutt = tk.Button(
            self.canvas,
            text="Select Images Folder",
            padx=10,
            pady=5,
            fg="black",
            command=self.getDir,
        )
        filebutt.place(relx=0.1, rely=0.925)

        filebutt = tk.Button(
            self.canvas,
            text="Select Individual Images",
            padx=10,
            pady=5,
            fg="black",
            command=self.get_paths,
        )
        filebutt.place(relx=0.22, rely=0.925)


        # add next button
        self.nextbutt = tk.Button(
            self.iframe,
            text="Save and Next",
            padx=10,
            pady=5,
            fg="black",
            command=self.bake_caption,
        )
        self.nextbutt.place(relx=0.8, rely=0.9)

        # adding the self.caption box
        self.caption = tk.Entry(self.iframe)
        self.caption.place(relwidth=0.55, height=30, relx=0.2, rely=0.9)

        # save files locally
        self.save = tk.Button(
            self.canvas,
            text="Export captions",
            padx=10,
            pady=5,
            fg="black",
            command=self.export_captions,
        )
        self.save.place(relx=0.8, rely=0.925)

                # save files locally
        self.tex = tk.Button(
            self.canvas,
            text="Generate pdf",
            padx=10,
            pady=5,
            fg="black",
            command=self._buildLaTeX,
        )
        self.tex.place(relx=0.9, rely=0.925)
    # ================ FUNCTIONS =================#

    # get images from directory (user selects directory) DEPRECATED
    def getDir(self):
        dirpath = filedialog.askdirectory(initialdir="./",
                                                            title="Select Images Folder")
        images = [
            [path.abspath(path.join(dirpath, file))]
            for file in listdir(dirpath)
            if file.endswith((".jpeg", ".jpg"))
        ]

        self.imageIncrementer = 0
        self.numberImages = len(images)
        self.imagepaths = images
        self.workingImage = self.imagepaths[self.imageIncrementer][0],
        self.listImages(self.imagepaths)
        self.load_image(self.imagepaths[self.imageIncrementer][0], self.imagemax)

    # user select individual photos
    def get_paths(self):
        paths = filedialog.askopenfilenames(initialdir='./',
                                                                   title='Select individual images to caption...',
                                                                   filetypes = (("JPEG, JPG", "*.jp*"), ("All Files", "*.*")))
        paths = [[path.abspath(file)] for file in paths]
        print(f"paths: {paths}\n\n")
        self.imageIncrementer=0
        self.workingdir = path.dirname(paths[self.imageIncrementer][0])
        self.numberImages = len(paths)
        self.imagepaths = paths
        self.workingImage = self.imagepaths[self.imageIncrementer][0],
        self.listImages(self.imagepaths)
        self.load_image(self.imagepaths[self.imageIncrementer][0], self.imagemax)

    # function to list images in the directory frame
    def listImages(self, imagelist):
        for item in self.dirframe.winfo_children():
            item.destroy()
        for image in imagelist:
            if image[0] == self.workingImage:
                colour = "yellow"
            else:
                colour = "grey"
            label = tk.Label(self.dirframe, text=image, bg=colour)
            label.pack()

    # loads the image into the window
    def load_image(self, imagepath: str, imagemax: Tuple):
        with Image.open(imagepath) as img:
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            img.thumbnail(imagemax)
            if not path.isdir('./tempfiles'):
                mkdir('./tempfiles')
            temppath = "./tempfiles/tempthumb.jpeg"
            try:
                img.save(temppath)
            except:
                mkdir('./tempfiles')
                img.save(temppath)

        # delete old image
        for label in self.imgframe.winfo_children():
            label.destroy()

         # load the thumbnail
        img = ImageTk.PhotoImage(Image.open(temppath))
        self.image = tk.Label(self.imgframe, image=img)
        self.image.image = img
        self.image.pack()

        # checks
        print(f"\n\n\n\nself.imagepaths: {self.imagepaths}\n\n\n\n")
        for i in self.imagepaths:
            print(f"\n\n{i}\n\n")


    # get the self.caption for the image
    def bake_caption(self):
        self.captiontext = (self.caption.get())  # "1.0","end-1c") # these options make the returned string nicer
        self.imagepaths[self.imageIncrementer].append(self.captiontext)
        self.caption.delete(0, "end")  # clears the input widget

        # increment the image counter and then do the next image
        if self.imageIncrementer > self.numberImages-1:
            
            # delete old image
            for label in self.imgframe.winfo_children():
                label.destroy()
            
            print("END OF FILES")
            # # checks
            print(f"\n\n\n\nself.imagepaths: {self.imagepaths}\n\n\n\n")
            for i in self.imagepaths:
                print(f"\n\n{i}\n\n")
    
        else:
            self.imageIncrementer += 1
            self.workingImage = self.imagepaths[self.imageIncrementer][0],
            self.listImages(self.imagepaths)
            self.load_image(self.imagepaths[self.imageIncrementer][0], self.imagemax)

    # exports the self.imagepaths to csv
    def export_captions(self):
        filename = filedialog.asksaveasfilename(
            initialdir="./",
            initialfile="captions.csv",
            filetypes=(("Comma Separated Values", "*.csv"), ("All Files", "*.*")),
        )
        if not filename.endswith(".csv"):
            filename += ".csv"
        with open(filename, "w") as outfile:
            writer = csv.writer(outfile)
            for row in self.imagepaths:
                if row: # removes empty rows
                    writer.writerow(row)

    # calls the LaTeXBuilder class to build latex file directly without using LaTexBuilder gui
    def _buildLaTeX(self):
        tex = LaTeXBuilder()
        tex.construct(self.imagepaths)
        tex.generate(initdir=self.workingdir, useroutput=True)

if __name__ == "__main__":
    app = ImageCaptioner()
    app.mainloop()
