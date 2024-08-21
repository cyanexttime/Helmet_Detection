import os
import shutil
import pandas as pd

# Load the CSV file
csv_file_path = "data/data/data_split.csv"
df = pd.read_csv(csv_file_path)

# Define the source and destination folders
source_folder = "data/data/image"
destination_folder = "data/data/datasets"

# Create the destination folders if they don't exist
sets = df["Set"].unique()

for set_name in sets:
    set_path = os.path.join(destination_folder, set_name)
    os.makedirs(set_path, exist_ok=True)

# Move files to corresponding set folders
for index, row in df.iterrows():
    video_id = row["video_id"]
    set_name = row["Set"]
    src_path = os.path.join(source_folder, video_id)
    dst_path = os.path.join(destination_folder, set_name, video_id)

    if os.path.exists(src_path):
        shutil.move(src_path, dst_path)
    else:
        print(f"Warning: {src_path} does not exist.")

print("Files have been successfully moved.")
