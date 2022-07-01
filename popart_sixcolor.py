poart#!/usr/bin/python3
'''Create popart from image.

Named colors:
RED	= (255,0,0)
BLUE	= (0,0,255)
GREEN	= (0,255,0)
CYAN	= (0,255,255)
YELLOW	= (255,255,0)
MAGENTA	= (255,0,255)

Prerequisite:
    Pillow (PIL fork)

Ref.:
    https://pillow.readthedocs.io
'''
# pylint: disable=invalid-name
# pylint: disable=useless-return
# pylint: disable=bad-whitespace

# Import modules.
from PIL import Image

# Set filenames.
FN_IN = "image_in.jpg"
FN_OUT = "image_out.jpg"

# Set number of cols.
NUM_COLS = 6

# Define colors.
RED	= (255 ,0 ,0)
GREEN	= (0, 255, 0)
BLUE	= (0, 0, 255)
YELLOW	= (255, 255, 0)
MAGENTA	= (255, 0, 255)
CYAN	= (0, 255, 255)

# Set array of base colors by names.
col_org = [RED, GREEN, BLUE, YELLOW, MAGENTA, CYAN]

# Initialise color array for mapping.
col = [(0,0,0) for i in range(6)]

# Set incidence table.
inc_tab = [(1, 1), (2, 1), (3, 2), (4, 3), (5, 2), (6, 3)]

# Map color tabel.
for i in inc_tab:
    idx_col = i[0] - 1
    idx_old = i[1] - 1
    col[idx_col] = col_org[idx_old]

# =====================
# Function show_image()
# =====================
def show_image(img):
    '''Show image.'''
    (wimg, himg) = (img.width, img.height)
    fac = (wimg / himg)
    (width, height) = (int(fac * 600),  600)
    img_resized = img.resize((width, height))
    img_resized.show()

# ====================
# Main script function
# ====================
def main():
    '''Main script function.'''
    # Read image.
    img_org = Image.open(FN_IN)
    # Show image.
    show_image(img_org)
    # Print mode.
    print("Mode:", img_org.mode)
    # Convert image.
    img_con = img_org.convert("P", palette=Image.Palette.ADAPTIVE, colors=NUM_COLS)
    # Convert image.
    img = img_con.convert("RGB")
    # Get width and height.
    width = img.size[0]
    height = img.size[1]
    # Set array.
    init = img.getpixel((0, 0))
    res = [init]
    # Loop over image.
    for i in range(0, width):
        for j in range(0, height):
            data = img.getpixel((i, j))
            for k in res:
                if data not in res:
                    res.append(data)
    # Print color table.
    print(col)
    # Print result.
    print(res)
    # Loop over image.
    for i in range(0, width):
        for j in range(0, height):
            data = img.getpixel((i, j))
            for k in res:
                idx_res = res.index(k)
                if data == k:
                    img.putpixel((i, j), col[idx_res])
    # Show image.
    show_image(img)
    # Save image.
    img.save(FN_OUT)
    # Return None.
    return None

# Execute script as module as well as program:
if __name__ == "__main__":
    # Call main function.
    main()
