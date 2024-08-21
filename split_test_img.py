import os
import shutil
import math

# Define the source folder where your images and txt files are located
source_folder = "datasets/HELMET/test/images"
# Define the destination folders
destination_folders = [f"images_{i}" for i in range(4)] + [
    f"labels_{i}" for i in range(4)
]

# Create destination folders if they don't exist
for folder in destination_folders:
    os.makedirs(folder, exist_ok=True)

# Get all image files and their corresponding txt files
image_files = [f for f in os.listdir(source_folder) if f.endswith((".jpg"))]


# Function to get the corresponding txt file
def get_label_file(image_file):
    return image_file.rsplit(".", 1)[0] + ".txt"


# Split image and txt files into 4 folders
num_folders = 4
for i, image_file in enumerate(image_files):
    # Calculate the folder index
    folder_index = i % num_folders

    # Define image and label file paths
    image_src = os.path.join(source_folder, image_file)
    label_src = os.path.join(source_folder, get_label_file(image_file))

    # Define destination paths
    image_dst = os.path.join(f"images_{folder_index}", image_file)
    label_dst = os.path.join(f"labels_{folder_index}", get_label_file(image_file))

    # Move the image file to the appropriate folder
    shutil.move(image_src, image_dst)

    # Move the label file to the appropriate folder
    if os.path.exists(label_src):
        shutil.move(label_src, label_dst)
    else:
        print(f"Warning: No label file for {image_file}")

print("Images and labels have been successfully split into folders.")
