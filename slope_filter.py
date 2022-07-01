#!/usr/bin/python3
'''Divides a picture with the help of a straight line equation.

The graphic output is optimised for a screen size of 1366x768 pixels. The
constant WIN_HEIGHT controls the graphic output.

The user has to change the constant FN_IN to the image the filter should be
applied. The filter then is applied to this image.

The movement in y-direction must be positive.
'''
# pylint: disable=c-extension-no-member
# pylint: disable=invalid-name
# pylint: disable=too-many-locals
# pylint: disable=broad-except

# Import the standard Python module.
import math
import traceback
import sys

# Import the third party Python modules.
import numpy as np
import cv2

# Set input filename.
FN_IN = "image_in.jpg"

# Set output filename.
FN_OUT = "image_out.jpg"

# Set border size.
BORDER_SIZE = 5

# Set border color.
BORDER_COLOR = [255, 0, 0]

# Set output constants.
BORDER = False

# Set window height.
WIN_HEIGHT = 600

# ================================
# Function ResizeWithAspectRatio()
# ================================
def ResizeWithAspectRatio(image, height=None, width=None, inter=cv2.INTER_AREA):
    '''Resize with aspect ration.'''
    # Initialse the variable dim.
    dim = None
    # If no height and no width is given return the image.
    if height is None and width is None:
        return image
    # Grab height and width of the image.
    (h, w) = image.shape[:2]
    # Resize the image.
    if width is None:
        width = int(w * height / h)
    elif height is None:
        height = int(h * width / w)
    # Set the new dimensions of image.
    dim = (width, height)
    # Return the resized image.
    return cv2.resize(image, dim, interpolation=inter)

# =====================
# Function show_image()
# =====================
def show_image(image, title="output", xpos=50, ypos=50):
    '''Show an given image on the screen.'''
    # Set the window name.
    win = "OUTPUT"
    # Create a new named window.
    cv2.namedWindow(win, cv2.WINDOW_NORMAL)
    # Resize the image for displaying.
    img_res = ResizeWithAspectRatio(image, height=WIN_HEIGHT, width=None)
    # Move the window to the new position.
    cv2.moveWindow(win, xpos, ypos)
    # Set the window title.
    cv2.setWindowTitle(win, title)
    # Display the image in the window.
    cv2.imshow(win, img_res)
    # Waiting for window to be closed.
    cv2.waitKey()
    # Destroy window.
    cv2.destroyAllWindows()

# =====================
# Function add_border()
# =====================
def add_border(image, bordersize, bordercolor):
    '''Add border to image.'''
    # Add border to image.
    img = cv2.copyMakeBorder(image,
                             top=bordersize, bottom=bordersize,
                             left=bordersize, right=bordersize,
                             borderType=cv2.BORDER_CONSTANT,
                             value=bordercolor)
    # Return the new image.
    return img

# =======================
# Function apply_filter()
# =======================
def apply_filter(img_input):
    '''Apply filter to image.'''
    # Grab rows and cols of the image.
    rows, cols = img_input.shape[:2]
    # Print rows and cols to screen.
    print("Rows:", rows, "Cols:", cols)
    # Calculate the slope.
    m = rows/cols
    # Set the movement.
    move = int(rows / 2)
    # Print the slope to screen.
    print("m", m)
    # Create output image.
    img_output = np.zeros(img_input.shape, dtype=img_input.dtype)
    # Loop over the height of the image.
    for i in range(rows):
        # Loop over the width of the image.
        for j in range(cols):
            # Calculate the offset values.
            offset_h = int(math.ceil(m * j + move))
            # Calculate new x and y values.
            if offset_h < rows:
                new_h = i - offset_h
            elif offset_h >= rows:
                new_h = i - offset_h + rows
            # Create the output image.
            img_output[i, j] = img_input[new_h, j]
    # return output image.
    return img_output

# ====================
# Main script function
# ====================
def main(fn_in, fn_out):
    '''Main script function.'''
    # Try to apply the filter to the image.
    try:
        # Read image from file.
        img_input = cv2.imread(fn_in)
        # Apply filter.
        img_output = apply_filter(img_input)
        # Add border to image.
        img_output = add_border(img_output, BORDER_SIZE, BORDER_COLOR) if BORDER else img_output
        # Display the image on the screen.
        show_image(img_output)
        # Write the image to the output file.
        cv2.imwrite(fn_out, img_output)
    except Exception as err:
        # Print error message to screen.
        print("Unknown error:", str(err))
        # Print traceback to screen.
        traceback.print_exception(*sys.exc_info())

# Execute script as program as well as module.
if __name__ == "__main__":
    # Call main script function.
    main(FN_IN, FN_OUT)
