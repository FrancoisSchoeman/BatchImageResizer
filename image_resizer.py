import tkinter.ttk

from PIL import Image as ImagePIL
import os
from tkinter import filedialog, ttk
from tkinter import messagebox
from tkinter import *


def browse_button():
    global dirs
    global path
    global new_path
    path = filedialog.askdirectory()
    path = f"{path}/"
    new_path = f"{path}/"
    dirs = os.listdir(new_path)


def callback(selection):
    global img_format
    img_format = selection
    return img_format


def resize():
    basewidth = int(size_entry.get())
    n = 0
    for item in dirs:
        if os.path.isfile(path + item):
            try:
                im = ImagePIL.open(path + item)
            except IOError:
                print(f"Error: {item} is not an image file.")
                continue

            if im.size[0] < im.size[1]:
                img_resize = resize_landscape(im, basewidth)
                n += 1
                final_img = img_resize.transpose(ImagePIL.ROTATE_90)

                og_name = item.split(".")
                save_image(final_img, og_name, n)

            elif im.size[0] > im.size[1] or im.size[0] == im.size[1]:
                img_resize = resize_portrait(im, basewidth)
                save_image(img_resize, item.split("."), n)
    
    messagebox.showinfo("Success", "Images Resized Successfully, Check Your Folder")


def resize_landscape(im, basewidth):
    transposed = im.transpose(ImagePIL.ROTATE_270)
    wpercent = (basewidth / float(transposed.size[0]))
    hsize = int((float(transposed.size[1]) * float(wpercent)))
    if basewidth > float(transposed.size[0]):
        img_resize = transposed.resize((basewidth, hsize), ImagePIL.BOX)
    elif basewidth < float(transposed.size[0]):
        img_resize = transposed.resize((basewidth, hsize), ImagePIL.ANTIALIAS)
    return img_resize


def resize_portrait(im, basewidth):
    wpercent = (basewidth / float(im.size[0]))
    hsize = int((float(im.size[1]) * float(wpercent)))
    if basewidth != im.size[0]:
        img_resize = im.resize((basewidth, hsize), ImagePIL.ANTIALIAS)
    return img_resize


def save_image(img, og_name, n):
    global img_format
    try:
        if name_entry.get() == "":
            img.save(fr"{path}{og_name[0]} resized.{img_format}", f'{img_format.upper()}', quality=90)
        else:
            img.save(fr"{path}{name_entry.get()} ({n}).{img_format}", f'{img_format.upper()}', quality=90)
    except OSError as e:
        if img_format == "jpeg":
            img_format = "png"
            img = img.convert("RGB")
            save_image(img, og_name, n)
        else:
            print("Error: Could not save image.")



# UI Design

root = Tk()

# TODO: THIS PROGRAM REQUIRES AWTHEMES 10.3.2 | Add your absolute path to the awthemes folder
root.tk.call('lappend', 'auto_path', 'C:/Users/path/to/your/awthemes-10.3.2')
root.tk.call('package', 'require', 'awdark')

s = tkinter.ttk.Style()
s.theme_use('awdark')

root.config(bg="#414141", padx=50, pady=50)
root.title("Image Resizer")
root.iconbitmap("Images/Image Resizer Logo.ico")

button_label = ttk.Label(text='Choose Folder Where Images Are Located')
button_label.grid(row=0, column=0, padx=10, pady=10, sticky=E)

button2 = ttk.Button(text="Choose Folder", command=browse_button)
button2.grid(row=0, column=1, padx=10, pady=10, sticky=W)

size_label = ttk.Label(text='Choose Your Width, eg. 1920 (Type Width Only):')
size_label.grid(row=1, column=0, padx=10, pady=10, sticky=E)

size_entry = ttk.Entry(width=20)
size_entry.grid(row=1, column=1, padx=10, pady=10, sticky=W)

name_label = ttk.Label(text="Type the name for the images, eg. Walter's Place:")
name_label.grid(row=2, column=0, padx=10, pady=10, sticky=E)

name_entry = ttk.Entry(width=40)
name_entry.grid(row=2, column=1, padx=10, pady=10, sticky=W)

png_format = StringVar(root)
png_format.set("Choose")    # default value

tiny_format = StringVar(root)
tiny_format.set("Choose")

format_label = ttk.Label(text="Choose Your Image Format")
format_label.grid(row=3, column=0, padx=10, pady=10, sticky=E)

format_entry = ttk.OptionMenu(root, png_format, "Choose", "png", "jpeg", "tiff", "ico", "gif", "pdf", "bmp", "webp", "eps", command=callback)
format_entry.grid(row=3, column=1, padx=10, pady=10, sticky=W)

resize_button = ttk.Button(text="Resize Images", command=resize)
resize_button.grid(row=4, column=0, padx=10, pady=10, sticky=E)

mainloop()
