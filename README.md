# zebrafish_OCT_measurer
A library that uses a trained nnU-Net model to automatically measure SD-OCT of zebrafish eyes.

# Background
nnU-Net was trained on 108 SD-OCT images (102 x 1024 pixels) of zebrafish eyes. SD-OCT images were obtained from a Lumedica OQ LabScope 3.0 XRD SD-OCT (Lumedica, Durham, NC, United States) with an 840 nm centre wavelength, 3.44 μm axial resolution, and a 4x microscope objective. Three experienced graders manually labelled 36 different SD-OCT images. The labels were: cornea + anterior chamber depth (cac), lens thickness (lt), vitreous chamber depth (vcd), retinal thickness (rt), and background.

