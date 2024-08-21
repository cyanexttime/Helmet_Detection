import os
import shutil


def move_jpg_files(source_folder, destination_folder):
    # Check if the destination folder exists, create if not
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # Loop through all files in the source folder
    for filename in os.listdir(source_folder):
        # Check if the file has a .jpg extension
        if filename.lower().endswith(".txt"):
            source_path = os.path.join(source_folder, filename)
            destination_path = os.path.join(destination_folder, filename)

            # Move the file to the destination folder
            shutil.move(source_path, destination_path)
            print(f"Moved: {filename}")


# Define your source and destination folders
source_folder = "datasets/HELMET/valid"
destination_folder = "datasets/HELMET/valid/labels"

# Call the function to move .jpg files
move_jpg_files(source_folder, destination_folder)
