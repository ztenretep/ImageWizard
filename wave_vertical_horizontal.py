#!/usr/bin/python3
'''Add horizontal and vertical wave effect to an image.

The graphic output is optimised for a screen size of 1366x768 pixels. The
constant WIN_HEIGHT controls the graphic output.

The constant MULTIPLIER controls the amplitude of sine and cosine of the
applied wave.

The user has to change the constant FN_IN to the image the filter should be
applied. The filter then is applied to this image.

For the functionality of the script, the Python modules opencv and numpy must
be installed.

The script was tested with JPEG and PNG images so far.
'''
# pylint: disable=invalid-name
# pylint: disable=c-extension-no-member
# pylint: disable=broad-except
# pylint: disable=too-many-function-args

# Import the standard Python module.
import math

# Import the third party Python modules.
import numpy as np
import cv2

# Set input filename.
FN_IN = "image_in.jpg"

# Set output filename.
FN_OUT = "image_out.jpg"

# Set multiplier.
MULTIPLIER = 20.0

# Set window height.
WIN_HEIGHT = 600

# ================================
# Function ResizeWithAspectRatio()
# ================================
def ResizeWithAspectRatio(image, height=None, width=None, inter=cv2.INTER_AREA):
    '''Resize with aspect ration.'''
    # Initialse the variable dim.
    dim = None
    # Return image, if no height and no width is given.
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

# =======================
# Function apply_filter()
# =======================
def apply_filter(img_input, multi):
    '''Apply filter to image.'''
    # Grab rows and cols of the image.
    rows, cols = img_input.shape[:2]
    # Create output image.
    img_output = np.zeros(img_input.shape, dtype=img_input.dtype)
    # Loop over rows and cols.
    for i in range(rows):
        for j in range(cols):
            # Calculate x and y radians.
            alpha_x = 2 * math.pi * i / 180
            alpha_y = 2 * math.pi * j / 180
            # Calculate the offset values.
            offset_x = int(multi * math.sin(alpha_x))
            offset_y = int(multi * math.sin(alpha_y))
            # Calculate new x and y values.
            new_x = (i+offset_y)%rows
            new_y = (j+offset_x)%cols
            # Create the output image.
            img_output[i, j] = img_input[new_x, new_y]
    # return output image.
    return img_output

# ====================
# Main script function
# ====================
def main(multi, fn_in, fn_out):
    '''Main script function.'''
    # Try to apply the filter to the image.
    try:
        # Read image from file.
        img_input = cv2.imread(fn_in)
        # Apply filter.
        img_output = apply_filter(img_input, multi)
        # Display the image on the screen.
        show_image(img_output)
        # Write the image to the output file.
        cv2.imwrite(fn_out, img_output)
    except Exception as err:
        # Print error message to screen.
        print("Unknown error:", str(err))

# Execute script as program as well as module.
if __name__ == "__main__":
    # Call main script function.
    main(MULTIPLIER, FN_IN, FN_OUT)
