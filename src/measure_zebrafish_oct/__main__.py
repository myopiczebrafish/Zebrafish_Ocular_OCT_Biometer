from run_folder import get_folder, process_folder, query_folder
import tempfile
from pathlib import Path

# the default entrypoint for the zebrafish segmenter.
dataset = '001'

# check that NNUNET has properly loaded the dataset location. #make this changable. 

# find the folder to segment

folder_to_run = get_folder()
output_folder = get_folder()

is_folder_of_folders = query_folder(folder_to_run)

if is_folder_of_folders:
    for subf in folder_to_run.iterdir():
        if not subf.is_dir():
            continue
        process_folder(subf, output_folder/subf.name, dataset)
else:
    process_folder(folder_to_run, output_folder, dataset)


