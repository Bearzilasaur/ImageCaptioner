# ImageCaptioner
Image captioner with tkinter and LaTeX written in python


# Structure

There are two programs:

1. The captioner
    - Shows thumbnails of images and allow you to caption them.
    - Provides the option to export caption or directly call program 2.
2. The PDF Builder
    - If run from program 1 (The Captioner) then it directly generates a pdf whereve the user saves it to.
    - If run separately, the user selects an exported csv of captions which it will use to generate the pdf. 

# How to Use
**NOTE:** It is recommended to export the captions.csv after each captioning session. If you have any issues with the caption, then the captions.csv file can be edited like a normal csv. Then the PDF Builder can be run separately.

## The Captioner
Double click the captioner.
In the bottom left of the screen you will have the option to load either a directory of images, or select images from within a directory. **WARNING: All images must come from the same directory.**
The caption can be written in the text box, then click **Save and Next** to save the caption and move to the next image.
Once this process is completed the image section will go **blank**. 
Now you can save the captions to the directory with the images that were captioned in this session.
Lastly, you have the option to directly generate the final pdf using the **PDF Builder**.

## The PDF Builder
*Note: The pdf builder is based on pylatex and LaTeX*
Double click the builder.
Now you can choose a directory which contains the images which were captioned, and the captions.csv file that you have previously exported.
The PDF Builder will then construct the pdf.


