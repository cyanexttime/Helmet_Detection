import os


def rename_files_in_directory(directory):
    # Get a list of all files in the directory
    for filename in os.listdir(directory):
        # Check if the file name follows the pattern
        if filename.startswith("BikesHelmets") and filename.endswith(".txt"):
            # Split the filename into the base name and extension
            base_name, extension = os.path.splitext(filename)
            # Replace all '.' in the base name with '_'
            new_base_name = base_name.replace(".", "_")
            # Reassemble the new filename
            new_filename = new_base_name + extension
            # Construct full file paths
            old_file = os.path.join(directory, filename)
            new_file = os.path.join(directory, new_filename)
            # Rename the file
            os.rename(old_file, new_file)
            print(f"Renamed: {old_file} to {new_file}")


# Specify the directory containing the files
directory = "D:/HocTap/Helmet_Detection/datasets/HELMET/train"

# Call the function to rename files
rename_files_in_directory(directory)
