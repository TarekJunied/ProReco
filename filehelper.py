import os


def gather_all_xes(dir_path):
    xes_files = []
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file.endswith(".xes"):
                xes_files.append(os.path.join(root, file))

    return xes_files

