#!/usr/bin/bash
#
# Description:
# The camera Canon EOS 550D saves images as JPG and CR2 files. I encountered
# the problem that I wanted to rename image data according to the naming which
# the camera uses. Therefor a distinction has to be made between CR2 and JPG
# files.
#
# An identification of the file type via the file name extensions is not a good
# option. A much better way is to use the so-called magic numbers.
#
# I identified the magic numbers with respect to the image file types .cr2 and
# .jpg, which the camera Canon EOS 550D is using.
#
# The script itself is straight forward and self explaining.
#
# Prerequisite:
# The function hexbytes uses the command xxd, The corresponding package must
# be installed.
#
# @param COUNT First number in name of first new image
#
# The user has to set the variable COUNT to his personal use.
#
# Reference Magic Numbers:
# https://en.wikipedia.org/wiki/List_of_file_signatures

# Set start number.
COUNT=8000

# Get all files by creation date.
# shellcheck disable=SC2035
FILES=$(ls -c *.*)

# Declare dictionary with magic numbers of image files.
declare -A FILE_TYPES=([CR2]="49492A00100000004352" [JPG]="FFD8FFE1457869660000")

# Initialise individual counter.
count_cr2="${COUNT}"
count_jpg="${COUNT}"

# =====================
# Function rename_image
# =====================
function rename_image {
    # Assign function arguments to variables.
    fn=$1
    ext=$2
    number=$3
    # Print original filename to screen.
    echo "Filename: ${fn}"
    # Create new filename.
    fn_new="img${number}.${ext}"
    # Print new filename to screen.
    echo "New filename:${fn_new}"
    # Rename file.
    mv -f "${fn}" "${fn_new}"
}

# =================
# Function hexbytes
# =================
function hexbytes {
    # Assign function argument to variable.
    fn=$1
    # Grab the first 12 bytes of file.
    hb=$(xxd -p -l 12 "${fn}")
    # Convert the hexbytes string to uppercase.
    hb=${hb^^}
    # Return the hexbytes.
    echo "${hb}"
}

# ==========================
# Function magic_number_cr2
# ==========================
function magic_number_cr2 {
    # Assign function argument to variable.
    hb=$1
    # Grab bytes for the magic number of cr2.
    mn_cr2=${hb:0:20}
    # Return the hexbytes.
    echo "${mn_cr2}"
}

# ==========================
# Function magic_number_jpg
# ==========================
function magic_number_jpg {
    # Assign function arguments.
    hb=$1
    # Grab bytes for the magic number of jpg.
    seq0=${hb:0:8}
    seq1=${hb:12:12}
    mn_jpg="${seq0}${seq1}"
    # Return the hexbytes.
    echo "${mn_jpg}"
}

# Ask if the files should be renamed.
read -p "Are you sure you want to rename the files?" -n 1 -r
# Exit the script if user input is false.
if [[ ! $REPLY =~ ^[JjYy]$ ]]; then
    # Exit without error.
    exit 0
fi

# Loop over all files.
for fn in ${FILES}; do
    # Grab first 12 bytes of file.
    hb=$(hexbytes "${fn}")
    # Grab bytes for the magic number of cr2.
    cr2=$(magic_number_cr2 "${hb}")
    # Grab bytes for the magic number of jpg.
    jpg=$(magic_number_jpg "${hb}")
    # Rename image file on there file types.
    if [[ "${cr2}" == "${FILE_TYPES[CR2]}" ]]; then
        # Rename image.
        rename_image "${fn}" "cr2" "${count_cr2}"
        # Increment counter.
        count_cr2=$((count_cr2+1))
    elif [[ "${jpg}" == "${FILE_TYPES[JPG]}" ]]; then
        # Rename image.
        rename_image "${fn}" "jpg" "${count_jpg}"
        # Increment counter.
        count_jpg=$((count_jpg+1))
    fi
done

# Exit without error.
exit 0
