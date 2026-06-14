import subprocess
from matplotlib import pyplot as plt
import numpy as np
import torch
import pandas as pd
import matplotlib.pyplot as plt
import cv2
import numpy as np
import time
import tkinter
import tkinter as tk
from tkinter import filedialog
from pathlib import Path
import tempfile

# Initialize Tkinter and hide the main root window
root = tk.Tk()
root.withdraw()

# Open the folder selection dialog
def get_folder():
    folder_selected = filedialog.askdirectory()
    print(f"Selected folder: {folder_selected}")
    return Path(folder_selected)

def crop_im(image_loc, out_loc, plot=False):  
    # Load the image
    img = cv2.imread(image_loc)
    if img is None:
        print("Error: Could not load image. Please check the path.")
        exit()

    height, width = img.shape[:2]
    one_fifth_w = width // 5
    start_x = 2 * one_fifth_w
    end_x = 3 * one_fifth_w
    cropped_img = img[:, start_x:end_x, 0] #image forced to be MONO.
    
    assert np.allclose(cropped_img.shape, (1024, 102)), f"Input shape {cropped_img.shape} after cropping didnt' match expected shape (1024, 102)"
    # Display the images
    if plot:
        cv2.imshow('Original Image', img)
        cv2.imshow('Cropped Image (Middle Fifth)', cropped_img)
        cv2.waitKey(10)
        cv2.destroyAllWindows()
    cv2.imwrite(Path(out_loc)/(image_loc.with_suffix("").name + "_0000.png"), cropped_img)
    return

def prep_folder_for_running(folder, out_folder):
    """
    Take a folder containing a bunch of images to test.
    Put them into an output folder, after prepping them all
    """
    return

def cce(start, stop, pmat, ce_loss):
    """
    Defines a loss based on the KL divergence between the predicted and given probabilities.
    High values, close to 1, indicate the network prediction was "confident"
    Nothing stops the network being confidently wrong, but this will pick up massively failed predictions.
    """
    bulk = np.zeros_like(pmat)
    bulk[start:stop] = 1
    ke = ce_loss(torch.as_tensor(pmat).log(), torch.as_tensor(bulk))
    return np.exp(-ke)
    
def write_file_probs(floc:Path):
    """
    Parses all output probability representations within a folder to a single CV detailing the measurement and 
    the confidence in said prediction.
    """
    ce_loss = torch.nn.KLDivLoss()
    logic_string = f"NAME,ACD,ACD CONF,LENS,LENS CONF,VCD,VCD CONF,RT,RT CONF"
    inp_list = [logic_string]

    for f in floc.iterdir():
        if not f.suffix == '.npz':
            continue

        probs = np.load(f)['probabilities']
        relative_sum = np.sum(probs, axis=-1).squeeze()

        total_sum = np.sum(relative_sum, axis=0)
        odds = relative_sum/total_sum[None]

        odds_t0 = odds[0, :-1] * odds[4, 1:]
        odds_t1 = odds[4, :-1] * odds[3, 1:]
        odds_t2 = odds[3, :-1] * odds[2, 1:]
        odds_t3 = odds[2, :-1] * odds[1, 1:]
        odds_t4 = odds[1, :-1] * odds[0, 1:]

        cornea_start = np.argmax(odds_t0)
        lens_start = np.argmax(odds_t1)
        vcd_start = np.argmax(odds_t2)
        retina_start = np.argmax(odds_t3)
        pcd_start = np.argmax(odds_t4)
        
        nums = f"{f.with_suffix('').name},{lens_start - cornea_start},{cce(cornea_start, lens_start, odds[4, :], ce_loss):.3f},{vcd_start - lens_start},{cce(lens_start, vcd_start, odds[3, :], ce_loss):.3f},{retina_start - vcd_start},{cce(vcd_start, retina_start, odds[2, :], ce_loss):.3f},{pcd_start - retina_start},{cce(retina_start, pcd_start, odds[1, :], ce_loss):.3f},"
        print(nums)
        inp_list.append(nums)

    with open(floc.parent/f'{floc.with_suffix("").name}.csv', 'w') as f:
        for l in inp_list:
            f.write(l + '\n')

    return 1

def run_full_AI_pipeline_on_folder(in_folder: Path, out_folder:Path, dataset='001'):
    in_folder.mkdir(exist_ok=True)
    print('Beginning running of NNUNET')
    subprocess.run([
        'nnUNetv2_predict',
        '-i',
        str(in_folder),
        '-o',
        str(out_folder),
        '-d',
        dataset,
        '-c', '2d',  '-chk',  'checkpoint_best.pth',  '--save_probabilities'])

    print("Condensing results to .csv")
    write_file_probs(out_folder)


def query_folder(folder: Path):
    f_dirs = [f.is_dir() for f in folder.iterdir()]
    if np.any(f_dirs):
        print(f"Found sub-folders in the target {folder}, predicting on the contents of each sub-folder.")
        return  True
    print("No subfolders; predicting on the input folder")
    return False



def process_folder(folder, output_folder, dataset='002'):
    images = [f for f in folder.iterdir() if f.suffix in [".jpg", ".tif", '.tiff', '.png']]
    with tempfile.TemporaryDirectory() as temp_dir:
        # process the input images to the input folder.
        # crop and rename the images to be processed by nnunet
        for im in images:
            crop_im(im, temp_dir)
        
        #then we run NNUNET on the folder
        run_full_AI_pipeline_on_folder(Path(temp_dir), output_folder, dataset=dataset)

if __name__ == "__main__":

    
    folder: Path = '/media/robin/ROBIN/vetbond appendix/'
    #if main argument is a folder of folders, run over each of the folders
        #remove the temporary directo
    #if it's a fodler of images, run on that fodler
    
    
