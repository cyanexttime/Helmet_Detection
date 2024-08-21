import os
import glob
import shutil


def rename_images_in_subfolders(main_folder_path, destination_folder_path):
    # Ensure the destination folder exists
    os.makedirs(destination_folder_path, exist_ok=True)

    # Get a list of all subfolders in the main folder
    subfolders = [f.path for f in os.scandir(main_folder_path) if f.is_dir()]

    # Process each subfolder
    for subfolder in subfolders:
        # Get the subfolder name
        subfolder_name = os.path.basename(subfolder)

        # Get all image files in the subfolder
        image_files = glob.glob(os.path.join(subfolder, "*"))

        # Sort files to ensure they are renamed in a consistent order
        image_files.sort()

        # Rename each image file and move it to the destination folder
        for i, file_path in enumerate(image_files, start=1):
            # Get the file extension
            file_extension = os.path.splitext(file_path)[1]

            # Create the new file name
            new_file_name = f"{subfolder_name}_{i}{file_extension}"

            # Get the full path for the new file name in the destination folder
            new_file_path = os.path.join(destination_folder_path, new_file_name)

            # Rename and move the file
            shutil.move(file_path, new_file_path)

            print(f"Renamed and moved '{file_path}' to '{new_file_path}'")


# Example usage:
# Provide the path to the main folder containing the subfolders with images
main_folder_path = "D:/HocTap/Helmet_Detection/data/data/datasets/TRAIN/validation"
# Provide the path to the destination folder where renamed images will be moved
destination_folder_path = (
    "D:/HocTap/Helmet_Detection/data/data/datasets/TRAIN/validation_1"
)

rename_images_in_subfolders(main_folder_path, destination_folder_path)
