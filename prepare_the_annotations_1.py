import os
import csv

# Define the image dimensions
image_width = 1920
image_height = 1080

# Mapping for labels to numbers
label_mapping = {
    "DNoHelmetP1NoHelmet": 0,
    "DHelmetP1Helmet": 1,
    "DHelmet": 2,
    "DNoHelmet": 3,
    "DHelmetP1NoHelmet": 4,
    "DHelmetP0NoHelmetP1NoHelmet": 5,
    "DHelmetP1NoHelmetP2NoHelmet": 6,
    "DNoHelmetP1NoHelmetP2NoHelmet": 7,
    "DHelmetP1NoHelmetP2Helmet": 8,
    "DNoHelmetP1Helmet": 9,
    "DHelmetP0NoHelmetP1NoHelmetP2Helmet": 10,
    "DNoHelmetP0NoHelmetP1NoHelmet": 11,
    "DNoHelmetP0NoHelmet": 12,
    "DHelmetP0NoHelmet": 13,
    "DNoHelmetP1HelmetP2Helmet": 14,
    "DHelmetP1HelmetP2Helmet": 15,
    "DNoHelmetP0NoHelmetP1NoHelmetP2NoHelmet": 16,
    "DHelmetP0NoHelmetP1NoHelmetP2NoHelmet": 17,
    "DHelmetP0NoHelmetP1Helmet": 18,
    "DHelmetP1HelmetP2NoHelmet": 19,
    "DNoHelmetP1NoHelmetP2NoHelmetP3NoHelmet": 20,
    "DHelmetP0Helmet": 21,
    "DNoHelmetP1NoHelmetP2Helmet": 22,
    "DHelmetP0NoHelmetP1HelmetP2Helmet": 23,
    "DHelmetP1NoHelmetP2NoHelmetP3Helmet": 24,
    "DHelmetP0HelmetP1Helmet": 25,
    "DNoHelmetP0NoHelmetP1Helmet": 26,
    "DHelmetP1NoHelmetP2NoHelmetP3NoHelmet": 27,
    "DNoHelmetP0NoHelmetP1NoHelmetP2NoHelmetP3NoHelmet": 28,
    "DHelmetP0HelmetP1NoHelmetP2Helmet": 29,
    "DHelmetP0HelmetP1NoHelmetP2NoHelmet": 30,
    "DNoHelmetP0HelmetP1NoHelmet": 31,
    "DHelmetP0HelmetP1HelmetP2Helmet": 32,
    "DHelmetP0NoHelmetP1NoHelmetP2NoHelmetP3Helmet": 33,
    "DNoHelmetP0NoHelmetP1NoHelmetP2Helmet": 34,
    "DHelmetP0NoHelmetP1NoHelmetP2NoHelmetP3NoHelmet": 35,
}


# Function to convert coordinates and dimensions to 0 to 1 grid
def convert_to_grid(x, y, w, h, img_width, img_height):
    x_grid = x / img_width
    y_grid = y / img_height
    w_grid = w / img_width
    h_grid = h / img_height
    return x_grid, y_grid, w_grid, h_grid


# Process each CSV file in the directory
input_folder = "data/data/datasets/LABEL/validation"
output_folder = "data/data/datasets/LABEL/Trying_stuff/validation"

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

for filename in os.listdir(input_folder):
    if filename.endswith(".csv"):
        input_csv = os.path.join(input_folder, filename)
        with open(input_csv, mode="r") as csv_file:
            csv_reader = csv.DictReader(csv_file)
            frame_data = {}

            # Organize data by frame_id
            for row in csv_reader:
                frame_id = row["frame_id"]
                label = row["label"]
                x = float(row["x"])
                y = float(row["y"])
                w = float(row["w"])
                h = float(row["h"])

                if frame_id not in frame_data:
                    frame_data[frame_id] = []

                frame_data[frame_id].append((label, x, y, w, h))

            # Write each frame_id data to a separate text file
            for frame_id, objects in frame_data.items():
                output_txt = os.path.join(
                    output_folder, f"{os.path.splitext(filename)[0]}_{frame_id}.txt"
                )
                with open(output_txt, mode="w") as txt_file:
                    for label, x, y, w, h in objects:
                        label_num = label_mapping.get(
                            label, -1
                        )  # Use -1 for unknown labels
                        x_grid, y_grid, w_grid, h_grid = convert_to_grid(
                            x, y, w, h, image_width, image_height
                        )
                        txt_file.write(
                            f"{label_num} {x_grid} {y_grid} {w_grid} {h_grid}\n"
                        )
