import sys
import os
from os.path import exists
from pathlib import Path
from array import array
from PIL import Image, ImageChops

import imghdr

def print_colored_text(text: str, color: str) -> None:
    colors = ["RED", "GREEN", "YELLOW"]
    print(f"\033[0;{str(colors.index(color) + 31)}m{text}\033[0m")

def check_arguments() -> None:
    if not len(sys.argv) % 2:
        quit(print_colored_text("❌ The arguments are not valid. Please use the --help flag to understand how to use this script.", "RED"))
    for i, arg in enumerate(sys.argv[1:], start=0):
        if (i % 2):
            split = arg.split('.')
            if not len(split) in range(2,4) or not split[0].isnumeric() or not split[1].isnumeric() or (len(split) == 3 and int(split[2]) not in range(0,2)):
                quit(print_colored_text("❌ '" + arg + "' is not a valid parameter! Example of a valid parameter: 10.5.0", "RED"))

def crop_image(image) -> Image:
    bg = Image.new(image.mode, image.size, image.getpixel((0,0)))
    diff = ImageChops.difference(image, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return image.crop(bbox)

def check_files() -> array:
    filesInfo = []
    for i, arg in enumerate(sys.argv[1:], start=0):
        if i % 2:
            continue
        if not exists(arg):
            quit(print_colored_text("❌ The file '"+ arg + "' does not exists!", "RED"))
        elif not imghdr.what(arg):
            quit(print_colored_text("❌ The file '"+ arg + "' does not exists!", "RED"))
        image = Image.open(arg)
        width, height = image.size
        parameters = sys.argv[i+2].split('.')
        if len(parameters) == 3 and int(parameters[2]) == 1:
            image = crop_image(image)
        filename = Path(arg).name
        data = { "filename": filename.split('.')[0],
                 "width": width,
                 "height": height,
                 "type": imghdr.what(arg),
                 "image": image,
                 "parameters": [int(el) for el in parameters] }
        filesInfo.append(data)
    return filesInfo

def create_image(images) -> None:
    if not os.path.exists("santoryupy"):
        os.mkdir("santoryupy")
    for image in images:
        folder = "./santoryupy/santoryued_" + image["filename"]
        if os.path.exists(folder):
            sfolder = folder
            z = 0
            while os.path.exists(folder):
                folder = sfolder + "_" + str(z)
                z += 1
        os.mkdir(folder)
        wPerCrop = image["width"] / image["parameters"][0]
        hPerCrop = image["height"] / image["parameters"][1]
        for i in range(1,image["parameters"][1]+1):
            top = hPerCrop * (i - 1)
            bottom = hPerCrop * i
            for j in range(1, image["parameters"][0]+1):
                filename = folder + "/" + image["filename"] + "_" + str(i) + "_" + str(j) + "." + image["type"]
                left = wPerCrop * (j - 1)
                right = wPerCrop * j
                cropped = image["image"].crop((left, top, right, bottom))
                cropped.save(filename)

def documentation() -> None:
    print_colored_text("How to launch the script:", "YELLOW")
    print_colored_text("Ex: .\santoryu.py [filename] [parameters] [filename2] [parameters2] .......\n", "YELLOW")
    print_colored_text("Parameters works like such:", "YELLOW")
    print_colored_text("[ SpritePerXColumn.SpritePerYRow.TrimWhiteSpace ]", "YELLOW")
    print_colored_text("For instance, if your sprite have 4 columns and 5 rows, your parameter will be 4.5", "YELLOW")
    print_colored_text("If you want to trim the useless whitespaces around your spritesheet, you just have to add a '.1' in your parameters, or an optional '.0' if you don't want to.", "YELLOW")
    print_colored_text("Ex: .\santoryu.py .\sprite.png 4.5 .\sprite2.png 10.9 .\sprite3.png 4.4.1 ...\n", "YELLOW")
    print_colored_text("A folder named 'santoryupy' will be created with all your spliced sprites inside.", "GREEN")

def main() -> int:
    if len(sys.argv) < 2:
        quit(print_colored_text("❌ You need to specify at least one file!", "RED"))
    if (sys.argv[1] == "--help"):
        quit(documentation())
    check_arguments()
    files = check_files()
    create_image(files)
    return 0

if __name__ == "__main__":
    main()