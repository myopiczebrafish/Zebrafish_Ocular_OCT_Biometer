# zebrafish_OCT_measurer
A library that uses a trained nnU-Net model to automatically measure SD-OCT images of zebrafish eyes.

# Installation and set up
## nnU-Net
The virtual environment and software requirements for nnU-Net are documented in the following link:  
https://github.com/MIC-DKFZ/nnUNet/blob/master/documentation/installation_instructions.md

Part of the installation steps requires setting up storage locations, which describe where raw datasets, pre-processed data used during training, and trained models are saved. (The weights and configuration of the trained model will need to be moved here.)

## Additional libraries
Several other libraries are required to be installed in the same virtual environment by running the following commands:  
`git clone https://github.com/rlav440/zebrafish_OCT_measurer`    
`cd zebrafish_oct_measurer`  
`pip install .`

## Weights
The weights and configuration of the trained model for zebrafish ocular SD-OCT segmentation can be downloaded as a folder called Dataset002_zebrafish from:  
https://huggingface.co/Robin-Laven/ZebrafishOCTMeasure

Once downloaded, the Dataset002_zebrafish folder should be placed in the folder mapped to `/path/to/nnUNet_results`. If the user has previously used nnU-Net to train a different model, Dataset002_zebrafish should be mapped to a temporary `nnUNet_results folder`, as explained in this link:  
https://github.com/MIC-DKFZ/nnUNet/blob/master/documentation/set_environment_variables.md

## Making predictions with the trained nnU-Net
Note that this network only accepts images of 512 x 1024 pixels and the central axis of the zebrafish eye should be in the middle of the image.  
An example input B scan:  
<img width="256" height="512" alt="4lv-AVG-20241212-130000" src="https://github.com/user-attachments/assets/f3af6866-6112-48fa-83a2-d5e9f9ebdb99" />

When Dataset002_zebrafish is in the appropriate `nnUNet_results folder`, the trained nnU-Net can be run following these steps:
1. Run the command  `python -m measure_zebrafish_oct` in the virtual environment.
Two pop-up windows will appear with prompts to:
2. Select the input folder, or folder of folders containing the SD-OCT images to be measured.
3. Select the output directory where the segmentations and .csv file of the measurements will be saved.

Once the appropriate folders are selected, the library will automatically pre-process the input folder images by performing a centre crop to produce images of 102 x 1024 pixel, converting the image formats to .png, and runs the trained nnU-Net on the processed images in the selected input folder(s).

## Output .csv file
The optical path length (pixels) of the cornea and anterior chamber depth (CACop), lens thickness (LTop), vitreous chamber depth (VCDop), and retinal thickness (RTop) along with the confidence will be saved as a .csv file in the selected output directory.
An example output.csv file is shown here:  
<p align="center">
  <img width="80%" alt="Screenshot 2026-06-25 at 8 01 46 PM" src="https://github.com/user-attachments/assets/0f75aec8-7de6-4ec3-93a6-36760128d902" />
</p>

## Pixel to micrometre conversion
The optical path length can be converted to the physical pathlength using the following equation:
 

# Training dataset
nnU-Net (**cite Isensee**) was trained according to the standard training protocol outlines in the nnU-Net documentation: 
https://github.com/MIC-DKFZ/nnUNet/blob/master/documentation/how_to_use_nnunet.md

The training dataset comprised 108 spectral-domain optical coherence tomography (SD-OCT) images (102 x 1024 pixels) of 6 to 13 weeks post-fertilisation (wpf) wildtype AB zebrafish eyes. 

SD-OCT images were obtained from a Lumedica OQ LabScope 3.0 XRD SD-OCT (Lumedica, Durham, NC, United States) with an 840 nm centre wavelength, 3.44 μm axial resolution, and a 4x microscope objective. 

Three experienced graders manually labelled 36 different SD-OCT images. The labels were the optical path lengths of the: cornea + anterior chamber depth (CACop), lens thickness (LTop), vitreous chamber depth (VCDop), retinal thickness (RTop), and background. The dataset comprised an equal number of frontal and transverse (relative to the axis of the fish body) scans of the right and left eyes, with axial lengths ranging from 868 to 1428 μm.

Training dataset details: 
<p align="center">
  <img width="80% alt="Screenshot 2026-06-25 at 7 08 43 PM" src="https://github.com/user-attachments/assets/88529d69-fc18-4ea9-ad4e-5a96c5f37eca" />
</p> 


| Age (wpf) | Number of images | CAC | VCD | LT | RT | AL |
| :---: | :---: | :---: | :---: | :---: | :---: |:---: |
| 6 | 3 | 20.75 ± 11.45 | 534.30 ± 4.11 | 222.70 ± 0.77 | 149.22 ± 2.61 | 926.97 ± 6.61 |
| 7 | 14 | 16.53 ± 5.33 | 581.82 ± 31.17 | 232.05 ± 35.80 | 151.26 ± 6.01 | 981.66 ± 63.56 |
| 8 | 31 | 18.40 ± 5.15 | 612.13 ± 45.87 | 251.90 ± 39.73 | 147.98 ± 7.35 | 1030.41 ± 87.67 |
| 10 | 32 | 22.01 ± 8.43 | 680.20 ± 52.92 | 297.32 ± 40.39 | 153.53 ± 8.34 | 1153.07 ± 100.86 |
| 13 | 28 | 24.10 ± 7.20 | 750.73 ± 56.96 | 344.41 ± 41.38 | 149.33 ± 6.33| 1268.57 ± 102.74 |

Table 1. Summary of training dataset used for nnU-Net (mean ± SD (μm)) and grouped by weeks post-fertilisation (wpf).


