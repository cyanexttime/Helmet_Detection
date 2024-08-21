import sys, os
import shutil
import yaml

ROOT = os.path.dirname(__file__)
DATASETS = os.path.join(ROOT, "datasets")
HELMET_ROOT = os.path.join(DATASETS, "HELMET")
TRAIN_IMG = os.path.join(HELMET_ROOT, "merge_images")
TRAIN_LABEL = os.path.join(HELMET_ROOT, "merge_labels")

YAML_ROOT = os.path.join(ROOT, "data")


NUM_CLIENTS = 4


def mergeTrainVal():

    orig_train_img = os.path.join(HELMET_ROOT, "train", "images")
    orig_train_lb = os.path.join(HELMET_ROOT, "train", "labels")
    orig_val_img = os.path.join(HELMET_ROOT, "valid", "images")
    orig_val_lb = os.path.join(HELMET_ROOT, "valid", "labels")

    dst_merge_img = os.path.join(HELMET_ROOT, "merge_images")
    dst_merge_lb = os.path.join(HELMET_ROOT, "merge_labels")

    # Remove existing directories if they exist
    if os.path.isdir(dst_merge_img) or os.path.isdir(dst_merge_lb):
        shutil.rmtree(dst_merge_img)
        shutil.rmtree(dst_merge_lb)

    # Create new directories
    os.mkdir(dst_merge_img)
    os.mkdir(dst_merge_lb)

    train_img_ids = []
    for train_img_name in os.listdir(orig_train_img):
        train_img_ids.append(train_img_name.split(".")[0])
    val_img_ids = []
    for val_img_name in os.listdir(orig_val_img):
        val_img_ids.append(val_img_name.split(".")[0])

    for train_img_id in train_img_ids:
        src_img = os.path.join(orig_train_img, train_img_id + ".jpg")
        src_lb = os.path.join(orig_train_lb, train_img_id + ".txt")

        dst_img = os.path.join(dst_merge_img, train_img_id + ".jpg")
        dst_lb = os.path.join(dst_merge_lb, train_img_id + ".txt")

        shutil.copyfile(src_img, dst_img)
        shutil.copyfile(src_lb, dst_lb)

    for val_img_id in val_img_ids:
        src_img = os.path.join(orig_val_img, val_img_id + ".jpg")
        src_lb = os.path.join(orig_val_lb, val_img_id + ".txt")

        dst_img = os.path.join(dst_merge_img, val_img_id + ".jpg")
        dst_lb = os.path.join(dst_merge_lb, val_img_id + ".txt")

        shutil.copyfile(src_img, dst_img)
        shutil.copyfile(src_lb, dst_lb)


def saveYaml(data_folder):
    save_path = os.path.join(YAML_ROOT, data_folder + ".yaml")

    output = {"path": "../datasets/{}".format(data_folder)}
    output["train"] = "images"
    output["val"] = "D:/HocTap/Helmet_Detection/datasets/HELMET/test/images"
    output["nc"] = 2
    output["names"] = ["With-Helmet", "Without-Helmet"]

    with open(save_path, "w+") as f:
        yaml.dump(output, f)


def copyData(img_id, client_root_folder):
    img_file_name = str(img_id) + ".jpg"
    label_file_name = str(img_id) + ".txt"

    src_img_path = os.path.join(TRAIN_IMG, img_file_name)
    src_label_path = os.path.join(TRAIN_LABEL, label_file_name)

    client_img_folder = os.path.join(client_root_folder, "images", img_file_name)
    client_label_folder = os.path.join(client_root_folder, "labels", label_file_name)

    shutil.copyfile(src_img_path, client_img_folder)
    shutil.copyfile(src_label_path, client_label_folder)


def evenSplit(output_prefix="even_"):
    # Get names without suffix
    img_files = os.listdir(TRAIN_IMG)

    img_ids = []
    for img_file in img_files:
        img_id = img_file.split(".")[0]
        img_ids.append(img_id)
    img_ids.sort()

    # Make directories for each client
    for client_id in range(0, NUM_CLIENTS):
        folder_name = "{}{}".format(output_prefix, str(client_id))
        folder_path = os.path.join(DATASETS, folder_name)
        # For each client, create a folder
        if os.path.isdir(folder_path):
            # Already exits, delete the whole folder
            shutil.rmtree(folder_path)
        # Create a folder for each client
        os.mkdir(folder_path)
        # Create image and label folders
        image_folder_path = os.path.join(folder_path, "images")
        label_folder_path = os.path.join(folder_path, "labels")
        os.mkdir(image_folder_path)
        os.mkdir(label_folder_path)

    current_client = 0
    # Copy image from VOC to the client folders
    for img_id in img_ids:
        if current_client == NUM_CLIENTS - 1:
            current_client = 0
        else:
            current_client += 1

        folder_name = "{}{}".format(output_prefix, str(current_client))
        folder_path = os.path.join(DATASETS, folder_name)
        copyData(img_id, folder_path)

        print("Copying {} to {}".format(img_id, folder_path))

    # Save yaml file
    for client_id in range(0, NUM_CLIENTS):
        saveYaml("{}{}".format(output_prefix, str(client_id)))
        print("Yaml file saved for ", client_id)


def noniidSplit(
    output_prefix="noniid_", split_num=4, split_ratios=[0.1, 0.2, 0.3, 0.4]
):
    assert len(split_ratios) == split_num
    assert sum(split_ratios) == 1

    # Get names without suffix
    img_files = os.listdir(TRAIN_IMG)

    img_ids = []
    for img_file in img_files:
        img_id = img_file.split(".")[0]
        img_ids.append(img_id)
    img_ids.sort()

    # Make directories for each client
    for client_id in range(0, NUM_CLIENTS):
        folder_name = "{}{}".format(output_prefix, str(client_id))
        folder_path = os.path.join(DATASETS, folder_name)
        # For each client, create a folder
        if os.path.isdir(folder_path):
            # Already exits, delete the whole folder
            shutil.rmtree(folder_path)
        # Create a folder for each client
        os.mkdir(folder_path)
        # Create image and label folders
        image_folder_path = os.path.join(folder_path, "images")
        label_folder_path = os.path.join(folder_path, "labels")
        os.mkdir(image_folder_path)
        os.mkdir(label_folder_path)

    # Calculate the splitting indexes
    split_indices = []  # In form of [[start1, end1], [start2, end2], ...]
    for client_i, split_ratio in enumerate(split_ratios):
        if client_i == 0:
            start_index = 0
        else:
            start_index = split_indices[client_i - 1][-1] + 1

        dataset_size = len(img_ids)
        sub_size = int(dataset_size * split_ratio)

        if client_i == split_num - 1:
            end_index = dataset_size - 1
        else:
            end_index = sub_size + start_index

        split_indices.append([start_index, end_index])

    # Copy image from VOC to the client folders
    for client_id, split_index in enumerate(split_indices):
        for img_index in range(split_index[0], split_index[1]):
            img_id = img_ids[img_index]
            folder_name = "{}{}".format(output_prefix, str(client_id))
            folder_path = os.path.join(DATASETS, folder_name)
            copyData(img_id, folder_path)

            print("Copying {} to {}".format(img_id, folder_path))

    # Save yaml file
    for client_id in range(0, NUM_CLIENTS):
        saveYaml("{}{}".format(output_prefix, str(client_id)))
        print("Yaml file saved for ", client_id)


if __name__ == "__main__":
    mergeTrainVal()
    evenSplit()
    noniidSplit()
