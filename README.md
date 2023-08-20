# Python script to prepend timestamp and move photos to YYYY-MM-DD subfolders

**Author:** Martin "Brozkeff" Malec (with the help of ChatGPT)

**License:** MIT License

## Summary

This script renames photos in the current directory based on their EXIF or filesystem creation date and time, then moves them into subfolders following the `YYYY-MM-DD` format.

The naming format after renaming is: `YYYYMMDD-HHmmss-ORIGINALFILENAME.ext`.

## Requirements

- You need to have PIL from the Pillow library installed
- This script assumes you run it in the directory with the photos
- The revert script only undoes the renaming and moving. If you had files with the same name as the folders this script creates, there will be issues.
- Using EXIF data might not always work, especially if the image doesn't have it or if it's corrupt. Always have a backup before running scripts like this on your data.
- Timestamp preservation: The os.rename method does not modify timestamps. Therefore, timestamps from the original photos should be preserved.

## Original ChatGPT (GPT-4) Prompt

Create a Python script that will batch rename filenames of photos in the current directory, create subfolders in the form  `YYYY-MM-DD` and move photos to the respective subfolders based on the date.

1. asks user whether run the script or not
2. for each photo find the creation date and time and
3. change the original name so that timestamp is prepended to the filename. Format should be `YYYYMMDD-HHmmss-ORIGINALFILENAME.ext`. Extensions should be converted to lowercase.

**Example:**

Original filename: `PXL_20230718_171616472.JPG` and new filename: `20230718-171617-PXL_20230718_171616472.jpg` for photos from a mobile phone, or original filename: `DSC_3321.JPG` and new filename: `20230709-141330-DSC_3321.jpg`  for photos from a camera. The timestamp should not be based on the original filename even though some photos have it such as the photos from Pixel phone, but rather from the EXIF if exists or filesystem creation date and time.

During the run logfile should be created and also a script should be created that could run in case this process needs to be reverted. The script should contain reverse steps = moving the files back to the original folder and renaming them back to the original filename.

Timestamps must be kept unchanged during the rename process, renamed photos must keep the timestamps of the date and time when the photo was captured, not when it was renamed!
