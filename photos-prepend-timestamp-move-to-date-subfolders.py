#!/usr/bin/env python3
"""
Prepend datetime to photo filenames and move photos to YYYY-MM-DD subfolders

Author: Martin Brozkeff Malec with the help of ChatGPT
Version: v2023-08-20
License: MIT License
Copyright (c) 2023 Martin Brozkeff Malec with the help of ChatGPT
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Description: This script renames photos in the current directory based on their
EXIF or filesystem creation date and time, then moves them into subfolders
following the YYYY-MM-DD format.
The naming format after renaming is: YYYYMMDD-HHmmss-ORIGINALFILENAME.ext.
If run with the -h parameter, it displays this help message.
"""

import sys

# Information variables
SCRIPT_NAME = "photos-prepend-timestamp-move-to-date-subfolders.py"
AUTHOR = "Martin Brozkeff Malec with the help of ChatGPT"
VERSION = "v2023-08-20"
LICENSE = "MIT License - https://opensource.org/licenses/MIT"

DESCRIPTION = """
This script renames photos in the current directory based on their EXIF or filesystem creation date and time, then moves them into subfolders following the YYYY-MM-DD format.
The naming format after renaming is: YYYYMMDD-HHmmss-ORIGINALFILENAME.ext.
"""

# Display script information and exit if -h parameter is used
if "-h" in sys.argv:
    print(f"Script Name: {SCRIPT_NAME}")
    print(f"Author: {AUTHOR}")
    print(f"Version: {VERSION}")
    print(f"License: {LICENSE}")
    print(DESCRIPTION)
    sys.exit(0)

# Display basic script information on every run
print(f"{SCRIPT_NAME} by {AUTHOR} - {VERSION}")


# Step 1: Importing necessary libraries
import os
import datetime
from PIL import Image

# Step 2: Confirm with the user to proceed
proceed = input("Do you want to proceed with renaming and moving photos? (yes/no): ")
if proceed.lower() not in ['y', 'yes']:
    exit("Operation aborted by the user.")

# Creating a log file and revert script
current_timestamp = datetime.datetime.now().strftime('%Y%m%dT%H%M%S')
with open(f"logfile_{current_timestamp}.txt", "w") as log, open("revert_script.py", "w") as revert_script:
    revert_script.write("# Generated on {}\nimport os\n\n".format(current_timestamp))
    
    # Step 3: Iterating through each file in the current directory
    for filename in os.listdir():
        # We are only interested in image files with typical extensions from cameras and phones
        # Pillow has limited support for HEIF/HEIC files.
        # To process metadata another library like pyheif or pillow-heif may be needed.
        # Currently not implemented and HEIF/HEIC behaviour is not tested.
        if filename.lower().endswith(('.jpg', '.jpeg', '.heif', '.heic')):
            try:
                # Open image using Pillow
                with Image.open(filename) as img:
                    # Extract creation date from EXIF or filesystem
                    exif_data = img._getexif()
                    if exif_data and 306 in exif_data:
                        # Extracting date from EXIF
                        creation_date = datetime.datetime.strptime(exif_data[306], '%Y:%m:%d %H:%M:%S')
                    else:
                        # Extracting date from filesystem as fallback
                        timestamp = os.path.getctime(filename)
                        creation_date = datetime.datetime.fromtimestamp(timestamp)
            
                # Create new filename with desired format
                new_filename = "{}-{}.{}".format(creation_date.strftime('%Y%m%d-%H%M%S'), filename.split('.')[0], filename.split('.')[1].lower())
            
                # Check if subfolder exists or not
                folder_name = creation_date.strftime('%Y-%m-%d')
                if not os.path.exists(folder_name):
                    os.mkdir(folder_name)
            
                # Step 6: Moving file to its corresponding folder
                os.rename(filename, os.path.join(folder_name, new_filename))
            
                # Logging the action
                log.write(f"Moved {filename} to {os.path.join(folder_name, new_filename)}\n")
            
                # Adding reverse action to the revert script
                revert_script.write(f"os.rename('{os.path.join(folder_name, new_filename)}', '{filename}')\n")
                
            except Exception as e:
                log.write(f"Failed processing {filename} due to {str(e)}\n")

print("Processing completed. Check logfile.txt for details and revert_script.py for undoing the changes.")
