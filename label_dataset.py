import os
import shutil

# Define the source folder containing the files
source_folder = "data/data/datasets/TRAIN/training"
# Define the folder containing the CSV files
annotations_folder = "data/data/annotation"
# Define the destination folder for the CSV files
destination_folder = "data/data/datasets/LABEL/training"

# List CSV files in the annotations folder
csv_files = [f for f in os.listdir(annotations_folder) if f.endswith(".csv")]

# List folder names in the source folder
source_folders = [
    d
    for d in os.listdir(source_folder)
    if os.path.isdir(os.path.join(source_folder, d))
]

# Create the destination folder if it doesn't exist
os.makedirs(destination_folder, exist_ok=True)

# Compare and move matching CSV files
for csv_file in csv_files:
    csv_name = os.path.splitext(csv_file)[0]  # Get the name without the .csv extension
    if csv_name in source_folders:
        src_path = os.path.join(annotations_folder, csv_file)
        dest_path = os.path.join(destination_folder, csv_file)
        shutil.move(src_path, dest_path)
        print(f"Moved: {csv_file} to {destination_folder}")

print("Operation completed.")
