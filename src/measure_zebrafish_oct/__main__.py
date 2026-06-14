from measure_zebrafish_oct.run_folder import get_folder, process_folder, query_folder
import tempfile
from pathlib import Path

# the default entrypoint for the zebrafish segmenter.
dataset = '001'

# check that NNUNET has properly loaded the dataset location. #make this changable. 

# find the folder to segment

folder_to_run = get_folder()
#folder_to_run = Path("/media/robin/KINGSTON/NN_analysis/round2")
output_folder = get_folder()
#output_folder = Path("/media/robin/KINGSTON/NN_analysis/outputs")


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
