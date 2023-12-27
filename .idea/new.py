import tkinter as tk
from PIL import Image, ImageTk

def make_transparent(widget):
    # Set the widget background to be transparent
    widget.configure(background='systemTransparent')

# Create the main window
root = tk.Tk()

# Create a transparent label using a Canvas
canvas = tk.Canvas(root, width=200, height=100, highlightthickness=0, bd=0)
canvas.pack()

# Create an image with text
text_image = Image.new('RGBA', (200, 100), (0, 0, 0, 0))  # Transparent image
text_draw = tk.PhotoImage(master=canvas, width=200, height=100)

# Draw text on the image
text_image.paste((255, 255, 255), (0, 0, 200, 100))  # White background
text_image.putalpha(0)  # Make the image transparent
text_draw.putdata(list(text_image.getdata()))

# Create an image item on the canvas
text_item = canvas.create_image(0, 0, anchor=tk.NW, image=text_draw)

# Run the Tkinter event loop
root.mainloop()
