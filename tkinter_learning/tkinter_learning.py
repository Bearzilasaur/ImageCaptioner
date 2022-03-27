import tkinter as tk
import os
from PIL import Image, ImageTk

# creating the window and then the canvas that sits inside of the window
root = tk.Tk()
canvas = tk.Canvas(root, width=600, height=300)
canvas.grid(columnspan=3, rowspan=3)

imagepath='tkinter_learning\cores.png'

# open image with PIL
img = Image.open(imagepath)

# convert form png to jpg
if imagepath.endswith('.png'):
    img = img.convert('RGB')

# resizing image and maintain aspect ratio
img.thumbnail((1080,1080))

# have to save thumbnail before using
thumbpath='./tempthumbs/tempthumb.png'
try:
    img.save(thumbpath)
except:
    os.mkdir('./tempthumbs')
    img.save(thumbpath )

# turn image into tk image for display
img =ImageTk.PhotoImage(Image.open(thumbpath))

# place the image inside of a tk.Label widget
img_label = tk.Label(root, image=img)
img_label.image=img

# place the tk.Label widget (img_label) inside the canvas grid
img_label.grid(column=1, row=0)

# input title label
txt_title = tk.Label(root, text='Type caption here:').grid(row=1, column=0)

# text input labels
txt_input = tk.Entry(root)
txt_input.grid(row=1, column=1)



root.mainloop()