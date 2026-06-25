from measure_zebrafish_oct.run_folder import get_folder, process_folder, query_folder
import tempfile
from pathlib import Path

# the default entrypoint for the zebrafish segmenter.
dataset = '002'
#this is a placeholder value

# find the folder to segment

folder_to_run = get_folder()
output_folder = get_folder()


def folder_recurse(in_folder, out_folder, dataset):
    is_folder_of_folders = query_folder(in_folder)
    if is_folder_of_folders:
        for subf in in_folder.iterdir():
            if not subf.is_dir():
                continue
            folder_recurse(subf, out_folder/subf.name, dataset)
    else:
        process_folder(in_folder, out_folder, dataset)

folder_recurse(folder_to_run, output_folder, dataset)
